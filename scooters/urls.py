from django.urls import path

from scooters import views as scooters
from scooters import template_views as scooters_temp

urlpatterns = [
    # API ENDPOINTS
    path('api/main/', scooters.ScooterListView.as_view(), name='scooter-list-api'),
    path('api/main/<int:scooter_id>/', scooters.ScooterDetailView.as_view(), name='scooter-detail-api'),


    # TEMPORARY RENDER TEMPLATES
    path('main/', scooters_temp.ScooterListView.as_view(), name='scooter-list'),
    path('main/<scooter_id>', scooters_temp.ScooterDetailView.as_view(), name='scooter-detail'),
]