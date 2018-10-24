from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                          MaxValueValidator(settings.NUMBER_OF_QUESTIONS)])
    progress_time = models.DateTimeField(auto_now=True, editable=True)
    progress_start = models.DateTimeField(auto_now_add=True, editable=True)


class Question(models.Model):
    question_image = models.ImageField(null=True, blank=True)
    number = models.IntegerField()
    answer = models.IntegerField()


