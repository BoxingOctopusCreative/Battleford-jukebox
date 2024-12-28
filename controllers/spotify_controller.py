import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import (
    SPOTIFY_CLIENT_ID, 
    SPOTIFY_CLIENT_SECRET, 
    SPOTIFY_REDIRECT_URI, 
    PLAYLIST_ID
)

class SpotifyController:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="playlist-modify-public playlist-modify-private"
        ))
        self.playlist_id = PLAYLIST_ID
        
    async def search_track(self, query):
        results = self.sp.search(q=query, type='track', limit=1)
        
        if not results['tracks']['items']:
            return None
            
        track = results['tracks']['items'][0]
        return {
            'uri': track['uri'],
            'name': track['name'],
            'artist': track['artists'][0]['name']
        }
    
    async def add_to_playlist(self, track_uri):
        self.sp.playlist_add_items(self.playlist_id, [track_uri])
        
    def get_playlist_url(self):
        return f"https://open.spotify.com/playlist/{self.playlist_id}" 