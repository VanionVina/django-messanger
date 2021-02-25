from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill


class Consumer(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('helicopter', 'Helicopter')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consumer')
    phone = models.CharField(max_length=20, verbose_name='Phone number')
    birth = models.DateField(verbose_name='Birthday')
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    friends = models.ManyToManyField('Consumer', default=None, blank=True,  verbose_name='Friends')
    avatar = ProcessedImageField(upload_to='avatars',
                                processors=[ResizeToFill(300, 300)],
                                format='JPEG',
                                options={'quality': 100},
                                default='avatars/default.jpg')

    def get_absolute_url(self):
        user_id = self.user.id
        return reverse('messanger:user_profile', kwargs={'user_id': user_id})

    def __str__(self):
        return self.user.username


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    image = ProcessedImageField(upload_to='chats', 
                                processors=[ResizeToFill(100, 100)],
                                format='JPEG',
                                options={'quality': 90},
                                default='chats/default.jpg')
    users = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now=True, auto_created=True)
    moderators = models.ManyToManyField(User, related_name='modeators')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('messanger:chat_room', kwargs={'chat_id': self.id})


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='From user',
                                  related_name='from_user')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, verbose_name='To chat room',
                                related_name='chat_room')
    text = models.TextField()
    sended = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f'Message from "{self.from_user}" to room "{self.chat_room}"'


class AddToFriendNotification(models.Model):
    send_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_from')
    send_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_to')
    agreed = models.BooleanField(null=True, blank=True)
    date_sended = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return f"Friend request from {self.send_from} to {self.send_to}"
