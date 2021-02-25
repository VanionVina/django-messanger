from django.contrib import admin

from .models import Consumer, ChatRoom, Message, AddToFriendNotification
# Register your models here.

admin.site.register(Consumer)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(AddToFriendNotification)