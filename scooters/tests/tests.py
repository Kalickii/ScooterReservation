import pytest
from django.urls import reverse
from django.views.generic import ListView

from scooters.models import Scooter

@pytest.mark.django_db
def test_scooter_list_access(client, staff_user, scooters):
    url = reverse('scooter-list')

    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooters'].count() == Scooter.objects.filter(available=True).count()

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooters'].count() == Scooter.objects.all().count()
