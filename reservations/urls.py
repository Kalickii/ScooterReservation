from django.urls import path

from reservations import views as res

urlpatterns = [
    path('', res.ReservationListView.as_view(), name='reservations-list'),
    path('new/<int:scooter_id>', res.ReservationCreateView.as_view(), name='reservations-create'),
    path('<int:reservation_id>', res.ReservationDetailView.as_view(), name='reservations-detail'),
    path('<int:reservation_id>/edit', res.ReservationUpdateView.as_view(), name='reservations-update'),
    path('create_checkout_session/<int:reservation_id>', res.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', res.PaymentSuccessView.as_view(), name='payment-success'),
    path('cancel/', res.PaymentCancelView.as_view(), name='payment-cancel'),
]
