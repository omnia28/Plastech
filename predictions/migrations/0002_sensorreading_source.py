# Generated by Django 5.2 on 2025-06-14 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorreading',
            name='source',
            field=models.CharField(default='firebase', max_length=50),
        ),
    ]
