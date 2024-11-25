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


@pytest.mark.django_db
def test_available_scooter_detail_view(client, available_scooter):
    url = reverse('scooter-detail', kwargs={'scooter_id': available_scooter.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooter'].brand == available_scooter.brand


@pytest.mark.django_db
def test_unavailable_scooter_detail_access(client, staff_user, unavailable_scooter):
    url = reverse('scooter-detail', kwargs={'scooter_id': unavailable_scooter.id})
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooter'].brand == unavailable_scooter.brand


@pytest.mark.django_db
def test_scooter_detail_delete(client, superuser_user, available_scooter):
    url = reverse('scooter-detail', kwargs={'scooter_id': available_scooter.id})
    client.force_login(superuser_user)
    assert Scooter.objects.filter(id=available_scooter.id).exists()
    response = client.post(url)
    assert Scooter.objects.filter(id=available_scooter.id).exists() is False
    assert response.status_code == 302
