import time
import threading

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

    def delete_after_delay(self):
        def check_and_delete():
            time.sleep(180)
            obj = Reservation.objects.get(pk=self.pk)
            if obj.payment_status == False:
                obj.delete()
            
        threading.Thread(target=check_and_delete, daemon=True).start()

    def save(self, *args, **kwargs):
        self.total_price = self.scooter.deposit_amount
        super().save(*args, **kwargs)
        self.delete_after_delay()
