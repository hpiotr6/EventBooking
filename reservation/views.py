from django.shortcuts import render
from django.http import HttpResponse
from .models import Reservation
# Create your views here.

rooms = [
    {'id': 1, 'name': 'Create event'},
    {'id': 2, 'name': 'Join Event'},
    {'id': 3, 'name': 'Login'},
    {'id': 4, 'name': 'Sport Facilities'},
]

def say_hello(request):
    return HttpResponse("Hello World")

def home(request):
    context = {'rooms': rooms}
    return render(request, "reservation/home.html", context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id']== int(pk):
            room = i
    context = {'room': room}
    return render(request, "reservation/room.html", context)
