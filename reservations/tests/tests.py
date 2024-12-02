import pytest


@pytest.mark.django_db
def test_reservation_calculate_price_method(reservation):
    reservation.calculate_price()
    assert reservation.total_price == 500
