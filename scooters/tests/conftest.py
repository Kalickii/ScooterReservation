from pytest import fixture

from scooters.models import Scooter


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
