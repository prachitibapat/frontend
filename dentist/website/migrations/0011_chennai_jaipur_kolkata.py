# Generated by Django 4.1.7 on 2023-04-30 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_delhi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chennai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tourist_spot', models.CharField(max_length=255)),
                ('Area', models.CharField(max_length=255)),
                ('City', models.CharField(max_length=255)),
                ('Rating', models.FloatField(max_length=255)),
                ('Categories', models.CharField(max_length=255)),
                ('Address', models.CharField(max_length=255)),
                ('latitude', models.FloatField(max_length=255)),
                ('longitude', models.FloatField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Jaipur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tourist_spot', models.CharField(max_length=255)),
                ('Area', models.CharField(max_length=255)),
                ('City', models.CharField(max_length=255)),
                ('Rating', models.FloatField(max_length=255)),
                ('Categories', models.CharField(max_length=255)),
                ('Address', models.CharField(max_length=255)),
                ('latitude', models.FloatField(max_length=255)),
                ('longitude', models.FloatField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Kolkata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tourist_spot', models.CharField(max_length=255)),
                ('Area', models.CharField(max_length=255)),
                ('City', models.CharField(max_length=255)),
                ('Rating', models.FloatField(max_length=255)),
                ('Categories', models.CharField(max_length=255)),
                ('Address', models.CharField(max_length=255)),
                ('latitude', models.FloatField(max_length=255)),
                ('longitude', models.FloatField(max_length=255)),
            ],
        ),
    ]
