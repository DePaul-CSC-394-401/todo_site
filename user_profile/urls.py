from django.urls import path
from . import views

app_name = "user_profile"
urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("register/", views.register, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("reset-password/", views.reset_password, name="reset_password"),
]
