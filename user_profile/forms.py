from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # email field added to the form

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
