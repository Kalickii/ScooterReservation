from django.contrib import admin

from reservations.models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'userprofile', 'scooter', 'start_date', 'end_date', 'payment_status', 'total_price')

admin.site.register(Reservation, ReservationAdmin)
