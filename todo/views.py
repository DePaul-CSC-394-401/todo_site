from django.shortcuts import redirect, render
from .models import Todo_Item
from .forms import TodoForm, RegisterForm, UpdateProfileForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site                             # Import the get_current_site function
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode          # Import the functions to encode and decode the uid
from django.utils.encoding import force_bytes, force_str                            # Import the functions to convert the uid to bytes and vice versa
from django.template.loader import render_to_string                                 # Import the function to render the email body   
from django.core.mail import EmailMessage                                           # Import the EmailMessage class
from django.contrib.auth.models import User                                         # Import the User model
from django.contrib.auth.tokens import default_token_generator as token_generator   # Import the default token generator

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save the form data to the database
            user.is_active = False          # Set the user to inactive
            user.save()                     # Save the user to the database

            # Confirmation email
            current_site = get_current_site(request)  # Get the current site
            mail_subject = "Activate your account"    # Set the email subject
            message = render_to_string("todo/email_confirmation.html", {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),     # Encode the user id
                    "token": token_generator.make_token(user),              # Generate the token
                })
            email = EmailMessage(mail_subject, message, to=[user.email])    # Create the email message
            email.send()                                                    # Send the email

            return render(request, 'todo/registration_pending.html')        # Pending message displayed to the user
    else:
        form = RegisterForm()
    return render(request, "todo/register.html", {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Decode the user id
        user = User.objects.get(pk=uid)                 # Get the user
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):  # Check the token
        user.is_active = True    # Activate the user
        user.save()              # Save the user
        login(request, user)     # Log the user in
        return redirect("todo_list")  # Redirect to the todo list
    else:
        return render(request, "todo/activation_invalid.html")  # Invalid activation link

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


# def search_results(request):
#     curr_user = request.user
#     search_text = request.GET.get("search_text")
#     search_type = request.GET.get("search_type").lower()
#     results = Todo_Item.search_by(search_type, search_text, curr_user)
#     return render(request, "todo/search-results.html", {"results": results})

def search_results(request):
    user = request.user
    q = request.GET.get("search_text")
    if q:
        results = Todo_Item.objects.filter(user=user).filter(Q(title__icontains=q) | Q(description__icontains=q))
    else:
        results = Todo_Item.objects.all()
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
