# Generated by Django 3.0.11 on 2021-01-14 07:23

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_ordercomment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='foreground_colour',
            field=colorfield.fields.ColorField(blank=True, default='#000000', max_length=18, null=True),
        ),
    ]
