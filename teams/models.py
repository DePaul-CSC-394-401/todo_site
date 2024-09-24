from django.db import models

from user_profile.models import CustomUser


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class TodoList(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TeamInvite(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sender"
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="receiver"
    )
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.team.name
