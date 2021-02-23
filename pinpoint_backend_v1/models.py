from django.db import models
from django.contrib.auth.models import User

class Pin(models.Model):
    address = models.CharField(max_length=180)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=5)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    user_id = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    username = models.CharField(max_length=180)

  #  user_id = models.ForeignKey(Profile, to_field='id', on_delete=models.DO_NOTHING)