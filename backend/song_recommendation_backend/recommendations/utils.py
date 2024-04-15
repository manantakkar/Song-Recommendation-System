import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from scipy.spatial.distance import cdist
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
from decouple import config
import json
from .logger import *




client_id = config('client_id')
client_secret = config('client_secret')




class RecommendPlaylist:
    """
    A class for recommending songs based on a specific playlist.
    """

   
    def generate_playlist_feature(complete_feature_set, playlist_df):
        """
        Summarize a user's playlist into a single vector.

        Parameters:
            complete_feature_set (DataFrame): DataFrame with all features for the Spotify songs.
            playlist_df (DataFrame): Playlist DataFrame.

        Returns:
            tuple: Tuple containing summarized playlist features and feature set of non-playlist songs.
        """
        complete_feature_set_playlist = complete_feature_set[complete_feature_set['id'].isin(playlist_df['id'].values)]
        complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['id'].isin(playlist_df['id'].values)]
        complete_feature_set_playlist_final = complete_feature_set_playlist.drop(columns="id")
        return complete_feature_set_playlist_final.sum(axis=0), complete_feature_set_nonplaylist

    def playlist_recommendations(df, features, nonplaylist_features):
        """
        Generate recommendations based on songs in a specific playlist.

        Parameters:
            df (DataFrame): Spotify DataFrame.
            features (Series): Summarized playlist feature (single vector).
            nonplaylist_features (DataFrame): Feature set of songs that are not in the selected playlist.

        Returns:
            DataFrame: Top 40 recommendations for that playlist.
        """
        np_df = df[df['id'].isin(nonplaylist_features['id'].values)]
        np_df['sim'] = cosine_similarity(nonplaylist_features.drop('id', axis=1).values, features.values.reshape(1, -1))[:, 0]
        np_df_top = np_df.sort_values('sim', ascending=False).head(40) 
        return np_df_top

   
    def recommend_using_playlist(self, song_df, complete_feature_set, playlistDF_test):
        """
        Recommend songs from a playlist.

        Parameters:
            songDF (DataFrame): Spotify DataFrame.
            complete_feature_set (DataFrame): DataFrame with all features for the Spotify songs.
            playlistDF_test (DataFrame): Playlist DataFrame.

        Returns:
            DataFrame: Top 40 recommendations for the playlist.
        """
        complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = RecommendPlaylist.generate_playlist_feature(complete_feature_set, playlistDF_test)
        return RecommendPlaylist.playlist_recommendations(song_df, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)




    def extract(self, URL):
        

        #use the clint secret and id details
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # the URI is split by ':' to get the username and playlist ID
        playlist_id = URL.split("/")[4].split("?")[0]
        playlist_tracks_data = sp.playlist_tracks(playlist_id)

        #lists that will be filled in with features
        playlist_tracks_id = []
        playlist_tracks_titles = []
        playlist_tracks_artists = []
        playlist_tracks_first_artists = []

        #go through the dictionary to extract the data
        for track in playlist_tracks_data['items']:
            playlist_tracks_id.append(track['track']['id'])
            playlist_tracks_titles.append(track['track']['name'])
            # adds a list of all artists involved in the song to the list of artists for the playlist
            artist_list = []
            for artist in track['track']['artists']:
                artist_list.append(artist['name'])
            playlist_tracks_artists.append(artist_list)
            playlist_tracks_first_artists.append(artist_list[0])

        #create a dataframe
        features = sp.audio_features(playlist_tracks_id)
        features_df = pd.DataFrame(data=features, columns=features[0].keys())
        features_df['title'] = playlist_tracks_titles
        features_df['first_artist'] = playlist_tracks_first_artists
        features_df['all_artists'] = playlist_tracks_artists
        features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                                    'danceability', 'energy', 'key', 'loudness',
                                    'mode', 'acousticness', 'instrumentalness',
                                    'liveness', 'valence', 'tempo',
                                    'duration_ms', 'time_signature']]
        
        return features_df




