from django.shortcuts import render
from django.http import HttpResponse
from .models import Reservation
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from .models import User, Event, Single, Group, Casual, Competitive, Pitch, Facility, City, Team, Affiliation, SportType, Frequency, PeriodicEvent
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

offsets = {
    "1": 0,
    "2": 7,
    "3": 21
}

def say_hello(request):
    return HttpResponse("Hello World")

def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    sport_types = SportType.objects.all()
    events = Event.objects.filter(sport_type_sport_type__sport_type_name__icontains=q)
    # events = Event.objects.all()
    user = request.user
    # events = Event.objects.all()

    context = {'rooms': rooms, "events": events, "user": user, "sport_types":sport_types}

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


    if request.method == "POST":
        post_req = request.POST.dict()
        print(post_req)

        dates = []
        is_cont = "event_type" not in post_req.keys()
        cont = None

        if is_cont:
            print(post_req["event_date"], post_req["end_date"])

            vals = []

            for i, k in enumerate(week_days.keys()):
                if k in post_req.keys():
                    vals.append(i)

            start_date = datetime.strptime(post_req["event_date"], "%Y-%m-%d")
            end_date = datetime.strptime(post_req["end_date"], "%Y-%m-%d")

            curr_date = start_date
            off = offsets[post_req["frequency"]]

            print(vals, off, curr_date <= end_date)
            print(curr_date.weekday())
            while curr_date <= end_date:
                
                if curr_date.weekday() in vals:
                    dates.append(curr_date)
                if curr_date.weekday() == 6:
                    curr_date += timedelta(days=off)
                

                curr_date += timedelta(days=1)
            
            cont = PeriodicEvent()
            cont.start_date = post_req["event_date"]
            cont.end_date = post_req["end_date"]
            cont.frequency_frequency = Frequency.objects.get(pk=int(post_req["frequency"]))
            cont.save()
        else:
            dates.append(post_req["event_date"])
        
        print(dates)


        for d in dates:
            new_event = Event()
            new_event.name = post_req["name"]
            sport_type_obj = SportType.objects.get_or_create(sport_type_name=post_req["sport"])[0]
            new_event.sport_type_sport_type = sport_type_obj
            new_event.status = "open"
            new_event.pitch_pitch = pitches[int(post_req["facility"]) - 1]
            new_event.city_name = new_event.pitch_pitch.facility_facility.city_city.name
            new_event.city_province = new_event.pitch_pitch.facility_facility.city_city.province
            new_event.pitch_capacity = new_event.pitch_pitch.capacity
            new_event.date = d
            new_event.hour = post_req["hour"]

            if cont:
                new_event.periodic_eventv1_periodic_event = cont

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
                
    # except Exception as e:
    #     print(e)
    #     messages.error(request, 'Bad input data in one or more fields')

    return render(request, path, context)

@login_required(login_url='login')
def joinEvent(request, pk):
    event = Event.objects.get(event_id=pk)
    casual_event = Casual.objects.get(event__event_id=pk)
    single_count = Single.objects.filter(event_id=pk).count()
    user = User.objects.get(user_id=request.user.user_id)
    context = {'event':event, 'casual_event':casual_event, "single_count":single_count}

    if request.method == "POST":
        
        reservation = Reservation()
        reservation.event_id = event.event_id
        reservation.save()
        single_reservation = Single()
        single_reservation.casual_event = casual_event
        single_reservation.event = reservation
        single_reservation.user_user = user
        single_reservation.save()
        return redirect('user-profile', pk=user.user_id)

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
    # unique_sport_types = Event.objects.values_list('sport_type').distinct()
    unique_sport_types = SportType.objects.values_list('sport_type_name', flat=True).distinct()
    sums_list = []

    for sport_type in unique_sport_types:
        casual_sum = Casual.objects.filter(event__sport_type_sport_type__sport_type_name=sport_type).aggregate(total_num_users=Sum('num_users'))
        competitive_sum = Competitive.objects.filter(event__sport_type_sport_type__sport_type_name=sport_type).aggregate(sum_teams=Sum('num_teams'))
        print(casual_sum, competitive_sum)
        total_sum = int(casual_sum["total_num_users"] or 0) + int(competitive_sum["sum_teams"] or 0)

        if total_sum:
            sums_list.append((sport_type, total_sum))

    sorted_sums_list = sorted(sums_list, key=lambda x: x[1], reverse=True)
    lsn = min(len(sums_list), 5)
    top_sport_types = sorted_sums_list[:lsn]

    context["sport_types"] = top_sport_types

    return render(request, 'reservation/stats.html', context)

def searchEvents(request):
    sport_types = SportType.objects.all()
    cities = City.objects.all()
    if request.method == 'GET':
        sport_type = request.GET.get('sport_type', '')
        city_name = request.GET.get('city_name', '')
        event_name = request.GET.get('event_name', '')


        # Filter events based on the search parameters
        # events = Event.objects.filter(Q(city_name__icontains=city_name))
        events = Event.objects.filter(Q(sport_type_sport_type__sport_type_name__icontains=sport_type) & 
                                      Q(city_name__icontains=city_name) & 
                                      Q(name__icontains=event_name))
        # events = Event.objects.all()
        context = {
            'events': events,
            "sport_types":sport_types,
            "cities": cities
        }
        return render(request, 'reservation/search-events.html', context)

    return render(request, 'reservation/search-events.html')
