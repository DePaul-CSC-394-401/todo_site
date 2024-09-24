from django.urls import path

from . import views

app_name = "teams"
urlpatterns = [
    path("", views.get_all_teams, name="get_teams"),
    path("team/<int:team_id>/", views.get_team, name="get_team"),
    path(
        "edit-todo-list/<int:todo_list_id>/",
        views.edit_todo_list,
        name="edit_todo_list",
    ),
    path(
        "team/<int:team_id>/delete-todo-list/<int:todo_list_id>",
        views.delete_todo_list,
        name="delete_todo_list",
    ),
    path(
        "team/<int:team_id>/delete-todo-list-confirmation/<int:todo_list_id>",
        views.delete_list_confirmation,
        name="delete_list_confirmation",
    ),
    path("edit-team/<int:team_id>/", views.edit_team, name="edit_team"),
    path("create-team/", views.create_team, name="create_team"),
    path("delete-team/<int:team_id>/", views.delete_team, name="delete_team"),
    path(
        "delete-team-confirmation/<int:team_id>/",
        views.delete_team_confirmation,
        name="delete_team_confirmation",
    ),
    path(
        "team/<int:team_id>/create-todo-list/",
        views.create_todo_list,
        name="create_todo_list",
    ),
    path(
        "create-todo-item/<int:todo_list_id>/",
        views.create_todo_item,
        name="create_todo_item",
    ),
    path(
        "edit-todo-item/<int:todo_list_id>/<int:todo_id>/",
        views.edit_todo_item,
        name="edit_todo_item",
    ),
    path(
        "delete-todo-item/<int:todo_list_id>/<int:todo_id>/",
        views.delete_todo_item,
        name="delete_todo_item",
    ),
    path("invites/", views.invites, name="invites"),
    path("accept-invite/<int:invite_id>/", views.accept_invite, name="accept-invite"),
]
