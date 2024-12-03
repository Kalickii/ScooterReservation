import pytest
from datetime import datetime, timedelta, date

from django.core.exceptions import ValidationError
from django.urls import reverse

from reservations.models import Reservation


@pytest.mark.django_db
def test_reservation_calculate_price_method(reservation):
    reservation.calculate_price()
    assert reservation.total_price == 500


@pytest.mark.django_db
def test_reservation_create_view_access(client, simple_user, available_scooter):
    url = reverse('reservations-create', kwargs={'scooter_id': available_scooter.pk})
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(simple_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_reservation_create_view_data(client, simple_user, available_scooter):
    url = reverse('reservations-create', kwargs={'scooter_id': available_scooter.pk})
    client.force_login(simple_user)
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data={
            'start_date':  date.today() + timedelta(days=1),
            'end_date': date.today() + timedelta(days=5),
    })
    assert response.status_code == 302
    assert response.url == reverse('scooter-list') ### WAITING TO BE FINISHED - REDIRECT TO PAYMENT CHECKOUT             !!!       !!!        !!!       !!!
    reservations = Reservation.objects.filter(scooter=available_scooter)
    assert reservations.count() == 1
    assert reservations.first().start_date == date.today() + timedelta(days=1)
    assert reservations.first().total_price == available_scooter.deposit_amount
    assert reservations.first().payment_status == False


@pytest.mark.django_db
def test_reservation_create_with_invalid_date(client, simple_user, available_scooter):
    url = reverse('reservations-create', kwargs={'scooter_id': available_scooter.pk})
    client.force_login(simple_user)
    response = client.post(url, data={
        'start_date': date.today() + timedelta(days=6),
        'end_date': date.today() + timedelta(days=3),
    })
    assert response.status_code == 200
    assert Reservation.objects.filter(scooter=available_scooter).exists() is False

    response = client.post(url, data={
        'start_date': date.today() + timedelta(days=2),
        'end_date': date.today() + timedelta(days=2),
    })
    assert response.status_code == 200
    assert Reservation.objects.filter(scooter=available_scooter).exists() is False


@pytest.mark.django_db
def test_reservation_create_with_taken_date(client, simple_user, available_scooter, reservation):
    url = reverse('reservations-create', kwargs={'scooter_id': available_scooter.pk})
    client.force_login(simple_user)
    response = client.post(url, data={
        'start_date': date.today() + timedelta(days=9),
        'end_date': date.today() + timedelta(days=16),
    })
    assert response.status_code == 200
    assert Reservation.objects.filter(scooter=available_scooter).exists()
    assert Reservation.objects.filter(start_date=date.today() + timedelta(days=9)).exists() is False
