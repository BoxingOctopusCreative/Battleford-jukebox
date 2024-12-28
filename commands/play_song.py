from discord.ext import commands
import asyncio
from functools import partial
from config import CHANNEL_ID, ECHO_DEVICE_NAME

class PlaySong(commands.Cog):
    def __init__(self, bot, spotify_controller, alexa_controller):
        self.bot = bot
        self.spotify_controller = spotify_controller
        self.alexa_controller = alexa_controller

    @commands.command(name='play')
    async def play_song(self, ctx, *, song_query):
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