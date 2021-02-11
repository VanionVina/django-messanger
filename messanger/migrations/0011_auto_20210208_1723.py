# Generated by Django 3.1.5 on 2021-02-08 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messanger', '0010_auto_20210208_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='to_user',
        ),
        migrations.AddField(
            model_name='message',
            name='chat_room',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='chat_room', to='messanger.chatroom', verbose_name='To chat room'),
            preserve_default=False,
        ),
    ]