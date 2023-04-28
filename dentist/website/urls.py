from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact.html', views.contact, name="contact"),
    path('about.html', views.about, name="about"),
    path('signin.html', views.signin, name='signin'),
    path('signup.html', views.signup, name='signup'),
    path('cities.html', views.cities, name='cities'),
    path('signout', views.signout, name="signout"),
    path('mumbai.html', views.mumbai, name="signout")
    # path('team.html', views.team, name='team'),
    # path('testimonial.html', views.testimonial, name='testimonial')
]