# Generated by Django 3.1.6 on 2022-11-11 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0013_auto_20221109_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='post/'),
        ),
    ]
