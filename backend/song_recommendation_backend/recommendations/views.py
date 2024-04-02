from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RecommendationScheme, Music
from .forms import RecommendationForm
from .music_recommender import MusicRecommender
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import recommend_from_playlist
from .features import extract
import pandas as pd
from django.conf import settings



@csrf_exempt
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
        attrs = data.get('attrs')

        # Now you can pass these arguments to your MusicRecommender constructor
     
        recommendations = MusicRecommender().generate(artist_name, genres, attrs)

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
        df = extract(URL)
        # Retrieve recommendations
        edm_top40 = recommend_from_playlist(songDF, complete_feature_set, df)
        print(f"---------------------------{edm_top40}")
        # Get number of recommendations from request data
        # number_of_recs = int(request.data.get('number_of_recs', 10))  # Default to 10 recommendations if not provided
        # my_songs = []
        # # Prepare response data
        # for i in range(number_of_recs):
        #     my_songs.append({
        #         'title': str(edm_top40.iloc[i, 1]) + ' - ' + '"' + str(edm_top40.iloc[i, 4]) + '"',
        #         'link': "https://open.spotify.com/track/" + str(edm_top40.iloc[i, -6]).split("/")[-1]
        #     })

        number_of_recs = int(request.data.get('number_of_recs', 5))  # Default to 5 recommendations if not provided
        my_songs = []
        for i in range(number_of_recs):
            my_songs.append([str(edm_top40.iloc[i,1]) + ' - '+ '"'+str(edm_top40.iloc[i,4])+'"', "https://open.spotify.com/track/"+ str(edm_top40.iloc[i,-6]).split("/")[-1]])
                # Return recommendations as JSON response
            
        print(f"---------------------------{my_songs}")
        return Response({'songs': my_songs})
