# Generated by Django 5.1.1 on 2024-09-14 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0008_alter_todo_item_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todo_item",
            name="priority",
            field=models.CharField(choices=[(3, "HIGH"), (2, "MEDIUM"), (1, "LOW")]),
        ),
    ]
