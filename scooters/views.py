from rest_framework.generics import ListAPIView, RetrieveAPIView

from scooters.serializers import ScooterSerializer
from .models import Scooter


class ScooterListView(ListAPIView):
    serializer_class = ScooterSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Scooter.objects.all()
        return Scooter.objects.filter(available=True)
