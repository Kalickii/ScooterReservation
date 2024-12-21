from django.db import models

from scooters.models import Scooter
from users.models import UserProfile


class Reservation(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_status = models.BooleanField(default=False)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.IntegerField(null=True, blank=True)
