from pytest_django.fixtures import client
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from scooters.serializers import ScooterSerializer
from .models import Scooter


class ScooterListView(ListAPIView):
    serializer_class = ScooterSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Scooter.objects.all()
        return Scooter.objects.filter(available=True)


class ScooterDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ScooterSerializer
    lookup_url_kwarg = 'scooter_id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Scooter.objects.all()
        return Scooter.objects.filter(available=True)

    def update(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)
