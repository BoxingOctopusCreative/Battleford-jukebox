import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Spotify configuration
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
PLAYLIST_ID = os.getenv('PLAYLIST_ID')

# Amazon AVS configuration
AVS_CLIENT_ID = os.getenv('AVS_CLIENT_ID')
AVS_CLIENT_SECRET = os.getenv('AVS_CLIENT_SECRET')
AVS_REFRESH_TOKEN = os.getenv('AVS_REFRESH_TOKEN')
ECHO_DEVICE_NAME = os.getenv('ECHO_DEVICE_NAME') 