from django.shortcuts import render
from django.http import HttpResponse
from .models import Reservation
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import User, Event, Single, Group, Casual, Competitive, Team, Pitch
from .forms import UserForm, MyUserCreationForm, TeamCreationForm, AffiliationForm,UpdateUserForm

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
    user = request.user
    # events = Event.objects.all()

    context = {'rooms': rooms, "events": events, "user": user}

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


def userProfile(request, pk):
    user = User.objects.get(user_id=pk)
    
    single_events = Single.objects.filter(user_user_id=pk)
    events = Event.objects.filter(casual__event_id__in=single_events.values_list("event_id"))
    # events = Event.objects.filter(
    #     Q(casual__event_id__in=)
    # )
    # room_messages = user.message_set.all()
    # topics = Topic.objects.all()
    context = {"user":user, "events":events}
    return render(request, 'reservation/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    # user_form = UpdateUserForm(request.POST, instance=request.user)
    context = {"user":user, "form":form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.user_id)

    return render(request, 'reservation/update-user.html', context)

@login_required(login_url='login')
def createTeam(request):

    form = TeamCreationForm()
    context = {'form':form}
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'reservation/create-team.html', context)

@login_required(login_url='login')
def joinTeam(request):

    form = AffiliationForm(initial={'user_user': request.user.user_id})
    context = {'form':form}
    if request.method == 'POST':
        form = AffiliationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'reservation/join-team.html', context)

def createEvent(request):
    path = "reservation/create_event.html"

    context = {}

    pitches = list(Pitch.objects.all())

    print(Pitch.objects.all())
    
    pitch_list = []

    for p in pitches:
        facility = p.facility_facility
        city = facility.city_city
        p_type = p.pitch_type_pitch_type
        l = "{}.{}, {}, {}".format(p_type.name, p.pitch_id, city.name, facility.address)
        pitch_list.append(l)

    context["pitch_list"] = pitch_list

    print(pitch_list)

    if request.method == "POST":
        post_req = request.POST.dict()
        print(post_req)

        new_event = Event()
        new_event.name = post_req["name"]
        new_event.sport_type = post_req["sport"]
        new_event.status = "open"
        new_event.pitch_pitch = pitches[int(post_req["facility"]) - 1]
        new_event.city_name = new_event.pitch_pitch.facility_facility.city_city.name
        new_event.city_province = new_event.pitch_pitch.facility_facility.city_city.province
        new_event.pitch_capacity = new_event.pitch_pitch.capacity
        new_event.date = post_req["event_date"]

        print(post_req["event_date"])
        
        subclass = None

        if "compet" in post_req.keys():
            subclass = Competitive()
            subclass.num_teams = 0
            subclass.teams_available = post_req["capacity"]
            subclass.max_num_teams = post_req["capacity"]
        else:
            subclass = Casual()
            subclass.num_users = 0
            subclass.pitch_capacity = post_req["capacity"]
            subclass.places_available = post_req["capacity"]

        subclass.event = new_event

        new_event.save()
        subclass.save()




    return render(request, path, context)
