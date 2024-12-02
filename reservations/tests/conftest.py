import pytest
from datetime import datetime
from reservations.models import Reservation
from scooters.tests.conftest import available_scooter
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
def reservation(available_scooter, simple_user):
    reservation = Reservation.objects.create(
        userprofile=simple_user.userprofile,
        scooter=available_scooter,
        start_date=datetime(2024, 12, 1),
        end_date=datetime(2024, 12, 7),
    )
    return reservation
