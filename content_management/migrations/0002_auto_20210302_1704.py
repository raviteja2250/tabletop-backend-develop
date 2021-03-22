# Generated by Django 3.0.11 on 2021-03-02 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_delete_chef'),
        ('content_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddIndex(
            model_name='brandcategoryorder',
            index=models.Index(fields=['category'], name='content_man_categor_9ef6bb_idx'),
        ),
        migrations.AddIndex(
            model_name='brandmenuitemorder',
            index=models.Index(fields=['menu_item'], name='content_man_menu_it_ba1d96_idx'),
        ),
        migrations.AddField(
            model_name='brandorder',
            name='brand',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='brand_orders', to='core.Brand'),
        ),
        migrations.AddIndex(
            model_name='brandorder',
            index=models.Index(fields=['brand'], name='content_man_brand_i_daa9ff_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='brandorder',
            unique_together={('brand', 'order')},
        ),
    ]