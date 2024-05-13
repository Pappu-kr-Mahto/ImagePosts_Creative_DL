from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100,default="")
    followers = models.ManyToManyField('self', related_name='followed_by',symmetrical=False, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    

class ImagePost(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image_post",null=True)
    likes = models.ManyToManyField(UserProfile, related_name='liked_by',blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
