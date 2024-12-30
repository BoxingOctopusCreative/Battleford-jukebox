from discord.ext import commands
import asyncio
from functools import partial

class AddSong(commands.Cog):
    def __init__(self, bot, spotify_controller):
        self.bot = bot
        self.spotify_controller = spotify_controller

    def format_track_display(self, track):
        return f"{track['name']} - {track['artist']} ({track['album']})"

    @commands.command(name='addsong')
    async def add_song(self, ctx, *, song_name):
        try:
            await ctx.send(f'🔎 Searching for: {song_name}...')
            
            results = self.spotify_controller.search_track(song_name)
            
            if results['exact_match']:
                track = results['exact_match']
                self.spotify_controller.add_to_playlist(track['uri'])
                await ctx.send(
                    f'✅ Added "{track["name"]}" by {track["artist"]} to the playlist!\n'
                    f'Playlist: {self.spotify_controller.get_playlist_url()}'
                )
            
            elif results['suggestions']:
                suggestions_text = "\n".join(
                    f"{i+1}. {self.format_track_display(track)}"
                    for i, track in enumerate(results['suggestions'])
                )
                
                await ctx.send(
                    f'❌ No exact match found for "{song_name}"\n'
                    f'Did you mean one of these?\n'
                    f'```\n{suggestions_text}\n```\n'
                    f'Reply with the number to add that song, or try your search again.'
                )
                
                def check(m):
                    return (
                        m.author == ctx.author and 
                        m.channel == ctx.channel and 
                        m.content.isdigit() and 
                        1 <= int(m.content) <= len(results['suggestions'])
                    )
                
                try:
                    msg = await self.bot.wait_for('message', timeout=30.0, check=check)
                    selected = results['suggestions'][int(msg.content) - 1]
                    self.spotify_controller.add_to_playlist(selected['uri'])
                    await ctx.send(
                        f'✅ Added "{selected["name"]}" by {selected["artist"]} to the playlist!\n'
                        f'Playlist: {self.spotify_controller.get_playlist_url()}'
                    )
                except asyncio.TimeoutError:
                    await ctx.send('❌ Selection timed out. Please try again.')
            
            else:
                await ctx.send(f'❌ No matches found for "{song_name}"')
                
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            await ctx.send(f'❌ An error occurred: {str(e)}') 