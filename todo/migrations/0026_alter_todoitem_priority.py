# Generated by Django 5.1.1 on 2024-09-19 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0025_alter_todoitem_due_date_alter_todoitem_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todoitem",
            name="priority",
            field=models.CharField(
                blank=True,
                choices=[("HIGH", "High"), ("MEDIUM", "Medium"), ("LOW", "Low")],
                null=True,
            ),
        ),
    ]
