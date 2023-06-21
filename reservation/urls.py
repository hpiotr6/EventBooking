from django.urls import path
from . import views


urlpatterns = [
    path('hello/', views.say_hello),
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),
    path('create-team/', views.createTeam, name="create-team"),
    path('join-team/', views.joinTeam, name="join-team"),
    path('update-user', views.updateUser, name="update-user"),
    path('create-event/', views.createEvent, name="create-event"),
    path('join-event/<str:pk>/', views.joinEvent, name="join-event"),
    path('search-event/', views.searchEvents, name="search-event"),
    path('stats/', views.stats, name="stats")
]