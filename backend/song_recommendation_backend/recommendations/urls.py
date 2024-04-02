from django.urls import path
from .views import recommend_artist, recommend_playlist

urlpatterns = [
    path('recommend_artist/', recommend_artist, name='recommend_artist'),
    path('recommend_playlist/', recommend_playlist, name='recommend_playlist')
]
