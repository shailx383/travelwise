# Generated by Django 3.0.5 on 2020-06-17 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addUser', '0006_remove_user_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='m', max_length=30),
            preserve_default=False,
        ),
    ]
