from discord.ext import commands
import asyncio
from functools import partial
from config import CHANNEL_ID

class AddSong(commands.Cog):
    def __init__(self, bot, spotify_controller):
        self.bot = bot
        self.spotify_controller = spotify_controller

    @commands.command(name='addsong')
    async def add_song(self, ctx, *, song_query):
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