from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q, F
from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Launch, LaunchStatus, LaunchServiceProvider, LaunchLocation, DataSyncRun
from .serializers import LaunchListSerializer, LaunchDetailSerializer


def dashboard(request):
    total_launches = Launch.objects.count()
    upcoming_count = Launch.objects.filter(net__gt=timezone.now()).count()
    past_count = Launch.objects.filter(net__lte=timezone.now()).count()
    provider_count = LaunchServiceProvider.objects.count()

    last_sync = DataSyncRun.objects.filter(status='success').first()
    total_benchmarks = 0

    recent_launches = Launch.objects.select_related(
        'status', 'launch_service_provider', 'pad__location'
    ).order_by('-net')[:5]

    context = {
        'total_launches': total_launches,
        'upcoming_count': upcoming_count,
        'past_count': past_count,
        'provider_count': provider_count,
        'last_sync': last_sync,
        'total_benchmarks': total_benchmarks,
        'recent_launches': recent_launches,
    }
    return render(request, 'dashboard/index.html', context)


def launch_list(request):
    query = request.GET.get('q', '')
    status_id = request.GET.get('status', '')
    provider_id = request.GET.get('provider', '')
    location_id = request.GET.get('location', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    sort = request.GET.get('sort', '-net')

    launches = Launch.objects.select_related(
        'status', 'launch_service_provider', 'pad__location'
    ).all()

    if query:
        launches = launches.filter(
            Q(name__icontains=query) |
            Q(rocket_name__icontains=query)
        )

    if status_id:
        launches = launches.filter(status_id=status_id)

    if provider_id:
        launches = launches.filter(launch_service_provider_id=provider_id)

    if location_id:
        launches = launches.filter(pad__location_id=location_id)

    if date_from:
        launches = launches.filter(net__gte=date_from)

    if date_to:
        launches = launches.filter(net__lte=date_to)

    launches = launches.order_by(sort)

    status_choices = LaunchStatus.objects.all()
    provider_choices = LaunchServiceProvider.objects.all()
    location_choices = LaunchLocation.objects.all()

    context = {
        'launches': launches,
        'status_choices': status_choices,
        'provider_choices': provider_choices,
        'location_choices': location_choices,
        'query': query,
        'status_id': status_id,
        'provider_id': provider_id,
        'location_id': location_id,
        'date_from': date_from,
        'date_to': date_to,
        'sort': sort,
    }
    return render(request, 'launches/list.html', context)


def launch_detail(request, slug):
    launch = get_object_or_404(
        Launch.objects.select_related(
            'status', 'launch_service_provider', 'pad__location', 'mission'
        ),
        slug=slug
    )
    context = {'launch': launch}
    return render(request, 'launches/detail.html', context)


@api_view(['GET'])
def dashboard_stats(request):
    total_launches = Launch.objects.count()
    upcoming_count = Launch.objects.filter(net__gt=timezone.now()).count()
    past_count = Launch.objects.filter(net__lte=timezone.now()).count()
    provider_count = LaunchServiceProvider.objects.count()

    last_sync = DataSyncRun.objects.filter(status='success').first()

    return Response({
        'total_launches': total_launches,
        'upcoming_count': upcoming_count,
        'past_count': past_count,
        'provider_count': provider_count,
        'last_sync': last_sync.started_at if last_sync else None,
    })


class LaunchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Launch.objects.select_related(
        'status', 'launch_service_provider', 'pad__location', 'mission'
    ).all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'rocket_name']
    ordering_fields = ['net', 'name']
    ordering = ['-net']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LaunchDetailSerializer
        return LaunchListSerializer
