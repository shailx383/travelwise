# Generated by Django 3.0.5 on 2020-08-17 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('plan1', '0036_auto_20200817_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='s3',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rooms', models.IntegerField()),
                ('ppl', models.IntegerField()),
                ('type', models.CharField(max_length=9)),
            ],
        ),
    ]
