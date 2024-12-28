# Battleford Jukebox

A Discord bot for managing music playback through Spotify and Alexa devices. Users can add songs to a Spotify playlist and control playback through Discord commands.

## Features

- Add songs to a designated Spotify playlist (`!addsong`)
- Play songs on Alexa devices (`!play`)
- Integration with Spotify and Alexa APIs

## Setup

### Prerequisites

- Python 3.12+
- Docker (optional)
- Discord Bot Token
- Spotify API credentials
- Alexa API credentials

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DISCORD_TOKEN=your_discord_token
CHANNEL_ID=your_channel_id
ECHO_DEVICE_NAME=your_alexa_device_name
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_PLAYLIST_ID=your_playlist_id
```

### Installation

#### Local Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Run the bot:

```bash
python main.py
```

#### Docker Setup

1. Build the container:

```bash
docker build -t battleford-jukebox .
```

1. Run the container:

```bash
docker run --env-file .env battleford-jukebox
```

## Developer Guide

### Project Structure

battleford-jukebox/
├── commands/ # Discord command modules
├── controllers/ # Core controller classes
├── config.py # Configuration and environment variables
├── main.py # Application entry point
├── requirements.txt # Python dependencies
└── Dockerfile # Container configuration

### Adding New Commands

1. Create a new file in the `commands/` directory:

```python
from discord.ext import commands

class NewCommand(commands.Cog):
    def __init__(self, bot, *required_controllers):
        self.bot = bot
        # Store any required controllers

    @commands.command(name='commandname')
    async def command_method(self, ctx, *args):
        # Command implementation
```

1. Register the command in `discord_controller.py`:

```python
from commands.new_command import NewCommand

class DiscordController:
    def register_commands(self):
        # ... existing commands ...
        self.bot.add_cog(NewCommand(self.bot, *required_controllers))
```

### Adding New Controllers

1. Create a new controller class in `controllers/`:

```python
class NewController:
    def __init__(self):
        # Initialize controller
        pass

    def some_method(self):
        # Implement controller functionality
        pass
```

1. Initialize the controller in `main.py`:

```python
new_controller = NewController()
discord_controller = DiscordController(
    spotify_controller,
    alexa_controller,
    new_controller
)
```

## Available Commands

- `!addsong <song name>` - Adds a song to the Spotify playlist
- `!play <song name>` - Plays a song on the configured Alexa device

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
