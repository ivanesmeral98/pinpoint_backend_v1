from django.contrib import admin
from pinpoint_backend_v1.models import Pin, Friend, CollabGroup, Profile

# Register your models here.
admin.site.register(Pin)
admin.site.register(Friend)
admin.site.register(CollabGroup)
admin.site.register(Profile)