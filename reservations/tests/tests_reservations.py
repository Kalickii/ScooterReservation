import pytest
from datetime import timedelta, date

from django.urls import reverse

from reservations.models import Reservation


@pytest.mark.django_db
def test_reservation_calculate_price_method(reservation):
    reservation.calculate_price()
    assert reservation.total_price == 500


# RESERVATION CREATE VIEW

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
    assert response.url == reverse('reservations-detail', kwargs={'reservation_id': Reservation.objects.get(start_date=date.today() + timedelta(days=1)).pk})
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
    reservation.payment_status = True
    reservation.save()
    url = reverse('reservations-create', kwargs={'scooter_id': available_scooter.pk})
    client.force_login(simple_user)
    response = client.post(url, data={
        'start_date': date.today() + timedelta(days=9),
        'end_date': date.today() + timedelta(days=16),
    })
    assert response.status_code == 200
    assert Reservation.objects.filter(scooter=available_scooter).exists()
    assert Reservation.objects.filter(start_date=date.today() + timedelta(days=9)).exists() is False


# RESERVATION LIST VIEW

@pytest.mark.django_db
def test_reservation_list_view_access(client, staff_user, simple_user):
    url = reverse('reservations-list')
    client.force_login(simple_user)
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_reservation_list_view_data(client, staff_user, superuser_user, reservations):
    url = reverse('reservations-list')
    client.force_login(staff_user)
    response = client.get(url)
    assert list(response.context['reservations']) == list(Reservation.objects.all().order_by('start_date'))



@pytest.mark.django_db
def test_reservation_list_view_delete_functionality_access(client, staff_user, superuser_user, reservation):
    url = reverse('reservations-list')
    assert Reservation.objects.filter(pk=reservation.pk).exists()
    client.force_login(staff_user)
    response = client.post(url, data={'reservation_id': reservation.pk})
    assert response.status_code == 302
    assert response.url == reverse('reservations-list')
    assert Reservation.objects.filter(pk=reservation.pk).exists()

    client.force_login(superuser_user)
    response = client.post(url, data={'reservation_id': reservation.pk})
    assert response.status_code == 302
    assert response.url == reverse('reservations-list')
    assert Reservation.objects.filter(pk=reservation.pk).exists() is False


# RESERVATION DETAIL VIEW

@pytest.mark.django_db
def test_reservation_detail_view_access(client, simple_user, simple_user2, staff_user, reservation):
    url = reverse('reservations-detail', kwargs={'reservation_id': reservation.pk})
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(simple_user)
    response = client.get(url)
    assert response.status_code == 200

    client.force_login(simple_user2)
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_reservation_detail_view_data(client, simple_user, reservation):
    url = reverse('reservations-detail', kwargs={'reservation_id': reservation.pk})
    client.force_login(simple_user)
    response = client.get(url)
    assert response.context['reservation'].start_date == reservation.start_date
    assert response.context['reservation'].end_date == reservation.end_date
    assert response.context['reservation'].payment_status == False


# RESERVATION UPDATE VIEW

@pytest.mark.django_db
def test_reservation_update_view_access(client, simple_user, staff_user, reservation):
    url = reverse('reservations-update', kwargs={'reservation_id': reservation.pk})
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(simple_user)
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_reservation_update_view_data(client, staff_user, reservation):
    url = reverse('reservations-update', kwargs={'reservation_id': reservation.pk})
    client.force_login(staff_user)
    response = client.post(url, data={
        'start_date': reservation.start_date + timedelta(days=1),
        'end_date': reservation.end_date - timedelta(days=1),
        'payment_status': True,
        'scooter': reservation.scooter.pk,
    })
    assert response.status_code == 302
    assert response.url == reverse('reservations-detail', kwargs={'reservation_id': reservation.pk})
    assert Reservation.objects.get(pk=reservation.pk).start_date == reservation.start_date + timedelta(days=1)
    assert Reservation.objects.get(pk=reservation.pk).end_date == reservation.end_date - timedelta(days=1)
    assert Reservation.objects.get(pk=reservation.pk).payment_status == True


@pytest.mark.django_db
def test_reservation_update_view_with_invalid_date(client, staff_user, reservation):
    url = reverse('reservations-update', kwargs={'reservation_id': reservation.pk})
    client.force_login(staff_user)
    response = client.post(url, data={
        'start_date': date.today() + timedelta(days=5),
        'end_date': date.today() + timedelta(days=2),
        'payment_status': True,
        'scooter': reservation.scooter.pk,
    })
    assert response.status_code == 200
    assert Reservation.objects.filter(pk=reservation.pk, start_date=date.today() + timedelta(days=5)).exists() is False

    response = client.post(url, data={
        'start_date': date.today() + timedelta(days=3),
        'end_date': date.today() + timedelta(days=3),
        'payment_status': True,
        'scooter': reservation.scooter.pk,
    })
    assert response.status_code == 200
    assert Reservation.objects.filter(pk=reservation.pk, start_date=date.today() + timedelta(days=3)).exists() is False



@pytest.mark.django_db
def test_reservation_update_view_with_taken_date(client, staff_user, reservations):
    reservation = Reservation.objects.all().first()
    url = reverse('reservations-update', kwargs={'reservation_id': reservation.pk})
    client.force_login(staff_user)
    response = client.post(url, data={
        'start_date': date.today() + timedelta(days=11),
        'end_date': date.today() + timedelta(days=14),
        'payment_status': True,
        'scooter': reservation.scooter.pk,
    })
    assert response.status_code == 200
    assert Reservation.objects.filter(pk=reservation.pk, end_date=date.today() + timedelta(days=10)).exists()
    assert Reservation.objects.filter(pk=reservation.pk, end_date=date.today() + timedelta(days=14)).exists() is False
