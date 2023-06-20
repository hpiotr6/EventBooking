from django.shortcuts import render
from django.http import HttpResponse
from .models import Reservation
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import User, Event
from .forms import UserForm, MyUserCreationForm

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

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    events = Event.objects.filter(sport_type__icontains=q)
    # events = Event.objects.all()

    context = {'rooms': rooms, "events": events}

    return render(request, "reservation/home.html", context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id']== int(pk):
            room = i
    context = {'room': room}
    return render(request, "reservation/room.html", context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'reservation/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'reservation/login_register.html', {'form': form})
