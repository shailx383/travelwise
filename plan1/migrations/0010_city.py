# Generated by Django 3.0.5 on 2020-07-21 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan1', '0009_delete_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='city',
            fields=[
                ('country', models.CharField(max_length=100)),
                ('city_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('currency', models.CharField(max_length=100)),
                ('continent', models.CharField(max_length=100)),
                ('weather', models.CharField(max_length=3)),
            ],
        ),
    ]
