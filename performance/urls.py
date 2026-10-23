from django.urls import path
from . import views

urlpatterns = [
    path('lab/', views.performance_lab, name='performance_lab'),
    path('lab/run/', views.run_benchmark, name='run_benchmark'),
    path('index-lab/', views.index_lab, name='index_lab'),
    path('index-lab/run/', views.run_index_benchmark, name='run_index_benchmark'),
    path('history/', views.benchmark_history, name='benchmark_history'),
    path('api/history/', views.benchmark_history_api, name='benchmark_history_api'),
]
