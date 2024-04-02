from .models import Music
from recommender.api import Recommender
from django.conf import settings
from decouple import config

class MusicRecommender:
   

    def generate(self, artist_name, genres, attrs):
        recommender = Recommender(client_id=config('client_id'), client_secret=config('client_secret'))
        recommender.artists = artist_name
        recommender.genres = genres
        recommender.track_attributes = attrs
        recommendations = recommender.find_recommendations()
        result = []
        # if len(result) > 0:
        #     for recommendation in recommendations['tracks']:
        #         music = Music.objects.create(
        #             name=recommendation['name'],
        #             link=recommendation['external_urls']['spotify'],
        #             artist=recommendation['artists'][0]['name'],
        #             image_link=recommendation['album']['images'][0]['url']
        #         )
        # result.append(recommendations)
        for recommendation in recommendations['tracks']:
            x = (recommendation['name'], recommendation['artists'][0]['name'])
            result.append(x)

        return result
       
           

