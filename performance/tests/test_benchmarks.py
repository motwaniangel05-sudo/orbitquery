from django.test import TestCase
from django.contrib.auth.models import User
from performance.models import BenchmarkRun
from performance.services import BenchmarkService


class BenchmarkServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_benchmark_creation(self):
        benchmark = BenchmarkRun.objects.create(
            user=self.user,
            benchmark_type='n_plus_one',
            strategy='baseline',
            record_limit=50,
            query_count=51,
            total_execution_time_ms=100.5,
            records_processed=50,
            median_execution_time_ms=100.5
        )
        self.assertEqual(benchmark.benchmark_type, 'n_plus_one')
        self.assertEqual(benchmark.strategy, 'baseline')
        self.assertIn('n_plus_one', str(benchmark))
        self.assertIn('baseline', str(benchmark))
