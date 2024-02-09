import discord

class ApartmentBuddy(discord.Client):

    def __init__(self, whitelisted_user_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.whitelisted_user_ids = whitelisted_user_ids

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user or message.content[0] != '!' or message.channel != 'buddy-commands':
            return
        
        if str(message.author) not in self.whitelisted_user_ids:
            await message.channel.send(f'{message.author} does not have permission to send commands.')
            return

        command_title = message.content.split(' ')[0]

        match command_title:
            case '!ping':
                await message.channel.send('pong!')
            case '!help':
                await message.channel.send('lol the only command right now is !ping')
            case _:
                await message.channel.send('Invalid command. Type !help for a list of possible commands.')
                

class DiscordBotManager:
    def __init__(self, discord_bot_token, whitelisted_user_ids):
        self.discord_bot_token = discord_bot_token
        self.whitelisted_user_ids = whitelisted_user_ids

        self.__initialize_apartment_buddy()

    def __initialize_apartment_buddy(self):

        intents = discord.Intents.default()
        intents.message_content = True

        self.apartment_buddy = ApartmentBuddy(whitelisted_user_ids=self.whitelisted_user_ids, intents=intents)

    def start_apartment_buddy(self):
        self.apartment_buddy.run(self.discord_bot_token)
    
def main():

    import json

    config_file_path = 'config.json'
    
    # Attempt to read json data into dict
    try:
        opened_json_file = open(config_file_path, 'r')
        discord_bot_config = dict(json.load(opened_json_file))
        opened_json_file.close()
    except Exception as e:
        print(f'Unable to open config file due to the following error: \n{e}')
        quit()

    discord_bot_manager = DiscordBotManager(**discord_bot_config)

    discord_bot_manager.start_apartment_buddy()

if __name__ == '__main__':
    main()


        
