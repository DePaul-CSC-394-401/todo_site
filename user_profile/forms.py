from django import forms
from django.contrib.auth.forms import UserCreationForm

from user_profile.models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # email field added to the form

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email"]
