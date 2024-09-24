from django import forms
from .models import TodoItem, Category, TodoList


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        exclude = [
            "user",
            "timer_started",
            "start_time",
            "end_time",
            "is_archived",
            "total_time_spent",
            "todo_list",
            "assigned_to",
        ]
        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "progress": forms.TextInput(
                attrs={
                    "step": "1",
                    "type": "range",
                    "value": "50",
                    "min": "0",
                    "max": "100",
                }
            ),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ["user"]
