# Generated by Django 3.1.5 on 2021-02-25 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messanger', '0019_auto_20210225_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='addtofriendnotification',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
