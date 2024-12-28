from controllers import (
    SpotifyController,
    #AlexaController,
    DiscordController
)

def main():
    # Initialize controllers
    spotify_controller = SpotifyController()
    #alexa_controller = AlexaController()
    discord_controller = DiscordController(spotify_controller) #, alexa_controller)
    
    # Run the bot
    discord_controller.run()

if __name__ == "__main__":
    main()
