from unicodedata import category

from django.shortcuts import redirect, render
from .models import TodoItem, Category
from .forms import TodoForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url="user_profile:login")
def create_todo_item(request):
    curr_user = request.user
    if request.method == "POST":
        todo_form = TodoForm(request.POST, initial={"category": None})
        if todo_form.is_valid():
            td_item = todo_form.save(commit=False)
            td_item.user = curr_user
            td_item.save()
            return redirect("todo:todo_list")
    else:
        todo_form = TodoForm()
    return render(
        request,
        "todo/create-todo-item.html",
        {"todo_form": todo_form, "curr_user": curr_user}
    )


@login_required(login_url="user_profile:login")
def todo_list(request):
    curr_user = request.user
    todo_items = TodoItem.objects.filter(user=curr_user)
    order_by = request.GET.get("order_by")
    filter_by_category = request.GET.get("filter-by-category")
    categories = Category.objects.filter(user=curr_user)
    if filter_by_category:
        todo_items = todo_items.filter(category__name=filter_by_category)
    if order_by == "priority_order":
        todo_items = todo_items.order_by_priority()
    if order_by == "due_date":
        todo_items = todo_items.order_by("due_date")
    return render(request, "todo/todo-list.html", {"todo_items": todo_items, "categories": categories})


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
            todo_form.save()
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
    curr_user = request.user
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = curr_user
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



# def search_results(request):
#     curr_user = request.user
#     search_text = request.GET.get("search_text")
#     search_type = request.GET.get("search_type").lower()
#     results = Todo_Item.search_by(search_type, search_text, curr_user)
#     return render(request, "todo/search-results.html", {"results": results})
