# Generated by Django 4.1.7 on 2023-05-01 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_all_categories_chennai_all_categories_delhi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chennai_user_output',
            name='all_lat_lon',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delhi_user_output',
            name='all_lat_lon',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jaipur_user_output',
            name='all_lat_lon',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kolkata_user_output',
            name='all_lat_lon',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mumbai_user_output',
            name='all_lat_lon',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
    ]
