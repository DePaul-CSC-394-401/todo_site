#!/bin/bash

# Step 1: Get the container ID for the "todo_site-web" image
CONTAINER_ID=$(docker ps --filter "ancestor=todo_site-web" --format "{{.ID}}")

# Check if the container ID was found
if [ -n "$CONTAINER_ID" ]; then
  echo "Container ID for 'todo_site-web' image: $CONTAINER_ID"

  # Step 2: Execute commands in Django shell inside the container
  docker exec -it "$CONTAINER_ID" sh -c "
python manage.py shell <<EOF
from django.contrib.auth.models import User
from todo.models import TodoItem, Category

# Retrieve the user
user = User.objects.get(username='team2')

# Delete all todo items
TodoItem.objects.filter(user=user).delete()

# Create categories
work_category, _ = Category.objects.get_or_create(user=user, name='Work')
personal_category, _ = Category.objects.get_or_create(user=user, name='Personal')
misc_category, _ = Category.objects.get_or_create(user=user, name='Misc')

# Create TodoItems

td1 = TodoItem(
    user=user,
    title='Complete Django Project',
    description='Finish the final project for Django web development course.',
    due_date='2024-09-30',
    priority=TodoItem.Priority.HIGH,
    category=work_category,
    is_archived=False
)
td1.save()

td2 = TodoItem(
    user=user,
    title='Grocery Shopping',
    description='Buy groceries for the week including fruits, vegetables, and milk.',
    due_date='2024-09-25',
    priority=TodoItem.Priority.MEDIUM,
    category=personal_category,
    is_archived=False
)
td2.save()

td3 = TodoItem(
    user=user,
    title='Book Doctor Appointment',
    description='Call the clinic and schedule a routine check-up.',
    due_date='2024-09-22',
    priority=TodoItem.Priority.LOW,
    category=misc_category,
    is_archived=False
)
td3.save()

td4 = TodoItem(
    user=user,
    title='Finish Homework',
    description='Complete the math homework by end of day.',
    due_date='2024-09-20',
    priority=TodoItem.Priority.HIGH,
    category=personal_category,
    is_archived=False
)
td4.save()

td5 = TodoItem(
    user=user,
    title='Submit Project Report',
    description='Prepare and submit the project report for the client.',
    due_date='2024-09-27',
    priority=TodoItem.Priority.MEDIUM,
    category=work_category,
    is_archived=False
)
td5.save()

td6 = TodoItem(
    user=user,
    title='Plan Weekend Trip',
    description='Research and plan for a weekend getaway.',
    due_date='2024-09-30',
    priority=TodoItem.Priority.LOW,
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
EOF
"
else
  echo "No running container found for the 'todo_site-web' image."
fi
