from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from website.models import All_Categories_Mumbai, Mumbai, User_Categories, User_Output, Delhi, Chennai, Jaipur, Kolkata, Mumbai_User_Output, Delhi_User_Output, Jaipur_User_Output, Kolkata_User_Output, Chennai_User_Output, All_Categories_Delhi, All_Categories_Kolkata, All_Categories_Jaipur, All_Categories_Chennai

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd
import csv
import googlemaps
import requests
import geopy.distance
import time
import folium
import webbrowser
import numpy as np
import io
import random
import math
import ast

def home(request):
    return render(request, 'home.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def about(request):
    return render(request, 'about.html', {})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return render(request, "home.html", {})
        else:
            messages.error(request, "Bad Credentials!!")
            return render(request, "signin.html")

    return render(request, 'signin.html', {})

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        mumbai_user_categories = Mumbai_User_Output()
        mumbai_user_categories.username = username
        mumbai_user_categories.save()

        delhi_user_output = Delhi_User_Output()
        delhi_user_output.username = username
        delhi_user_output.save()

        jaipur_user_output = Jaipur_User_Output()
        jaipur_user_output.username = username
        jaipur_user_output.save()

        chennai_user_output = Chennai_User_Output()
        chennai_user_output.username = username
        chennai_user_output.save()

        kolkata_user_output = Kolkata_User_Output()
        kolkata_user_output.username = username
        kolkata_user_output.save()

        user_output = User_Categories()
        user_output.username = username
        user_output.save()

        messages.success(
            request, "Your Account has been created succesfully")
        return redirect('signin')

    return render(request, 'signup.html', {})

def cities(request):
    return render(request, 'cities.html', {})

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

#MUMBAI
def mumbai(request):
    if request.method == "POST":
        
        if request.POST.get('action') == 'button2':
            
            options = ChromeOptions()
            options.add_argument("--use--fake-ui-for-media-stream")
            driver = Chrome(options=options)
            timeout = 20
            driver.get("https://whatmylocation.com/")
            wait = WebDriverWait(driver, timeout)
            time.sleep(3)
            current_longitude = driver.find_element(By.ID, "longitude").text
            current_latitude = driver.find_element(By.ID, "latitude").text
            current_location = [current_latitude,current_longitude]
            driver.quit()
            print(type(current_longitude))
            print(type(current_latitude))
            print(type(current_location))

            mumbai_data = []

            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            filtered_categories = user_categories_object.mumbai_all_spots

            for x, y in zip(Mumbai.objects.all().values(), filtered_categories):
                if y != "Null" and all(x.values()):
                    mumbai_data.append(x)

            def googleapi_resource_extraction():
                
                #Filtering by Latitude and Longitude
                lat_lon = pd.DataFrame([[x.get("latitude"), x.get("longitude")] for x in mumbai_data], columns=['latitude', 'longitude'])
                
                #Spliting into 5 parts of 23 each and 24th in diff variable
                lat_lon_split = np.array_split(lat_lon, 5)
                lat_lon_1 = lat_lon_split[0][:-1]
                lat_lon_2 = lat_lon_split[1][:-1]
                lat_lon_3 = lat_lon_split[2][:-1]
                lat_lon_4 = lat_lon_split[3][:-1]
                lat_lon_5 = lat_lon_split[4][:-1]
                lat_lon_1_last = lat_lon_split[0][-1:]
                lat_lon_2_last = lat_lon_split[1][-1:]
                lat_lon_3_last = lat_lon_split[2][-1:]
                lat_lon_4_last = lat_lon_split[3][-1:]
                lat_lon_5_last = lat_lon_split[4][-1:]
                
                #Storing Data in json format
                json_spit_1 = googleapi_link_maker(lat_lon_1,lat_lon_1_last)
                json_spit_2 = googleapi_link_maker(lat_lon_2,lat_lon_2_last)
                json_spit_3 = googleapi_link_maker(lat_lon_3,lat_lon_3_last)
                json_spit_4 = googleapi_link_maker(lat_lon_4,lat_lon_4_last)
                json_spit_5 = googleapi_link_maker(lat_lon_5,lat_lon_5_last)
                
                #Storing Data in file for future Reference(Will be removed in final code)
                # with open('json_spit_1.json', 'w') as f:
                #     json.dump(json_spit_1, f)
                #     f.close
                # with open('json_spit_2.json', 'w') as f:
                #     json.dump(json_spit_2, f)
                #     f.close
                # with open('json_spit_3.json', 'w') as f:
                #     json.dump(json_spit_3, f)
                #     f.close
                # with open('json_spit_4.json', 'w') as f:
                #     json.dump(json_spit_4, f)
                #     f.close
                # with open('json_spit_5.json', 'w') as f:
                #     json.dump(json_spit_5, f)
                #     f.close
                
                #Making dataframe for the distance collected
                dis_list = []
                dur_list = []
                dis_list,dur_list = df_dis_tim_collection(json_spit_1,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_2,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_3,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_4,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_5,dis_list,dur_list)
                
                #Making Location DataFrame containing distance,duration
                global loc_dir_tim
                loc_dir_tim = pd.DataFrame([[x.get("Tourist_spot"), x.get("latitude"), x.get("longitude"), dis_list[i], dur_list[i]] for i, x in enumerate(mumbai_data)], 
                           columns=['Tourist_spot', 'latitude', 'longitude', 'Distance_Meters', 'Duration_Seconds'])
                
                #Making list of closest 5 number of places
                top_loc_lat_lon = closest_5_places(loc_dir_tim)
                return top_loc_lat_lon
            
            def googleapi_link_maker(lat_lon,lat_lon_last):
    
                #Fetching GoogleAPI Key
                # with open('apikey.txt') as f:
                #     api_key = f.readline()
                #     f.close

                api_key = "AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4"
                
                #Generating Link
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + current_latitude + '%2C' + current_longitude + '&destinations='
                for x in lat_lon.index:
                    link_main = link_main + str(lat_lon['latitude'][x]) + '%2C' + str(lat_lon['longitude'][x]) + '%7C'
                link_main = link_main + str(lat_lon_last['latitude'].iloc[-1]) + '%2C' + str(lat_lon_last['longitude'].iloc[-1])
                link_main = link_main + '&key=' + api_key
                
                #Intilizing GoogleAPI parameters
                url = link_main
                payload = {}
                headers = {}
                
                #Calling GoogleAPI
                response = requests.request("GET", url, headers=headers, data=payload)
                json_content = response.json()
                
                #Returning all values
                return json_content
            
            def df_dis_tim_collection(json,dis_list,dur_list):
    
                #Filtering out data to get required parameters
                for i in range(len(json['rows'][0]['elements'])):
                    distance = json['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                    duration = json['rows'][0]['elements'][i]['duration']['value']
                    dur_list.append(duration)
                return dis_list,dur_list
            
            def closest_5_places(loc_dir_tim):
    
                #Calculating 5 number of places
                loc_dir_tim_dup_sorted = loc_dir_tim.sort_values(by=['Distance_Meters'])
                loc_dir_tim_dup_sorted_top5 = loc_dir_tim_dup_sorted[0:7]
                global top_loc_name_dis_time
                top_loc_name_dis_time = loc_dir_tim_dup_sorted_top5[["Tourist_spot","Distance_Meters","Duration_Seconds"]]
                loc_dir_tim_dup_sorted_top5_lat_lon = loc_dir_tim_dup_sorted_top5[["latitude","longitude"]]
                loc_dir_tim_dup_sorted_top5_lat_lon_list = loc_dir_tim_dup_sorted_top5_lat_lon.values.tolist()
                return loc_dir_tim_dup_sorted_top5_lat_lon_list
            
            #Will be used for folium maps
            top_loc_lat_lon = googleapi_resource_extraction()
            data_list = top_loc_name_dis_time.to_dict('records')

            #Making a Distance Matrix
            def get_distance_matrix(locations):
                n = len(locations)
                distance_matrix = [[0] * n for i in range(n)]
                for x in range(n):
                    dis_list = link_maker(x)
                    print(f'dis_list for x={x}: {dis_list}')
                    for y in range(n):
                        if x == y:
                            continue
                        elif(x < y):
                            distance_matrix[x][y] = dis_list[y-1]
                        elif(x > y):
                            distance_matrix[x][y] = dis_list[y]
                return distance_matrix

            def link_maker(x):
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[x][0]) + '%2C' + str(actual_route_sequence[x][1]) + '&destinations='
                for y in actual_route_sequence[:-1]:
                    if y == actual_route_sequence[x]:
                        continue
                    link_main = link_main + str(y[0]) + '%2C' + str(y[1]) + '%7C'
                link_main = link_main + str(actual_route_sequence[-1][0]) + '%2C' + str(actual_route_sequence[-1][1])
                link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                
                payload={}
                headers = {}

                response = requests.request("GET", link_main, headers=headers, data=payload)
                json_content = response.json()
                
                dis_list = []
                for i in range(len(json_content['rows'][0]['elements'])):
                    distance = json_content['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                
                return dis_list

            actual_route_sequence = []
            actual_route_sequence.append(current_location)
            for x in top_loc_lat_lon:
                actual_route_sequence.append(x)

            distance_matrix = get_distance_matrix(actual_route_sequence)

            #Calculating Total Distance in Algorithm
            def total_distance_required(actual_route_sequence,algoritm_sequence):
                total_distance = 0
                for x in range(len(algoritm_sequence)-1):
                    link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[algoritm_sequence[x]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x]][1]) + '&destinations='
                    link_main = link_main + str(actual_route_sequence[algoritm_sequence[x+1]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x+1]][1])
                    link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                    
                    #Intilizing GoogleAPI parameters
                    url = link_main
                    payload = {}
                    headers = {}

                    #Calling GoogleAPI
                    response = requests.request("GET", url, headers=headers, data=payload)
                    json_content = response.json()
                    
                    #Calculating the distance
                    distance = json_content['rows'][0]['elements'][0]['distance']['value']
                    total_distance = total_distance + distance
                return total_distance
            
            #Tabu Search Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def get_neighborhood(route):
                neighborhood = []
                for i in range(1, len(route)-1):
                    for j in range(i+1, len(route)):
                        new_route = route.copy()
                        new_route[i:j] = reversed(new_route[i:j])
                        neighborhood.append(new_route)
                return neighborhood

            def get_best_neighbor(neighbors, distance_matrix, tabu_list):
                best_neighbor = None
                best_distance = None
                for neighbor in neighbors:
                    if neighbor not in tabu_list:
                        distance = route_distance(neighbor, distance_matrix)
                        if best_distance is None or distance < best_distance:
                            best_neighbor = neighbor
                            best_distance = distance
                return best_neighbor, best_distance

            def tabu_search(locations, distance_matrix, starting_point=0, tabu_size=15, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                tabu_list = []
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution
                for i in range(max_iterations):
                    neighborhood = get_neighborhood(current_solution)
                    best_neighbor, best_distance = get_best_neighbor(neighborhood, distance_matrix, tabu_list)
                    if best_neighbor is None:
                        break
                    current_solution = best_neighbor
                    if best_distance < route_distance(best_solution, distance_matrix):
                        best_solution = best_neighbor
                    tabu_list.append(best_neighbor)
                    if len(tabu_list) > tabu_size:
                        tabu_list.pop(0)
                return best_solution
            
            ##Tabu Search Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            tabu_route = tabu_search(actual_route_sequence, distance_matrix)
            print(tabu_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            tabu_total_time = end_time - start_time

            print("Total time elapsed:", tabu_total_time, "seconds")

            tabu_distance = total_distance_required(actual_route_sequence,tabu_route)

            print("Total distance: ", tabu_distance, "meters")

            #Genetic Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def generate_random_route(n, starting_point):
                route = list(range(n))
                route.remove(starting_point)
                random.shuffle(route)
                route.insert(0, starting_point)
                return route

            def crossover(parent1, parent2):
                crossover_point1 = random.randint(1, len(parent1)-2)
                crossover_point2 = random.randint(crossover_point1+1, len(parent1)-1)
                child = parent1.copy()
                for i in range(crossover_point1, crossover_point2):
                    if parent2[i] not in child:
                        for j in range(len(child)):
                            if child[j] == parent2[i]:
                                child[j] = child[i]
                                child[i] = parent2[i]
                                break
                return child

            def mutation(route):
                mutation_point1 = random.randint(1, len(route)-2)
                mutation_point2 = random.randint(1, len(route)-2)
                route[mutation_point1], route[mutation_point2] = route[mutation_point2], route[mutation_point1]
                return route

            def genetic_algorithm(locations, distance_matrix, starting_point=0, population_size=50, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                population = [generate_random_route(n, starting_point) for i in range(population_size)]
                best_route = population[0]
                for i in range(max_iterations):
                    fitness_scores = [1/route_distance(route, distance_matrix) for route in population]
                    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
                    if route_distance(sorted_population[0], distance_matrix) < route_distance(best_route, distance_matrix):
                        best_route = sorted_population[0]
                    new_population = [sorted_population[0]]
                    for i in range(1, population_size):
                        parent1 = sorted_population[random.randint(0, int(population_size/2))]
                        parent2 = sorted_population[random.randint(0, int(population_size/2))]
                        child = crossover(parent1, parent2)
                        if random.uniform(0, 1) < 0.1:
                            child = mutation(child)
                        new_population.append(child)
                    population = new_population
                return best_route
            
            ##Genetic Algorithm Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            genetic_route = genetic_algorithm(actual_route_sequence, distance_matrix)
            print(genetic_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            genetic_route_total_time = end_time - start_time

            print("Total time elapsed:", genetic_route_total_time, "seconds")

            genetic_distance = total_distance_required(actual_route_sequence,genetic_route)

            print("Total distance: ", genetic_distance, "meters")

            #Simulated Annealing with Google API
            def route_distance(route, distance_matrix):
                # Calculate the total distance of a route
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def simulated_annealing(locations, distance_matrix, starting_point=0, temperature=10000, cooling_factor=0.9995, max_iterations=10000):
                # Initialize the current and best solutions
                n = len(locations)
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution

                # Start the simulated annealing algorithm
                for i in range(max_iterations):
                    # Choose a random neighbor by swapping two cities in the route
                    neighbor = current_solution.copy()
                    i = random.randint(1, n-2)
                    j = random.randint(i+1, n-1)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                    # Calculate the difference in distance between the current and the new solution
                    current_distance = route_distance(current_solution, distance_matrix)
                    neighbor_distance = route_distance(neighbor, distance_matrix)
                    delta = neighbor_distance - current_distance

                    # Accept the new solution if it's better or with a certain probability if it's worse
                    if delta < 0 or random.random() < math.exp(-delta/temperature):
                        current_solution = neighbor
                        if neighbor_distance < route_distance(best_solution, distance_matrix):
                            best_solution = neighbor

                    # Decrease the temperature
                    temperature *= cooling_factor

                return best_solution
            
            ##Simulated Annealing Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            simulated_annealing_route = simulated_annealing(actual_route_sequence, distance_matrix)
            print(simulated_annealing_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            simulated_annealing_total_time = end_time - start_time

            print("Total time elapsed:", simulated_annealing_total_time, "seconds")

            simulated_annealing_distance = total_distance_required(actual_route_sequence,simulated_annealing_route)

            print("Total distance: ", simulated_annealing_distance, "meters")

            context = {'TT': tabu_total_time,"TD": tabu_distance,
                       'GT': genetic_route_total_time,"GD": genetic_distance,
                       'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
                       'TLNDT': data_list}
            user_output = Mumbai_User_Output.objects.get(username=Username_current)
            user_output.current_location = current_location
            user_output.tabu_total_time = tabu_total_time
            user_output.tabu_distance = tabu_distance
            user_output.genetic_route_total_time =genetic_route_total_time
            user_output.genetic_distance = genetic_distance
            user_output.simulated_annealing_total_time = simulated_annealing_total_time
            user_output.simulated_annealing_distance = simulated_annealing_distance
            user_output.top_loc_name_dis_time = data_list
            user_output.tabu_route = tabu_route
            user_output.genetic_route = genetic_route
            user_output.simulated_annealing_route = simulated_annealing_route
            user_output.all_lat_lon = actual_route_sequence
            user_output.save()

            return redirect('mumbai_show')   

        elif request.POST.get('action') == 'button1':
            categories_order_list = request.POST.getlist('category_boxes')
            print(categories_order_list)
            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            user_categories_object.mumbai_categories = categories_order_list
            user_categories_object.save()
            user_categories = user_categories_object.mumbai_categories
            # print(user_categories)

            mumbai_data_categories = []
            for x in Mumbai.objects.all().values():
                mumbai_data_categories.append(x.get("Categories"))
            # print(mumbai_data_categories)

            filtered_categories = []

            i=0
            for cat in mumbai_data_categories:
                i = i+1
                found = False
                for req in user_categories:
                    if req in cat:
                        City_Location_Name = Mumbai.objects.get(id=i)
                        filtered_categories.append(City_Location_Name.Tourist_spot)
                        found = True
                        break
                if not found:
                    filtered_categories.append("Null")
            print(filtered_categories)

            user_categories_object.mumbai_all_spots = filtered_categories
            user_categories_object.save()
        
        elif request.POST.get('action') == 'button3':
            return redirect('mumbai_show') 

    mumbai_data = []
    for x in Mumbai.objects.all().values():
        mumbai_data.append(x)

    categories_list = []
    for x in All_Categories_Mumbai.objects.all().values():
        categories_list.append(x)
    
    context = {'categories': categories_list,"mumbai_try": mumbai_data}

    return render(request, 'mumbai.html', context)

def mumbai_show(request):
    
    Username_current = request.user.username
    user_output = Mumbai_User_Output.objects.get(username=Username_current)
    current_location = user_output.current_location
    tabu_total_time = user_output.tabu_total_time
    tabu_distance = user_output.tabu_distance
    genetic_route_total_time = user_output.genetic_route_total_time
    genetic_distance = user_output.genetic_distance
    simulated_annealing_total_time = user_output.simulated_annealing_total_time
    simulated_annealing_distance = user_output.simulated_annealing_distance
    top_loc_name_dis_time = user_output.top_loc_name_dis_time
    top_loc_name_dis_time = ast.literal_eval(top_loc_name_dis_time)
    tabu_route = user_output.tabu_route
    tabu_route = ast.literal_eval(tabu_route)
    genetic_route = user_output.genetic_route
    genetic_route = ast.literal_eval(genetic_route)
    simulated_annealing_route = user_output.simulated_annealing_route
    simulated_annealing_route = ast.literal_eval(simulated_annealing_route)
    all_lat_lon = user_output.all_lat_lon
    all_lat_lon = ast.literal_eval(all_lat_lon)
    print(all_lat_lon)
    print(type(all_lat_lon))
    if tabu_distance <= genetic_distance and tabu_distance <= simulated_annealing_distance:
        best_route = tabu_route
    elif genetic_distance <= simulated_annealing_distance:
        best_route = genetic_route
    else:
        best_route = simulated_annealing_route
        
    # Print the text version of the best route
    print("The best route to visit the tourist spots is as follows:")
    locations = [top_loc_name_dis_time[i-1]['Tourist_spot'] for i in best_route[1:]]
    route_text = f"Starting from your current location, visit {', '.join(locations[:-1])}, and {locations[-1]}."
    print(route_text)

    print(top_loc_name_dis_time)
    
    # m = folium.Map(location=[19.0760, 72.8777], zoom_start=12)

    tourist_spots = []
    tourist_spots.append

    # add markers for each tourist spot
    for spot in top_loc_name_dis_time:
        tourist_spot = spot['Tourist_spot']
        mumbai_spot = Mumbai.objects.get(Tourist_spot=tourist_spot)
        print(mumbai_spot)
        lat = mumbai_spot.latitude
        lon = mumbai_spot.longitude
        tourist_spots.append({'name': tourist_spot, 'latitude':  lat , 'longitude': lon})
    
    print(tourist_spots)

    # Create a map centered at Mumbai
    current_location = ast.literal_eval(current_location)
    map = folium.Map(location=current_location, zoom_start=14)
    folium.Marker(location=[current_location[0], current_location[1]], icon=folium.Icon(color='pink')).add_to(map)

    # Add markers for each tourist spot
    for spot in tourist_spots:
        folium.Marker(location=[spot["latitude"], spot["longitude"]], popup=spot["name"], icon=folium.Icon(color='purple')).add_to(map)
    
    # Convert the map to HTML and pass it to the template
    map_html = map._repr_html_()
    
    context = {'TT': tabu_total_time,"TD": tabu_distance,
               'GT': genetic_route_total_time,"GD": genetic_distance,
               'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
               'TLNDT': top_loc_name_dis_time, 
               'TR': tabu_route,
               'GR' : genetic_route,
               'SAR' : simulated_annealing_route,
               'BR' : best_route,
               'CL' : route_text,
               'MAPS' : map_html}
    
    if request.POST.get('action') == 'button':
        link_maker = "https://www.google.com/maps/dir/?api=1&origin=" + all_lat_lon[0][0] + "," + all_lat_lon[0][1] + "&waypoints="
        link_maker = link_maker + str(all_lat_lon[1][0]) + "," + str(all_lat_lon[1][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[2][0]) + "," + str(all_lat_lon[2][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[3][0]) + "," + str(all_lat_lon[3][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[4][0]) + "," + str(all_lat_lon[4][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[5][0]) + "," + str(all_lat_lon[7][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[6][0]) + "," + str(all_lat_lon[6][1]) + "|"
        link_maker = link_maker + "&destination=" + str(all_lat_lon[7][0]) + "," + str(all_lat_lon[7][1])

        print(link_maker)
        return redirect(link_maker)

    return render(request, 'mumbai_show.html', context)

#DELHI
def delhi(request):
    if request.method == "POST":
        
        if request.POST.get('action') == 'delhi_button2':
            
            # options = ChromeOptions()
            # options.add_argument("--use--fake-ui-for-media-stream")
            # driver = Chrome(options=options)
            # timeout = 20
            # driver.get("https://whatmylocation.com/")
            # wait = WebDriverWait(driver, timeout)
            # time.sleep(3)
            # current_longitude = driver.find_element(By.ID, "longitude").text
            # current_latitude = driver.find_element(By.ID, "latitude").text
            # current_location = [current_latitude,current_longitude]
            # driver.quit()
            # print(type(current_longitude))
            # print(type(current_latitude))
            # print(type(current_location))
            
            current_latitude = "28.609927"
            current_longitude = "77.211876"
            current_location = ["28.609927","77.211876"]

            delhi_data = []

            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            filtered_categories = user_categories_object.delhi_all_spots

            for x, y in zip(Delhi.objects.all().values(), filtered_categories):
                if y != "Null" and all(x.values()):
                    delhi_data.append(x)

            def googleapi_resource_extraction():
                
                #Filtering by Latitude and Longitude
                lat_lon = pd.DataFrame([[x.get("latitude"), x.get("longitude")] for x in delhi_data], columns=['latitude', 'longitude'])
                
                #Spliting into 5 parts of 23 each and 24th in diff variable
                lat_lon_split = np.array_split(lat_lon, 5)
                lat_lon_1 = lat_lon_split[0][:-1]
                lat_lon_2 = lat_lon_split[1][:-1]
                lat_lon_3 = lat_lon_split[2][:-1]
                lat_lon_4 = lat_lon_split[3][:-1]
                lat_lon_5 = lat_lon_split[4][:-1]
                lat_lon_1_last = lat_lon_split[0][-1:]
                lat_lon_2_last = lat_lon_split[1][-1:]
                lat_lon_3_last = lat_lon_split[2][-1:]
                lat_lon_4_last = lat_lon_split[3][-1:]
                lat_lon_5_last = lat_lon_split[4][-1:]
                
                #Storing Data in json format
                json_spit_1 = googleapi_link_maker(lat_lon_1,lat_lon_1_last)
                json_spit_2 = googleapi_link_maker(lat_lon_2,lat_lon_2_last)
                json_spit_3 = googleapi_link_maker(lat_lon_3,lat_lon_3_last)
                json_spit_4 = googleapi_link_maker(lat_lon_4,lat_lon_4_last)
                json_spit_5 = googleapi_link_maker(lat_lon_5,lat_lon_5_last)
                
                #Storing Data in file for future Reference(Will be removed in final code)
                # with open('json_spit_1.json', 'w') as f:
                #     json.dump(json_spit_1, f)
                #     f.close
                # with open('json_spit_2.json', 'w') as f:
                #     json.dump(json_spit_2, f)
                #     f.close
                # with open('json_spit_3.json', 'w') as f:
                #     json.dump(json_spit_3, f)
                #     f.close
                # with open('json_spit_4.json', 'w') as f:
                #     json.dump(json_spit_4, f)
                #     f.close
                # with open('json_spit_5.json', 'w') as f:
                #     json.dump(json_spit_5, f)
                #     f.close
                
                #Making dataframe for the distance collected
                dis_list = []
                dur_list = []
                dis_list,dur_list = df_dis_tim_collection(json_spit_1,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_2,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_3,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_4,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_5,dis_list,dur_list)
                
                #Making Location DataFrame containing distance,duration
                global loc_dir_tim
                loc_dir_tim = pd.DataFrame([[x.get("Tourist_spot"), x.get("latitude"), x.get("longitude"), dis_list[i], dur_list[i]] for i, x in enumerate(delhi_data)], 
                           columns=['Tourist_spot', 'latitude', 'longitude', 'Distance_Meters', 'Duration_Seconds'])
                
                #Making list of closest 5 number of places
                top_loc_lat_lon = closest_5_places(loc_dir_tim)
                return top_loc_lat_lon
            
            def googleapi_link_maker(lat_lon,lat_lon_last):
    
                #Fetching GoogleAPI Key
                # with open('apikey.txt') as f:
                #     api_key = f.readline()
                #     f.close

                api_key = "AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4"
                
                #Generating Link
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + current_latitude + '%2C' + current_longitude + '&destinations='
                for x in lat_lon.index:
                    link_main = link_main + str(lat_lon['latitude'][x]) + '%2C' + str(lat_lon['longitude'][x]) + '%7C'
                link_main = link_main + str(lat_lon_last['latitude'].iloc[-1]) + '%2C' + str(lat_lon_last['longitude'].iloc[-1])
                link_main = link_main + '&key=' + api_key
                
                #Intilizing GoogleAPI parameters
                url = link_main
                payload = {}
                headers = {}
                
                #Calling GoogleAPI
                response = requests.request("GET", url, headers=headers, data=payload)
                json_content = response.json()
                
                #Returning all values
                return json_content
            
            def df_dis_tim_collection(json,dis_list,dur_list):
    
                #Filtering out data to get required parameters
                for i in range(len(json['rows'][0]['elements'])):
                    distance = json['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                    duration = json['rows'][0]['elements'][i]['duration']['value']
                    dur_list.append(duration)
                return dis_list,dur_list
            
            def closest_5_places(loc_dir_tim):
    
                #Calculating 5 number of places
                loc_dir_tim_dup_sorted = loc_dir_tim.sort_values(by=['Distance_Meters'])
                loc_dir_tim_dup_sorted_top5 = loc_dir_tim_dup_sorted[0:7]
                global top_loc_name_dis_time
                top_loc_name_dis_time = loc_dir_tim_dup_sorted_top5[["Tourist_spot","Distance_Meters","Duration_Seconds"]]
                loc_dir_tim_dup_sorted_top5_lat_lon = loc_dir_tim_dup_sorted_top5[["latitude","longitude"]]
                loc_dir_tim_dup_sorted_top5_lat_lon_list = loc_dir_tim_dup_sorted_top5_lat_lon.values.tolist()
                return loc_dir_tim_dup_sorted_top5_lat_lon_list
            
            #Will be used for folium maps
            top_loc_lat_lon = googleapi_resource_extraction()
            data_list = top_loc_name_dis_time.to_dict('records')

            #Making a Distance Matrix
            def get_distance_matrix(locations):
                n = len(locations)
                distance_matrix = [[0] * n for i in range(n)]
                for x in range(n):
                    dis_list = link_maker(x)
                    for y in range(n):
                        # if x == y:
                        #     continue
                        if(x < y):
                            distance_matrix[x][y] = dis_list[y-1]
                        elif(x > y):
                            distance_matrix[x][y] = dis_list[y]
                return distance_matrix

            def link_maker(x):
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[x][0]) + '%2C' + str(actual_route_sequence[x][1]) + '&destinations='
                for y in actual_route_sequence[:-1]:
                    if y == actual_route_sequence[x]:
                        continue
                    link_main = link_main + str(y[0]) + '%2C' + str(y[1]) + '%7C'
                link_main = link_main + str(actual_route_sequence[-1][0]) + '%2C' + str(actual_route_sequence[-1][1])
                link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                
                payload={}
                headers = {}

                response = requests.request("GET", link_main, headers=headers, data=payload)
                json_content = response.json()
                
                dis_list = []
                for i in range(len(json_content['rows'][0]['elements'])):
                    distance = json_content['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                
                return dis_list

            actual_route_sequence = []
            actual_route_sequence.append(current_location)
            for x in top_loc_lat_lon:
                actual_route_sequence.append(x)

            print(actual_route_sequence)
            distance_matrix = get_distance_matrix(actual_route_sequence)

            #Calculating Total Distance in Algorithm
            def total_distance_required(actual_route_sequence,algoritm_sequence):
                total_distance = 0
                for x in range(len(algoritm_sequence)-1):
                    link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[algoritm_sequence[x]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x]][1]) + '&destinations='
                    link_main = link_main + str(actual_route_sequence[algoritm_sequence[x+1]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x+1]][1])
                    link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                    
                    #Intilizing GoogleAPI parameters
                    url = link_main
                    payload = {}
                    headers = {}

                    #Calling GoogleAPI
                    response = requests.request("GET", url, headers=headers, data=payload)
                    json_content = response.json()
                    
                    #Calculating the distance
                    distance = json_content['rows'][0]['elements'][0]['distance']['value']
                    total_distance = total_distance + distance
                return total_distance
            
            #Tabu Search Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def get_neighborhood(route):
                neighborhood = []
                for i in range(1, len(route)-1):
                    for j in range(i+1, len(route)):
                        new_route = route.copy()
                        new_route[i:j] = reversed(new_route[i:j])
                        neighborhood.append(new_route)
                return neighborhood

            def get_best_neighbor(neighbors, distance_matrix, tabu_list):
                best_neighbor = None
                best_distance = None
                for neighbor in neighbors:
                    if neighbor not in tabu_list:
                        distance = route_distance(neighbor, distance_matrix)
                        if best_distance is None or distance < best_distance:
                            best_neighbor = neighbor
                            best_distance = distance
                return best_neighbor, best_distance

            def tabu_search(locations, distance_matrix, starting_point=0, tabu_size=15, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                tabu_list = []
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution
                for i in range(max_iterations):
                    neighborhood = get_neighborhood(current_solution)
                    best_neighbor, best_distance = get_best_neighbor(neighborhood, distance_matrix, tabu_list)
                    if best_neighbor is None:
                        break
                    current_solution = best_neighbor
                    if best_distance < route_distance(best_solution, distance_matrix):
                        best_solution = best_neighbor
                    tabu_list.append(best_neighbor)
                    if len(tabu_list) > tabu_size:
                        tabu_list.pop(0)
                return best_solution
            
            ##Tabu Search Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            tabu_route = tabu_search(actual_route_sequence, distance_matrix)
            print(tabu_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            tabu_total_time = end_time - start_time

            print("Total time elapsed:", tabu_total_time, "seconds")

            tabu_distance = total_distance_required(actual_route_sequence,tabu_route)

            print("Total distance: ", tabu_distance, "meters")

            #Genetic Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def generate_random_route(n, starting_point):
                route = list(range(n))
                route.remove(starting_point)
                random.shuffle(route)
                route.insert(0, starting_point)
                return route

            def crossover(parent1, parent2):
                crossover_point1 = random.randint(1, len(parent1)-2)
                crossover_point2 = random.randint(crossover_point1+1, len(parent1)-1)
                child = parent1.copy()
                for i in range(crossover_point1, crossover_point2):
                    if parent2[i] not in child:
                        for j in range(len(child)):
                            if child[j] == parent2[i]:
                                child[j] = child[i]
                                child[i] = parent2[i]
                                break
                return child

            def mutation(route):
                mutation_point1 = random.randint(1, len(route)-2)
                mutation_point2 = random.randint(1, len(route)-2)
                route[mutation_point1], route[mutation_point2] = route[mutation_point2], route[mutation_point1]
                return route

            def genetic_algorithm(locations, distance_matrix, starting_point=0, population_size=50, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                population = [generate_random_route(n, starting_point) for i in range(population_size)]
                best_route = population[0]
                for i in range(max_iterations):
                    fitness_scores = [1/route_distance(route, distance_matrix) for route in population]
                    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
                    if route_distance(sorted_population[0], distance_matrix) < route_distance(best_route, distance_matrix):
                        best_route = sorted_population[0]
                    new_population = [sorted_population[0]]
                    for i in range(1, population_size):
                        parent1 = sorted_population[random.randint(0, int(population_size/2))]
                        parent2 = sorted_population[random.randint(0, int(population_size/2))]
                        child = crossover(parent1, parent2)
                        if random.uniform(0, 1) < 0.1:
                            child = mutation(child)
                        new_population.append(child)
                    population = new_population
                return best_route
            
            ##Genetic Algorithm Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            genetic_route = genetic_algorithm(actual_route_sequence, distance_matrix)
            print(genetic_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            genetic_route_total_time = end_time - start_time

            print("Total time elapsed:", genetic_route_total_time, "seconds")

            genetic_distance = total_distance_required(actual_route_sequence,genetic_route)

            print("Total distance: ", genetic_distance, "meters")

            #Simulated Annealing with Google API
            def route_distance(route, distance_matrix):
                # Calculate the total distance of a route
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def simulated_annealing(locations, distance_matrix, starting_point=0, temperature=10000, cooling_factor=0.9995, max_iterations=10000):
                # Initialize the current and best solutions
                n = len(locations)
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution

                # Start the simulated annealing algorithm
                for i in range(max_iterations):
                    # Choose a random neighbor by swapping two cities in the route
                    neighbor = current_solution.copy()
                    i = random.randint(1, n-2)
                    j = random.randint(i+1, n-1)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                    # Calculate the difference in distance between the current and the new solution
                    current_distance = route_distance(current_solution, distance_matrix)
                    neighbor_distance = route_distance(neighbor, distance_matrix)
                    delta = neighbor_distance - current_distance

                    # Accept the new solution if it's better or with a certain probability if it's worse
                    if delta < 0 or random.random() < math.exp(-delta/temperature):
                        current_solution = neighbor
                        if neighbor_distance < route_distance(best_solution, distance_matrix):
                            best_solution = neighbor

                    # Decrease the temperature
                    temperature *= cooling_factor

                return best_solution
            
            ##Simulated Annealing Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            simulated_annealing_route = simulated_annealing(actual_route_sequence, distance_matrix)
            print(simulated_annealing_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            simulated_annealing_total_time = end_time - start_time

            print("Total time elapsed:", simulated_annealing_total_time, "seconds")

            simulated_annealing_distance = total_distance_required(actual_route_sequence,simulated_annealing_route)

            print("Total distance: ", simulated_annealing_distance, "meters")

            context = {'TT': tabu_total_time,"TD": tabu_distance,
                       'GT': genetic_route_total_time,"GD": genetic_distance,
                       'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
                       'TLNDT': data_list}
            user_output = Delhi_User_Output.objects.get(username=Username_current)
            user_output.current_location = current_location
            user_output.tabu_total_time = tabu_total_time
            user_output.tabu_distance = tabu_distance
            user_output.genetic_route_total_time =genetic_route_total_time
            user_output.genetic_distance = genetic_distance
            user_output.simulated_annealing_total_time = simulated_annealing_total_time
            user_output.simulated_annealing_distance = simulated_annealing_distance
            user_output.top_loc_name_dis_time = data_list
            user_output.tabu_route = tabu_route
            user_output.genetic_route = genetic_route
            user_output.simulated_annealing_route = simulated_annealing_route
            user_output.all_lat_lon = actual_route_sequence
            user_output.save()

            return redirect('delhi_show')   

        elif request.POST.get('action') == 'delhi_button1':
            categories_order_list = request.POST.getlist('category_boxes')
            print(categories_order_list)
            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            user_categories_object.delhi_categories = categories_order_list
            user_categories_object.save()
            user_categories = user_categories_object.delhi_categories
            # print(user_categories)

            delhi_data_categories = []
            for x in Delhi.objects.all().values():
                delhi_data_categories.append(x.get("Categories"))
            # print(mumbai_data_categories)

            filtered_categories = []

            i=0
            for cat in delhi_data_categories:
                i = i+1
                found = False
                for req in user_categories:
                    if req in cat:
                        City_Location_Name = Delhi.objects.get(id=i)
                        filtered_categories.append(City_Location_Name.Tourist_spot)
                        found = True
                        break
                if not found:
                    filtered_categories.append("Null")
            print(filtered_categories)

            user_categories_object.delhi_all_spots = filtered_categories
            user_categories_object.save()
        
        elif request.POST.get('action') == 'button3':
            return redirect('delhi_show')

    delhi_data = []
    for x in Delhi.objects.all().values():
        delhi_data.append(x)

    categories_list = []
    for x in All_Categories_Delhi.objects.all().values():
        categories_list.append(x)
    
    context = {'categories': categories_list,"delhi_try": delhi_data}

    return render(request, 'delhi.html', context)

def delhi_show(request):
    Username_current = request.user.username
    user_output = Delhi_User_Output.objects.get(username=Username_current)
    current_location = user_output.current_location
    tabu_total_time = user_output.tabu_total_time
    tabu_distance = user_output.tabu_distance
    genetic_route_total_time = user_output.genetic_route_total_time
    genetic_distance = user_output.genetic_distance
    simulated_annealing_total_time = user_output.simulated_annealing_total_time
    simulated_annealing_distance = user_output.simulated_annealing_distance
    top_loc_name_dis_time = user_output.top_loc_name_dis_time
    top_loc_name_dis_time = ast.literal_eval(top_loc_name_dis_time)
    tabu_route = user_output.tabu_route
    tabu_route = ast.literal_eval(tabu_route)
    genetic_route = user_output.genetic_route
    genetic_route = ast.literal_eval(genetic_route)
    simulated_annealing_route = user_output.simulated_annealing_route
    simulated_annealing_route = ast.literal_eval(simulated_annealing_route)
    all_lat_lon = user_output.all_lat_lon
    all_lat_lon = ast.literal_eval(all_lat_lon)
    if tabu_distance <= genetic_distance and tabu_distance <= simulated_annealing_distance:
        best_route = tabu_route
    elif genetic_distance <= simulated_annealing_distance:
        best_route = genetic_route
    else:
        best_route = simulated_annealing_route
        
    # Print the text version of the best route
    print("The best route to visit the tourist spots is as follows:")
    locations = [top_loc_name_dis_time[i-1]['Tourist_spot'] for i in best_route[1:]]
    route_text = f"Starting from your current location, visit {', '.join(locations[:-1])}, and {locations[-1]}."
    print(route_text)

    print(top_loc_name_dis_time)
    
    
    # m = folium.Map(location=[19.0760, 72.8777], zoom_start=12)

    tourist_spots = []
    tourist_spots.append

    # add markers for each tourist spot
    for spot in top_loc_name_dis_time:
        tourist_spot = spot['Tourist_spot']
        mumbai_spot = Delhi.objects.get(Tourist_spot=tourist_spot)
        print(mumbai_spot)
        lat = mumbai_spot.latitude
        lon = mumbai_spot.longitude
        tourist_spots.append({'name': tourist_spot, 'latitude':  lat , 'longitude': lon})
    
    print(tourist_spots)

    # Create a map centered at Mumbai
    current_location = ast.literal_eval(current_location)
    map = folium.Map(location=current_location, zoom_start=14)
    folium.Marker(location=[current_location[0], current_location[1]], icon=folium.Icon(color='pink')).add_to(map)

    # Add markers for each tourist spot
    for spot in tourist_spots:
        folium.Marker(location=[spot["latitude"], spot["longitude"]], popup=spot["name"], icon=folium.Icon(color='purple')).add_to(map)
    
    # Convert the map to HTML and pass it to the template
    map_html = map._repr_html_()
    
    context = {'TT': tabu_total_time,"TD": tabu_distance,
               'GT': genetic_route_total_time,"GD": genetic_distance,
               'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
               'TLNDT': top_loc_name_dis_time, 
               'TR': tabu_route,
               'GR' : genetic_route,
               'SAR' : simulated_annealing_route,
               'BR' : best_route,
               'CL' : route_text,
               'MAPS' : map_html}
    
    if request.POST.get('action') == 'button':
        link_maker = "https://www.google.com/maps/dir/?api=1&origin=" + all_lat_lon[0][0] + "," + all_lat_lon[0][1] + "&waypoints="
        link_maker = link_maker + str(all_lat_lon[1][0]) + "," + str(all_lat_lon[1][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[2][0]) + "," + str(all_lat_lon[2][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[3][0]) + "," + str(all_lat_lon[3][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[4][0]) + "," + str(all_lat_lon[4][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[5][0]) + "," + str(all_lat_lon[7][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[6][0]) + "," + str(all_lat_lon[6][1]) + "|"
        link_maker = link_maker + "&destination=" + str(all_lat_lon[7][0]) + "," + str(all_lat_lon[7][1])

        print(link_maker)
        return redirect(link_maker)

    return render(request, 'mumbai_show.html', context)
    return render(request, 'delhi_show.html', context)

#KOLKATA
def kolkata(request):
    if request.method == "POST":
        
        if request.POST.get('action') == 'button2':
            
            # options = ChromeOptions()
            # options.add_argument("--use--fake-ui-for-media-stream")
            # driver = Chrome(options=options)
            # timeout = 20
            # driver.get("https://whatmylocation.com/")
            # wait = WebDriverWait(driver, timeout)
            # time.sleep(3)
            # current_longitude = driver.find_element(By.ID, "longitude").text
            # current_latitude = driver.find_element(By.ID, "latitude").text
            # current_location = [current_latitude,current_longitude]
            # driver.quit()

            current_latitude = "22.567276"
            current_longitude = "88.359991"
            current_location = ["22.567276","88.359991"]

            kolkata_data = []

            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            filtered_categories = user_categories_object.kolkata_all_spots

            for x, y in zip(Kolkata.objects.all().values(), filtered_categories):
                if y != "Null" and all(x.values()):
                    kolkata_data.append(x)
            print(kolkata_data)

            def googleapi_resource_extraction():
                
                #Filtering by Latitude and Longitude
                lat_lon = pd.DataFrame([[x.get("latitude"), x.get("longitude")] for x in kolkata_data], columns=['latitude', 'longitude'])
                
                #Spliting into 5 parts of 23 each and 24th in diff variable
                lat_lon_split = np.array_split(lat_lon, 5)
                lat_lon_1 = lat_lon_split[0][:-1]
                lat_lon_2 = lat_lon_split[1][:-1]
                lat_lon_3 = lat_lon_split[2][:-1]
                lat_lon_4 = lat_lon_split[3][:-1]
                lat_lon_5 = lat_lon_split[4][:-1]
                lat_lon_1_last = lat_lon_split[0][-1:]
                lat_lon_2_last = lat_lon_split[1][-1:]
                lat_lon_3_last = lat_lon_split[2][-1:]
                lat_lon_4_last = lat_lon_split[3][-1:]
                lat_lon_5_last = lat_lon_split[4][-1:]
                
                #Storing Data in json format
                json_spit_1 = googleapi_link_maker(lat_lon_1,lat_lon_1_last)
                json_spit_2 = googleapi_link_maker(lat_lon_2,lat_lon_2_last)
                json_spit_3 = googleapi_link_maker(lat_lon_3,lat_lon_3_last)
                json_spit_4 = googleapi_link_maker(lat_lon_4,lat_lon_4_last)
                json_spit_5 = googleapi_link_maker(lat_lon_5,lat_lon_5_last)
                
                #Storing Data in file for future Reference(Will be removed in final code)
                # with open('json_spit_1.json', 'w') as f:
                #     json.dump(json_spit_1, f)
                #     f.close
                # with open('json_spit_2.json', 'w') as f:
                #     json.dump(json_spit_2, f)
                #     f.close
                # with open('json_spit_3.json', 'w') as f:
                #     json.dump(json_spit_3, f)
                #     f.close
                # with open('json_spit_4.json', 'w') as f:
                #     json.dump(json_spit_4, f)
                #     f.close
                # with open('json_spit_5.json', 'w') as f:
                #     json.dump(json_spit_5, f)
                #     f.close
                
                #Making dataframe for the distance collected
                dis_list = []
                dur_list = []
                dis_list,dur_list = df_dis_tim_collection(json_spit_1,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_2,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_3,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_4,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_5,dis_list,dur_list)
                
                #Making Location DataFrame containing distance,duration
                global loc_dir_tim
                loc_dir_tim = pd.DataFrame([[x.get("Tourist_spot"), x.get("latitude"), x.get("longitude"), dis_list[i], dur_list[i]] for i, x in enumerate(kolkata_data)], 
                           columns=['Tourist_spot', 'latitude', 'longitude', 'Distance_Meters', 'Duration_Seconds'])
                
                #Making list of closest 5 number of places
                top_loc_lat_lon = closest_5_places(loc_dir_tim)
                return top_loc_lat_lon
            
            def googleapi_link_maker(lat_lon,lat_lon_last):
    
                #Fetching GoogleAPI Key
                # with open('apikey.txt') as f:
                #     api_key = f.readline()
                #     f.close

                api_key = "AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4"
                
                #Generating Link
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + current_latitude + '%2C' + current_longitude + '&destinations='
                for x in lat_lon.index:
                    link_main = link_main + str(lat_lon['latitude'][x]) + '%2C' + str(lat_lon['longitude'][x]) + '%7C'
                link_main = link_main + str(lat_lon_last['latitude'].iloc[-1]) + '%2C' + str(lat_lon_last['longitude'].iloc[-1])
                link_main = link_main + '&key=' + api_key
                
                #Intilizing GoogleAPI parameters
                url = link_main
                payload = {}
                headers = {}
                
                #Calling GoogleAPI
                response = requests.request("GET", url, headers=headers, data=payload)
                json_content = response.json()
                
                #Returning all values
                return json_content
            
            def df_dis_tim_collection(json,dis_list,dur_list):
    
                #Filtering out data to get required parameters
                for i in range(len(json['rows'][0]['elements'])):
                    distance = json['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                    duration = json['rows'][0]['elements'][i]['duration']['value']
                    dur_list.append(duration)
                return dis_list,dur_list
            
            def closest_5_places(loc_dir_tim):
    
                #Calculating 5 number of places
                loc_dir_tim_dup_sorted = loc_dir_tim.sort_values(by=['Distance_Meters'])
                loc_dir_tim_dup_sorted_top5 = loc_dir_tim_dup_sorted[0:7]
                global top_loc_name_dis_time
                top_loc_name_dis_time = loc_dir_tim_dup_sorted_top5[["Tourist_spot","Distance_Meters","Duration_Seconds"]]
                loc_dir_tim_dup_sorted_top5_lat_lon = loc_dir_tim_dup_sorted_top5[["latitude","longitude"]]
                loc_dir_tim_dup_sorted_top5_lat_lon_list = loc_dir_tim_dup_sorted_top5_lat_lon.values.tolist()
                return loc_dir_tim_dup_sorted_top5_lat_lon_list
            
            #Will be used for folium maps
            top_loc_lat_lon = googleapi_resource_extraction()
            data_list = top_loc_name_dis_time.to_dict('records')
            

            #Making a Distance Matrix
            def get_distance_matrix(locations):
                n = len(locations)
                distance_matrix = [[0] * n for i in range(n)]
                for x in range(n):
                    dis_list = link_maker(x)
                    for y in range(n):
                        if x == y:
                            continue
                        elif(x < y):
                            distance_matrix[x][y] = dis_list[y-1]
                        elif(x > y):
                            distance_matrix[x][y] = dis_list[y]
                return distance_matrix

            def link_maker(x):
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[x][0]) + '%2C' + str(actual_route_sequence[x][1]) + '&destinations='
                for y in actual_route_sequence[:-1]:
                    if y == actual_route_sequence[x]:
                        continue
                    link_main = link_main + str(y[0]) + '%2C' + str(y[1]) + '%7C'
                link_main = link_main + str(actual_route_sequence[-1][0]) + '%2C' + str(actual_route_sequence[-1][1])
                link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                
                payload={}
                headers = {}

                response = requests.request("GET", link_main, headers=headers, data=payload)
                json_content = response.json()
                
                dis_list = []
                for i in range(len(json_content['rows'][0]['elements'])):
                    distance = json_content['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                
                return dis_list

            actual_route_sequence = []
            actual_route_sequence.append(current_location)
            for x in top_loc_lat_lon:
                actual_route_sequence.append(x)

            distance_matrix = get_distance_matrix(actual_route_sequence)

            #Calculating Total Distance in Algorithm
            def total_distance_required(actual_route_sequence,algoritm_sequence):
                total_distance = 0
                for x in range(len(algoritm_sequence)-1):
                    link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[algoritm_sequence[x]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x]][1]) + '&destinations='
                    link_main = link_main + str(actual_route_sequence[algoritm_sequence[x+1]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x+1]][1])
                    link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                    
                    #Intilizing GoogleAPI parameters
                    url = link_main
                    payload = {}
                    headers = {}

                    #Calling GoogleAPI
                    response = requests.request("GET", url, headers=headers, data=payload)
                    json_content = response.json()
                    
                    #Calculating the distance
                    distance = json_content['rows'][0]['elements'][0]['distance']['value']
                    total_distance = total_distance + distance
                return total_distance
            
            #Tabu Search Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def get_neighborhood(route):
                neighborhood = []
                for i in range(1, len(route)-1):
                    for j in range(i+1, len(route)):
                        new_route = route.copy()
                        new_route[i:j] = reversed(new_route[i:j])
                        neighborhood.append(new_route)
                return neighborhood

            def get_best_neighbor(neighbors, distance_matrix, tabu_list):
                best_neighbor = None
                best_distance = None
                for neighbor in neighbors:
                    if neighbor not in tabu_list:
                        distance = route_distance(neighbor, distance_matrix)
                        if best_distance is None or distance < best_distance:
                            best_neighbor = neighbor
                            best_distance = distance
                return best_neighbor, best_distance

            def tabu_search(locations, distance_matrix, starting_point=0, tabu_size=15, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                tabu_list = []
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution
                for i in range(max_iterations):
                    neighborhood = get_neighborhood(current_solution)
                    best_neighbor, best_distance = get_best_neighbor(neighborhood, distance_matrix, tabu_list)
                    if best_neighbor is None:
                        break
                    current_solution = best_neighbor
                    if best_distance < route_distance(best_solution, distance_matrix):
                        best_solution = best_neighbor
                    tabu_list.append(best_neighbor)
                    if len(tabu_list) > tabu_size:
                        tabu_list.pop(0)
                return best_solution
            
            ##Tabu Search Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            tabu_route = tabu_search(actual_route_sequence, distance_matrix)
            print(tabu_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            tabu_total_time = end_time - start_time

            print("Total time elapsed:", tabu_total_time, "seconds")

            tabu_distance = total_distance_required(actual_route_sequence,tabu_route)

            print("Total distance: ", tabu_distance, "meters")

            #Genetic Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def generate_random_route(n, starting_point):
                route = list(range(n))
                route.remove(starting_point)
                random.shuffle(route)
                route.insert(0, starting_point)
                return route

            def crossover(parent1, parent2):
                crossover_point1 = random.randint(1, len(parent1)-2)
                crossover_point2 = random.randint(crossover_point1+1, len(parent1)-1)
                child = parent1.copy()
                for i in range(crossover_point1, crossover_point2):
                    if parent2[i] not in child:
                        for j in range(len(child)):
                            if child[j] == parent2[i]:
                                child[j] = child[i]
                                child[i] = parent2[i]
                                break
                return child

            def mutation(route):
                mutation_point1 = random.randint(1, len(route)-2)
                mutation_point2 = random.randint(1, len(route)-2)
                route[mutation_point1], route[mutation_point2] = route[mutation_point2], route[mutation_point1]
                return route

            def genetic_algorithm(locations, distance_matrix, starting_point=0, population_size=50, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                population = [generate_random_route(n, starting_point) for i in range(population_size)]
                best_route = population[0]
                for i in range(max_iterations):
                    fitness_scores = [1/route_distance(route, distance_matrix) for route in population]
                    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
                    if route_distance(sorted_population[0], distance_matrix) < route_distance(best_route, distance_matrix):
                        best_route = sorted_population[0]
                    new_population = [sorted_population[0]]
                    for i in range(1, population_size):
                        parent1 = sorted_population[random.randint(0, int(population_size/2))]
                        parent2 = sorted_population[random.randint(0, int(population_size/2))]
                        child = crossover(parent1, parent2)
                        if random.uniform(0, 1) < 0.1:
                            child = mutation(child)
                        new_population.append(child)
                    population = new_population
                return best_route
            
            ##Genetic Algorithm Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            genetic_route = genetic_algorithm(actual_route_sequence, distance_matrix)
            print(genetic_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            genetic_route_total_time = end_time - start_time

            print("Total time elapsed:", genetic_route_total_time, "seconds")

            genetic_distance = total_distance_required(actual_route_sequence,genetic_route)

            print("Total distance: ", genetic_distance, "meters")

            #Simulated Annealing with Google API
            def route_distance(route, distance_matrix):
                # Calculate the total distance of a route
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def simulated_annealing(locations, distance_matrix, starting_point=0, temperature=10000, cooling_factor=0.9995, max_iterations=10000):
                # Initialize the current and best solutions
                n = len(locations)
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution

                # Start the simulated annealing algorithm
                for i in range(max_iterations):
                    # Choose a random neighbor by swapping two cities in the route
                    neighbor = current_solution.copy()
                    i = random.randint(1, n-2)
                    j = random.randint(i+1, n-1)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                    # Calculate the difference in distance between the current and the new solution
                    current_distance = route_distance(current_solution, distance_matrix)
                    neighbor_distance = route_distance(neighbor, distance_matrix)
                    delta = neighbor_distance - current_distance

                    # Accept the new solution if it's better or with a certain probability if it's worse
                    if delta < 0 or random.random() < math.exp(-delta/temperature):
                        current_solution = neighbor
                        if neighbor_distance < route_distance(best_solution, distance_matrix):
                            best_solution = neighbor

                    # Decrease the temperature
                    temperature *= cooling_factor

                return best_solution
            
            ##Simulated Annealing Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            simulated_annealing_route = simulated_annealing(actual_route_sequence, distance_matrix)
            print(simulated_annealing_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            simulated_annealing_total_time = end_time - start_time

            print("Total time elapsed:", simulated_annealing_total_time, "seconds")

            simulated_annealing_distance = total_distance_required(actual_route_sequence,simulated_annealing_route)

            print("Total distance: ", simulated_annealing_distance, "meters")

            context = {'TT': tabu_total_time,"TD": tabu_distance,
                       'GT': genetic_route_total_time,"GD": genetic_distance,
                       'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
                       'TLNDT': data_list}
            user_output = Kolkata_User_Output.objects.get(username=Username_current)
            user_output.current_location = current_location
            user_output.tabu_total_time = tabu_total_time
            user_output.tabu_distance = tabu_distance
            user_output.genetic_route_total_time =genetic_route_total_time
            user_output.genetic_distance = genetic_distance
            user_output.simulated_annealing_total_time = simulated_annealing_total_time
            user_output.simulated_annealing_distance = simulated_annealing_distance
            user_output.top_loc_name_dis_time = data_list
            user_output.tabu_route = tabu_route
            user_output.genetic_route = genetic_route
            user_output.simulated_annealing_route = simulated_annealing_route
            user_output.all_lat_lon = actual_route_sequence
            user_output.save()

            return redirect('kolkata_show')   

        elif request.POST.get('action') == 'button1':
            categories_order_list = request.POST.getlist('category_boxes')
            print(categories_order_list)
            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            user_categories_object.kolkata_categories = categories_order_list
            user_categories_object.save()
            user_categories = user_categories_object.kolkata_categories
            # print(user_categories)

            kolkata_data_categories = []
            for x in Kolkata.objects.all().values():
                kolkata_data_categories.append(x.get("Categories"))
            # print(mumbai_data_categories)

            filtered_categories = []

            i=0
            for cat in kolkata_data_categories:
                i = i+1
                found = False
                for req in user_categories:
                    if req in cat:
                        City_Location_Name = Kolkata.objects.get(id=i)
                        filtered_categories.append(City_Location_Name.Tourist_spot)
                        found = True
                        break
                if not found:
                    filtered_categories.append("Null")
            print(filtered_categories)

            user_categories_object.kolkata_all_spots = filtered_categories
            user_categories_object.save()
        
        elif request.POST.get('action') == 'button3':
            return redirect('kolkata_show') 

    kolkata_data = []
    for x in Kolkata.objects.all().values():
        kolkata_data.append(x)

    categories_list = []
    for x in All_Categories_Kolkata.objects.all().values():
        categories_list.append(x)
    
    context = {'categories': categories_list,"kolkata_try": kolkata_data}

    return render(request, 'kolkata.html', context)

def kolkata_show(request):
    Username_current = request.user.username
    user_output = Kolkata_User_Output.objects.get(username=Username_current)
    current_location = user_output.current_location
    tabu_total_time = user_output.tabu_total_time
    tabu_distance = user_output.tabu_distance
    genetic_route_total_time = user_output.genetic_route_total_time
    genetic_distance = user_output.genetic_distance
    simulated_annealing_total_time = user_output.simulated_annealing_total_time
    simulated_annealing_distance = user_output.simulated_annealing_distance
    top_loc_name_dis_time = user_output.top_loc_name_dis_time
    top_loc_name_dis_time = ast.literal_eval(top_loc_name_dis_time)
    tabu_route = user_output.tabu_route
    tabu_route = ast.literal_eval(tabu_route)
    genetic_route = user_output.genetic_route
    genetic_route = ast.literal_eval(genetic_route)
    simulated_annealing_route = user_output.simulated_annealing_route
    simulated_annealing_route = ast.literal_eval(simulated_annealing_route)
    all_lat_lon = user_output.all_lat_lon
    all_lat_lon = ast.literal_eval(all_lat_lon)
    if tabu_distance <= genetic_distance and tabu_distance <= simulated_annealing_distance:
        best_route = tabu_route
    elif genetic_distance <= simulated_annealing_distance:
        best_route = genetic_route
    else:
        best_route = simulated_annealing_route
        
    # Print the text version of the best route
    print("The best route to visit the tourist spots is as follows:")
    locations = [top_loc_name_dis_time[i-1]['Tourist_spot'] for i in best_route[1:]]
    route_text = f"Starting from your current location, visit {', '.join(locations[:-1])}, and {locations[-1]}."
    print(route_text)

    print(top_loc_name_dis_time)
    
    # m = folium.Map(location=[19.0760, 72.8777], zoom_start=12)

    tourist_spots = []
    tourist_spots.append

    # add markers for each tourist spot
    for spot in top_loc_name_dis_time:
        tourist_spot = spot['Tourist_spot']
        mumbai_spot = Kolkata.objects.get(Tourist_spot=tourist_spot)
        print(mumbai_spot)
        lat = mumbai_spot.latitude
        lon = mumbai_spot.longitude
        tourist_spots.append({'name': tourist_spot, 'latitude':  lat , 'longitude': lon})
    
    print(tourist_spots)

    # Create a map centered at Mumbai
    current_location = ast.literal_eval(current_location)
    map = folium.Map(location=current_location, zoom_start=14)
    folium.Marker(location=[current_location[0], current_location[1]], icon=folium.Icon(color='pink')).add_to(map)

    # Add markers for each tourist spot
    for spot in tourist_spots:
        folium.Marker(location=[spot["latitude"], spot["longitude"]], popup=spot["name"], icon=folium.Icon(color='purple')).add_to(map)
    
    # Convert the map to HTML and pass it to the template
    map_html = map._repr_html_()
    
    context = {'TT': tabu_total_time,"TD": tabu_distance,
               'GT': genetic_route_total_time,"GD": genetic_distance,
               'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
               'TLNDT': top_loc_name_dis_time, 
               'TR': tabu_route,
               'GR' : genetic_route,
               'SAR' : simulated_annealing_route,
               'BR' : best_route,
               'CL' : route_text,
               'MAPS' : map_html}
    
    if request.POST.get('action') == 'button':
        link_maker = "https://www.google.com/maps/dir/?api=1&origin=" + all_lat_lon[0][0] + "," + all_lat_lon[0][1] + "&waypoints="
        link_maker = link_maker + str(all_lat_lon[1][0]) + "," + str(all_lat_lon[1][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[2][0]) + "," + str(all_lat_lon[2][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[3][0]) + "," + str(all_lat_lon[3][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[4][0]) + "," + str(all_lat_lon[4][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[5][0]) + "," + str(all_lat_lon[7][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[6][0]) + "," + str(all_lat_lon[6][1]) + "|"
        link_maker = link_maker + "&destination=" + str(all_lat_lon[7][0]) + "," + str(all_lat_lon[7][1])

        print(link_maker)
        return redirect(link_maker)
    
    return render(request, 'kolkata_show.html', context)

#CHENNAI
def chennai(request):
    if request.method == "POST":
        
        if request.POST.get('action') == 'button2':
            
            # options = ChromeOptions()
            # options.add_argument("--use--fake-ui-for-media-stream")
            # driver = Chrome(options=options)
            # timeout = 20
            # driver.get("https://whatmylocation.com/")
            # wait = WebDriverWait(driver, timeout)
            # time.sleep(3)
            # current_longitude = driver.find_element(By.ID, "longitude").text
            # current_latitude = driver.find_element(By.ID, "latitude").text
            # current_location = [current_latitude,current_longitude]
            # driver.quit()

            current_latitude = "13.069523"
            current_longitude = "80.266508"
            current_location = ["13.069523","80.266508"]

            chennai_data = []

            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            filtered_categories = user_categories_object.chennai_all_spots

            for x, y in zip(Chennai.objects.all().values(), filtered_categories):
                if y != "Null" and all(x.values()):
                    chennai_data.append(x)

            def googleapi_resource_extraction():
                
                #Filtering by Latitude and Longitude
                lat_lon = pd.DataFrame([[x.get("latitude"), x.get("longitude")] for x in chennai_data], columns=['latitude', 'longitude'])
                
                #Spliting into 5 parts of 23 each and 24th in diff variable
                lat_lon_split = np.array_split(lat_lon, 5)
                lat_lon_1 = lat_lon_split[0][:-1]
                lat_lon_2 = lat_lon_split[1][:-1]
                lat_lon_3 = lat_lon_split[2][:-1]
                lat_lon_4 = lat_lon_split[3][:-1]
                lat_lon_5 = lat_lon_split[4][:-1]
                lat_lon_1_last = lat_lon_split[0][-1:]
                lat_lon_2_last = lat_lon_split[1][-1:]
                lat_lon_3_last = lat_lon_split[2][-1:]
                lat_lon_4_last = lat_lon_split[3][-1:]
                lat_lon_5_last = lat_lon_split[4][-1:]
                
                #Storing Data in json format
                json_spit_1 = googleapi_link_maker(lat_lon_1,lat_lon_1_last)
                json_spit_2 = googleapi_link_maker(lat_lon_2,lat_lon_2_last)
                json_spit_3 = googleapi_link_maker(lat_lon_3,lat_lon_3_last)
                json_spit_4 = googleapi_link_maker(lat_lon_4,lat_lon_4_last)
                json_spit_5 = googleapi_link_maker(lat_lon_5,lat_lon_5_last)
                
                #Storing Data in file for future Reference(Will be removed in final code)
                # with open('json_spit_1.json', 'w') as f:
                #     json.dump(json_spit_1, f)
                #     f.close
                # with open('json_spit_2.json', 'w') as f:
                #     json.dump(json_spit_2, f)
                #     f.close
                # with open('json_spit_3.json', 'w') as f:
                #     json.dump(json_spit_3, f)
                #     f.close
                # with open('json_spit_4.json', 'w') as f:
                #     json.dump(json_spit_4, f)
                #     f.close
                # with open('json_spit_5.json', 'w') as f:
                #     json.dump(json_spit_5, f)
                #     f.close
                
                #Making dataframe for the distance collected
                dis_list = []
                dur_list = []
                dis_list,dur_list = df_dis_tim_collection(json_spit_1,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_2,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_3,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_4,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_5,dis_list,dur_list)
                
                #Making Location DataFrame containing distance,duration
                global loc_dir_tim
                loc_dir_tim = pd.DataFrame([[x.get("Tourist_spot"), x.get("latitude"), x.get("longitude"), dis_list[i], dur_list[i]] for i, x in enumerate(chennai_data)], 
                           columns=['Tourist_spot', 'latitude', 'longitude', 'Distance_Meters', 'Duration_Seconds'])
                
                #Making list of closest 5 number of places
                top_loc_lat_lon = closest_5_places(loc_dir_tim)
                return top_loc_lat_lon
            
            def googleapi_link_maker(lat_lon,lat_lon_last):
    
                #Fetching GoogleAPI Key
                # with open('apikey.txt') as f:
                #     api_key = f.readline()
                #     f.close

                api_key = "AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4"
                
                #Generating Link
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + current_latitude + '%2C' + current_longitude + '&destinations='
                for x in lat_lon.index:
                    link_main = link_main + str(lat_lon['latitude'][x]) + '%2C' + str(lat_lon['longitude'][x]) + '%7C'
                link_main = link_main + str(lat_lon_last['latitude'].iloc[-1]) + '%2C' + str(lat_lon_last['longitude'].iloc[-1])
                link_main = link_main + '&key=' + api_key
                
                #Intilizing GoogleAPI parameters
                url = link_main
                payload = {}
                headers = {}
                
                #Calling GoogleAPI
                response = requests.request("GET", url, headers=headers, data=payload)
                json_content = response.json()
                
                #Returning all values
                return json_content
            
            def df_dis_tim_collection(json,dis_list,dur_list):
    
                #Filtering out data to get required parameters
                for i in range(len(json['rows'][0]['elements'])):
                    distance = json['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                    duration = json['rows'][0]['elements'][i]['duration']['value']
                    dur_list.append(duration)
                return dis_list,dur_list
            
            def closest_5_places(loc_dir_tim):
    
                #Calculating 5 number of places
                loc_dir_tim_dup_sorted = loc_dir_tim.sort_values(by=['Distance_Meters'])
                loc_dir_tim_dup_sorted_top5 = loc_dir_tim_dup_sorted[0:7]
                global top_loc_name_dis_time
                top_loc_name_dis_time = loc_dir_tim_dup_sorted_top5[["Tourist_spot","Distance_Meters","Duration_Seconds"]]
                loc_dir_tim_dup_sorted_top5_lat_lon = loc_dir_tim_dup_sorted_top5[["latitude","longitude"]]
                loc_dir_tim_dup_sorted_top5_lat_lon_list = loc_dir_tim_dup_sorted_top5_lat_lon.values.tolist()
                return loc_dir_tim_dup_sorted_top5_lat_lon_list
            
            #Will be used for folium maps
            top_loc_lat_lon = googleapi_resource_extraction()
            print(top_loc_name_dis_time)
            data_list = top_loc_name_dis_time.to_dict('records')
            print(top_loc_name_dis_time)

            #Making a Distance Matrix
            def get_distance_matrix(locations):
                n = len(locations)
                distance_matrix = [[0] * n for i in range(n)]
                for x in range(n):
                    dis_list = link_maker(x)
                    for y in range(n):
                        if x == y:
                            continue
                        elif(x < y):
                            distance_matrix[x][y] = dis_list[y-1]
                        elif(x > y):
                            distance_matrix[x][y] = dis_list[y]
                return distance_matrix

            def link_maker(x):
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[x][0]) + '%2C' + str(actual_route_sequence[x][1]) + '&destinations='
                for y in actual_route_sequence[:-1]:
                    if y == actual_route_sequence[x]:
                        continue
                    link_main = link_main + str(y[0]) + '%2C' + str(y[1]) + '%7C'
                link_main = link_main + str(actual_route_sequence[-1][0]) + '%2C' + str(actual_route_sequence[-1][1])
                link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                
                payload={}
                headers = {}

                response = requests.request("GET", link_main, headers=headers, data=payload)
                json_content = response.json()
                
                dis_list = []
                for i in range(len(json_content['rows'][0]['elements'])):
                    distance = json_content['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                
                return dis_list

            actual_route_sequence = []
            actual_route_sequence.append(current_location)
            for x in top_loc_lat_lon:
                actual_route_sequence.append(x)

            distance_matrix = get_distance_matrix(actual_route_sequence)

            #Calculating Total Distance in Algorithm
            def total_distance_required(actual_route_sequence,algoritm_sequence):
                total_distance = 0
                for x in range(len(algoritm_sequence)-1):
                    link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[algoritm_sequence[x]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x]][1]) + '&destinations='
                    link_main = link_main + str(actual_route_sequence[algoritm_sequence[x+1]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x+1]][1])
                    link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                    
                    #Intilizing GoogleAPI parameters
                    url = link_main
                    payload = {}
                    headers = {}

                    #Calling GoogleAPI
                    response = requests.request("GET", url, headers=headers, data=payload)
                    json_content = response.json()
                    
                    #Calculating the distance
                    distance = json_content['rows'][0]['elements'][0]['distance']['value']
                    total_distance = total_distance + distance
                return total_distance
            
            #Tabu Search Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def get_neighborhood(route):
                neighborhood = []
                for i in range(1, len(route)-1):
                    for j in range(i+1, len(route)):
                        new_route = route.copy()
                        new_route[i:j] = reversed(new_route[i:j])
                        neighborhood.append(new_route)
                return neighborhood

            def get_best_neighbor(neighbors, distance_matrix, tabu_list):
                best_neighbor = None
                best_distance = None
                for neighbor in neighbors:
                    if neighbor not in tabu_list:
                        distance = route_distance(neighbor, distance_matrix)
                        if best_distance is None or distance < best_distance:
                            best_neighbor = neighbor
                            best_distance = distance
                return best_neighbor, best_distance

            def tabu_search(locations, distance_matrix, starting_point=0, tabu_size=15, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                tabu_list = []
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution
                for i in range(max_iterations):
                    neighborhood = get_neighborhood(current_solution)
                    best_neighbor, best_distance = get_best_neighbor(neighborhood, distance_matrix, tabu_list)
                    if best_neighbor is None:
                        break
                    current_solution = best_neighbor
                    if best_distance < route_distance(best_solution, distance_matrix):
                        best_solution = best_neighbor
                    tabu_list.append(best_neighbor)
                    if len(tabu_list) > tabu_size:
                        tabu_list.pop(0)
                return best_solution
            
            ##Tabu Search Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            tabu_route = tabu_search(actual_route_sequence, distance_matrix)
            print(tabu_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            tabu_total_time = end_time - start_time

            print("Total time elapsed:", tabu_total_time, "seconds")

            tabu_distance = total_distance_required(actual_route_sequence,tabu_route)

            print("Total distance: ", tabu_distance, "meters")

            #Genetic Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def generate_random_route(n, starting_point):
                route = list(range(n))
                route.remove(starting_point)
                random.shuffle(route)
                route.insert(0, starting_point)
                return route

            def crossover(parent1, parent2):
                crossover_point1 = random.randint(1, len(parent1)-2)
                crossover_point2 = random.randint(crossover_point1+1, len(parent1)-1)
                child = parent1.copy()
                for i in range(crossover_point1, crossover_point2):
                    if parent2[i] not in child:
                        for j in range(len(child)):
                            if child[j] == parent2[i]:
                                child[j] = child[i]
                                child[i] = parent2[i]
                                break
                return child

            def mutation(route):
                mutation_point1 = random.randint(1, len(route)-2)
                mutation_point2 = random.randint(1, len(route)-2)
                route[mutation_point1], route[mutation_point2] = route[mutation_point2], route[mutation_point1]
                return route

            def genetic_algorithm(locations, distance_matrix, starting_point=0, population_size=50, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                population = [generate_random_route(n, starting_point) for i in range(population_size)]
                best_route = population[0]
                for i in range(max_iterations):
                    fitness_scores = [1/route_distance(route, distance_matrix) for route in population]
                    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
                    if route_distance(sorted_population[0], distance_matrix) < route_distance(best_route, distance_matrix):
                        best_route = sorted_population[0]
                    new_population = [sorted_population[0]]
                    for i in range(1, population_size):
                        parent1 = sorted_population[random.randint(0, int(population_size/2))]
                        parent2 = sorted_population[random.randint(0, int(population_size/2))]
                        child = crossover(parent1, parent2)
                        if random.uniform(0, 1) < 0.1:
                            child = mutation(child)
                        new_population.append(child)
                    population = new_population
                return best_route
            
            ##Genetic Algorithm Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            genetic_route = genetic_algorithm(actual_route_sequence, distance_matrix)
            print(genetic_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            genetic_route_total_time = end_time - start_time

            print("Total time elapsed:", genetic_route_total_time, "seconds")

            genetic_distance = total_distance_required(actual_route_sequence,genetic_route)

            print("Total distance: ", genetic_distance, "meters")

            #Simulated Annealing with Google API
            def route_distance(route, distance_matrix):
                # Calculate the total distance of a route
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def simulated_annealing(locations, distance_matrix, starting_point=0, temperature=10000, cooling_factor=0.9995, max_iterations=10000):
                # Initialize the current and best solutions
                n = len(locations)
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution

                # Start the simulated annealing algorithm
                for i in range(max_iterations):
                    # Choose a random neighbor by swapping two cities in the route
                    neighbor = current_solution.copy()
                    i = random.randint(1, n-2)
                    j = random.randint(i+1, n-1)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                    # Calculate the difference in distance between the current and the new solution
                    current_distance = route_distance(current_solution, distance_matrix)
                    neighbor_distance = route_distance(neighbor, distance_matrix)
                    delta = neighbor_distance - current_distance

                    # Accept the new solution if it's better or with a certain probability if it's worse
                    if delta < 0 or random.random() < math.exp(-delta/temperature):
                        current_solution = neighbor
                        if neighbor_distance < route_distance(best_solution, distance_matrix):
                            best_solution = neighbor

                    # Decrease the temperature
                    temperature *= cooling_factor

                return best_solution
            
            ##Simulated Annealing Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            simulated_annealing_route = simulated_annealing(actual_route_sequence, distance_matrix)
            print(simulated_annealing_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            simulated_annealing_total_time = end_time - start_time

            print("Total time elapsed:", simulated_annealing_total_time, "seconds")

            simulated_annealing_distance = total_distance_required(actual_route_sequence,simulated_annealing_route)

            print("Total distance: ", simulated_annealing_distance, "meters")

            context = {'TT': tabu_total_time,"TD": tabu_distance,
                       'GT': genetic_route_total_time,"GD": genetic_distance,
                       'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
                       'TLNDT': data_list}
            user_output = Chennai_User_Output.objects.get(username=Username_current)
            user_output.current_location = current_location
            user_output.tabu_total_time = tabu_total_time
            user_output.tabu_distance = tabu_distance
            user_output.genetic_route_total_time =genetic_route_total_time
            user_output.genetic_distance = genetic_distance
            user_output.simulated_annealing_total_time = simulated_annealing_total_time
            user_output.simulated_annealing_distance = simulated_annealing_distance
            user_output.top_loc_name_dis_time = data_list
            user_output.tabu_route = tabu_route
            user_output.genetic_route = genetic_route
            user_output.simulated_annealing_route = simulated_annealing_route
            user_output.all_lat_lon = actual_route_sequence
            user_output.save()

            return redirect('chennai_show')   

        elif request.POST.get('action') == 'button1':
            categories_order_list = request.POST.getlist('category_boxes')
            print(categories_order_list)
            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            user_categories_object.chennai_categories = categories_order_list
            user_categories_object.save()
            user_categories = user_categories_object.chennai_categories
            # print(user_categories)

            chennai_data_categories = []
            for x in Chennai.objects.all().values():
                chennai_data_categories.append(x.get("Categories"))
            # print(mumbai_data_categories)

            filtered_categories = []

            i=0
            for cat in chennai_data_categories:
                i = i+1
                found = False
                for req in user_categories:
                    if req in cat:
                        City_Location_Name = Chennai.objects.get(id=i)
                        filtered_categories.append(City_Location_Name.Tourist_spot)
                        found = True
                        break
                if not found:
                    filtered_categories.append("Null")
            print(filtered_categories)

            user_categories_object.chennai_all_spots = filtered_categories
            user_categories_object.save()

        elif request.POST.get('action') == 'button3':
            return redirect('chennai_show')

    chennai_data = []
    for x in Chennai.objects.all().values():
        chennai_data.append(x)

    categories_list = []
    for x in All_Categories_Chennai.objects.all().values():
        categories_list.append(x)
    
    context = {'categories': categories_list,"chennai_try": chennai_data}

    return render(request, 'chennai.html', context)

def chennai_show(request):
    Username_current = request.user.username
    user_output = Chennai_User_Output.objects.get(username=Username_current)
    current_location = user_output.current_location
    tabu_total_time = user_output.tabu_total_time
    tabu_distance = user_output.tabu_distance
    genetic_route_total_time = user_output.genetic_route_total_time
    genetic_distance = user_output.genetic_distance
    simulated_annealing_total_time = user_output.simulated_annealing_total_time
    simulated_annealing_distance = user_output.simulated_annealing_distance
    top_loc_name_dis_time = user_output.top_loc_name_dis_time
    print(top_loc_name_dis_time)
    print(type(top_loc_name_dis_time))
    top_loc_name_dis_time = ast.literal_eval(top_loc_name_dis_time)
    tabu_route = user_output.tabu_route
    tabu_route = ast.literal_eval(tabu_route)
    genetic_route = user_output.genetic_route
    genetic_route = ast.literal_eval(genetic_route)
    simulated_annealing_route = user_output.simulated_annealing_route
    simulated_annealing_route = ast.literal_eval(simulated_annealing_route)
    all_lat_lon = user_output.all_lat_lon
    all_lat_lon = ast.literal_eval(all_lat_lon)
    if tabu_distance <= genetic_distance and tabu_distance <= simulated_annealing_distance:
        best_route = tabu_route
    elif genetic_distance <= simulated_annealing_distance:
        best_route = genetic_route
    else:
        best_route = simulated_annealing_route
        
    # Print the text version of the best route
    print("The best route to visit the tourist spots is as follows:")
    locations = [top_loc_name_dis_time[i-1]['Tourist_spot'] for i in best_route[1:]]
    route_text = f"Starting from your current location, visit {', '.join(locations[:-1])}, and {locations[-1]}."
    print(route_text)

    print(top_loc_name_dis_time)
    
    # m = folium.Map(location=[19.0760, 72.8777], zoom_start=12)

    tourist_spots = []
    tourist_spots.append

    # add markers for each tourist spot
    for spot in top_loc_name_dis_time:
        tourist_spot = spot['Tourist_spot']
        mumbai_spot = Chennai.objects.get(Tourist_spot=tourist_spot)
        print(mumbai_spot)
        lat = mumbai_spot.latitude
        lon = mumbai_spot.longitude
        tourist_spots.append({'name': tourist_spot, 'latitude':  lat , 'longitude': lon})
    
    print(tourist_spots)

    # Create a map centered at Mumbai
    current_location = ast.literal_eval(current_location)
    map = folium.Map(location=current_location, zoom_start=14)
    folium.Marker(location=[current_location[0], current_location[1]], icon=folium.Icon(color='pink')).add_to(map)

    # Add markers for each tourist spot
    for spot in tourist_spots:
        folium.Marker(location=[spot["latitude"], spot["longitude"]], popup=spot["name"], icon=folium.Icon(color='purple')).add_to(map)
    
    # Convert the map to HTML and pass it to the template
    map_html = map._repr_html_()
    
    context = {'TT': tabu_total_time,"TD": tabu_distance,
               'GT': genetic_route_total_time,"GD": genetic_distance,
               'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
               'TLNDT': top_loc_name_dis_time, 
               'TR': tabu_route,
               'GR' : genetic_route,
               'SAR' : simulated_annealing_route,
               'BR' : best_route,
               'CL' : route_text,
               'MAPS' : map_html}
    
    if request.POST.get('action') == 'button':
        link_maker = "https://www.google.com/maps/dir/?api=1&origin=" + all_lat_lon[0][0] + "," + all_lat_lon[0][1] + "&waypoints="
        link_maker = link_maker + str(all_lat_lon[1][0]) + "," + str(all_lat_lon[1][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[2][0]) + "," + str(all_lat_lon[2][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[3][0]) + "," + str(all_lat_lon[3][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[4][0]) + "," + str(all_lat_lon[4][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[5][0]) + "," + str(all_lat_lon[7][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[6][0]) + "," + str(all_lat_lon[6][1]) + "|"
        link_maker = link_maker + "&destination=" + str(all_lat_lon[7][0]) + "," + str(all_lat_lon[7][1])

        print(link_maker)
        return redirect(link_maker)
    
    return render(request, 'chennai_show.html', context)

#JAIPUR
def jaipur(request):
    if request.method == "POST":
        
        if request.POST.get('action') == 'button2':
            
            # options = ChromeOptions()
            # options.add_argument("--use--fake-ui-for-media-stream")
            # driver = Chrome(options=options)
            # timeout = 20
            # driver.get("https://whatmylocation.com/")
            # wait = WebDriverWait(driver, timeout)
            # time.sleep(3)
            # current_longitude = driver.find_element(By.ID, "longitude").text
            # current_latitude = driver.find_element(By.ID, "latitude").text
            # current_location = [current_latitude,current_longitude]
            # driver.quit()

            current_latitude = "26.899320"
            current_longitude = "75.798556"
            current_location = ["26.899320","75.798556"]

            jaipur_data = []

            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            filtered_categories = user_categories_object.jaipur_all_spots
            print(filtered_categories)

            for x, y in zip(Jaipur.objects.all().values(), filtered_categories):
                if y != "Null" and all(x.values()):
                    jaipur_data.append(x)

            def googleapi_resource_extraction():
                
                #Filtering by Latitude and Longitude
                lat_lon = pd.DataFrame([[x.get("latitude"), x.get("longitude")] for x in jaipur_data], columns=['latitude', 'longitude'])
                
                #Spliting into 5 parts of 23 each and 24th in diff variable
                lat_lon_split = np.array_split(lat_lon, 5)
                lat_lon_1 = lat_lon_split[0][:-1]
                lat_lon_2 = lat_lon_split[1][:-1]
                lat_lon_3 = lat_lon_split[2][:-1]
                lat_lon_4 = lat_lon_split[3][:-1]
                lat_lon_5 = lat_lon_split[4][:-1]
                lat_lon_1_last = lat_lon_split[0][-1:]
                lat_lon_2_last = lat_lon_split[1][-1:]
                lat_lon_3_last = lat_lon_split[2][-1:]
                lat_lon_4_last = lat_lon_split[3][-1:]
                lat_lon_5_last = lat_lon_split[4][-1:]
                
                #Storing Data in json format
                json_spit_1 = googleapi_link_maker(lat_lon_1,lat_lon_1_last)
                json_spit_2 = googleapi_link_maker(lat_lon_2,lat_lon_2_last)
                json_spit_3 = googleapi_link_maker(lat_lon_3,lat_lon_3_last)
                json_spit_4 = googleapi_link_maker(lat_lon_4,lat_lon_4_last)
                json_spit_5 = googleapi_link_maker(lat_lon_5,lat_lon_5_last)
                
                #Storing Data in file for future Reference(Will be removed in final code)
                # with open('json_spit_1.json', 'w') as f:
                #     json.dump(json_spit_1, f)
                #     f.close
                # with open('json_spit_2.json', 'w') as f:
                #     json.dump(json_spit_2, f)
                #     f.close
                # with open('json_spit_3.json', 'w') as f:
                #     json.dump(json_spit_3, f)
                #     f.close
                # with open('json_spit_4.json', 'w') as f:
                #     json.dump(json_spit_4, f)
                #     f.close
                # with open('json_spit_5.json', 'w') as f:
                #     json.dump(json_spit_5, f)
                #     f.close
                
                #Making dataframe for the distance collected
                dis_list = []
                dur_list = []
                dis_list,dur_list = df_dis_tim_collection(json_spit_1,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_2,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_3,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_4,dis_list,dur_list)
                dis_list,dur_list = df_dis_tim_collection(json_spit_5,dis_list,dur_list)
                
                #Making Location DataFrame containing distance,duration
                global loc_dir_tim
                loc_dir_tim = pd.DataFrame([[x.get("Tourist_spot"), x.get("latitude"), x.get("longitude"), dis_list[i], dur_list[i]] for i, x in enumerate(jaipur_data)], 
                           columns=['Tourist_spot', 'latitude', 'longitude', 'Distance_Meters', 'Duration_Seconds'])
                
                #Making list of closest 5 number of places
                top_loc_lat_lon = closest_5_places(loc_dir_tim)
                print(top_loc_lat_lon)
                print(top_loc_name_dis_time)
                return top_loc_lat_lon
            
            def googleapi_link_maker(lat_lon,lat_lon_last):
    
                #Fetching GoogleAPI Key
                # with open('apikey.txt') as f:
                #     api_key = f.readline()
                #     f.close

                api_key = "AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4"
                
                #Generating Link
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + current_latitude + '%2C' + current_longitude + '&destinations='
                for x in lat_lon.index:
                    link_main = link_main + str(lat_lon['latitude'][x]) + '%2C' + str(lat_lon['longitude'][x]) + '%7C'
                link_main = link_main + str(lat_lon_last['latitude'].iloc[-1]) + '%2C' + str(lat_lon_last['longitude'].iloc[-1])
                link_main = link_main + '&key=' + api_key
                
                #Intilizing GoogleAPI parameters
                url = link_main
                payload = {}
                headers = {}
                
                #Calling GoogleAPI
                response = requests.request("GET", url, headers=headers, data=payload)
                json_content = response.json()
                
                #Returning all values
                return json_content
            
            def df_dis_tim_collection(json,dis_list,dur_list):
    
                #Filtering out data to get required parameters
                for i in range(len(json['rows'][0]['elements'])):
                    distance = json['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                    duration = json['rows'][0]['elements'][i]['duration']['value']
                    dur_list.append(duration)
                return dis_list,dur_list
            
            def closest_5_places(loc_dir_tim):
    
                #Calculating 5 number of places
                loc_dir_tim_dup_sorted = loc_dir_tim.sort_values(by=['Distance_Meters'])
                loc_dir_tim_dup_sorted_top5 = loc_dir_tim_dup_sorted[0:7]
                global top_loc_name_dis_time
                top_loc_name_dis_time = loc_dir_tim_dup_sorted_top5[["Tourist_spot","Distance_Meters","Duration_Seconds"]]
                loc_dir_tim_dup_sorted_top5_lat_lon = loc_dir_tim_dup_sorted_top5[["latitude","longitude"]]
                loc_dir_tim_dup_sorted_top5_lat_lon_list = loc_dir_tim_dup_sorted_top5_lat_lon.values.tolist()
                return loc_dir_tim_dup_sorted_top5_lat_lon_list
            
            #Will be used for folium maps
            top_loc_lat_lon = googleapi_resource_extraction()
            data_list = top_loc_name_dis_time.to_dict('records')
            
            #Making a Distance Matrix
            def get_distance_matrix(locations):
                n = len(locations)
                distance_matrix = [[0] * n for i in range(n)]
                for x in range(n):
                    dis_list = link_maker(x)
                    print(f'dis_list for x={x}: {dis_list}')
                    for y in range(n):
                        if x == y:
                            continue
                        elif(x < y):
                            distance_matrix[x][y] = dis_list[y-1]
                        elif(x > y):
                            distance_matrix[x][y] = dis_list[y]
                return distance_matrix

            def link_maker(x):
                link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[x][0]) + '%2C' + str(actual_route_sequence[x][1]) + '&destinations='
                for y in actual_route_sequence[:-1]:
                    if y == actual_route_sequence[x]:
                        continue
                    link_main = link_main + str(y[0]) + '%2C' + str(y[1]) + '%7C'
                link_main = link_main + str(actual_route_sequence[-1][0]) + '%2C' + str(actual_route_sequence[-1][1])
                link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                
                payload={}
                headers = {}

                response = requests.request("GET", link_main, headers=headers, data=payload)
                json_content = response.json()
                
                dis_list = []
                for i in range(len(json_content['rows'][0]['elements'])):
                    distance = json_content['rows'][0]['elements'][i]['distance']['value']
                    dis_list.append(distance)
                
                return dis_list

            actual_route_sequence = []
            actual_route_sequence.append(current_location)
            for x in top_loc_lat_lon:
                actual_route_sequence.append(x)
            print(actual_route_sequence)
            distance_matrix = get_distance_matrix(actual_route_sequence)

            #Calculating Total Distance in Algorithm
            def total_distance_required(actual_route_sequence,algoritm_sequence):
                total_distance = 0
                for x in range(len(algoritm_sequence)-1):
                    link_main = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(actual_route_sequence[algoritm_sequence[x]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x]][1]) + '&destinations='
                    link_main = link_main + str(actual_route_sequence[algoritm_sequence[x+1]][0]) + '%2C' + str(actual_route_sequence[algoritm_sequence[x+1]][1])
                    link_main = link_main + '&key=' + 'AIzaSyDyF68-OxQ439I_Mg9yWVi0OhXfTpoTra4'
                    
                    #Intilizing GoogleAPI parameters
                    url = link_main
                    payload = {}
                    headers = {}

                    #Calling GoogleAPI
                    response = requests.request("GET", url, headers=headers, data=payload)
                    json_content = response.json()
                    
                    #Calculating the distance
                    distance = json_content['rows'][0]['elements'][0]['distance']['value']
                    total_distance = total_distance + distance
                return total_distance
            
            #Tabu Search Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def get_neighborhood(route):
                neighborhood = []
                for i in range(1, len(route)-1):
                    for j in range(i+1, len(route)):
                        new_route = route.copy()
                        new_route[i:j] = reversed(new_route[i:j])
                        neighborhood.append(new_route)
                return neighborhood

            def get_best_neighbor(neighbors, distance_matrix, tabu_list):
                best_neighbor = None
                best_distance = None
                for neighbor in neighbors:
                    if neighbor not in tabu_list:
                        distance = route_distance(neighbor, distance_matrix)
                        if best_distance is None or distance < best_distance:
                            best_neighbor = neighbor
                            best_distance = distance
                return best_neighbor, best_distance

            def tabu_search(locations, distance_matrix, starting_point=0, tabu_size=15, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                tabu_list = []
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution
                for i in range(max_iterations):
                    neighborhood = get_neighborhood(current_solution)
                    best_neighbor, best_distance = get_best_neighbor(neighborhood, distance_matrix, tabu_list)
                    if best_neighbor is None:
                        break
                    current_solution = best_neighbor
                    if best_distance < route_distance(best_solution, distance_matrix):
                        best_solution = best_neighbor
                    tabu_list.append(best_neighbor)
                    if len(tabu_list) > tabu_size:
                        tabu_list.pop(0)
                return best_solution
            
            ##Tabu Search Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            tabu_route = tabu_search(actual_route_sequence, distance_matrix)
            print(tabu_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            tabu_total_time = end_time - start_time

            print("Total time elapsed:", tabu_total_time, "seconds")

            tabu_distance = total_distance_required(actual_route_sequence,tabu_route)

            print("Total distance: ", tabu_distance, "meters")

            #Genetic Algorithm with Google API
            def route_distance(route, distance_matrix):
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def generate_random_route(n, starting_point):
                route = list(range(n))
                route.remove(starting_point)
                random.shuffle(route)
                route.insert(0, starting_point)
                return route

            def crossover(parent1, parent2):
                crossover_point1 = random.randint(1, len(parent1)-2)
                crossover_point2 = random.randint(crossover_point1+1, len(parent1)-1)
                child = parent1.copy()
                for i in range(crossover_point1, crossover_point2):
                    if parent2[i] not in child:
                        for j in range(len(child)):
                            if child[j] == parent2[i]:
                                child[j] = child[i]
                                child[i] = parent2[i]
                                break
                return child

            def mutation(route):
                mutation_point1 = random.randint(1, len(route)-2)
                mutation_point2 = random.randint(1, len(route)-2)
                route[mutation_point1], route[mutation_point2] = route[mutation_point2], route[mutation_point1]
                return route

            def genetic_algorithm(locations, distance_matrix, starting_point=0, population_size=50, max_iterations=1000):
                random.seed(0)
                n = len(locations)
                population = [generate_random_route(n, starting_point) for i in range(population_size)]
                best_route = population[0]
                for i in range(max_iterations):
                    fitness_scores = [1/route_distance(route, distance_matrix) for route in population]
                    sorted_population = [x for _, x in sorted(zip(fitness_scores, population), reverse=True)]
                    if route_distance(sorted_population[0], distance_matrix) < route_distance(best_route, distance_matrix):
                        best_route = sorted_population[0]
                    new_population = [sorted_population[0]]
                    for i in range(1, population_size):
                        parent1 = sorted_population[random.randint(0, int(population_size/2))]
                        parent2 = sorted_population[random.randint(0, int(population_size/2))]
                        child = crossover(parent1, parent2)
                        if random.uniform(0, 1) < 0.1:
                            child = mutation(child)
                        new_population.append(child)
                    population = new_population
                return best_route
            
            ##Genetic Algorithm Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            genetic_route = genetic_algorithm(actual_route_sequence, distance_matrix)
            print(genetic_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            genetic_route_total_time = end_time - start_time

            print("Total time elapsed:", genetic_route_total_time, "seconds")

            genetic_distance = total_distance_required(actual_route_sequence,genetic_route)

            print("Total distance: ", genetic_distance, "meters")

            #Simulated Annealing with Google API
            def route_distance(route, distance_matrix):
                # Calculate the total distance of a route
                dist = 0
                for i in range(len(route)-1):
                    dist += distance_matrix[route[i]][route[i+1]]
                return dist

            def simulated_annealing(locations, distance_matrix, starting_point=0, temperature=10000, cooling_factor=0.9995, max_iterations=10000):
                # Initialize the current and best solutions
                n = len(locations)
                current_solution = list(range(n))
                current_solution.remove(starting_point)
                current_solution.insert(0, starting_point)
                best_solution = current_solution

                # Start the simulated annealing algorithm
                for i in range(max_iterations):
                    # Choose a random neighbor by swapping two cities in the route
                    neighbor = current_solution.copy()
                    i = random.randint(1, n-2)
                    j = random.randint(i+1, n-1)
                    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

                    # Calculate the difference in distance between the current and the new solution
                    current_distance = route_distance(current_solution, distance_matrix)
                    neighbor_distance = route_distance(neighbor, distance_matrix)
                    delta = neighbor_distance - current_distance

                    # Accept the new solution if it's better or with a certain probability if it's worse
                    if delta < 0 or random.random() < math.exp(-delta/temperature):
                        current_solution = neighbor
                        if neighbor_distance < route_distance(best_solution, distance_matrix):
                            best_solution = neighbor

                    # Decrease the temperature
                    temperature *= cooling_factor

                return best_solution
            
            ##Simulated Annealing Time Calculation
            # Record start time
            start_time = time.time()

            # Define global variable to track function call count
            call_count = 0

            #Running the Code
            simulated_annealing_route = simulated_annealing(actual_route_sequence, distance_matrix)
            print(simulated_annealing_route)

            # Record end time
            end_time = time.time()

            # Calculate total time elapsed
            simulated_annealing_total_time = end_time - start_time

            print("Total time elapsed:", simulated_annealing_total_time, "seconds")

            simulated_annealing_distance = total_distance_required(actual_route_sequence,simulated_annealing_route)

            print("Total distance: ", simulated_annealing_distance, "meters")

            context = {'TT': tabu_total_time,"TD": tabu_distance,
                       'GT': genetic_route_total_time,"GD": genetic_distance,
                       'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
                       'TLNDT': data_list}
            user_output = Jaipur_User_Output.objects.get(username=Username_current)
            user_output.current_location = current_location
            user_output.tabu_total_time = tabu_total_time
            user_output.tabu_distance = tabu_distance
            user_output.genetic_route_total_time =genetic_route_total_time
            user_output.genetic_distance = genetic_distance
            user_output.simulated_annealing_total_time = simulated_annealing_total_time
            user_output.simulated_annealing_distance = simulated_annealing_distance
            user_output.top_loc_name_dis_time = data_list
            user_output.tabu_route = tabu_route
            user_output.genetic_route = genetic_route
            user_output.simulated_annealing_route = simulated_annealing_route
            user_output.all_lat_lon = actual_route_sequence
            user_output.save()

            return redirect('jaipur_show')   

        elif request.POST.get('action') == 'button1':
            categories_order_list = request.POST.getlist('category_boxes')
            print(categories_order_list)
            Username_current = request.user.username
            user_categories_object = User_Categories.objects.get(username=Username_current)
            user_categories_object.jaipur_categories = categories_order_list
            user_categories_object.save()
            user_categories = user_categories_object.jaipur_categories
            # print(user_categories)

            jaipur_data_categories = []
            for x in Jaipur.objects.all().values():
                jaipur_data_categories.append(x.get("Categories"))
            # print(mumbai_data_categories)

            filtered_categories = []

            i=0
            for cat in jaipur_data_categories:
                i = i+1
                found = False
                for req in user_categories:
                    if req in cat:
                        City_Location_Name = Jaipur.objects.get(id=i)
                        filtered_categories.append(City_Location_Name.Tourist_spot)
                        found = True
                        break
                if not found:
                    filtered_categories.append("Null")
            print(filtered_categories)

            user_categories_object.jaipur_all_spots = filtered_categories
            user_categories_object.save()

        elif request.POST.get('action') == 'button3':
            return redirect('jaipur_show') 

    jaipur_data = []
    for x in Jaipur.objects.all().values():
        jaipur_data.append(x)

    categories_list = []
    for x in All_Categories_Jaipur.objects.all().values():
        categories_list.append(x)
    
    context = {'categories': categories_list,"jaipur_try": jaipur_data}

    return render(request, 'jaipur.html', context)

def jaipur_show(request):
    Username_current = request.user.username
    user_output = Jaipur_User_Output.objects.get(username=Username_current)
    current_location = user_output.current_location
    tabu_total_time = user_output.tabu_total_time
    tabu_distance = user_output.tabu_distance
    genetic_route_total_time = user_output.genetic_route_total_time
    genetic_distance = user_output.genetic_distance
    simulated_annealing_total_time = user_output.simulated_annealing_total_time
    simulated_annealing_distance = user_output.simulated_annealing_distance
    top_loc_name_dis_time = user_output.top_loc_name_dis_time
    top_loc_name_dis_time = ast.literal_eval(top_loc_name_dis_time)
    tabu_route = user_output.tabu_route
    tabu_route = ast.literal_eval(tabu_route)
    genetic_route = user_output.genetic_route
    genetic_route = ast.literal_eval(genetic_route)
    simulated_annealing_route = user_output.simulated_annealing_route
    simulated_annealing_route = ast.literal_eval(simulated_annealing_route)
    all_lat_lon = user_output.all_lat_lon
    all_lat_lon = ast.literal_eval(all_lat_lon)
    if tabu_distance <= genetic_distance and tabu_distance <= simulated_annealing_distance:
        best_route = tabu_route
    elif genetic_distance <= simulated_annealing_distance:
        best_route = genetic_route
    else:
        best_route = simulated_annealing_route
        
    # Print the text version of the best route
    print("The best route to visit the tourist spots is as follows:")
    locations = [top_loc_name_dis_time[i-1]['Tourist_spot'] for i in best_route[1:]]
    route_text = f"Starting from your current location, visit {', '.join(locations[:-1])}, and {locations[-1]}."
    print(route_text)

    print(top_loc_name_dis_time)
    
    
    # m = folium.Map(location=[19.0760, 72.8777], zoom_start=12)

    tourist_spots = []
    tourist_spots.append

    # add markers for each tourist spot
    for spot in top_loc_name_dis_time:
        tourist_spot = spot['Tourist_spot']
        jaipur_spot = Jaipur.objects.get(Tourist_spot=tourist_spot)
        print(jaipur_spot)
        lat = jaipur_spot.latitude
        lon = jaipur_spot.longitude
        tourist_spots.append({'name': tourist_spot, 'latitude':  lat , 'longitude': lon})
    
    print(tourist_spots)

    # Create a map centered at Mumbai
    current_location = ast.literal_eval(current_location)
    map = folium.Map(location=current_location, zoom_start=14)
    folium.Marker(location=[current_location[0], current_location[1]], icon=folium.Icon(color='pink')).add_to(map)

    # Add markers for each tourist spot
    for spot in tourist_spots:
        folium.Marker(location=[spot["latitude"], spot["longitude"]], popup=spot["name"], icon=folium.Icon(color='purple')).add_to(map)
    
    # Convert the map to HTML and pass it to the template
    map_html = map._repr_html_()
    
    context = {'TT': tabu_total_time,"TD": tabu_distance,
               'GT': genetic_route_total_time,"GD": genetic_distance,
               'ST': simulated_annealing_total_time,"SD": simulated_annealing_distance,
               'TLNDT': top_loc_name_dis_time, 
               'TR': tabu_route,
               'GR' : genetic_route,
               'SAR' : simulated_annealing_route,
               'BR' : best_route,
               'CL' : route_text,
               'MAPS' : map_html}
    
    if request.POST.get('action') == 'button':
        link_maker = "https://www.google.com/maps/dir/?api=1&origin=" + all_lat_lon[0][0] + "," + all_lat_lon[0][1] + "&waypoints="
        link_maker = link_maker + str(all_lat_lon[1][0]) + "," + str(all_lat_lon[1][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[2][0]) + "," + str(all_lat_lon[2][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[3][0]) + "," + str(all_lat_lon[3][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[4][0]) + "," + str(all_lat_lon[4][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[5][0]) + "," + str(all_lat_lon[7][1]) + "|"
        link_maker = link_maker + str(all_lat_lon[6][0]) + "," + str(all_lat_lon[6][1]) + "|"
        link_maker = link_maker + "&destination=" + str(all_lat_lon[7][0]) + "," + str(all_lat_lon[7][1])

        print(link_maker)
        return redirect(link_maker)
    
    return render(request, 'jaipur_show.html', context)