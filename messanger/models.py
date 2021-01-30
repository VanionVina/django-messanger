from django.db import models
from django.contrib.auth.models import User



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

