import time
import statistics
from django.db import connection
from django.db.models import Count, Q
from django.utils import timezone
from .models import BenchmarkRun
from launches.models import Launch


class BenchmarkService:
    @staticmethod
    def capture_queries():
        from django.test.utils import CaptureQueriesContext
        return CaptureQueriesContext(connection)

    @staticmethod
    def execute_baseline_n_plus_one(limit: int) -> tuple:
        queries = []
        with BenchmarkService.capture_queries() as capture:
            start_time = time.perf_counter()

            launches = Launch.objects.all()[:limit]
            records = []

            for launch in launches:
                record = {
                    'name': launch.name,
                    'status_name': launch.status.name,
                    'provider_name': launch.launch_service_provider.name,
                    'location_name': launch.pad.location.name,
                    'mission_name': launch.mission.name if launch.mission else None,
                }
                records.append(record)

            end_time = time.perf_counter()
            queries = [q['sql'] for q in capture.captured_queries]

        total_time_ms = (end_time - start_time) * 1000
        db_time_ms = sum(float(q.get('time', 0)) * 1000 for q in capture.captured_queries)
        python_time_ms = total_time_ms - db_time_ms

        return total_time_ms, db_time_ms, python_time_ms, len(queries), len(records), queries

    @staticmethod
    def execute_optimised_query(limit: int) -> tuple:
        queries = []
        with BenchmarkService.capture_queries() as capture:
            start_time = time.perf_counter()

            launches = Launch.objects.select_related(
                'status', 'launch_service_provider', 'pad__location', 'mission'
            ).all()[:limit]
            records = []

            for launch in launches:
                record = {
                    'name': launch.name,
                    'status_name': launch.status.name,
                    'provider_name': launch.launch_service_provider.name,
                    'location_name': launch.pad.location.name,
                    'mission_name': launch.mission.name if launch.mission else None,
                }
                records.append(record)

            end_time = time.perf_counter()
            queries = [q['sql'] for q in capture.captured_queries]

        total_time_ms = (end_time - start_time) * 1000
        db_time_ms = sum(float(q.get('time', 0)) * 1000 for q in capture.captured_queries)
        python_time_ms = total_time_ms - db_time_ms

        return total_time_ms, db_time_ms, python_time_ms, len(queries), len(records), queries

    @staticmethod
    def run_benchmark(benchmark_type: str, strategy: str, limit: int, user=None) -> BenchmarkRun:
        sample_size = 5
        execution_times = []
        query_counts = []
        all_queries = []

        for _ in range(sample_size):
            if strategy == 'baseline':
                total_time, db_time, python_time, query_count, records, queries = \
                    BenchmarkService.execute_baseline_n_plus_one(limit)
            else:
                total_time, db_time, python_time, query_count, records, queries = \
                    BenchmarkService.execute_optimised_query(limit)

            execution_times.append(total_time)
            query_counts.append(query_count)
            all_queries.extend(queries)

        median_time = statistics.median(execution_times)
        median_query_count = statistics.median(query_counts)

        benchmark = BenchmarkRun.objects.create(
            user=user,
            benchmark_type=benchmark_type,
            strategy=strategy,
            record_limit=limit,
            query_count=int(median_query_count),
            total_execution_time_ms=median_time,
            db_query_time_ms=db_time,
            python_time_ms=python_time,
            records_processed=records,
            sample_size=sample_size,
            median_execution_time_ms=median_time,
            sql_queries=all_queries[:10],
        )

        return benchmark

    @staticmethod
    def compare_with_baseline(benchmark: BenchmarkRun):
        baseline = BenchmarkRun.objects.filter(
            benchmark_type=benchmark.benchmark_type,
            strategy='baseline',
            record_limit=benchmark.record_limit
        ).order_by('-created_at').first()

        if baseline and benchmark.strategy == 'optimised':
            improvement = ((baseline.median_execution_time_ms - benchmark.median_execution_time_ms) /
                         baseline.median_execution_time_ms) * 100
            benchmark.improvement_percentage = improvement
            benchmark.compared_to_run = baseline
            benchmark.save()

        return baseline


class IndexBenchmarkService:
    @staticmethod
    def get_query_plan(query: str) -> str:
        with connection.cursor() as cursor:
            cursor.execute(f"EXPLAIN ANALYZE {query}")
            rows = cursor.fetchall()
            return '\n'.join(str(row) for row in rows)

    @staticmethod
    def benchmark_date_filter(limit: int, with_index: bool = False) -> tuple:
        query = f"SELECT * FROM launches_launch WHERE net IS NOT NULL ORDER BY net DESC LIMIT {limit}"

        with connection.cursor() as cursor:
            start_time = time.perf_counter()
            cursor.execute(query)
            results = cursor.fetchall()
            end_time = time.perf_counter()

        total_time_ms = (end_time - start_time) * 1000
        query_plan = IndexBenchmarkService.get_query_plan(query)

        return total_time_ms, len(results), query_plan

    @staticmethod
    def run_index_benchmark(limit: int, index_name: str = '', user=None) -> BenchmarkRun:
        sample_size = 5
        execution_times = []

        for _ in range(sample_size):
            total_time, records, _ = IndexBenchmarkService.benchmark_date_filter(limit)
            execution_times.append(total_time)

        median_time = statistics.median(execution_times)
        _, _, query_plan = IndexBenchmarkService.benchmark_date_filter(limit)

        benchmark = BenchmarkRun.objects.create(
            user=user,
            benchmark_type='index',
            strategy='baseline',
            record_limit=limit,
            query_count=1,
            total_execution_time_ms=median_time,
            records_processed=records,
            sample_size=sample_size,
            median_execution_time_ms=median_time,
            query_plan=query_plan,
            index_name=index_name,
        )

        return benchmark
