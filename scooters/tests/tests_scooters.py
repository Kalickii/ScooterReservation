import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from scooters.models import Scooter


@pytest.mark.django_db
def test_scooter_list_access(client, staff_user, scooters):
    url = reverse('scooter-list')

    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooters'].count() == Scooter.objects.filter(available=True).count()

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooters'].count() == Scooter.objects.all().count()


@pytest.mark.django_db
def test_available_scooter_detail_view(client, available_scooter):
    url = reverse('scooter-detail', kwargs={'scooter_id': available_scooter.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooter'].brand == available_scooter.brand


@pytest.mark.django_db
def test_unavailable_scooter_detail_access(client, staff_user, unavailable_scooter):
    url = reverse('scooter-detail', kwargs={'scooter_id': unavailable_scooter.id})
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooter'].brand == unavailable_scooter.brand


@pytest.mark.django_db
def test_scooter_detail_delete(client, superuser_user, available_scooter):
    url = reverse('scooter-detail', kwargs={'scooter_id': available_scooter.id})
    client.force_login(superuser_user)
    assert Scooter.objects.filter(id=available_scooter.id).exists()
    response = client.post(url)
    assert Scooter.objects.filter(id=available_scooter.id).exists() is False
    assert response.status_code == 302


@pytest.mark.django_db
def test_scooter_detail_edit_access(client, staff_user, superuser_user, available_scooter):
    url = reverse('scooter-update', kwargs={'scooter_id': available_scooter.id})

    response = client.get(url)
    assert response.status_code == 404

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(superuser_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_scooter_detail_edit_data(client, superuser_user, available_scooter):
    available_scooter.image = SimpleUploadedFile(
                name='test_image.jpg',
                content=b'some_fake_image_content',
                content_type='image/jpeg',
            )
    available_scooter.save()
    url = reverse('scooter-update', kwargs={'scooter_id': available_scooter.id})
    client.force_login(superuser_user)
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['scooter'].available == True
    assert response.context['scooter'].daily_price == 100
    response = client.post(url, data={
        'available': False,
        'daily_price': 200,
        'weekly_price': available_scooter.weekly_price,
        'monthly_price': available_scooter.monthly_price,
        'deposit_amount': available_scooter.deposit_amount,
    })
    assert response.status_code == 302
    assert Scooter.objects.get(id=available_scooter.id).available is False
    assert Scooter.objects.get(id=available_scooter.id).daily_price == 200


@pytest.mark.django_db
def test_scooter_create_access(client, staff_user, superuser_user):
    url = reverse('scooter-create')

    response = client.get(url)
    assert response.status_code == 404

    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 404

    client.force_login(superuser_user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_scooter_create_data(client, superuser_user, create_image):
    url = reverse('scooter-create')
    client.force_login(superuser_user)
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, data={
        'brand': 'Romet',
        'scooter_model': 'Zadymiarz 4T',
        'capacity': 50,
        'year': 2015,
        'registration_number': 'KRAM30B',
        'available': False,
        'image': create_image,
        'daily_price': 100,
        'weekly_price': 400,
        'monthly_price': 1300,
        'deposit_amount': 400,
    })
    assert response.status_code == 302
    assert Scooter.objects.count() == 1
    assert Scooter.objects.first().available is False
    assert Scooter.objects.first().registration_number == 'KRAM30B'
