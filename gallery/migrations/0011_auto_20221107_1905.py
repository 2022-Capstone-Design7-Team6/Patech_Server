# Generated by Django 3.1.6 on 2022-11-07 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0010_auto_20221107_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='plant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants', to='gallery.plant'),
        ),
    ]
