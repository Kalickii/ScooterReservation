from django.urls import path

from scooters import views as scooters


urlpatterns = [
    path('', scooters.ScooterListView.as_view(), name='scooter-list'),
    path('<scooter_id>', scooters.ScooterDetailView.as_view(), name='scooter-detail'),
    path('<scooter_id>/edit', scooters.ScooterUpdateView.as_view(), name='scooter-update'),
    path('create/', scooters.ScooterCreateView.as_view(), name='scooter-create'),
]
