from django.shortcuts import render

def home(request):
	return render(request, 'home.html', {})

def contact(request):
	return render(request, 'contact.html', {})

def about(request):
	return render(request, 'about.html', {})

def booking(request):
	return render(request, 'booking.html', {})

def room(request):
	return render(request, 'room.html', {})

def service(request):
	return render(request, 'service.html', {})

def team(request):
	return render(request, 'team.html', {})

def testimonial(request):
	return render(request, 'testimonial.html', {})