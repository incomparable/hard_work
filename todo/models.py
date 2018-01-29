from __future__ import unicode_literals
from datetime import *
# import datetime
from django.db import models
from django.contrib.auth.models import User

class Todo1(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=50, unique=True)
    stars = models.CharField(max_length=40)
    message = models.TextField()

    def __str__(self):
        return self.stars


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profiles'