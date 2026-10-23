from django.db import models
from django.contrib.auth.models import User


class BenchmarkRun(models.Model):
    STRATEGY_CHOICES = [
        ('baseline', 'Baseline (N+1)'),
        ('optimised', 'Optimised (select_related/prefetch_related)'),
    ]

    BENCHMARK_TYPE_CHOICES = [
        ('n_plus_one', 'N+1 Query Detection'),
        ('index', 'Index Performance'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    benchmark_type = models.CharField(max_length=20, choices=BENCHMARK_TYPE_CHOICES)
    strategy = models.CharField(max_length=20, choices=STRATEGY_CHOICES)
    record_limit = models.IntegerField()
    query_count = models.IntegerField()
    total_execution_time_ms = models.FloatField()
    db_query_time_ms = models.FloatField(null=True, blank=True)
    python_time_ms = models.FloatField(null=True, blank=True)
    records_processed = models.IntegerField()
    sample_size = models.IntegerField(default=1)
    median_execution_time_ms = models.FloatField()
    improvement_percentage = models.FloatField(null=True, blank=True)
    compared_to_run = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='comparisons')
    sql_queries = models.JSONField(default=list, blank=True)
    query_plan = models.TextField(blank=True)
    index_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['benchmark_type']),
            models.Index(fields=['strategy']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.benchmark_type} - {self.strategy} - {self.created_at}"
