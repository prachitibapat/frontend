from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from website.models import All_Categories_Mumbai, Mumbai

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def home(request):
    return render(request, 'home.html')


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
            fname = user.first_name
            return render(request, "home.html", {"fname": fname})
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
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 characters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

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

def mumbai(request):
    if request.method == "POST":
        
        options = ChromeOptions()
        options.add_argument("--use--fake-ui-for-media-stream")
        driver = Chrome(options=options)
        timeout = 20
        driver.get("https://whatmylocation.com/")
        wait = WebDriverWait(driver, timeout)
        time.sleep(3)
        current_longitude = driver.find_element(By.ID, "longitude").text
        current_latitude = driver.find_element(By.ID, "latitude").text
        current_location = current_location = [current_latitude,current_longitude]
        driver.quit()
    
    mumbai_data = []
    for x in Mumbai.objects.all().values():
        mumbai_data.append(x)

    categories_list = []
    for x in All_Categories_Mumbai.objects.all().values():
        categories_list.append(x)
    context = {'categories': categories_list,"mumbai_try":mumbai_data}

    return render(request, 'mumbai.html', context)