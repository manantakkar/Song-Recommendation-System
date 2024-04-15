from django.urls import path
from .views import *

urlpatterns = [
    path('recommend-playlist/', recommend_playlist, name='recommend-playlist'),
    path('recommend-song/', recommend_song, name='recommend-song'),
    path('search/', search_from_spotify, name='search'),
]
