import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from commands.add_song import AddSong
#from commands.play_song import PlaySong

class DiscordController:
    def __init__(self, spotify_controller):#, alexa_controller):
        # Set up intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.messages = True
        
        # Initialize bot
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.spotify_controller = spotify_controller
        #self.alexa_controller = alexa_controller
        
        # Register commands
        self.register_commands()
        
    def register_commands(self):
        @self.bot.event
        async def on_ready():
            print(f'Bot is ready and logged in as {self.bot.user}')
            print("Attempting to load AddSong cog...")
            try:
                await self.bot.add_cog(AddSong(self.bot, self.spotify_controller))
                print("Successfully loaded AddSong cog")
                print(f'Loaded commands: {[command.name for command in self.bot.commands]}')
            except Exception as e:
                print(f"Error loading AddSong cog: {str(e)}")

        @self.bot.event
        async def on_message(message):
            print(f"Received message: {message.content}")
            await self.bot.process_commands(message)  # This is crucial!

        # Add command cogs
        #self.bot.add_cog(AddSong(self.bot, self.spotify_controller))
        #self.bot.add_cog(PlaySong(self.bot, self.spotify_controller, self.alexa_controller))

    def run(self):
        self.bot.run(DISCORD_TOKEN) 