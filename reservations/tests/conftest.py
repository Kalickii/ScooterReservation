import pytest
from datetime import date, timedelta
from reservations.models import Reservation
from scooters.tests.conftest import available_scooter, staff_user, superuser_user
from users.models import CustomUser


@pytest.fixture
def simple_user():
    user = CustomUser.objects.create_user(
        email='simpleuser@gmail.com',
        first_name='simple',
        last_name='user',
        phone_number='123456789',
        password='simplepassword123'
    )
    return user


@pytest.fixture
def simple_user2():
    user = CustomUser.objects.create_user(
        email='simpleuser2@gmail.com',
        first_name='simple2',
        last_name='user2',
        phone_number='987654321',
        password='simplepassword123'
    )
    return user


@pytest.fixture
def reservation(available_scooter, simple_user):
    reservation = Reservation.objects.create(
        userprofile=simple_user.userprofile,
        scooter=available_scooter,
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=10),
    )
    return reservation


@pytest.fixture
def reservations(available_scooter, simple_user):
    Reservation.objects.create(
        userprofile=simple_user.userprofile,
        scooter=available_scooter,
        start_date=date.today() + timedelta(days=1),
        end_date=date.today() + timedelta(days=10),
    )
    Reservation.objects.create(
        userprofile=simple_user.userprofile,
        scooter=available_scooter,
        start_date=date.today() + timedelta(days=13),
        end_date=date.today() + timedelta(days=15),
    )
    Reservation.objects.create(
        userprofile=simple_user.userprofile,
        scooter=available_scooter,
        start_date=date.today() + timedelta(days=23),
        end_date=date.today() + timedelta(days=29),
    )
    Reservation.objects.create(
        userprofile=simple_user.userprofile,
        scooter=available_scooter,
        start_date=date.today() + timedelta(days=16),
        end_date=date.today() + timedelta(days=19),
    )
    Reservation.objects.create(
        userprofile=simple_user.userprofile,
        scooter=available_scooter,
        start_date=date.today() + timedelta(days=30),
        end_date=date.today() + timedelta(days=31),
    )
