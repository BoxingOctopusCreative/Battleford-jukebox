import requests
from config import (
    AVS_CLIENT_ID, 
    AVS_CLIENT_SECRET, 
    AVS_REFRESH_TOKEN
)

class AlexaController:
    def __init__(self):
        self.token = None
        self.base_url = "https://api.amazonalexa.com/v1"
        self._refresh_access_token()

    def _refresh_access_token(self):
        token_url = "https://api.amazon.com/auth/o2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": AVS_REFRESH_TOKEN,
            "client_id": AVS_CLIENT_ID,
            "client_secret": AVS_CLIENT_SECRET
        }
        response = requests.post(token_url, data=data)
        self.token = response.json()["access_token"]

    async def play_spotify(self, device_name, track_name, artist_name):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Get list of devices
        devices_response = requests.get(
            f"{self.base_url}/devices",
            headers=headers
        ).json()

        # Find the specified device
        device = next(
            (d for d in devices_response["devices"] 
             if d["displayName"].lower() == device_name.lower()),
            None
        )

        if not device:
            raise ValueError(f"Device '{device_name}' not found")

        # Send command to play music
        command = {
            "type": "Alexa.Music.PlaySearchPhrase",
            "payload": {
                "searchPhrase": f"play {track_name} by {artist_name} on Spotify",
                "musicProviderId": "SPOTIFY"
            }
        }

        response = requests.post(
            f"{self.base_url}/devices/{device['id']}/directives",
            headers=headers,
            json=command
        )

        if response.status_code != 200:
            raise Exception(f"Failed to send command: {response.text}") 