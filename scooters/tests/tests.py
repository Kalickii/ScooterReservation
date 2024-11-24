import pytest

from scooters.models import Scooter

@pytest.mark.django_db
def test_scooter_list_as_user(scooters):
    pass