from random import choice
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    gender = models.CharField(choices=[("male", "Мужской"), ("female", "Женский")])
