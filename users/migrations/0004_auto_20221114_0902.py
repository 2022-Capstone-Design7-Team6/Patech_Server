# Generated by Django 3.1.6 on 2022-11-14 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20221106_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='total_gain',
            field=models.IntegerField(default=0),
        ),
    ]