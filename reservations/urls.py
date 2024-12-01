from django.urls import path

from reservations import views as res

urlpatterns = [
    path('', res.ReservationListView.as_view(), name='reservations-list'),
    path('new/', res.ReservationCreateView.as_view(), name='reservations-create'),
    path('<int:pk>/', res.ReservationDetailView.as_view(), name='reservations-detail'),
    path('<int:pk>/edit/', res.ReservationUpdateView.as_view(), name='reservation-update'),
]