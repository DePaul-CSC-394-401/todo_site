from django.shortcuts import render, redirect
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
    authenticate,
    update_session_auth_hash,
)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import RegisterForm, UpdateProfileForm
from django.contrib.sites.shortcuts import (
    get_current_site,
)
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.utils.encoding import (
    force_bytes,
    force_str,
)
from django.template.loader import (
    render_to_string,
)
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.tokens import (
    default_token_generator as token_generator,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import CustomUser


# Create your views here.


def welcome(request):
    return render(request, "user_profile/welcome.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("todo:todo_list")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the form data to the database
            user.is_active = False  # Set the user to inactive
            user.save()  # Save the user to the database

            # Confirmation email
            current_site = get_current_site(request)  # Get the current site
            mail_subject = "Activate your account"  # Set the email subject
            message = render_to_string(
                "user_profile/email_confirmation.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(
                        force_bytes(user.pk)
                    ),  # Encode the user id
                    "token": token_generator.make_token(user),  # Generate the token
                },
            )
            email = EmailMessage(
                mail_subject, message, to=[user.email]
            )  # Create the email message
            email.send()  # Send the email

            return render(
                request, "user_profile/registration_pending.html"
            )  # Pending message displayed to the user
    else:
        form = RegisterForm()
    return render(request, "user_profile/register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Decode the user id
        user = CustomUser.objects.get(pk=uid)  # Get the user
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):  # Check the token
        user.is_active = True  # Activate the user
        user.save()  # Save the user
        auth_login(request, user)  # Log the user in
        return redirect("todo:todo_list")
    else:
        return render(
            request, "user_profile/activation_invalid.html"
        )  # Invalid activation link


def login(request):
    if request.user.is_authenticated:
        return redirect("todo:todo_list")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("todo:todo_list")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()
    return render(request, "user_profile/login.html", {"form": form})


@login_required(login_url="user_profile:login")
def logout(request):
    auth_logout(request)
    return render(
        request,
        "user_profile/logout.html",
    )


@login_required(login_url="user_profile:login")
def profile(request):
    if request.method == "POST":
        profile_form = UpdateProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return render(
                request,
                "user_profile/profile.html",
                {"profile_form": profile_form, "updated": True},
            )
    else:
        profile_form = UpdateProfileForm(instance=request.user)

    return render(request, "user_profile/profile.html", {"profile_form": profile_form})


@login_required(login_url="user_profile:login")
def reset_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return render(
                request, "user_profile/change_password.html", {"updated": True}
            )
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "user_profile/change_password.html", {"form": form})
