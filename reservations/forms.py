from datetime import date, timedelta
from django import forms
from django.core.exceptions import ValidationError

from reservations.models import Reservation
from gettext import gettext as _

from scooters.models import Scooter


class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'start_date',
            'end_date',
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'min': date.today() + timedelta(days=1)}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'min': date.today() + timedelta(days=2)}),
        }

    def __init__(self, *args, **kwargs):
        """
        Passing scooter_id argument from url to form
        """
        self.scooter_id = kwargs.pop('scooter_id')
        super(ReservationCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Validation - checking if start date is not equal to end date, or after end_date,
        - checking if there is no previous reservation for given dates for current scooter
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and (start_date >= end_date):
            raise ValidationError(_('Start date must be before end date'))

        current_delta = end_date - start_date
        current_period = [(start_date + timedelta(days=i)) for i in range(0, current_delta.days + 1)]

        for reservation in Reservation.objects.filter(scooter=Scooter.objects.get(id=self.scooter_id)):
            delta = reservation.end_date - reservation.start_date
            period = [(reservation.start_date + timedelta(days=i)) for i in range(0, delta.days + 1)]

            for day in current_period:
                if day in period:
                    raise ValidationError(_('There is a reservation somewhere in this period'))
        return cleaned_data
