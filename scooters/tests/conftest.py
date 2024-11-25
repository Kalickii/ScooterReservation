from pytest import fixture

from scooters.models import Scooter
from users.models import CustomUser


@fixture
def staff_user():
    staff_user = CustomUser.objects.create_user(
        email='staff@gmail.com',
        first_name='Staff',
        last_name='User',
        phone_number='+5555555555',
        is_staff=True,
    )
    return staff_user


@fixture
def scooters():
    for _ in range(5):
        scooter = Scooter.objects.create(
            brand=f"Yamaha{_}",
            scooter_model=f"XMax 300 {_}",
            capacity=300,
            year=2022,
            registration_number=f"KR12345{_}",
            available= bool(_ % 2),
            image=None,
            daily_price=100,
            weekly_price=600,
            monthly_price=2000,
            deposit_amount=500,
        )


@fixture
def available_scooter():
    scooter = Scooter.objects.create(
        brand="Yamaha",
        scooter_model="XMax 300",
        capacity=300,
        year=2022,
        registration_number="KR12345",
        available=True,
        image=None,
        daily_price=100,
        weekly_price=600,
        monthly_price=2000,
        deposit_amount=500,
    )
    return scooter


@fixture
def unavailable_scooter():
    scooter = Scooter.objects.create(
        brand="Yamaha",
        scooter_model="XMax 300",
        capacity=300,
        year=2022,
        registration_number="KR12345",
        available=False,
        image=None,
        daily_price=100,
        weekly_price=600,
        monthly_price=2000,
        deposit_amount=500,
    )
    return scooter
