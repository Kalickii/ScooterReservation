from django.views.generic import ListView

from scooters.models import Scooter


class ScooterListView(ListView):
    model = Scooter
    context_object_name = 'scooters'
    template_name = 'scooters/main.html'
