# Generated by Django 5.1.1 on 2024-09-18 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0018_rename_todo_item_todoitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="todoitem",
            name="testing",
            field=models.CharField(default="test", max_length=100),
            preserve_default=False,
        ),
    ]