class RecommendSongYear:
   
    """
    A class for recommending songs based on input song list.
    
    Attributes:
        song_cluster_pipeline (sklearn.pipeline.Pipeline): Pipeline for clustering songs based on audio features.
        number_cols (list): List of numerical column names used for clustering.
        spotify_data (pandas.DataFrame): DataFrame containing Spotify song data.
    
    Methods:
        __init__: Initializes the RecommendSongYear class and fits the clustering pipeline to the Spotify data.
        find_song: Finds a song using the Spotify API based on name, artist, and year.
        get_mean_vector: Calculates the mean vector for a list of songs.
        flatten_dict_list: Flattens a list of dictionaries into a single dictionary.
        recommend_songs: Recommends songs based on an input song list, artist, year, and number of songs.
        get_recommended_song_info: Retrieves additional information for a recommended song from the Spotify API.
        get_spotify_info: Retrieves Spotify information (year and artist) for a given song name.
    """

    def __init__(self):

        """
        Initializes the RecommendSongYear class and fits the clustering pipeline to the Spotify data.
        """
         
        self.song_cluster_pipeline = Pipeline([('scaler', StandardScaler()), 
                                               ('kmeans', KMeans(n_clusters=20))])
        self.number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 
                            'explicit', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 
                            'popularity', 'speechiness', 'tempo']
        self.spotify_data = pd.read_csv("datasets/spotify_data.csv")
        self.song_cluster_pipeline.fit(self.spotify_data[self.number_cols])
        self.spotify_data['cluster_label'] = self.song_cluster_pipeline.predict(self.spotify_data[self.number_cols])

    
    def find_song(self, name, artist, year):
        
        """
        Find a song using the Spotify API.

        Parameters:
            name (str): The name of the song.
            artist (str): The artist of the song.
            year (int): The year of the song.

        Returns:
            DataFrame: A DataFrame containing information about the found song.
        """
    
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
        song_data = defaultdict()
        results = sp.search(q= 'track: {} artists: {} year: {}'.format(name,artist,year), limit=1)
        if results['tracks']['items'] == []:
            return None

        results = results['tracks']['items'][0]
        track_id = results['id']
        audio_features = sp.audio_features(track_id)[0]

        song_data['name'] = [name]
        song_data['year'] = [year]
        song_data['explicit'] = [int(results['explicit'])]
        song_data['duration_ms'] = [results['duration_ms']]
        song_data['popularity'] = [results['popularity']]

        for key, value in audio_features.items():
            song_data[key] = value

        return pd.DataFrame(song_data)


    
    
    def get_mean_vector(self, song_list):
       
        """
        Get the mean vector for a list of songs.

        Parameters:
            song_list (list): List of song dictionaries.

        Returns:
            array: Mean vector of the songs.
        """
        song_vectors = []
    
        for song in song_list:
            song_data = self.find_song(song['name'], song['artist'], song['year'])
            if song_data is None:
                audit_logger.error('Error: {} does not exist'.format(song['name']))
                return None
            song_vector = song_data[self.number_cols].values
            song_vectors.append(song_vector)  
        
        song_matrix = np.array(list(song_vectors))
        return np.mean(song_matrix, axis=0)
    



    def flatten_dict_list(self, dict_list):

        """
        Flatten a list of dictionaries into a single dictionary.

        Parameters:
            dict_list (list): List of dictionaries.

        Returns:
            defaultdict: Flattened dictionary.
        """

        flattened_dict = defaultdict()
        for key in dict_list[0].keys():
            flattened_dict[key] = []

        for dictionary in dict_list:
            for key, value in dictionary.items():
                flattened_dict[key].append(value)
        return flattened_dict
    
    
    
    def recommend_songs(self, songs, artist, year, n_songs):
        
        """
        Recommend songs based on input song list.

        Parameters:
            songs (list): List of song names.
            artist (str): The artist of the songs.
            year (int): The release year of the songs.
            n_songs (int): Number of songs to recommend.

        Returns:
            list: List of recommended songs with additional information.
        """
        try:
            metadata_cols = ['name', 'year', 'artists']
            audit_logger.debug(f"User Input----> song: {songs}, artist: {artist}, year: {year}, n_songs: {n_songs}")
            song_list = []
            for song in songs:
                        
                if not artist or not year:
                    year, artist = self.get_spotify_info(song.title(), year = year, artist = artist)
                
                song_list.append({'name': song.title(), 'artist': artist, 'year': int(year)})
                year = ''
                artist = ''
            audit_logger.debug(f"Song List: {song_list}")
            song_dict = self.flatten_dict_list(song_list)
            
            song_center = self.get_mean_vector(song_list)
            
            scaler = self.song_cluster_pipeline.steps[0][1]
            scaled_data = scaler.transform(self.spotify_data[self.number_cols])
            scaled_song_center = scaler.transform(song_center.reshape(1, -1))
            distances = cdist(scaled_song_center, scaled_data, 'cosine')
            index = list(np.argsort(distances)[:, :n_songs][0])
            
            rec_songs = self.spotify_data.iloc[index]
            rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
            rec_songs = rec_songs[metadata_cols].to_dict(orient='records')
            spotify_info = []
            for song in rec_songs:
                name = song["name"]
                year = song["year"]
                artists = eval(song["artists"])  # Convert string representation of list to actual list
            
                image_link, spotify_link, _ , _ = self.get_recommended_song_info(name, artists, year)
                
                spotify_info.append({
                    "name": name.title(),
                    "year": year,
                    "artist": artists,
                    "spotify_link": spotify_link,
                    "image_link": image_link
                })
            audit_logger.info(f"Recommended songs: {spotify_info}")
            return spotify_info
        
        except Exception as e:
            audit_logger.error(f"Error in recommending songs: {str(e)}")        
            return None


    def get_recommended_song_info(self, song_name, artists, release_year):

        """
        Retrieve additional information for a recommended song from the Spotify API.

        Parameters:
            song_name (str): The name of the recommended song.
            artists (list): List of artists for the recommended song.
            release_year (str): The release year of the recommended song.

        Returns:
            Additional information for the recommended song (image link, Spotify link, artist name, year).
        """
        # Authenticate with Spotify API
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Search for the song
        # if release_year == '':
        #     query = f'track:{song_name} artist:{artists[0]}'

        # else:
        query = f'track:{song_name} artist:{artists[0]} year:{release_year}'
           
        results = sp.search(q=query, type='track', limit=1)

        # Extract the release year, artist name, image link, and Spotify link from the first search result
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            year = track['album']['release_date'][:4]  # Extract the year part
            artist_name = track['artists'][0]['name']  # Extract the artist name
            image_link = track['album']['images'][0]['url'] if track['album']['images'] else None  # Extract the image link
            spotify_link = track['external_urls']['spotify']  # Extract the Spotify link
            return image_link, spotify_link, artist_name, year
        else:
            return None, None, None, None

    
    
    
    def get_spotify_info(self, song_name, year='', artist=''):

        """
        Retrieve Spotify information (year and artist) for a given song name.

        Parameters:
            song_name (str): The name of the song.
            year (int): The release year of the song (optional).
            artist (str): The artist of the song (optional).

        Returns:
            Spotify information (year and artist) for the given song name.
        """
        # Authenticate with Spotify API
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Search for the song
        
        if artist and year:
            query = f'track:{song_name} artist:{artist} year:{year}'
        elif artist:
            query = f'track:{song_name} artist:{artist}'
        elif year:
            query = f'track:{song_name} year:{year}'
        else:
            query = f'track:{song_name}'

        
        results = sp.search(q=query, type='track', limit=1)

        # Extract the release year, artist name from the first search result
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            release_year = track['album']['release_date'][:4]  # Extract the year part
            artist_name = track['artists'][0]['name']  # Extract the artist name
            return release_year, artist_name
        else:
            return None, None


   




