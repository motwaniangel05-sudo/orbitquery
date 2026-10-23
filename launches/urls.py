from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/launches', views.LaunchViewSet, basename='launch')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('launches/', views.launch_list, name='launch_list'),
    path('launches/<slug:slug>/', views.launch_detail, name='launch_detail'),
    path('api/stats/', views.dashboard_stats, name='dashboard_stats'),
] + router.urls
