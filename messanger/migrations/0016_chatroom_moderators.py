# Generated by Django 3.1.5 on 2021-02-19 17:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messanger', '0015_auto_20210209_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='moderators',
            field=models.ManyToManyField(related_name='modeators', to=settings.AUTH_USER_MODEL),
        ),
    ]
