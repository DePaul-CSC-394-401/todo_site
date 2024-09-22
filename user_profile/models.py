# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

from teams.models import Team


class CustomUser(AbstractUser):
    username = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField()
    teams = models.ManyToManyField(Team, blank=True)

    def __str__(self):
        return self.username
