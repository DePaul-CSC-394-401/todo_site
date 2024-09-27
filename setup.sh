#!/bin/bash

# Step 1: Get the container ID for the "todo_site-web" image
CONTAINER_ID=$(docker ps --filter "ancestor=todo_site-web" --format "{{.ID}}")

# Check if the container ID was found
if [ -n "$CONTAINER_ID" ]; then
  echo "Container ID for 'todo_site-web' image: $CONTAINER_ID"

  # Step 2: Execute commands in Django shell inside the container
  docker exec -it "$CONTAINER_ID" sh -c "
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from teams.models import Team, TodoList, TeamInvite
from todo.models import Category, TodoItem
import datetime

UserModel = get_user_model()

# Delete all users
UserModel.objects.all().delete()

# Delete all todo items
TodoItem.objects.all().delete()

# Delete all categories
Category.objects.all().delete()

# Delete all teams
Team.objects.all().delete()

# Delete all todo lists
TodoList.objects.all().delete()

# Delete all invites
TeamInvite.objects.all().delete()

# Create superuser
super_user = UserModel.objects.create_user('team2', password='password')
super_user.is_superuser = True
super_user.is_staff = True
super_user.save()

# Create users
user1 = UserModel.objects.create_user(username='jane_doe', email='jane.doe@depaul.edu', password='Green123$')
user1.save()

user2 = UserModel.objects.create_user(username='john_doe', email='jdoe2@example.com', password='Yellow123$')
user2.save()

user3 = UserModel.objects.create_user(username='asmith', email='asmith3@example.com', password='Blue123$')
user3.save()

# Create teams
team1 = Team(name='Team Alpha', description='A team that excels at innovation and problem-solving')
team1.save()
team1.customuser_set.add(user1)

team2 = Team(name='Team Bravo', description='Focused on developing high-quality software solutions')
team2.save()
team2.customuser_set.add(user2)

team3 = Team(name='Team Charlie', description='A dedicated team specializing in data analysis and insights')
team3.save()
team3.customuser_set.add(user3)

# ---- Personal Todo List for user1 ----
# Create categories
work_category = Category(user=user1, name='Work')
work_category.save()

personal_category = Category(user=user1, name='Personal')
personal_category.save()

misc_category = Category(user=user1, name='Misc')
misc_category.save()

# Create TodoItems
x = datetime.datetime(2024, 9, 30, 12, 5)
td1 = TodoItem(
    user=user1,
    title='Complete Django Project',
    description='Finish the final project for Django web development course.',
    due_date=x,
    priority=TodoItem.Priority.HIGH,
    category=work_category,
    is_archived=False
)
td1.save()

x = datetime.datetime(2024, 9, 25, 18, 22)
td2 = TodoItem(
    user=user1,
    title='Grocery Shopping',
    description='Buy groceries for the week including fruits, vegetables, and milk.',
    due_date=x,
    priority=TodoItem.Priority.MEDIUM,
    category=personal_category,
    is_archived=False
)
td2.save()

x = datetime.datetime(2024, 9, 22, 22, 45)
td3 = TodoItem(
    user=user1,
    title='Book Doctor Appointment',
    description='Call the clinic and schedule a routine check-up.',
    due_date=x,
    priority=TodoItem.Priority.LOW,
    category=misc_category,
    is_archived=False
)
td3.save()

x = datetime.datetime(2024, 9, 20, 23, 59)
td4 = TodoItem(
    user=user1,
    title='Finish Homework',
    description='Complete the math homework by end of day.',
    due_date=x,
    priority=TodoItem.Priority.LOW,
    category=personal_category,
    is_archived=False
)
td4.save()

x = datetime.datetime(2024, 9, 27, 15, 2)
td5 = TodoItem(
    user=user1,
    title='Submit Project Report',
    description='Prepare and submit the project report for the client.',
    due_date=x,
    priority=TodoItem.Priority.MEDIUM,
    category=work_category,
    is_archived=False
)
td5.save()

x = datetime.datetime(2024, 9, 30, 14, 25)
td6 = TodoItem(
    user=user1,
    title='Plan Weekend Trip',
    description='Research and plan for a weekend getaway.',
    due_date=x,
    priority=TodoItem.Priority.HIGH,
    category=misc_category,
    is_archived=False
)
td6.save()

print('TodoItems created:')
print(td1)
print(td2)
print(td3)
print(td4)
print(td5)
print(td6)
# ---- Personal Todo List for user1 ----


EOF
"
else
  echo "No running container found for the 'todo_site-web' image."
fi
