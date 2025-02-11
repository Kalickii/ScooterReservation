from .models import UserProfile

from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField



User = get_user_model()


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=True)
    phone_number = PhoneNumberField(required=True)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=phone_number).exists():
            self.add_error("phone_number", "That phone number is already taken.")
        return phone_number

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        UserProfile.objects.create(user=user)
        return user
