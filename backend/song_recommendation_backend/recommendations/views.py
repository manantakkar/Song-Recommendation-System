from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
import json
from .logger import audit_logger, exception_logger
from django.views.decorators.csrf import csrf_exempt
from .models import RecommendationScheme, Music
from .forms import RecommendationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import RecommendPlaylist, RecommendArtist, RecommendSongYear
import pandas as pd
from django.conf import settings
from decouple import config
import requests
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials




    
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




@csrf_exempt
@api_view(['POST'])
def recommend_playlist(request):
    if request.method == 'POST':
        song_df = pd.read_csv(settings.CSV_FILE_PATH)
        complete_feature_set = pd.read_csv(settings.COMPLETE_PATH)
        json_data = json.loads(request.body.decode('utf-8'))
        # Get URL from request data
        URL = json_data.get('URL', '')

        if URL is None or URL == '':
            return JsonResponse({'error': 'Please enter the spotify playlist URL'}, status=400)
        
        # Use extract function to get features dataframe
        df = RecommendPlaylist().extract(URL)
        
        # Retrieve recommendations
        recommends = RecommendPlaylist().recommend_using_playlist(song_df, complete_feature_set, df)

    
        number_of_recs = int(json_data.get('number_of_recs', 10))  # Default to 10 recommendations if not provided
        my_songs = []
        for i in range(number_of_recs):
        
            my_songs.append({'name': str(recommends.iloc[i,4]), 'artist': str(recommends.iloc[i,1]), 'spotify_link': "https://open.spotify.com/track/"+ str(recommends.iloc[i,-6]).split("/")[-1]})
        
        # Return recommendations as JSON response    
        return Response(my_songs)

    

@csrf_exempt
@api_view(['POST'])
def recommend_song(request):
    
    if request.method == 'POST':
        # songs = request.POST.get('songs')
        
        json_data = json.loads(request.body.decode('utf-8'))

        # Extract the 'songs' field from the JSON data
        songs = json_data.get('songs')
        artist = json_data.get('artist', '')
        year = json_data.get('year', '')
        n_songs = json_data.get('n_songs', 10)#Default to 10 recommendations if not provided
        if n_songs == 0:
            n_songs = 10
        
        audit_logger.info(f"Input: {songs}, {artist}, {year}, {n_songs}")
         
        if songs == None:
            return JsonResponse({'error': 'Please enter the song details'}, status=400)

        recommendation = RecommendSongYear().recommend_songs(songs, artist, year, n_songs)
    
        if len(recommendation) > 0:
            return Response({'songs': recommendation})
        elif recommendation == None:
            return JsonResponse({'error': 'Enter artist name and release year'}, status=500)
        else:
            return HttpResponseServerError

    

@csrf_exempt
@api_view(['POST'])
def search_from_dataset(request):
    df = pd.read_csv(settings.SONGS_PATH)
    df['name'] = df['name'].str.lower()

    df.set_index('name', inplace=True)  
    # sorted_df = df.sort_values(by='popularity', ascending=False)

    song_name = request.POST.get('songs').lower()
    regex_pattern = f".*{re.escape(song_name)}.*"
    
    result = df[df.index.str.contains(regex_pattern, case=False, regex=True)]

    # result = df.loc[(df.index == song_name)]
    result = result.reset_index().to_dict(orient="records")

    result = [r['name'].title() for r in result if r['name'].startswith(song_name) ]

    # for r in result:
    #     r['name'] = r['name'].title()    

    return Response({'songs': set(result)})





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








