from django.shortcuts import redirect, render
from .models import TodoItem, Category
from .forms import TodoForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone


@login_required(login_url="user_profile:login")
def create_todo_item(request):
    user = request.user
    if request.method == "POST":
        todo_form = TodoForm(request.POST, initial={"category": None})
        if todo_form.is_valid():
            td_item = todo_form.save(commit=False)
            td_item.user = user
            td_item.save()
            return redirect("todo:todo_list")
    else:
        todo_form = TodoForm()
    return render(
        request, "todo/create-todo-item.html", {"todo_form": todo_form, "user": user}
    )


@login_required(login_url="user_profile:login")
def todo_list(request):
    user = request.user
    todo_items = TodoItem.objects.filter(user=user)
    order_by = request.GET.get("order_by")
    filter_by_category = request.GET.get("filter-by-category")
    categories = Category.objects.filter(user=user)
    if filter_by_category:
        todo_items = todo_items.filter(category__name=filter_by_category)
    if order_by == "priority_order":
        todo_items = todo_items.order_by_priority()
    if order_by == "due_date":
        todo_items = todo_items.order_by("due_date")
    return render(
        request,
        "todo/todo-list.html",
        {"todo_items": todo_items, "categories": categories},
    )


@login_required(login_url="user_profile:login")
def search_results(request):
    user = request.user
    q = request.GET.get("search_text")
    results = None
    if q:
        results = TodoItem.objects.filter(user=user).filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )
    return render(request, "todo/search-results.html", {"results": results})


@login_required(login_url="user_profile:login")
def mark_completed(request, pk):
    td_item = TodoItem.objects.get(pk=pk)
    td_item.is_completed = True
    td_item.save()
    return redirect("todo:todo_list")


@login_required(login_url="user_profile:login")
def edit_todo_item(request, pk):
    td_item = TodoItem.objects.get(id=pk)
    if request.method == "POST":
        todo_form = TodoForm(request.POST, instance=td_item)
        if todo_form.is_valid():
            td_item = todo_form.save(commit=False)
            td_item.update_total_time_spent()
            td_item.save()
            return redirect("todo:todo_list")
    else:
        todo_form = TodoForm(instance=td_item)
    return render(
        request,
        "todo/edit-todo-item.html",
        {"todo_form": todo_form, "td_item": td_item},
    )


@login_required(login_url="user_profile:login")
def delete_todo_item(request, pk):
    td_item = TodoItem.objects.get(pk=pk)
    td_item.delete()
    return redirect("todo:todo_list")


@login_required(login_url="user_profile:login")
def delete_confirmation(request, pk):
    td_item = TodoItem.objects.get(id=pk)
    return render(request, "todo/delete-confirmation.html", {"td_item": td_item})


@login_required(login_url="user_profile:login")
def categories(request):
    user = request.user
    categories_list = Category.objects.filter(user=user)
    return render(request, "todo/categories.html", {"categories_list": categories_list})


@login_required(login_url="user_profile:login")
def create_category(request):
    user = request.user
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = user
            category.save()
            return redirect("todo:categories")
    else:
        form = CategoryForm()
    return render(request, "todo/create-category.html", {"form": form})


@login_required(login_url="user_profile:login")
def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect("todo:categories")


@login_required(login_url="user_profile:login")
def archive(request, pk):
    td = TodoItem.objects.get(id=pk)
    td.is_archived = True
    td.save()
    return redirect("todo:todo_list")


@login_required(login_url="user_profile:login")
def view_archive(request):
    user = request.user
    archived_td_items = TodoItem.objects.filter(user=user).filter(is_archived=True)
    return render(
        request, "todo/view_archive.html", {"archived_td_items": archived_td_items}
    )


@login_required(login_url="user_profile:login")
def restore_from_archive(request, pk):
    td = TodoItem.objects.get(id=pk)
    td.is_archived = False
    td.save()
    return redirect("todo:view_archive")


@login_required(login_url="user_profile:login")
def start_todo_item(request, pk):
    td = TodoItem.objects.get(id=pk)
    td.start_time = timezone.now()
    td.timer_started = True
    td.save()
    return redirect("todo:todo_list")


@login_required(login_url="user_profile:login")
def stop_todo_item(request, pk):
    td = TodoItem.objects.get(id=pk)
    td.end_time = timezone.now()
    td.update_total_time_spent()
    td.timer_started = False
    td.save()
    return redirect("todo:todo_list")


# def search_results(request):
#     user = request.user
#     search_text = request.GET.get("search_text")
#     search_type = request.GET.get("search_type").lower()
#     results = Todo_Item.search_by(search_type, search_text, user)
#     return render(request, "todo/search-results.html", {"results": results})
