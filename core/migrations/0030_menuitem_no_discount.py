# Generated by Django 3.0.11 on 2021-02-18 04:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_menuitem_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='no_discount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='no_discount',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='discounted_price',
            field=models.FloatField(default=0, validators=[
                                    django.core.validators.MinValueValidator(0)]),
        ),
    ]
