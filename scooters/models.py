from django.db import models


def directory_path(instance, filename):
    return 'scooters/{0}/{1}'.format(instance.registration_number, filename)

class Scooter(models.Model):
    brand = models.CharField(max_length=50)
    scooter_model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    year = models.IntegerField()
    registration_number = models.CharField(max_length=50, unique=True)
    available = models.BooleanField(default=False)
    image = models.ImageField(upload_to=directory_path)
    daily_price = models.IntegerField()
    weekly_price = models.IntegerField()
    monthly_price = models.IntegerField()
    deposit_amount = models.IntegerField()

    def __str__(self):
        return f'{self.brand} {self.scooter_model}'
