from django.urls import path
from . import views

urlpatterns = [
    path('', views.summoner_view, name='home'),
    path('profile/<str:summoner_puuid>/<str:summoner_gameName>/<str:summoner_tagLine>/', views.profile_view, name='profile'),
]
