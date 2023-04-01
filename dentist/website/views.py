from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'home.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def about(request):
    return render(request, 'about.html', {})


def booking(request):
    return render(request, 'booking.html', {})


def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(
            request, "Your Account has been created succesfully")
        return redirect('home')

    return render(request, 'signup.html', {})


def service(request):
    return render(request, 'service.html', {})


def team(request):
    return render(request, 'team.html', {})


def testimonial(request):
    return render(request, 'testimonial.html', {})
