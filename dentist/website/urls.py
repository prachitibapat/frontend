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
    path('mumbai.html', views.mumbai, name="mumbai"),
    path('mumbai_show.html', views.mumbai_show, name="mumbai_show"),
    path('delhi.html', views.delhi, name="delhi"),
    path('delhi_show.html', views.delhi_show, name="delhi_show"),
    path('kolkata.html', views.kolkata, name="kolkata"),
    path('kolkata_show.html', views.kolkata_show, name="kolkata_show"),
    path('jaipur.html', views.jaipur, name="jaipur"),
    path('jaipur_show.html', views.jaipur_show, name="jaipur_show"),
    path('chennai.html', views.chennai, name="chennai"),
    path('chennai_show.html', views.chennai_show, name="chennai_show"),
]

