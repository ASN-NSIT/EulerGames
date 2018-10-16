from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(settings.NUMBER_OF_QUESTIONS)])


class Question(models.Model):
    question_text = models.CharField(max_length=5000)
    answer = models.IntegerField()

