# Generated by Django 3.1.6 on 2022-11-09 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0011_auto_20221107_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='length',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='plant',
            name='harvest_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='event',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='photo',
            name='text',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
