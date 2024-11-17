import pytest

from users.models import CustomUser, UserProfile


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
