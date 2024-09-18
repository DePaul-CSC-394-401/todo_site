from django import forms
from .models import TodoItem


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        exclude = ["user"]
        widgets = {"due_date": forms.SelectDateWidget}
