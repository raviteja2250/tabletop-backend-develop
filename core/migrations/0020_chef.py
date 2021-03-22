# Generated by Django 3.0.11 on 2021-01-07 17:59

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20210105_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(error_messages={'unique': 'A chef with that username already exists.'}, max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('image', models.URLField(blank=True, null=True)),
                ('youtube_video', models.URLField(blank=True, null=True)),
                ('instagram_account', models.URLField(blank=True, null=True)),
                ('facebook_account', models.URLField(blank=True, null=True)),
                ('twitter_account', models.URLField(blank=True, null=True)),
                ('tiktok_account', models.URLField(blank=True, null=True)),
                ('brands', models.ManyToManyField(blank=True, related_name='chefs', to='core.Brand')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
