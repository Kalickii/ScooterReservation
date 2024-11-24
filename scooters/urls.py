from django.urls import path

from scooters import views as scooters_temp


urlpatterns = [
    path('main/', scooters_temp.ScooterListView.as_view(), name='scooter-list'),
    path('main/<scooter_id>', scooters_temp.ScooterDetailView.as_view(), name='scooter-detail'),
]