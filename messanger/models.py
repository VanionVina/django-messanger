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
    users = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now=True, auto_created=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='From user',
                                  related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='To user',
                                related_name='to_user')
    text = models.TextField()
    sended = models.DateTimeField(auto_created=True, auto_now=True)

    def __str__(self):
        return f'Message from {self.from_user} to {self.sended}'

