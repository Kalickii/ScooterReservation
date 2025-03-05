import pytest
from rest_framework.reverse import reverse

from reservations.models import Reservation
from users.models import CustomUser, UserProfile
from scooters.tests.conftest import staff_user, superuser_user
from reservations.tests.conftest import simple_user, simple_user2, reservations, available_scooter


@pytest.mark.django_db
def test_userprofile_creation():
    user = CustomUser.objects.create_user(
        email='test@example.com',
        password='password123',
        first_name='John',
        last_name='Doe',
        phone_number='+1234567890'
    )
    assert UserProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_user_dashboard_access(client, simple_user, simple_user2):
    url = reverse('user-dashboard')
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(simple_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['user'] == simple_user

    client.force_login(simple_user2)
    response = client.get(reverse('user-dashboard'), kwargs={'user_id': simple_user.id})
    assert response.status_code == 200
    assert response.context['user'] == simple_user2


@pytest.mark.django_db
def test_user_dashboard_reservations(client, simple_user, reservations):
    url = reverse('user-dashboard')
    client.force_login(simple_user)
    response = client.get(url)
    assert response.context['reservations'][0] == Reservation.objects.filter(userprofile=simple_user.userprofile).order_by('start_date').reverse().first()
    assert response.context['reservations'].count() == Reservation.objects.filter(userprofile=simple_user.userprofile).count()


@pytest.mark.django_db
def test_user_dashboard_incoming_reservation(client, simple_user, reservations):
    url = reverse('user-dashboard')
    client.force_login(simple_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['next_reservation'] == Reservation.objects.filter(userprofile=simple_user.userprofile).order_by('start_date').first()

