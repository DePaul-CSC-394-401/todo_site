# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField()
    teams = models.ManyToManyField(to="teams.Team", blank=True)

    def __str__(self):
        return self.username
