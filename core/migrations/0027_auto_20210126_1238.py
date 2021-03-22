# Generated by Django 3.0.11 on 2021-01-26 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210120_0122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='complete_time',
            new_name='completed_time',
        ),
        migrations.AddField(
            model_name='order',
            name='received_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
