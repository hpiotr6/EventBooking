# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from .managers import CustomUserManager
from .managers import UserManager


class Permission(models.Model):
    permission_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'permission'



class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'user'

# class User(models.Model):
#     # age = models.IntegerField(null=True, blank=True)
#     # nickname = models.CharField(max_length=100, null=True, blank=True)
#     user_id = models.AutoField(primary_key=True)
#     password = models.CharField(max_length=30)
#     name = models.CharField(max_length=30)
#     surname = models.CharField(max_length=30)
#     date_of_birth = models.DateField()
#     email = models.EmailField(unique=True, null=True)
#     permission_permission = models.ForeignKey(Permission, models.DO_NOTHING)

#     # USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['name']

#     # # objects = CustomUserManager()
#     # objects = UserManager()

#     class Meta:
#         managed = False
#         db_table = 'user'


class Affiliation(models.Model):
    user_user = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    team_team = models.ForeignKey('Team', models.DO_NOTHING)
    # team_event_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'affiliation'
        unique_together = (('user_user', 'team_team'),)


class AmenityCategory(models.Model):
    amenity_cat_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    facility_facility = models.ForeignKey('Facility', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amenity_category'


class Casual(models.Model):
    event = models.OneToOneField('Event', models.DO_NOTHING, primary_key=True)
    num_users = models.IntegerField()
    pitch_capacity = models.IntegerField()
    places_available = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'casual'


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    province = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'city'


class Competitive(models.Model):
    event = models.OneToOneField('Event', models.DO_NOTHING, primary_key=True)
    num_teams = models.IntegerField()
    max_num_teams = models.IntegerField()
    teams_available = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'competitive'


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    sport_type = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    pitch_pitch = models.ForeignKey('Pitch', models.DO_NOTHING)
    # calendar_entry_calendar_entry_id = models.IntegerField(unique=True)
    pitch_capacity = models.IntegerField()
    city_name = models.CharField(max_length=30)
    city_province = models.CharField(max_length=30)
    periodic_event_periodic_event_id = models.IntegerField(blank=True, null=True)
    periodic_eventv1_periodic_event = models.ForeignKey('PeriodicEvent', models.CASCADE, blank=True, null=True)
    date = models.DateField()
    hour = models.TimeField()
    # datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'event'


class Facility(models.Model):
    facility_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=20)
    city_city = models.OneToOneField(City, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'facility'


class Frequency(models.Model):
    frequency_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'frequency'


class GearType(models.Model):
    gear_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'gear_type'


class Group(models.Model):
    user_id = models.IntegerField(primary_key=True)
    event = models.ForeignKey('Reservation', models.DO_NOTHING)
    competitive_event = models.ForeignKey(Competitive, models.DO_NOTHING)
    team_team = models.ForeignKey('Team', models.DO_NOTHING)
    # team_event_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'group'
        unique_together = (('user_id', 'event'), ('competitive_event', 'team_team'),)


class PeriodicEvent(models.Model):
    periodic_event_id = models.AutoField(primary_key=True)
    frequency_frequency = models.OneToOneField(Frequency, models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'periodic_event'



class Pitch(models.Model):
    pitch_id = models.AutoField(primary_key=True)
    capacity = models.IntegerField()
    pitch_type_pitch_type = models.ForeignKey('PitchType', models.DO_NOTHING)
    facility_facility = models.ForeignKey(Facility, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pitch'


class PitchType(models.Model):
    pitch_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'pitch_type'


class Reservation(models.Model):
    event_id = models.IntegerField(primary_key=True)
    pay_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'reservation'


class Single(models.Model):
    event = models.OneToOneField(Reservation, models.DO_NOTHING, primary_key=True)
    casual_event = models.ForeignKey(Casual, models.DO_NOTHING)
    user_user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'single'
        unique_together = (('casual_event', 'user_user'),)


class SportGear(models.Model):
    sport_gear_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    facility_facility = models.ForeignKey(Facility, models.DO_NOTHING)
    gear_type_gear_type = models.ForeignKey(GearType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sport_gear'


class SportType(models.Model):
    sport_type_id = models.IntegerField(primary_key=True)
    sport_type_name = models.CharField(max_length=100)
    # event_event = models.ForeignKey(Event, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sport_type'


class StatCity(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    quantity = models.IntegerField()
    city_city = models.ForeignKey(City, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stat_city'


class StatSportType(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    quantity = models.IntegerField(blank=True, null=True)
    sport_type_sport_type = models.ForeignKey(SportType, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stat_sport_type'


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'team'
        unique_together = (('team_id'),)


class WeekDay(models.Model):
    week_day_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    periodic_event_periodic_event = models.ForeignKey(PeriodicEvent, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'week_day'
