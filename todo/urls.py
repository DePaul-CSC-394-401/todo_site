from django.urls import path
from . import views
from django.contrib.auth import views as auth_views #Used for login and logout views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", views.register, name="register"), #User Registeration
    path("login/", auth_views.LoginView.as_view(template_name="todo/login.html"), name="login"), #User Login
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), #User Logout
    path("profile/", views.profile, name="profile"), #User Profile
    path("", views.todo_list, name="todo_list"),
    path("create-todo-item", views.create_todo_item, name="create_todo_item"),
    path("edit-todo-item/<int:pk>/", views.edit_todo_item, name="edit_todo_item"),
    path(
        "delete-confirmation/<int:pk>",
        views.delete_confirmation,
        name="delete_confirmation",
    ),
    path("delete-todo-item/<int:pk>", views.delete_todo_item, name="delete_todo_item"),
    path("maACrk-completed/<int:pk>/", views.mark_completed, name="mark_completed"),
    path("search/", views.search_results, name="search_results"),
]
