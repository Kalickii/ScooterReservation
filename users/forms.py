from .models import UserProfile

from allauth.account.forms import SignupForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=True)
    phone_number = PhoneNumberField(required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        UserProfile.objects.create(user=user)
        return user
