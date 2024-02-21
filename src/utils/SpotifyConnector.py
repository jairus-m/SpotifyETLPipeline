"""Connector module for Spotify API"""

import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd 

class SpotifyData():
    """
    Class object to interact with Spotify API
    
    Attributes:
        client_id: client id
        client_secret: client secret
        sp: spotipy.Spotify class object
    Methods:
        get_songs: downloads the 50 most recently played songs
        create_song_data: creates dataframe from listening data

    """
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=["user-read-recently-played", "playlist-modify-private"],
                redirect_uri="http://localhost:3000",
                client_id=client_id,
                client_secret=client_secret,
                show_dialog=True,
                cache_path="token.txt"
                )
            )
        self._logger = logging.getLogger(__name__)
    
    def get_songs(self) -> dict:
        """
        Gets the recently played songs from Spotipy API

        :returns: recently_played songs
        :return type: nested json
        """
        user_id = self.sp.current_user()["id"]
        recently_played = self.sp.current_user_recently_played(limit=50)['items']
        return recently_played
    

    def create_song_data(self, songs: dict) -> pd.DataFrame:
        """
        Creates dataframe from listening data

        :param songs: nested json containing listening history
        :returns: pd.DataFrame 
        """
        song_history = []
        for track in songs:
            song_name = track['track']['name']
            artist = track['track']['artists'][0]['name']
            album = track['track']['album']['name']
            time = pd.to_datetime(track['played_at']).tz_convert('America/Los_Angeles').strftime('%m/%d/%Y %H:%M:%S')
            duration_ms = track['track']['duration_ms']
            track_id = track['track']['id']

            song_entry = {
                'time':time,
                'track_id':track_id,
                'song_name':song_name,
                'artist':artist,
                'album':album,
                'duration':duration_ms,
                }

            song_history.append(song_entry)

        df = pd.DataFrame(song_history)
        df['time'] = df['time'].astype('datetime64[ns]').sort_values()
        
        return df.sort_values(by='time', ascending=False)

    