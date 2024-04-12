from django.urls import path
from .views import *

urlpatterns = [
    path('recommend-artist/', recommend_artist, name='recommend-artist'),
    path('recommend-playlist/', recommend_playlist, name='recommend-playlist'),
    path('recommend-song/', recommend_song, name='recommend-song'),

    path('search/', search_from_dataset, name='search'),
    path('', trending_songs, name='trending_songs'),
    
]
