from allauth.core.internal.httpkit import redirect
from django.views.generic import ListView, DetailView, UpdateView

from scooters.models import Scooter


class ScooterListView(ListView):
    model = Scooter
    context_object_name = 'scooters'
    template_name = 'scooters/main.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Scooter.objects.all()
        return Scooter.objects.filter(available=True)


class ScooterDetailView(DetailView):
    model = Scooter
    context_object_name = 'scooter'
    template_name = 'scooters/scooter_detail.html'
    pk_url_kwarg = 'scooter_id'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Scooter.objects.all()
        return Scooter.objects.filter(available=True)

    def post(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            Scooter.objects.get(pk=self.kwargs['scooter_id']).delete()
            return redirect('scooter-list')


class ScooterUpdateView(UpdateView):
    pass
