# Generated by Django 5.1.4 on 2024-12-05 15:19

import scooters.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scooter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
                ('scooter_model', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
                ('year', models.IntegerField()),
                ('registration_number', models.CharField(max_length=50, unique=True)),
                ('available', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to=scooters.models.directory_path)),
                ('daily_price', models.IntegerField()),
                ('weekly_price', models.IntegerField()),
                ('monthly_price', models.IntegerField()),
                ('deposit_amount', models.IntegerField()),
            ],
        ),
    ]
