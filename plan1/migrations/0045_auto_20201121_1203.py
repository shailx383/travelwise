# Generated by Django 3.0.5 on 2020-11-21 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan1', '0044_attractions_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='s2',
            name='budget_max',
        ),
        migrations.RemoveField(
            model_name='s2',
            name='budget_min',
        ),
        migrations.AddField(
            model_name='s2',
            name='budget',
            field=models.CharField(default='low', max_length=3),
            preserve_default=False,
        ),
    ]