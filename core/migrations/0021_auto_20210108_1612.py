# Generated by Django 3.0.11 on 2021-01-08 08:12

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_chef'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='color',
        ),
        migrations.AddField(
            model_name='brand',
            name='background_colour',
            field=colorfield.fields.ColorField(blank=True, default='#FFFFFF', max_length=18, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='foreground_colour',
            field=colorfield.fields.ColorField(blank=True, default='#FFFFFF', max_length=18, null=True),
        ),
        migrations.AddField(
            model_name='brand',
            name='secondary_colour',
            field=colorfield.fields.ColorField(blank=True, default='#FFFFFF', max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='brand',
            name='abbreviation',
            field=models.CharField(blank=True, default='', max_length=5, null=True),
        ),
    ]