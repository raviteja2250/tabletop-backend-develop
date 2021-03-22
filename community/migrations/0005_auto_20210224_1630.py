# Generated by Django 3.0.11 on 2021-02-24 08:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('community', '0004_cheffollower'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cheffollower',
            unique_together={('chef', 'user')},
        ),
        migrations.AddIndex(
            model_name='cheffollower',
            index=models.Index(fields=['user', 'chef'], name='community_c_user_id_d1fde9_idx'),
        ),
        migrations.AddIndex(
            model_name='cheffollower',
            index=models.Index(fields=['user'], name='community_c_user_id_a4163e_idx'),
        ),
        migrations.AddIndex(
            model_name='likedchefmedia',
            index=models.Index(fields=['media', 'user'], name='community_l_media_i_f4b9c6_idx'),
        ),
        migrations.AddIndex(
            model_name='likedchefmedia',
            index=models.Index(fields=['media'], name='community_l_media_i_d63cf2_idx'),
        ),
        migrations.AddIndex(
            model_name='likedchefpost',
            index=models.Index(fields=['post', 'user'], name='community_l_post_id_e4af76_idx'),
        ),
        migrations.AddIndex(
            model_name='likedchefpost',
            index=models.Index(fields=['post'], name='community_l_post_id_f8709a_idx'),
        ),
        migrations.AddIndex(
            model_name='likedchefrecipe',
            index=models.Index(fields=['recipe', 'user'], name='community_l_recipe__65136f_idx'),
        ),
        migrations.AddIndex(
            model_name='likedchefrecipe',
            index=models.Index(fields=['recipe'], name='community_l_recipe__6a5bfe_idx'),
        ),
    ]