from django.contrib import admin
from .models import BenchmarkRun


@admin.register(BenchmarkRun)
class BenchmarkRunAdmin(admin.ModelAdmin):
    list_display = ['benchmark_type', 'strategy', 'record_limit', 'query_count', 'median_execution_time_ms', 'created_at']
    list_filter = ['benchmark_type', 'strategy']
    readonly_fields = ['created_at', 'sql_queries', 'query_plan']
