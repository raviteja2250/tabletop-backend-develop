# Generated by Django 3.0.11 on 2020-11-26 05:50

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('logo', models.URLField(blank=True, null=True)),
                ('menu_item_placeholder', models.URLField(blank=True, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('delivery', models.BooleanField(default=True)),
                ('dine_in', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CookingItem',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('preparing', 'Preparing'), ('cooked', 'Cooked'), ('picked_up', 'Picked Up')], default='preparing', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('value', models.FloatField()),
                ('type', models.CharField(choices=[('percent', 'Percent'), ('flat', 'Flat Value')], default='flat', max_length=10)),
                ('code', models.CharField(blank=True, max_length=30, null=True)),
                ('is_auto', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('value', models.FloatField()),
                ('type', models.CharField(choices=[('percent', 'Percent'), ('flat', 'Flat Value')], default='flat', max_length=10)),
                ('order_type', multiselectfield.db.fields.MultiSelectField(choices=[('dine_in', 'Dine In'), ('delivery', 'Delivery'), ('accepted', 'Take away')], max_length=25)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GiftSet',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GiftSetCategory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('block_or_street', models.CharField(max_length=300)),
                ('postcode', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_or_building', models.CharField(blank=True, max_length=300, null=True)),
                ('country_code', models.CharField(default='SG', max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('signature_dish', models.BooleanField(default=False)),
                ('promotion', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('complete_time', models.DateTimeField(blank=True, null=True)),
                ('due_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('checked_out', 'Checked out'), ('received', 'Received'), ('rejected', 'Rejected'), ('accepted', 'Accepted'), ('preparing', 'Preparing'), ('cooked', 'Cooked'), ('ready_to_send', 'Ready to send')], default='checked_out', max_length=15)),
                ('type', models.CharField(choices=[('dine_in', 'Dine In'), ('delivery', 'Delivery'), ('accepted', 'Take away')], default='dine_in', max_length=15)),
                ('payment_link', models.URLField(blank=True, null=True)),
                ('payment_psp_reference', models.CharField(blank=True, max_length=50, null=True)),
                ('refunded_psp_reference', models.CharField(blank=True, max_length=50, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('refunded', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UsedTimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_time_slots', to='core.Brand')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='used_time_slots', to='core.Order')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_time_slots', to='core.TimeSlot')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('menu_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='core.MenuItem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='core.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]