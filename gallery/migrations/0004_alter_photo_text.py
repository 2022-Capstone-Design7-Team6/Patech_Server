# Generated by Django 4.0.8 on 2022-11-02 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_remove_plant_days_plant_start_date_alter_plant_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='text',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
