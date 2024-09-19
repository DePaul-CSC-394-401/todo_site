from django.urls import path

from . import views

app_name = "todo"
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
    path("search-results/", views.search_results, name="search_results"),
    path("categories/", views.categories, name="categories"),
    path("create-category/", views.create_category, name="create_category"),
    path("delete-category/<int:pk>/", views.delete_category, name="delete_category"),
    path("archive/<int:pk>/", views.archive, name="archive"),
    path("view-archive/", views.view_archive, name="view_archive"),
    path(
        "restore-from-archive/<int:pk>/",
        views.restore_from_archive,
        name="restore_from_archive",
    ),
    path("start-todo-item/<int:pk>/", views.start_todo_item, name="start_todo_item"),
    path("stop-todo-item/<int:pk>/", views.stop_todo_item, name="stop_todo_item"),
]
