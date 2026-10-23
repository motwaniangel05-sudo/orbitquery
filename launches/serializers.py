from rest_framework import serializers
from .models import Launch, LaunchStatus, LaunchLocation, LaunchPad, LaunchServiceProvider, Mission


class LaunchStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchStatus
        fields = ['id', 'external_id', 'name', 'abbrev', 'description']


class LaunchLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchLocation
        fields = ['id', 'external_id', 'name', 'country_code', 'description', 'timezone_name']


class LaunchPadSerializer(serializers.ModelSerializer):
    location = LaunchLocationSerializer(read_only=True)

    class Meta:
        model = LaunchPad
        fields = ['id', 'external_id', 'name', 'location', 'latitude', 'longitude', 'map_url']


class LaunchServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaunchServiceProvider
        fields = ['id', 'external_id', 'name', 'type', 'url']


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ['id', 'external_id', 'name', 'description', 'type', 'orbit_name', 'orbit_abbrev']


class LaunchListSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    provider_name = serializers.CharField(source='launch_service_provider.name', read_only=True)
    location_name = serializers.CharField(source='pad.location.name', read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)

    class Meta:
        model = Launch
        fields = [
            'id', 'external_id', 'slug', 'name', 'status_name', 'net',
            'provider_name', 'location_name', 'image', 'is_upcoming'
        ]


class LaunchDetailSerializer(serializers.ModelSerializer):
    status = LaunchStatusSerializer(read_only=True)
    launch_service_provider = LaunchServiceProviderSerializer(read_only=True)
    pad = LaunchPadSerializer(read_only=True)
    mission = MissionSerializer(read_only=True)
    is_upcoming = serializers.BooleanField(read_only=True)

    class Meta:
        model = Launch
        fields = [
            'id', 'external_id', 'slug', 'name', 'status', 'net', 'window_start',
            'window_end', 'probability', 'weather_concerns', 'holdreason',
            'failreason', 'hashtag', 'launch_service_provider', 'pad', 'mission',
            'rocket_name', 'rocket_family', 'rocket_configuration', 'image',
            'infographic', 'webcast_live', 'is_upcoming', 'orbital_launch_attempt_count',
            'location_launch_attempt_count', 'pad_launch_attempt_count',
            'agency_launch_attempt_count', 'last_updated'
        ]
