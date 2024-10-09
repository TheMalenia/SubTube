from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    wallet = models.IntegerField(default=0)
    renewal = models.BooleanField(default=False)

class SubscriptionType(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    time = models.IntegerField(default=30)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    video_file = models.FileField(upload_to="videos/")
    created_at = models.DateTimeField(auto_now_add=True)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    view = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, blank=False)
    user = models.ForeignKey(User ,on_delete=models.CASCADE, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} to {self.video.title}"
        
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    subscription_type = models.ForeignKey(SubscriptionType, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username} - {self.subscription_type.title}'
    
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watch_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} watched {self.video.title}'
