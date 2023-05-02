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

class Delhi(models.Model):
    Tourist_spot = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    Rating = models.FloatField(max_length=255)
    Categories = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    latitude = models.FloatField(max_length=255)
    longitude = models.FloatField(max_length=255)

class Chennai(models.Model):
    Tourist_spot = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    Rating = models.FloatField(max_length=255)
    Categories = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    latitude = models.FloatField(max_length=255)
    longitude = models.FloatField(max_length=255)

class Jaipur(models.Model):
    Tourist_spot = models.CharField(max_length=255)
    Area = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    Rating = models.FloatField(max_length=255)
    Categories = models.CharField(max_length=255)
    Address = models.CharField(max_length=255)
    latitude = models.FloatField(max_length=255)
    longitude = models.FloatField(max_length=255)

class Kolkata(models.Model):
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
    
class All_Categories_Delhi(models.Model):
    categories = models.CharField(max_length=255)
    
class All_Categories_Jaipur(models.Model):
    categories = models.CharField(max_length=255)
    
class All_Categories_Kolkata(models.Model):
    categories = models.CharField(max_length=255)
    
class All_Categories_Chennai(models.Model):
    categories = models.CharField(max_length=255)

class User_Categories(models.Model):
    username = models.CharField(max_length=255)
    categories = models.CharField(max_length=255)
    mumbai_categories = models.CharField(max_length=255)
    delhi_categories = models.CharField(max_length=255)
    kolkata_categories = models.CharField(max_length=255)
    jaipur_categories = models.CharField(max_length=255)
    chennai_categories = models.CharField(max_length=255)
    all_spots = models.CharField(max_length=510)
    mumbai_all_spots = models.CharField(max_length=510)
    delhi_all_spots = models.CharField(max_length=510)
    chennai_all_spots = models.CharField(max_length=510)
    jaipur_all_spots = models.CharField(max_length=510)
    kolkata_all_spots = models.CharField(max_length=510)
    
class User_Output(models.Model):
    username = models.CharField(max_length=255)
    tabu_total_time = models.CharField(max_length=510)
    tabu_distance = models.CharField(max_length=510)
    genetic_route_total_time = models.CharField(max_length=510)
    genetic_distance = models.CharField(max_length=510)
    simulated_annealing_total_time = models.CharField(max_length=510)
    simulated_annealing_distance = models.CharField(max_length=510)
    tabu_route = models.CharField(max_length=255)
    genetic_route = models.CharField(max_length=255)
    simulated_annealing_route = models.CharField(max_length=255)
    best_route = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)
    top_loc_name_dis_time = models.CharField(max_length=100000)

class Mumbai_User_Output(models.Model):
    username = models.CharField(max_length=255)
    tabu_total_time = models.CharField(max_length=510)
    tabu_distance = models.CharField(max_length=510)
    genetic_route_total_time = models.CharField(max_length=510)
    genetic_distance = models.CharField(max_length=510)
    simulated_annealing_total_time = models.CharField(max_length=510)
    simulated_annealing_distance = models.CharField(max_length=510)
    tabu_route = models.CharField(max_length=255)
    genetic_route = models.CharField(max_length=255)
    simulated_annealing_route = models.CharField(max_length=255)
    best_route = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)
    top_loc_name_dis_time = models.CharField(max_length=100000)
    all_lat_lon = models.CharField(max_length=255)

class Delhi_User_Output(models.Model):
    username = models.CharField(max_length=255)
    tabu_total_time = models.CharField(max_length=510)
    tabu_distance = models.CharField(max_length=510)
    genetic_route_total_time = models.CharField(max_length=510)
    genetic_distance = models.CharField(max_length=510)
    simulated_annealing_total_time = models.CharField(max_length=510)
    simulated_annealing_distance = models.CharField(max_length=510)
    tabu_route = models.CharField(max_length=255)
    genetic_route = models.CharField(max_length=255)
    simulated_annealing_route = models.CharField(max_length=255)
    best_route = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)
    top_loc_name_dis_time = models.CharField(max_length=100000)
    all_lat_lon = models.CharField(max_length=255)
    
class Chennai_User_Output(models.Model):
    username = models.CharField(max_length=255)
    tabu_total_time = models.CharField(max_length=510)
    tabu_distance = models.CharField(max_length=510)
    genetic_route_total_time = models.CharField(max_length=510)
    genetic_distance = models.CharField(max_length=510)
    simulated_annealing_total_time = models.CharField(max_length=510)
    simulated_annealing_distance = models.CharField(max_length=510)
    tabu_route = models.CharField(max_length=255)
    genetic_route = models.CharField(max_length=255)
    simulated_annealing_route = models.CharField(max_length=255)
    best_route = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)
    top_loc_name_dis_time = models.CharField(max_length=100000)
    all_lat_lon = models.CharField(max_length=255)
    
class Kolkata_User_Output(models.Model):
    username = models.CharField(max_length=255)
    tabu_total_time = models.CharField(max_length=510)
    tabu_distance = models.CharField(max_length=510)
    genetic_route_total_time = models.CharField(max_length=510)
    genetic_distance = models.CharField(max_length=510)
    simulated_annealing_total_time = models.CharField(max_length=510)
    simulated_annealing_distance = models.CharField(max_length=510)
    tabu_route = models.CharField(max_length=255)
    genetic_route = models.CharField(max_length=255)
    simulated_annealing_route = models.CharField(max_length=255)
    best_route = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)
    top_loc_name_dis_time = models.CharField(max_length=100000)
    all_lat_lon = models.CharField(max_length=255)
    
class Jaipur_User_Output(models.Model):
    username = models.CharField(max_length=255)
    tabu_total_time = models.CharField(max_length=510)
    tabu_distance = models.CharField(max_length=510)
    genetic_route_total_time = models.CharField(max_length=510)
    genetic_distance = models.CharField(max_length=510)
    simulated_annealing_total_time = models.CharField(max_length=510)
    simulated_annealing_distance = models.CharField(max_length=510)
    tabu_route = models.CharField(max_length=255)
    genetic_route = models.CharField(max_length=255)
    simulated_annealing_route = models.CharField(max_length=255)
    best_route = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)
    top_loc_name_dis_time = models.CharField(max_length=100000)
    all_lat_lon = models.CharField(max_length=255)