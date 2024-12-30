import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import (
    SPOTIFY_CLIENT_ID, 
    SPOTIFY_CLIENT_SECRET, 
    SPOTIFY_REDIRECT_URI, 
    PLAYLIST_ID
)
from difflib import SequenceMatcher
from typing import Optional, Dict, List

class SpotifyController:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="playlist-modify-public playlist-modify-private"
        ))
        self.playlist_id = PLAYLIST_ID
    
    def _calculate_similarity(self, query: str, track_name: str, artist_name: str) -> float:
        # Normalize strings for comparison
        query = query.lower().strip()
        track_name = track_name.lower().strip()
        artist_name = artist_name.lower().strip()
        
        # Check if query contains both song and artist (e.g., "Song - Artist")
        if " - " in query:
            query_song, query_artist = query.split(" - ", 1)
            song_similarity = SequenceMatcher(None, query_song.strip(), track_name).ratio()
            artist_similarity = SequenceMatcher(None, query_artist.strip(), artist_name).ratio()
            return (song_similarity + artist_similarity) / 2
        
        # Otherwise just check song title
        return SequenceMatcher(None, query, track_name).ratio()
    
    def _format_track_info(self, track: Dict) -> Dict:
        return {
            'uri': track['uri'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'duration': track['duration_ms'] // 1000  # Convert to seconds
        }
    
    def search_track(self, query: str, threshold: float = 0.9) -> Dict:
        """
        Search for a track with exact matching and suggestions.
        Returns a dict with 'exact_match' and 'suggestions' keys.
        """
        print(f"Searching for track: {query}")
        results = self.sp.search(q=query, type='track', limit=5)
        
        tracks = results['tracks']['items']
        if not tracks:
            return {'exact_match': None, 'suggestions': []}
        
        matches = []
        for track in tracks:
            similarity = self._calculate_similarity(query, track['name'], track['artists'][0]['name'])
            matches.append((similarity, self._format_track_info(track)))
        
        # Sort by similarity score
        matches.sort(reverse=True, key=lambda x: x[0])
        
        # Get best match and check if it meets threshold
        best_match = matches[0]
        exact_match = best_match[1] if best_match[0] >= threshold else None
        
        # Get up to 3 suggestions (excluding exact match)
        suggestions = [m[1] for m in matches[0:3] if m[1] != exact_match]
        
        return {
            'exact_match': exact_match,
            'suggestions': suggestions
        }
    
    def add_to_playlist(self, track_uri: str) -> None:
        print(f"Adding track {track_uri} to playlist {self.playlist_id}")
        self.sp.playlist_add_items(self.playlist_id, [track_uri])
        
    def get_playlist_url(self) -> str:
        return f"https://open.spotify.com/playlist/{self.playlist_id}" 