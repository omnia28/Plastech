# Generated by Django 5.2 on 2025-06-16 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictions', '0003_alter_sensorreading_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorreading',
            name='unique_sensor_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
