from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Todo_Item

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True) # enail field added to the form

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"] 

class UpdateProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo_Item
        exclude = ["user"]
        widgets = {"due_date": forms.SelectDateWidget}
