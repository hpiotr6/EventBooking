from django.shortcuts import render
from django.http import HttpResponse
from .models import Reservation
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from .models import User, Event, Single, Group, Casual, Competitive, Pitch, Facility, City, Team, Affiliation, SportType
from .forms import UserForm, MyUserCreationForm, TeamCreationForm, AffiliationForm,UpdateUserForm, SingleForm
from collections import Counter

# Create your views here.

rooms = [
    {'id': 1, 'name': 'Create event'},
    {'id': 2, 'name': 'Join Event'},
    {'id': 3, 'name': 'Login'},
    {'id': 4, 'name': 'Sport Facilities'},
]

week_days = {
    "mon": "Monday",
    "tue": "Tuesday",
    "wed": "Wednesday",
    "thu": "Thursday",
    "fri": "Friday",
    "sat": "Saturday",
    "sun": "Sunday"
}

def say_hello(request):
    return HttpResponse("Hello World")

def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # events = Event.objects.filter(sport_type_sport_type__icontains=q)
    events = Event.objects.all()
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
    
    single = Single.objects.filter(user_user_id=pk)
    events = Event.objects.filter(casual__event_id__in=single.values_list("event_id"))
    affiliations = Affiliation.objects.filter(user_user=pk)
    teams = Team.objects.filter(team_id__in=affiliations.values_list("team_team_id"))
    # events = Event.objects.filter(
    #     Q(casual__event_id__in=)
    # )
    # room_messages = user.message_set.all()
    # topics = Topic.objects.all()
    context = {"user":user, "events":events, "teams":teams}
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
    pk = request.user.user_id
    affiliations = Affiliation.objects.filter(user_user=pk)
    teams_without_user = Team.objects.exclude(team_id__in=affiliations.values_list("team_team_id"))

    if request.method == 'POST':
        form = AffiliationForm(request.POST, pk=pk, teams_queryset=teams_without_user)
        if form.is_valid():
            affiliation = form.save(commit=False)
            affiliation.user_user = request.user
            affiliation.save()
            return redirect('home')
    else:
        form = AffiliationForm(pk=pk, teams_queryset=teams_without_user)

    context = {'form': form}
    return render(request, 'reservation/join-team.html', context)

def createEvent(request):
    path = "reservation/create_event.html"

    context = {"week_days": week_days}

    pitches = list(Pitch.objects.all())

    sport_types = SportType.objects.all()

    print(Pitch.objects.all())
    
    pitch_list = []


    for p in pitches:
        facility = p.facility_facility
        city = facility.city_city
        p_type = p.pitch_type_pitch_type
        l = "{}.{}, {}, {}".format(p_type.name, p.pitch_id, city.name, facility.address)
        pitch_list.append(l)

    context["pitch_list"] = pitch_list
    context["sport_types"] = sport_types

    try:
        if request.method == "POST":
            post_req = request.POST.dict()
            print(post_req)

            new_event = Event()
            new_event.name = post_req["name"]
            sport_type_obj = SportType.objects.get_or_create(sport_type_name=post_req["sport"])[0]
            new_event.sport_type_sport_type = sport_type_obj
            new_event.status = "open"
            new_event.pitch_pitch = pitches[int(post_req["facility"]) - 1]
            new_event.city_name = new_event.pitch_pitch.facility_facility.city_city.name
            new_event.city_province = new_event.pitch_pitch.facility_facility.city_city.province
            new_event.pitch_capacity = new_event.pitch_pitch.capacity
            new_event.date = post_req["event_date"]
            new_event.hour = post_req["hour"]
            
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
    except:
        messages.error(request, 'Bad input data in one or more fields')

    return render(request, path, context)

@login_required(login_url='login')
def joinEvent(request):
    pk = request.user.user_id
    user = User.objects.get(user_id=pk)
    # casual_events = Casual.objects.exclude()
    events = Event.objects.exclude(casual__event_id=pk)
    context = {'events':events}
    # if request.method == 'POST':
    #     post_req = request.POST.dict()
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')

    return render(request, 'reservation/join-event.html', context)

def stats(request):
    context = {}



    city_names = Event.objects.values_list('city_name', flat=True)
    city_counts = Counter(city_names)
    tcp = min(5, len(city_names))

    top_cities = city_counts.most_common(tcp)

    context["top_cities"] = top_cities

    #facilities
    facilities = Facility.objects.annotate(event_count=Count('pitch__event'))
    fac_cnt = Facility.objects.count()
    n = min(fac_cnt, 5)

    sorted_facilities = sorted(facilities, key=lambda x: x.event_count, reverse=True)

    print(sorted_facilities)

    top_facilities = sorted_facilities[:n]
    context["facilities"] = top_facilities

    #sports
    unique_sport_types = Event.objects.values_list('sport_type', flat=True).distinct()

    sums_list = []

    for sport_type in unique_sport_types:
        casual_sum = Casual.objects.filter(event__sport_type=sport_type).aggregate(sum_users=Sum('num_users'))['sum_users']
        competitive_sum = Competitive.objects.filter(event__sport_type=sport_type).aggregate(sum_teams=Sum('num_teams'))['sum_teams']
        total_sum = int(casual_sum or 0) + int(competitive_sum or 0)

        if total_sum:
            sums_list.append((sport_type, total_sum))

    sorted_sums_list = sorted(sums_list, key=lambda x: x[1], reverse=True)
    lsn = min(len(sums_list), 5)
    top_sport_types = sorted_sums_list[:lsn]

    context["sport_types"] = top_sport_types

    return render(request, 'reservation/stats.html', context)
