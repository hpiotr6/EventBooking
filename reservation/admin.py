from django.contrib import admin
from .models import Event, PeriodicEvent, Competitive, Casual, Group, Single
from .models import Team, Affiliation, Frequency
from .models import City, PitchType, Pitch, AmenityCategory, Facility, GearType, SportGear
from .models import Permission, Reservation, SportType, WeekDay
# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import User



# admin.site.register(UserAdmin)
admin.site.register(User)
admin.site.register(Event)
admin.site.register(PeriodicEvent)
admin.site.register(Competitive)
admin.site.register(Casual)
admin.site.register(Group)
admin.site.register(Single)
admin.site.register(Team)
admin.site.register(Affiliation)
admin.site.register(City)
admin.site.register(PitchType)
admin.site.register(Pitch)
admin.site.register(AmenityCategory)
admin.site.register(Facility)
admin.site.register(GearType)
admin.site.register(SportGear)
admin.site.register(Permission)
admin.site.register(Reservation)
admin.site.register(SportType)
admin.site.register(WeekDay)
admin.site.register(Frequency)
