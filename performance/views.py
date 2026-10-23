from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BenchmarkRun
from .services import BenchmarkService, IndexBenchmarkService


def performance_lab(request):
    recent_benchmarks = BenchmarkRun.objects.filter(
        benchmark_type='n_plus_one'
    ).order_by('-created_at')[:10]

    context = {
        'recent_benchmarks': recent_benchmarks,
    }
    return render(request, 'performance/lab.html', context)


@login_required
def run_benchmark(request):
    if request.method == 'POST':
        limit = int(request.POST.get('limit', 50))
        strategy = request.POST.get('strategy', 'baseline')

        benchmark = BenchmarkService.run_benchmark(
            benchmark_type='n_plus_one',
            strategy=strategy,
            limit=limit,
            user=request.user
        )

        BenchmarkService.compare_with_baseline(benchmark)

        return render(request, 'performance/partials/benchmark_result.html', {
            'benchmark': benchmark
        })

    return render(request, 'performance/lab.html')


def index_lab(request):
    recent_benchmarks = BenchmarkRun.objects.filter(
        benchmark_type='index'
    ).order_by('-created_at')[:10]

    context = {
        'recent_benchmarks': recent_benchmarks,
    }
    return render(request, 'performance/index_lab.html', context)


@login_required
def run_index_benchmark(request):
    if request.method == 'POST':
        limit = int(request.POST.get('limit', 100))
        index_name = request.POST.get('index_name', '')

        benchmark = IndexBenchmarkService.run_index_benchmark(
            limit=limit,
            index_name=index_name,
            user=request.user
        )

        return render(request, 'performance/partials/index_result.html', {
            'benchmark': benchmark
        })

    return render(request, 'performance/index_lab.html')


def benchmark_history(request):
    try:
        benchmarks = BenchmarkRun.objects.all().order_by('-created_at')
    except Exception:
        benchmarks = []

    benchmark_type = request.GET.get('type', '')
    strategy = request.GET.get('strategy', '')

    if benchmarks and benchmark_type:
        benchmarks = benchmarks.filter(benchmark_type=benchmark_type)

    if benchmarks and strategy:
        benchmarks = benchmarks.filter(strategy=strategy)

    context = {
        'benchmarks': benchmarks,
        'benchmark_type': benchmark_type,
        'strategy': strategy,
    }
    return render(request, 'performance/history.html', context)


@api_view(['GET'])
def benchmark_history_api(request):
    benchmarks = BenchmarkRun.objects.all().order_by('-created_at')
    serializer_data = []

    for b in benchmarks:
        serializer_data.append({
            'id': b.id,
            'benchmark_type': b.benchmark_type,
            'strategy': b.strategy,
            'record_limit': b.record_limit,
            'query_count': b.query_count,
            'median_execution_time_ms': b.median_execution_time_ms,
            'improvement_percentage': b.improvement_percentage,
            'created_at': b.created_at,
        })

    return Response(serializer_data)
