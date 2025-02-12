import time
import threading

import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.db import models

from scooters.models import Scooter
from users.models import UserProfile

stripe.api_key = settings.STRIPE_SECRET_KEY

class Reservation(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_status = models.BooleanField(default=False)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.IntegerField(null=True, blank=True)

    # def delete_after_delay(self):
    #     def check_and_delete():
    #         print('started countdown')
    #         time.sleep(10)
    #         reservation = Reservation.objects.filter(pk=self.pk, payment_status=False).first()
    #         if reservation:
    #             if reservation.stripe_payment_intent_id:
    #                 session = stripe.checkout.Session.retrieve(reservation.stripe_payment_intent_id)
    #                 if session.payment_status == "open":
    #                     print(f"Rezerwacja {reservation.pk} - płatność w toku, ponowne sprawdzenie za 3 min")
    #                     threading.Thread(target=check_and_delete, daemon=True).start()
    #                     return
    #                 if session.payment_status == "paid":
    #                     print(f"Rezerwacja {reservation.pk} - zapłacona, nie usuwam")
    #                     return
    #             print('rezerwacja usunięta')
    #             reservation.delete()

    #     threading.Thread(target=check_and_delete, daemon=True).start()

    def save(self, *args, **kwargs):
        self.total_price = self.scooter.deposit_amount
        super().save(*args, **kwargs)
        self.delete_after_delay()
