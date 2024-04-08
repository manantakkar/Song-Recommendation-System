from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from .models import RecommendationScheme, Music
from .forms import RecommendationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import RecommendPlaylist, RecommendSong, RecommendArtist
import pandas as pd
from django.conf import settings
from decouple import config
import requests



    
@csrf_exempt
@api_view(['GET'])
def trending_songs(request):
    
    # Last.fm API endpoint for getting top tracks
    API_KEY = config('last_fm_key')
    endpoint = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={API_KEY}&format=json'

    # Make a GET request to the Last.fm API
    response = requests.get(endpoint)

    
    # Check if the request was successful
    if response.status_code == 200:
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the trending tracks
        trending_tracks = data['tracks']['track']

        # Extract required fields from each track
        trending_songs = []
        for track in trending_tracks:
            song_name = track['name']
            artist_name = track['artist']['name']
            song_url = track['url']
            trending_songs.append({'song_name': song_name, 'artist': artist_name, 'url': song_url})

        return JsonResponse({'trending_songs': trending_songs})
    
    else:
        # If the request was not successful, return an error response
        return JsonResponse({'error': 'Failed to fetch trending tracks'}, status=response.status_code)







@csrf_exempt
@api_view(['POST'])
def recommend_artist(request):
    if request.method == 'POST':
        # Parse JSON data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Extract artist_name, genres, and attrs from the parsed JSON data
        artist_name = data.get('artist_name')
        genres = data.get('genres')

        #Call generate function in RecommendArtist class
        recommendations = RecommendArtist().generate(artist_name, genres)

        # Serialize recommendations and return as JSON response
        # serialized_recommendations = [{'name': r.name, 'link': r.link, 'artist': r.artist, 'image_link': r.image_link} for r in recommendations]
        return JsonResponse({'recommendations': recommendations})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)




@api_view(['POST'])
def recommend_playlist(request):
    if request.method == 'POST':

        songDF = pd.read_csv(settings.CSV_FILE_PATH)
        complete_feature_set = pd.read_csv(settings.COMPLETE_PATH)
        
        # Get URL from request data
        URL = request.data.get('URL')
        
        # Use extract function to get features dataframe
        df = RecommendPlaylist().extract(URL)
        
        # Retrieve recommendations
        edm_top40 = RecommendPlaylist().recommend_from_playlist(songDF, complete_feature_set, df)
    
        number_of_recs = int(request.data.get('number_of_recs', 5))  # Default to 5 recommendations if not provided
        my_songs = []
        for i in range(number_of_recs):
            my_songs.append({'title': str(edm_top40.iloc[i,1]) + ' - '+ '"'+str(edm_top40.iloc[i,4])+'"', 'link': "https://open.spotify.com/track/"+ str(edm_top40.iloc[i,-6]).split("/")[-1]})
        
        # Return recommendations as JSON response    
        return Response({'songs': my_songs})
    


@api_view(['POST'])
def recommend_song(request):
    
    if request.method == 'POST':
        song_list = request.POST.get('songs')
        song_list = json.loads(song_list)
        n_songs = request.POST.get('n_songs', 10) #Default to 10 recommendations if not provided

        spotify_data = pd.read_csv("datasets/data.csv")
        recommendation = RecommendSong().recommend_songs(song_list, n_songs)

        return Response({'songs': recommendation})
    





# import os
# import pickle
# from django.shortcuts import render
# from django.http import HttpResponse

# def load_model_and_data():
#     try: 
#         print(f"YEH::::::::::::::::::::::::::::::::::::::::::::::::::")  
#         # Load the pickled model and data
#         with open('datasets/df.pkl', 'rb') as file:
#             df = pd.read_pickle(file)
#         with open('datasets/similarity.pkl', 'rb') as file:
#             similarity = pd.read_pickle(file)
#         print(f"YEH: {similarity}, {df}")
#         return df, similarity
#     except Exception as e:
#         print(f"ERRR: {str(e)}")

# def recommendation(song_df, df, similarity):
#     # Your recommendation function
#     # This function should return a list of recommended songs
#     # based on the input song
#     idx = df[df['song'] == song_df].index[0]
#     distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
#     recommended_songs = [df.iloc[m_id[0]]['song'] for m_id in distances[1:21]]
#     return recommended_songs

# def recommend_lyrics(request):
#     # Load model and data
#     df, similarity = load_model_and_data()
    
#     if request.method == 'POST':
#         song = request.POST.get('song')
#         if song:
#             # Get recommendations for the selected song
#             recommendations = recommendation(song, df, similarity)
#             return render({'recommendations': recommendations})








