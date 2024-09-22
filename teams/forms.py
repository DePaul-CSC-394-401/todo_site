from django import forms

from teams.models import Team
from todo.models import SharedTodoList, SharedTodoItem


# class CreateTodoListForm(forms.Form):
#     list_name = forms.CharField(required=True, max_length=100)
#     list_description = forms.CharField(required=True, max_length=100)
#     td_title = forms.CharField(required=False, max_length=100)
#     td_description = forms.CharField(required=False, max_length=100)
#     td_due_date = forms.DateTimeField(required=False)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"


class SharedListForm(forms.ModelForm):
    class Meta:
        model = SharedTodoList
        exclude = ["team"]


class SharedTodoItemForm(forms.ModelForm):
    class Meta:
        model = SharedTodoItem
        exclude = [
            "assigned_user",
            "is_archived",
            "total_time_spent",
            "start_time",
            "end_time",
            "timer_started",
            "progress",
            "shared_todo_list",
        ]
        widgets = {"due_date": forms.DateTimeInput(attrs={"type": "datetime-local"})}
