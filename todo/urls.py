from django.urls import path
from . import views

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("create-todo-item", views.create_todo_item, name="create_todo_item"),
    path("edit-todo-item/<int:pk>/", views.edit_todo_item, name="edit_todo_item"),
    path(
        "delete-confirmation/<int:pk>",
        views.delete_confirmation,
        name="delete_confirmation",
    ),
    path("delete-todo-item/<int:pk>", views.delete_todo_item, name="delete_todo_item"),
    path("mark-completed/<int:pk>/", views.mark_completed, name="mark_completed"),
    path("search/", views.search_results, name="search_results"),
]
