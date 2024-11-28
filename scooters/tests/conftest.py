from PIL import Image
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
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
def superuser_user():
    superuser_user = CustomUser.objects.create_superuser(
        email='superuser@gmail.com',
        first_name='Superuser',
        last_name='User',
        phone_number='+555566666',
        password='admin',
    )
    return superuser_user


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
            image=SimpleUploadedFile(
                name='test_image.jpg',
                content=b'some_fake_image_content',
                content_type='image/jpeg',
            ),
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
        image=SimpleUploadedFile(
            name='test_image.jpg',
            content=b'some_fake_image_content',
            content_type='image/jpeg',
        ),
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
        image=SimpleUploadedFile(
            name='test_image.jpg',
            content=b'some_fake_image_content',
            content_type='image/jpeg',
        ),
        daily_price=100,
        weekly_price=600,
        monthly_price=2000,
        deposit_amount=500,
    )
    return scooter


@fixture
def create_image():
    image = Image.new('RGB', (100, 100))
    buffer = BytesIO()
    image.save(buffer, 'JPEG')
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=buffer.getvalue(),
        content_type='image/jpeg',
    )
