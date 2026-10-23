import uuid
from django.test import TestCase
from launches.models import Launch, LaunchStatus, LaunchLocation, LaunchPad, LaunchServiceProvider, Mission


class LaunchModelTest(TestCase):
    def setUp(self):
        self.status = LaunchStatus.objects.create(
            external_id=1,
            name='Launch Successful',
            abbrev='Success',
            description='Successful launch'
        )
        self.location = LaunchLocation.objects.create(
            external_id=1,
            name='Test Location',
            country_code='USA',
            description='Test location'
        )
        self.pad = LaunchPad.objects.create(
            external_id=1,
            name='Pad 1',
            location=self.location
        )
        self.provider = LaunchServiceProvider.objects.create(
            external_id=1,
            name='Test Provider',
            type='Commercial'
        )
        self.mission = Mission.objects.create(
            external_id=1,
            name='Test Mission',
            description='Test mission description'
        )

    def test_launch_creation(self):
        launch = Launch.objects.create(
            external_id=uuid.uuid4(),
            slug='test-launch',
            name='Test Launch',
            status=self.status,
            launch_service_provider=self.provider,
            pad=self.pad,
            mission=self.mission
        )
        self.assertEqual(launch.name, 'Test Launch')
        self.assertEqual(str(launch), 'Test Launch')

    def test_external_id_uniqueness(self):
        test_uuid = uuid.uuid4()
        Launch.objects.create(
            external_id=test_uuid,
            slug='test-launch-1',
            name='Test Launch 1',
            status=self.status,
            launch_service_provider=self.provider,
            pad=self.pad
        )
        with self.assertRaises(Exception):
            Launch.objects.create(
                external_id=test_uuid,
                slug='test-launch-2',
                name='Test Launch 2',
                status=self.status,
                launch_service_provider=self.provider,
                pad=self.pad
            )
