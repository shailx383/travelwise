# Generated by Django 3.0.5 on 2020-07-25 05:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('plan1', '0023_delete_s2'),
    ]

    operations = [
        migrations.CreateModel(
            name='s2',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('weather', models.CharField(max_length=3)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('budget', models.IntegerField()),
            ],
        ),
    ]
