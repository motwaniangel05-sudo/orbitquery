from django.db import models
from django.utils import timezone


class LaunchStatus(models.Model):
    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class LaunchLocation(models.Model):
    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=3)
    description = models.TextField(blank=True)
    timezone_name = models.CharField(max_length=100, blank=True)
    total_launch_count = models.IntegerField(default=0)
    total_landing_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class LaunchPad(models.Model):
    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    location = models.ForeignKey(LaunchLocation, on_delete=models.CASCADE, related_name='pads')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    map_url = models.URLField(blank=True, null=True)
    wiki_url = models.URLField(blank=True, null=True)
    total_launch_count = models.IntegerField(default=0)
    orbital_launch_attempt_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.location.name} - {self.name}"


class LaunchServiceProvider(models.Model):
    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Mission(models.Model):
    external_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    launch_designator = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True)
    orbit_name = models.CharField(max_length=100, blank=True)
    orbit_abbrev = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Launch(models.Model):
    external_id = models.UUIDField(unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=300)
    status = models.ForeignKey(LaunchStatus, on_delete=models.PROTECT, related_name='launches')
    net = models.DateTimeField(null=True, blank=True)
    window_start = models.DateTimeField(null=True, blank=True)
    window_end = models.DateTimeField(null=True, blank=True)
    probability = models.IntegerField(null=True, blank=True)
    weather_concerns = models.TextField(blank=True, null=True)
    holdreason = models.TextField(blank=True, null=True)
    failreason = models.TextField(blank=True, null=True)
    hashtag = models.CharField(max_length=100, blank=True, null=True)
    launch_service_provider = models.ForeignKey(
        LaunchServiceProvider, on_delete=models.PROTECT, related_name='launches'
    )
    pad = models.ForeignKey(LaunchPad, on_delete=models.PROTECT, related_name='launches')
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True, blank=True, related_name='launches')
    rocket_name = models.CharField(max_length=200, blank=True)
    rocket_family = models.CharField(max_length=100, blank=True)
    rocket_configuration = models.CharField(max_length=200, blank=True)
    image = models.URLField(blank=True, null=True)
    infographic = models.URLField(blank=True, null=True)
    webcast_live = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    orbital_launch_attempt_count = models.IntegerField(default=0, null=True)
    location_launch_attempt_count = models.IntegerField(default=0, null=True)
    pad_launch_attempt_count = models.IntegerField(default=0, null=True)
    agency_launch_attempt_count = models.IntegerField(default=0, null=True)

    class Meta:
        ordering = ['-net']
        indexes = [
            models.Index(fields=['net']),
            models.Index(fields=['status']),
            models.Index(fields=['launch_service_provider']),
            models.Index(fields=['-net', 'status']),
        ]

    def __str__(self):
        return self.name

    @property
    def is_upcoming(self):
        if self.net is None:
            return False
        return self.net > timezone.now()


class DataSyncRun(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('running', 'Running'),
        ('success', 'Success'),
        ('error', 'Error'),
    ], default='running')
    records_fetched = models.IntegerField(default=0)
    records_created = models.IntegerField(default=0)
    records_updated = models.IntegerField(default=0)
    records_skipped = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    api_url = models.URLField()

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"Sync run {self.started_at} - {self.status}"
