from django import forms

from teams.models import Team, TodoList, TeamInvite
from todo.models import TodoItem


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"


class TodoListForm(forms.ModelForm):
    class Meta:
        model = TodoList
        exclude = ["team"]


class TeamTodoForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        exclude = [
            "user",
            "todo_list",
            "timer_started",
            "start_time",
            "end_time",
            "is_archived",
            "total_time_spent",
            "category",
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


class SendInviteForm(forms.ModelForm):
    class Meta:
        model = TeamInvite
        exclude = ["team", "accepted", "sender"]
