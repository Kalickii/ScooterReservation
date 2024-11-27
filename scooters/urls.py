from django.urls import path

from scooters import views as scooters


urlpatterns = [
    path('', scooters.ScooterListView.as_view(), name='scooter-list'),
    path('detail/<scooter_id>', scooters.ScooterDetailView.as_view(), name='scooter-detail'),
    path('detail/<scooter_id>/edit', scooters.ScooterUpdateView.as_view(), name='scooter-update'),
    path('add', scooters.ScooterCreateView.as_view(), name='scooter-create'),
]
