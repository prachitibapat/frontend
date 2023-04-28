# Generated by Django 4.1.7 on 2023-04-22 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='All_Categories_Mumbai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.CharField(choices=[('poi', 'Points of Interest & Landmarks'), ('mon', 'Monuments & Statues'), ('scenic', 'Scenic Drives'), ('bridges', 'Bridges'), ('religious', 'Religious Sites'), ('historic', 'Historic Sites'), ('arch', 'Architectural Buildings'), ('neigh', 'Neighbourhoods'), ('museums', 'History Museums'), ('caves', 'Caverns & Caves'), ('natpark', 'National Parks'), ('beach', 'Beaches'), ('spmuseums', 'Speciality Museums'), ('mall', 'Shopping Malls'), ('waterpark', 'Water Parks'), ('stadium', 'Arenas & Stadiums'), ('gallery', 'Art Galleries'), ('park', 'Parks'), ('market', 'Flea & Street Markets'), ('theatre', 'Theatres'), ('garden', 'Gardens'), ('sports', 'Sports Complexes'), ('water', 'Bodies of Water'), ('horses', 'Horse Tracks'), ('scimuseums', 'Science Museums'), ('ferry', 'Ferries'), ('hammam', 'Hammams & Turkish Baths'), ('spa', 'Spas'), ('library', 'Libraries'), ('fountain', 'Fountains'), ('nature', 'Nature & Wildlife Areas'), ('island', 'Islands'), ('ship', 'Ships'), ('pier', 'Piers & Boardwalks'), ('church', 'Churches & Cathedrals'), ('opera', 'Operas'), ('playground', 'Playgrounds')], max_length=255)),
            ],
        ),
    ]