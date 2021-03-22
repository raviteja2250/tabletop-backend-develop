# Generated by Django 3.0.11 on 2020-12-17 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20201216_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('checked_out', 'Checked out'), ('failed', 'Failed'), ('received', 'Received'), ('rejected', 'Rejected'), ('accepted', 'Accepted'), ('preparing', 'Preparing'), ('cooked', 'Cooked'), ('ready_to_send', 'Ready to send')], default='checked_out', max_length=15),
        ),
    ]