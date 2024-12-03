from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView


from reservations.forms import ReservationCreateForm
from reservations.models import Reservation
from scooters.models import Scooter


class ReservationListView(ListView):
    pass


class ReservationUpdateView(UpdateView):
    pass


class ReservationCreateView(UserPassesTestMixin, CreateView):
    model = Reservation
    template_name = 'reservations/reservation_create.html'
    pk_url_kwarg = 'scooter_id'
    form_class = ReservationCreateForm

    def form_valid(self, form):
        scooter = Scooter.objects.get(pk=self.kwargs['scooter_id'])
        form.instance.scooter = scooter
        form.instance.userprofile = self.request.user.userprofile
        form.instance.total_price = scooter.deposit_amount
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'scooter_id': self.kwargs['scooter_id']})
        return kwargs

    def get_success_url(self):
        return reverse('scooter-list') ### WAITING TO BE FINISHED - REDIRECT TO PAYMENT CHECKOUT

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        raise Http404 ### WAITING TO BE FINISHED - REDIRECT TO REGISTER WEBSITE


class ReservationDetailView(DetailView):
    pass
