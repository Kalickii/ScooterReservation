from rest_framework.generics import ListAPIView

from scooters.serializers import ScooterSerializer
from .models import Scooter


class ScooterListView(ListAPIView):
    serializer_class = ScooterSerializer

    def get_queryset(self):
        return Scooter.objects.filter(available=True)

