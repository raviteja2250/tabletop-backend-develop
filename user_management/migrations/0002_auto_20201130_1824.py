# Generated by Django 3.0.11 on 2020-11-30 10:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='Phone is invalid', regex='^(\\+\\d{1,3})?,?\\s?\\d{8,13}')]),
        ),
    ]