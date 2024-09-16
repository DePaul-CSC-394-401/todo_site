from django import forms
from .models import Todo_Item


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo_Item
        exclude = ["user"]
        widgets = {"due_date": forms.SelectDateWidget}
