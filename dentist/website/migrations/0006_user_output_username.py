# Generated by Django 4.2 on 2023-04-29 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_user_output'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_output',
            name='username',
            field=models.CharField(default='adhaskj', max_length=255),
            preserve_default=False,
        ),
    ]
