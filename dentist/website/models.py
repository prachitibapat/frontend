from django.db import models

# Create your models here.
class Mumbai(models.Model):
    Tourist_spot = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    Rating = models.FloatField(max_length=255)
    Categories = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    latitude = models.FloatField(max_length=255)
    longitude = models.FloatField(max_length=255)

class All_Categories_Mumbai(models.Model):
    categories = models.CharField(max_length=255)

class User_Categories(models.Model):
    username = models.CharField(max_length=255)
    categories = models.CharField(max_length=255)
    all_spots = models.CharField(max_length=510)

class User_Output(models.Model):
    username = models.CharField(max_length=255)
    tabu_total_time = models.CharField(max_length=510)
    tabu_distance = models.CharField(max_length=510)
    genetic_route_total_time = models.CharField(max_length=510)
    genetic_distance = models.CharField(max_length=510)
    simulated_annealing_total_time = models.CharField(max_length=510)
    simulated_annealing_distance = models.CharField(max_length=510)
    top_loc_name_dis_time = models.CharField(max_length=100000)