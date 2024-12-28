from discord.ext import commands
import asyncio
from functools import partial
from config import CHANNEL_ID


class AddSong(commands.Cog):
    def __init__(self, bot, spotify_controller):
        self.bot = bot
        self.spotify_controller = spotify_controller

    @commands.command(name='addsong')
    async def add_song(self, ctx, *, song_name):
        try:
            print(f"Searching for: {song_name}")
            track = self.spotify_controller.search_track(song_name)
            
            if not track:
                await ctx.send(f'Could not find song: {song_name}')
                return
                
            print(f"Found track: {track}")
            self.spotify_controller.add_to_playlist(track['uri'])
            
            await ctx.send(
                f'Successfully added "{track["name"]}" by {track["artist"]} to the playlist!\n'
                f'Playlist: {self.spotify_controller.get_playlist_url()}'
            )
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            await ctx.send(f'An error occurred: {str(e)}') 