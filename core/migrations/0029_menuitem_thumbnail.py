# Generated by Django 3.0.11 on 2021-02-04 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_chef_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]
