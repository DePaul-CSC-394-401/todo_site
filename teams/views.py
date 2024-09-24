from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from todo.forms import TodoForm
from todo.models import TodoList, TodoItem
from user_profile.models import CustomUser
from .forms import TeamForm, TodoListForm, TeamTodoForm, SendInviteForm
from .models import Team, TeamInvite


# Create your views here.


@login_required(login_url="user_profile:login")
def get_all_teams(request):
    user = request.user
    teams_list = Team.objects.filter(customuser=user)
    context = {"teams_list": teams_list}
    return render(request, "teams/get-all-teams.html", context)


@login_required(login_url="user_profile:login")
def get_team(request, team_id):
    team = Team.objects.get(pk=team_id)
    todo_lists = TodoList.objects.filter(team=team)
    todo_dict = {}  # todo_list_object: todo_items_list
    if request.method == "POST":
        invite_form = SendInviteForm(request.POST)
        if invite_form.is_valid():
            invite = invite_form.save(commit=False)
            invite.team = team
            invite.sender = request.user
            invite.save()
            messages.success(request, "Team Invite Sent!")
    else:
        invite_form = SendInviteForm()
    for todo_list in todo_lists:
        todo_dict[todo_list] = TodoItem.objects.filter(todo_list=todo_list)
    context = {"team": team, "todo_dict": todo_dict, "invite_form": invite_form}
    return render(request, "teams/get-team.html", context)


@login_required(login_url="user_profile:login")
def edit_team(request, team_id):
    team = Team.objects.get(pk=team_id)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated")
            return redirect("teams:get_team", team_id=team_id)
    else:
        form = TeamForm(instance=team)
    context = {"form": form}
    return render(request, "teams/edit-team.html", context)


@login_required(login_url="user_profile:login")
def create_team(request):
    user = request.user
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            team.customuser_set.add(user)
            team.save()
            messages.success(request, "Team Created!")
            return redirect("teams:get_team", team_id=team.id)
    else:
        form = TeamForm()
    context = {"form": form}
    return render(request, "teams/create-team.html", context)


@login_required(login_url="user_profile:login")
def delete_team(request, team_id):
    team = Team.objects.get(pk=team_id)
    team.delete()
    messages.success(request, "Team deleted")
    return redirect("teams:get_teams")


@login_required(login_url="user_profile:login")
def create_todo_list(request, team_id):
    team = Team.objects.get(pk=team_id)
    if request.method == "POST":
        form = TodoListForm(request.POST)
        if form.is_valid():
            todo_list = form.save(commit=False)
            todo_list.team = team
            todo_list.save()
            messages.success(request, "Shared Todo List Created!")
            return redirect("teams:get_team", team_id=team_id)
    else:
        form = TodoListForm()
    context = {"form": form}
    return render(request, "teams/create-todo-list.html", context)


@login_required(login_url="user_profile:login")
def edit_todo_list(request, todo_list_id):
    todo_list = TodoList.objects.get(pk=todo_list_id)
    todo_items = TodoItem.objects.filter(todo_list=todo_list)
    if request.method == "POST":
        todo_list_form = TodoListForm(request.POST, instance=todo_list)
        if todo_list_form.is_valid():
            todo_list_form.save()
            messages.success(request, "Todo List Successfully Updated")
    else:
        todo_list_form = TodoListForm(instance=todo_list)
    context = {
        "todo_list": todo_list,
        "todo_items": todo_items,
        "todo_list_form": todo_list_form,
    }
    return render(request, "teams/edit-todo-list.html", context)


@login_required(login_url="user_profile:login")
def delete_todo_list(request, team_id, todo_list_id):
    todo_list = TodoList.objects.get(pk=todo_list_id)
    todo_list.delete()
    return redirect("teams:get_team", team_id=team_id)


@login_required(login_url="user_profile:login")
def create_todo_item(request, todo_list_id):
    todo_list = TodoList.objects.get(pk=todo_list_id)
    # todo: option to view users for current team, to assign item to user
    team = Team.objects.get(todolist=todo_list)
    team_users = CustomUser.objects.filter(teams__exact=team)
    if request.method == "POST":
        form = TeamTodoForm(request.POST)
        form.fields["assigned_to"].queryset = team_users
        if form.is_valid():
            item = form.save(commit=False)
            item.todo_list = todo_list
            item.save()
            messages.success(request, "Todo Item Created")
            return redirect("teams:edit_todo_list", todo_list_id=todo_list_id)
    else:
        form = TeamTodoForm()
        form.fields["assigned_to"].queryset = team_users
    context = {"form": form}
    return render(request, "teams/create-todo-item.html", context)


@login_required(login_url="user_profile:login")
def delete_todo_item(request, todo_id, todo_list_id):
    todo_item = TodoItem.objects.get(pk=todo_id)
    todo_item.delete()
    messages.success(request, "Todo Item Deleted")
    return redirect("teams:edit_todo_list", todo_list_id=todo_list_id)


@login_required(login_url="user_profile:login")
def edit_todo_item(
    request,
    todo_list_id,
    todo_id,
):
    todo_item = TodoItem.objects.get(pk=todo_id)
    todo_list = TodoList.objects.get(todoitem=todo_item)
    team = Team.objects.get(todolist=todo_list)
    team_users = CustomUser.objects.filter(teams__exact=team)
    # todo: ability to assign to user
    if request.method == "POST":
        form = TeamTodoForm(request.POST, instance=todo_item)
        form.fields["assigned_to"].queryset = team_users
        if form.is_valid():
            form.save()
            messages.success(request, "Todo Item Updated")
            return redirect("teams:edit_todo_list", todo_list_id=todo_list_id)
    else:
        form = TeamTodoForm(instance=todo_item)
        form.fields["assigned_to"].queryset = team_users
    context = {"form": form, "todo_item": todo_item}
    return render(request, "teams/edit-todo-item.html", context)


@login_required(login_url="user_profile:login")
def delete_list_confirmation(request, team_id, todo_list_id):
    context = {
        "todo_list_id": todo_list_id,
        "team_id": team_id,
        "delete_todo_list": True,
    }
    return render(request, "teams/confirm-deletion.html", context)


@login_required(login_url="user_profile:login")
def delete_team_confirmation(request, team_id):
    context = {"team_id": team_id, "delete_team": True}
    return render(request, "teams/confirm-deletion.html", context)


def invites(request):
    invites = TeamInvite.objects.filter(receiver=request.user)
    context = {"invites": invites}
    return render(request, "teams/invites.html", context)


def accept_invite(request, invite_id):
    user = request.user
    team_invite = TeamInvite.objects.get(pk=invite_id)
    team = team_invite.team
    team.customuser_set.add(user)
    team_invite.delete()
    return redirect("teams:invites")
