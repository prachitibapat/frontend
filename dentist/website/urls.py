from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact.html', views.contact, name="contact"),
    path('about.html', views.about, name="about"),
    path('booking.html', views.booking, name='booking'),
    path('room.html', views.room, name='room'),
    path('service.html', views.service, name='service'),
    path('team.html', views.team, name='team'),
    path('testimonial.html', views.testimonial, name='testimonial')
]