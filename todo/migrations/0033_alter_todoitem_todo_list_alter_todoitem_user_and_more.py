# Generated by Django 5.1.1 on 2024-09-23 21:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0002_todolist"),
        ("todo", "0032_remove_sharedtodolist_team_todoitem_assigned_to_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="todoitem",
            name="todo_list",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="teams.todolist",
            ),
        ),
        migrations.AlterField(
            model_name="todoitem",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.DeleteModel(
            name="TodoList",
        ),
    ]
