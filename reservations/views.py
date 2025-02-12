from datetime import datetime

import stripe
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.conf import settings

from reservations.forms import ReservationCreateForm, ReservationUpdateForm
from reservations.models import Reservation
from scooters.models import Scooter
from gettext import gettext as _


stripe.api_key = settings.STRIPE_SECRET_KEY

class ReservationListView(UserPassesTestMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'
    queryset = Reservation.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        incoming_reservations = Reservation.objects.filter(start_date__gt=datetime.today()).order_by('start_date')
        past_reservations = Reservation.objects.filter(start_date__lte=datetime.today(), payment_status=True).order_by('start_date')
        context.update({
                'incoming_reservations': incoming_reservations,
                'past_reservations': past_reservations
                        })
        return context


    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            Reservation.objects.get(pk=request.POST.get('reservation_id')).delete()
        return redirect('reservations-list')


class ReservationUpdateView(UserPassesTestMixin, UpdateView):
    model = Reservation
    template_name = 'reservations/reservation_edit.html'
    pk_url_kwarg = 'reservation_id'
    form_class = ReservationUpdateForm

    def get_success_url(self):
        return reverse('reservations-detail', kwargs={'reservation_id': self.object.pk})

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404


class ReservationCreateView(UserPassesTestMixin, CreateView):
    model = Reservation
    template_name = 'reservations/reservation_create.html'
    pk_url_kwarg = 'scooter_id'
    form_class = ReservationCreateForm

    def form_valid(self, form):
        scooter_id = self.kwargs['scooter_id']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        with transaction.atomic():
            scooter = Scooter.objects.select_for_update().get(id=scooter_id)

            conflicting_reservations = Reservation.objects.filter(
                scooter=scooter,
                start_date__lte=end_date,
                end_date__gte=start_date
            )

            if conflicting_reservations.exists():
                form.add_error(None, _('This scooter already has a reservation somewhere in that period'))
                return self.form_invalid(form)

            form.instance.scooter = scooter
            form.instance.userprofile = self.request.user.userprofile
            return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'scooter_id': self.kwargs['scooter_id']})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scooter = Scooter.objects.get(pk=self.kwargs['scooter_id'])
        reservations = Reservation.objects.filter(scooter=scooter, end_date__gt=datetime.today(), payment_status=True).order_by('start_date')
        context.update({'reservations': reservations})
        return context

    def get_success_url(self):
        return reverse('reservations-detail', kwargs={'reservation_id': self.object.id})

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        raise Http404


class ReservationDetailView(UserPassesTestMixin, DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'
    pk_url_kwarg = 'reservation_id'
    context_object_name = 'reservation'

    def get_object(self, **kwargs):
        return get_object_or_404(Reservation, pk=self.kwargs['reservation_id'])

    def test_func(self):
        reservation = self.get_object()
        user = self.request.user
        return user.is_authenticated and (user.userprofile == reservation.userprofile or user.is_staff)

    def handle_no_permission(self):
        raise Http404


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        reservation_id = self.kwargs['reservation_id']
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        image_url = request.build_absolute_uri(reservation.scooter.image.url)
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'pln',
                        'product_data': {
                            'name': f'{reservation.scooter} Reservation',
                            'images': [image_url],
                        },
                        'unit_amount': int(reservation.total_price * 100),
                    },
                    'quantity': 1,
            },
            ],
            mode='payment',
            success_url=f'http://127.0.0.1:8000/reservations/success/?reservation_id={reservation_id}',
            cancel_url=f'http://127.0.0.1:8000/reservations/cancel/?reservation_id={reservation_id}',
        )
        reservation.stripe_payment_intent_id = checkout_session.id
        reservation.save()
        return redirect(checkout_session.url)


class PaymentSuccessView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        reservation = get_object_or_404(Reservation, pk=self.request.GET.get('reservation_id'))
        reservation.payment_status = True
        reservation.save()
        return render(request, 'reservations/payment_success.html')

    def test_func(self):
        reservation = get_object_or_404(Reservation, pk=self.request.GET.get('reservation_id'))
        return self.request.user == reservation.userprofile.user

    def handle_no_permission(self):
        raise Http404


class PaymentCancelView(UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        reservation = Reservation.objects.get(pk=request.GET.get('reservation_id'))
        reservation.delete()
        return render(request, 'reservations/payment_cancel.html')

    def test_func(self):
        reservation = get_object_or_404(Reservation, pk=self.request.GET.get('reservation_id'))
        return self.request.user == reservation.userprofile.user

    def handle_no_permission(self):
        raise Http404
