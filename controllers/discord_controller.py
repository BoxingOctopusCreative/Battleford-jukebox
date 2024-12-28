import discord
from discord.ext import commands
import asyncio
from functools import partial
from config import CHANNEL_ID, DISCORD_TOKEN, ECHO_DEVICE_NAME

class DiscordController:
    def __init__(self, spotify_controller, alexa_controller):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        
        # Initialize bot
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.spotify_controller = spotify_controller
        self.alexa_controller = alexa_controller
        
        # Register commands
        self.register_commands()
        
    def register_commands(self):
        @self.bot.event
        async def on_ready():
            print(f'Bot is ready and logged in as {self.bot.user}')

        @self.bot.command(name='addsong')
        async def add_song(ctx, *, song_query):
            await self.handle_add_song(ctx, song_query)

        @self.bot.command(name='play')
        async def play_song(ctx, *, song_query):
            await self.handle_play_song(ctx, song_query)

    async def handle_add_song(self, ctx, song_query):
        if ctx.channel.id != CHANNEL_ID:
            return

        try:
            await ctx.send(f'Searching for: {song_query}...')
            
            # Search for track
            loop = asyncio.get_event_loop()
            track = await loop.run_in_executor(None, 
                partial(self.spotify_controller.search_track, song_query))
            
            if not track:
                await ctx.send(f'Could not find song: {song_query}')
                return

            # Add to playlist
            await loop.run_in_executor(None,
                partial(self.spotify_controller.add_to_playlist, track['uri']))
            
            # Get playlist URL
            playlist_url = self.spotify_controller.get_playlist_url()
            
            await ctx.send(
                f'Successfully added "{track["name"]}" by {track["artist"]} to the playlist!\n'
                f'Playlist: {playlist_url}'
            )
        
        except Exception as e:
            await ctx.send(f'An error occurred: {str(e)}')

    async def handle_play_song(self, ctx, song_query):
        if ctx.channel.id != CHANNEL_ID:
            return

        try:
            await ctx.send(f'Searching for and playing: {song_query} on {ECHO_DEVICE_NAME}...')
            
            # Search for track
            loop = asyncio.get_event_loop()
            track = await loop.run_in_executor(None, 
                partial(self.spotify_controller.search_track, song_query))
            
            if not track:
                await ctx.send(f'Could not find song: {song_query}')
                return

            # Play on Alexa
            await self.alexa_controller.play_spotify(ECHO_DEVICE_NAME, track['name'], track['artist'])
            
            await ctx.send(f'Now playing "{track["name"]}" by {track["artist"]} on {ECHO_DEVICE_NAME}')
        
        except Exception as e:
            await ctx.send(f'An error occurred: {str(e)}')

    def run(self):
        self.bot.run(DISCORD_TOKEN) 