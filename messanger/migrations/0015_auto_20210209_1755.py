# Generated by Django 3.1.5 on 2021-02-09 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messanger', '0014_privateroom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privateroom',
            name='privaters',
        ),
        migrations.DeleteModel(
            name='PrivateMessage',
        ),
        migrations.DeleteModel(
            name='PrivateRoom',
        ),
    ]