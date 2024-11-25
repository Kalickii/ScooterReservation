from django.urls import path

from scooters import views as scooters


urlpatterns = [
    path('main/', scooters.ScooterListView.as_view(), name='scooter-list'),
    path('main/<scooter_id>', scooters.ScooterDetailView.as_view(), name='scooter-detail'),
    path('main/<scooter_id>/edit', scooters.ScooterUpdateView.as_view(), name='scooter-update'),
]
