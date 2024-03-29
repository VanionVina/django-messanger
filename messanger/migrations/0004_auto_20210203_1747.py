# Generated by Django 3.1.5 on 2021-02-03 17:47

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('messanger', '0003_consumer_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(default='media/avatars/default.jpeg', upload_to='avatars'),
        ),
    ]
