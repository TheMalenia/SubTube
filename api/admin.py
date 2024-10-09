from django.contrib import admin
from .models import User, Video, Subscription, SubscriptionType, History, Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Video)
admin.site.register(Subscription)
admin.site.register(SubscriptionType)
admin.site.register(History)
admin.site.register(Comment)