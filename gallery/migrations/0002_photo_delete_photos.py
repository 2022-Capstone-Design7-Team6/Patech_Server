# Generated by Django 4.0.8 on 2022-11-02 10:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.png', upload_to='post/')),
                ('text', models.CharField(max_length=50)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('plant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='gallery.plant')),
            ],
        ),
        migrations.DeleteModel(
            name='photos',
        ),
    ]
