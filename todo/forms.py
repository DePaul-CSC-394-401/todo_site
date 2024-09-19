from django import forms
from .models import TodoItem, Category


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        exclude = ["user"]
        widgets = {"due_date": forms.SelectDateWidget}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ["user"]
