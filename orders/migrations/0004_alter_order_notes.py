# Generated by Django 5.2 on 2025-06-08 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_notes_alter_order_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
