# Generated by Django 3.1.6 on 2022-11-16 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0018_auto_20221116_0231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='event',
        ),
        migrations.AddField(
            model_name='photo',
            name='event_chgpot',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photo',
            name='event_harvest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='photo',
            name='event_water',
            field=models.BooleanField(default=False),
        ),
    ]