from django.db import models
from django.contrib.auth.models import User

class Pin(models.Model):
    name = models.CharField(max_length=180, default="name")
    address = models.CharField(max_length=180)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=5)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    username = models.CharField(max_length=180)
    rating = models.DecimalField(max_digits=1, decimal_places=1, blank=True, default=5)

class Friend(models.Model):
    username = models.CharField(max_length=180)
    friend = models.CharField(max_length=180)


