from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
import json
from .logger import audit_logger
from django.views.decorators.csrf import csrf_exempt
from .models import RecommendationScheme, Music
from .forms import RecommendationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import RecommendPlaylist, RecommendSongYear
import pandas as pd
from django.conf import settings
from decouple import config
import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials





@csrf_exempt
@api_view(['POST'])
def recommend_playlist(request):
    if request.method == 'POST':
        song_df = pd.read_csv(settings.CSV_FILE_PATH)
        complete_feature_set = pd.read_csv(settings.COMPLETE_PATH)
        json_data = json.loads(request.body.decode('utf-8'))
        # Get URL from request data
        URL = json_data.get('URL', '')
        n_songs = int(json_data.get('n_songs', 10))  # Default to 10 recommendations if not provided
        
        if URL is None or URL == '':
            return JsonResponse({'error': 'Please enter the spotify playlist URL'}, status=400)
        
        # Use extract function to get features dataframe
        df = RecommendPlaylist().extract(URL)
        
        # Retrieve recommendations
        recommends = RecommendPlaylist().recommend_using_playlist(song_df, complete_feature_set, df, n_songs)


        my_songs = []
        for i in range(n_songs):
            my_songs.append({'name': str(recommends.iloc[i,4]), 'artist': str(recommends.iloc[i,1]), 'spotify_link': "https://open.spotify.com/track/"+ str(recommends.iloc[i,-6]).split("/")[-1]})
        
        audit_logger.info(f"Recommended Songs: {my_songs}")
        # Return recommendations as JSON response    
        return Response(my_songs)

    

@csrf_exempt
@api_view(['POST'])
def recommend_song(request):
    
    if request.method == 'POST':
        # songs = request.POST.get('songs')
        
        json_data = json.loads(request.body)

        # Extract the 'songs' field from the JSON data
        songs = json_data.get('songs')
        artist = json_data.get('artist', '')
        year = json_data.get('year', '')
        n_songs = json_data.get('n_songs', 10) #Default to 10 recommendations if not provided
          
        recommendation = RecommendSongYear().recommend_songs(songs, artist, year, n_songs)
    
        if recommendation == None:
            return JsonResponse({'error': 'Enter artist name and release year'}, status=500)
        elif len(recommendation) > 0:
            return Response({'songs': recommendation})
        else:
            return HttpResponseServerError

    



@csrf_exempt
@api_view(['GET'])
def search_from_spotify(request):
    song_name = request.query_params.get("search")
    client_id = config('client_id')
    client_secret = config('client_secret')

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    result = sp.search(q=song_name, type='track', limit=10)

    response_data = []
    for track in result['tracks']['items']:
        response_data.append({
            'name': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'year': track['album']['release_date'][:4],
            'image_link': track['album']['images'][0]['url']
        })

    return Response({'songs': response_data})