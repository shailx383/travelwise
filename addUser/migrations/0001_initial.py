# Generated by Django 3.0.5 on 2020-06-05 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=16)),
            ],
        ),
    ]
