from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Case, Value, When
from django.contrib.postgres.search import SearchVector
from django.utils import timezone
from datetime import timedelta

from teams.models import Team, TodoList


# Create your models here.
class TodoQuerySet(models.QuerySet):
    def order_by_priority(self):
        return self.alias(
            priority_order=Case(
                When(priority=TodoItem.Priority.HIGH, then=Value(1)),
                When(priority=TodoItem.Priority.MEDIUM, then=Value(2)),
                When(priority=TodoItem.Priority.LOW, then=Value(3)),
            )
        ).order_by("priority_order", "title")

    def order_by_date(self):
        return self.alias().order_by("due_date")


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    todo_item = models.ForeignKey('TodoItem', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification: {self.message}"

class TodoItem(models.Model):

    class Priority(models.TextChoices):
        HIGH = "HIGH", _("High")
        MEDIUM = "MEDIUM", _("Medium")
        LOW = "LOW", _("Low")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(choices=Priority.choices, null=True, blank=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    is_archived = models.BooleanField(default=False)
    total_time_spent = models.DurationField(default=timedelta)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    timer_started = models.BooleanField(default=False)
    progress = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=True, blank=True
    )
    todo_list = models.ForeignKey(
        TodoList, on_delete=models.CASCADE, null=True, blank=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_to",
    )
    reminder_sent = models.BooleanField(default=False) # new field to track if reminder has been sent
    objects = TodoQuerySet.as_manager()

    def update_total_time_spent(self):
        if self.start_time and self.end_time:
            self.total_time_spent += self.end_time - self.start_time
            self.start_time, self.end_time = None, None

    @staticmethod
    def search_by(search_type, search_text, curr_user):
        return (
            TodoItem.objects.filter(user=curr_user)
            .annotate(search=SearchVector(search_type))
            .filter(search=search_text)
        )

    def __str__(self) -> str:
        return f"Title: {self.title}, Description: {self.description}, Due Date: {self.due_date.strftime('%m/%d/%Y at %H:%M:%S')}, Is Completed: {self.is_completed}"


    def send_reminder(self, reminder_timeframe=timedelta(days=1)):
        if not self.reminder_sent and self.due_date:
            if timezone.now() >= self.due_date - reminder_timeframe:
                Notification.objects.create(
                    user=self.user,
                    todo_item=self,
                    message=f"Reminder: {self.title} is due soon."
                )
                self.reminder_sent = True
                self.save()