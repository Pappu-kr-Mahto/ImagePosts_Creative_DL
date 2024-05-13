from django.contrib import admin
from .models import UserProfile, ImagePost

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(ImagePost)