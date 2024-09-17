from django.shortcuts import redirect, render
from .models import Todo_Item
from .forms import TodoForm, RegisterForm, UpdateProfileForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required 

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Automatically log in the user after registration
            return redirect("todo_list")
    else:
        form = RegisterForm()

    return render(request, "todo/register.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        profile_form = UpdateProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect("profile")
    else:
        profile_form = UpdateProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, "todo/profile.html", {
        "profile_form": profile_form, 
        "password_form": password_form
        })

def create_todo_item(request):
    curr_user = request.user
    if request.method == "POST":
        todo_form = TodoForm(request.POST)
        if todo_form.is_valid():
            td_item = todo_form.save(commit=False)
            td_item.user = curr_user
            td_item.save()
    else:
        todo_form = TodoForm()
    return render(
        request,
        "todo/create-todo-item.html",
        {"todo_form": todo_form, "curr_user": curr_user},
    )


def todo_list(request):
    curr_user = request.user
    order_by = request.GET.get("order_by")
    if order_by == "priority_order":
        todo_items = Todo_Item.objects.filter(user=curr_user).order_by_priority()
    else:
        todo_items = Todo_Item.objects.filter(user=curr_user).order_by_date()
    return render(request, "todo/todo-list.html", {"todo_items": todo_items})


def search_results(request):
    curr_user = request.user
    search_text = request.GET.get("search_text")
    search_type = request.GET.get("search_type").lower()
    results = Todo_Item.search_by(search_type, search_text, curr_user)
    return render(request, "todo/search-results.html", {"results": results})


def mark_completed(request, pk):
    td_item = Todo_Item.objects.get(pk=pk)
    td_item.is_completed = True
    td_item.save()
    return redirect("todo_list")


def edit_todo_item(request, pk):
    td_item = Todo_Item.objects.get(id=pk)
    if request.method == "POST":
        todo_form = TodoForm(request.POST, instance=td_item)
        if todo_form.is_valid():
            todo_form.save()
    else:
        todo_form = TodoForm(instance=td_item)
    return render(
        request,
        "todo/edit-todo-item.html",
        {"todo_form": todo_form, "td_item": td_item},
    )


def delete_todo_item(request, pk):
    td_item = Todo_Item.objects.get(pk=pk)
    td_item.delete()
    return redirect("todo_list")


def delete_confirmation(request, pk):
    td_item = Todo_Item.objects.get(id=pk)
    return render(request, "todo/delete-confirmation.html", {"td_item": td_item})
