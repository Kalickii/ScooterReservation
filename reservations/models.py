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

    def delete_after_delay(self):
        '''
        Function for deleting reservation if user does not open checkout session to do the payment in 3 minutes after creating reservation.
        If user open checkout session, everything else is handled by webhooks
        '''
        def check_and_delete():
            time.sleep(180)
            reservation = Reservation.objects.filter(pk=self.pk, payment_status=False).first()
            if reservation:
                if reservation.stripe_payment_intent_id:
                    session = stripe.checkout.Session.retrieve(reservation.stripe_payment_intent_id)
                    if session.status == "open":
                        return
                reservation.delete()

        threading.Thread(target=check_and_delete, daemon=True).start()

    def save(self, *args, **kwargs):
        self.total_price = self.scooter.deposit_amount
        super().save(*args, **kwargs)
        if not self.stripe_payment_intent_id:
            self.delete_after_delay()
