# Generated by Django 3.0.5 on 2020-11-06 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0004_auto_20201012_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='flights',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('cost_per_head', models.IntegerField()),
                ('clas', models.CharField(max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='transport',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=20)),
                ('cost_per_head', models.IntegerField()),
                ('clas', models.CharField(max_length=12)),
            ],
        ),
    ]
