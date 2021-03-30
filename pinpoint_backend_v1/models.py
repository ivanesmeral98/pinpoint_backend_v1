from django.db import models
from django.contrib.auth.models import User

class Pin(models.Model):
    name = models.CharField(max_length=180)
    address = models.CharField(max_length=180)
    latitude = models.DecimalField(max_digits=19, decimal_places=10, blank=True, default=5)
    longitude = models.DecimalField(max_digits=19, decimal_places=10, blank=True, default=5)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    username = models.CharField(max_length=180)
   # rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, default=5)

class Friend(models.Model):
    username = models.CharField(max_length=180)
    friend = models.CharField(max_length=180)

class CollabGroup(models.Model):
	username = models.CharField(max_length=180)
	group_id = models.CharField(max_length=180)