# Generated by Django 3.1.6 on 2022-11-06 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20221106_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='depa_weight',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='jjokpa_weight',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='onion_weight',
            field=models.FloatField(default=0),
        ),
    ]
