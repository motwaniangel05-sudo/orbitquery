from django.contrib import admin
from .models import (
    Launch, LaunchStatus, LaunchLocation, LaunchPad,
    LaunchServiceProvider, Mission, DataSyncRun
)


@admin.register(LaunchStatus)
class LaunchStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'abbrev']
    search_fields = ['name', 'abbrev']


@admin.register(LaunchLocation)
class LaunchLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country_code', 'total_launch_count']
    search_fields = ['name', 'country_code']


@admin.register(LaunchPad)
class LaunchPadAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'total_launch_count']
    list_filter = ['location']
    search_fields = ['name']


@admin.register(LaunchServiceProvider)
class LaunchServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type']
    search_fields = ['name', 'type']


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'type', 'orbit_name']
    search_fields = ['name', 'type']


@admin.register(Launch)
class LaunchAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'net', 'launch_service_provider', 'pad']
    list_filter = ['status', 'launch_service_provider', 'pad__location']
    search_fields = ['name', 'slug']
    date_hierarchy = 'net'
    readonly_fields = ['external_id', 'last_updated']


@admin.register(DataSyncRun)
class DataSyncRunAdmin(admin.ModelAdmin):
    list_display = ['started_at', 'status', 'records_fetched', 'records_created', 'records_updated']
    list_filter = ['status']
    readonly_fields = ['started_at', 'completed_at']
