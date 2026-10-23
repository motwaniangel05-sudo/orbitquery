import time
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from launches.models import (
    Launch, LaunchStatus, LaunchLocation, LaunchPad,
    LaunchServiceProvider, Mission, DataSyncRun
)
from launches.services.api_client import LaunchLibrary2Client


class Command(BaseCommand):
    help = 'Import launch data from Launch Library 2 API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Number of launches to import (default: 50)'
        )
        parser.add_argument(
            '--offset',
            type=int,
            default=0,
            help='Offset for pagination (default: 0)'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        offset = options['offset']
        client = LaunchLibrary2Client()

        sync_run = DataSyncRun.objects.create(
            status='running',
            api_url=f"{client.base_url}/launch/",
        )

        self.stdout.write(f"Starting sync: limit={limit}, offset={offset}")
        start_time = time.time()

        try:
            data = client.get_launches(limit=limit, offset=offset)
            results = data.get('results', [])
            sync_run.records_fetched = len(results)

            self.stdout.write(f"Fetched {len(results)} launches from API")

            for launch_data in results:
                self._import_launch(launch_data, sync_run)

            sync_run.status = 'success'
            sync_run.completed_at = timezone.now()
            sync_run.save()

            duration = time.time() - start_time
            self.stdout.write(
                self.style.SUCCESS(
                    f"Sync completed in {duration:.2f}s. "
                    f"Created: {sync_run.records_created}, "
                    f"Updated: {sync_run.records_updated}, "
                    f"Skipped: {sync_run.records_skipped}"
                )
            )

        except Exception as e:
            sync_run.status = 'error'
            sync_run.error_message = str(e)
            sync_run.completed_at = timezone.now()
            sync_run.save()
            self.stdout.write(self.style.ERROR(f"Sync failed: {e}"))
            raise

    def _import_launch(self, launch_data: dict, sync_run: DataSyncRun):
        try:
            with transaction.atomic():
                status = self._get_or_create_status(launch_data.get('status'))
                location = self._get_or_create_location(launch_data.get('pad', {}).get('location'))
                pad = self._get_or_create_pad(launch_data.get('pad'), location)
                provider = self._get_or_create_provider(launch_data.get('launch_service_provider'))
                mission = self._get_or_create_mission(launch_data.get('mission'))

                launch, created = Launch.objects.update_or_create(
                    external_id=launch_data['id'],
                    defaults={
                        'slug': launch_data.get('slug', ''),
                        'name': launch_data.get('name', ''),
                        'status': status,
                        'net': launch_data.get('net'),
                        'window_start': launch_data.get('window_start'),
                        'window_end': launch_data.get('window_end'),
                        'probability': launch_data.get('probability'),
                        'weather_concerns': launch_data.get('weather_concerns') or '',
                        'holdreason': launch_data.get('holdreason') or '',
                        'failreason': launch_data.get('failreason') or '',
                        'hashtag': launch_data.get('hashtag') or '',
                        'launch_service_provider': provider,
                        'pad': pad,
                        'mission': mission,
                        'rocket_name': launch_data.get('rocket', {}).get('configuration', {}).get('name', ''),
                        'rocket_family': launch_data.get('rocket', {}).get('configuration', {}).get('family', ''),
                        'rocket_configuration': launch_data.get('rocket', {}).get('configuration', {}).get('full_name', ''),
                        'image': launch_data.get('image') or '',
                        'infographic': launch_data.get('infographic') or '',
                        'webcast_live': launch_data.get('webcast_live', False),
                        'orbital_launch_attempt_count': launch_data.get('orbital_launch_attempt_count', 0),
                        'location_launch_attempt_count': launch_data.get('location_launch_attempt_count', 0),
                        'pad_launch_attempt_count': launch_data.get('pad_launch_attempt_count', 0),
                        'agency_launch_attempt_count': launch_data.get('agency_launch_attempt_count', 0),
                    }
                )

                if created:
                    sync_run.records_created += 1
                else:
                    sync_run.records_updated += 1

        except Exception as e:
            sync_run.records_skipped += 1
            self.stdout.write(self.style.WARNING(f"Skipped launch {launch_data.get('id')}: {e}"))

    def _get_or_create_status(self, status_data: dict):
        if not status_data:
            return None
        status, _ = LaunchStatus.objects.get_or_create(
            external_id=status_data['id'],
            defaults={
                'name': status_data.get('name', ''),
                'abbrev': status_data.get('abbrev', ''),
                'description': status_data.get('description', ''),
            }
        )
        return status

    def _get_or_create_location(self, location_data: dict):
        if not location_data:
            return None
        location, _ = LaunchLocation.objects.get_or_create(
            external_id=location_data['id'],
            defaults={
                'name': location_data.get('name', ''),
                'country_code': location_data.get('country_code', ''),
                'description': location_data.get('description', ''),
                'timezone_name': location_data.get('timezone_name', ''),
                'total_launch_count': location_data.get('total_launch_count', 0),
                'total_landing_count': location_data.get('total_landing_count', 0),
            }
        )
        return location

    def _get_or_create_pad(self, pad_data: dict, location: LaunchLocation):
        if not pad_data:
            return None
        pad, _ = LaunchPad.objects.get_or_create(
            external_id=pad_data['id'],
            defaults={
                'name': pad_data.get('name', ''),
                'location': location,
                'latitude': pad_data.get('latitude'),
                'longitude': pad_data.get('longitude'),
                'map_url': pad_data.get('map_url') or '',
                'wiki_url': pad_data.get('wiki_url') or '',
                'total_launch_count': pad_data.get('total_launch_count', 0),
                'orbital_launch_attempt_count': pad_data.get('orbital_launch_attempt_count', 0),
            }
        )
        return pad

    def _get_or_create_provider(self, provider_data: dict):
        if not provider_data:
            return None
        provider, _ = LaunchServiceProvider.objects.get_or_create(
            external_id=provider_data['id'],
            defaults={
                'name': provider_data.get('name', ''),
                'type': provider_data.get('type', ''),
                'url': provider_data.get('url', ''),
            }
        )
        return provider

    def _get_or_create_mission(self, mission_data: dict):
        if not mission_data:
            return None
        orbit = mission_data.get('orbit', {})
        mission, _ = Mission.objects.get_or_create(
            external_id=mission_data['id'],
            defaults={
                'name': mission_data.get('name', ''),
                'description': mission_data.get('description', ''),
                'launch_designator': mission_data.get('launch_designator') or '',
                'type': mission_data.get('type', ''),
                'orbit_name': orbit.get('name', '') if orbit else '',
                'orbit_abbrev': orbit.get('abbrev', '') if orbit else '',
            }
        )
        return mission
