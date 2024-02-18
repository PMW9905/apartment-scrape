import json

from discord.ext import commands, tasks
from discord import Intents

import asyncio

from apartment_web_scraper import ApartmentWebScraper
from apartment_data import ApartmentData
from apartment_db import Database


# Config file will always be defined as config.json
# Must be generated by user before execution
config_file_path = 'config.json'

# Attempt to read json data into dict
print('Reading config data...')
try:
    opened_json_file = open(config_file_path, 'r')
    discord_bot_config = dict(json.load(opened_json_file))
    opened_json_file.close()
except Exception as e:
    print(f'Unable to open config file due to the following error:')
    print(e)
    quit()

# Spawning apartment_db
print('spawning apartment db...')
apartment_db = Database('apartment.db')
asyncio.run(apartment_db.create_tables())

# Spawning apartment_web_scraper
print('Spawning apartment_web_scraper...')
apartment_web_scraper = ApartmentWebScraper()
apartment_web_scraper.start_driver()

# Defining bot intents
print('Defining bot intents...')
intents = Intents.default()
intents.message_content = True

# Defining bot commands
print('Defining bot commands...')
bot = commands.Bot(command_prefix='!', intents = intents)

@bot.check
async def globally_whitelisted(ctx):
    return str(ctx.author.id) in discord_bot_config['whitelisted_user_ids']

#@bot.loop(hour=1)
@bot.command(name='hourly-scrape')
async def hourly_scrape(ctx):
    print('Performing hourly scrape...') 
    # Grab complexes and layouts to scrape
    all_subscribed_complexes = await apartment_db.list_all_complex()
    all_subscribed_layouts = await apartment_db.list_all_layouts()

    if len(all_subscribed_complexes) == 0 or len(all_subscribed_layouts) == 0:
        print('No complexes/layouts to subscribe to...')
        return
    # Scrape those complexes/layouts
    unannounced_wanted_apartments = []
    
    # Running loop for interacting with apartment web scraper
    loop = asyncio.get_running_loop()

    for complex_name, url in all_subscribed_complexes.items():
        print(f'Scraping for {complex_name} at {url}')
        scraped_apartments = await loop.run_in_executor(None, apartment_web_scraper.get_available_apartments_from_url, url)

        print(f'Apartments scraped:')
        for apt in scraped_apartments:
            print(apt)        
        # Only select the apartments that are wanted
        print(f'Getting wanted layouts for {complex_name}')
        wanted_layouts = all_subscribed_layouts[complex_name]
        print(f'Getting wanted apartments for {complex_name}')
        wanted_apartments = [
           apt for apt in scraped_apartments
           if apt.layout_name in wanted_layouts
        ]

        print('Wanted layouts:')
        for apt in wanted_layouts:
            print(apt)

        print('Wanted apartments from scraped list:')
        for apt in wanted_apartments:
            print(apt)

        print('Excluding apartments that have already been notified')
        # For each wanted apartment, see if it's been visited yet
        unannounced_wanted_apartments += [
            apt for apt in wanted_apartments
            if not await apartment_db.is_apartment_already_notified(apt.unit_number, apt.layout_name, complex_name)
        ]

    print('Marking unannounced wanted apartments as notified')
    # mark unannounced wanted apartments as visited
    for apt in unannounced_wanted_apartments:
        await apartment_db.mark_apartment_as_notified(apt.unit_number, apt.layout_name, complex_name)

    # Announce wanted apartments!
    print(unannounced_wanted_apartments) 
 

# Basic greet command
@bot.command(name='get-my-id')
async def greet(ctx):
    print('Sending user id...')
    await ctx.send(ctx.author.id)

@bot.command(name='add-complex')
async def add_complex(ctx, complex_name: str, complex_url: str):
    result = await apartment_db.add_complex(complex_name, complex_url)

    if result:
        await ctx.send(f"Complex '{complex_name}' added successfully.")
    else:
        await ctx.send(f"An error occured while trying to add '{complex_name}'.")


@bot.command(name='remove-complex')
async def remove_complex(ctx, complex_name: str):
    result = await apartment_db.remove_complex(complex_name)

    if result:
        await ctx.send(f"Complex '{complex_name}' removed successfully.")
    else:
        await ctx.send(f"An error occured while trying to remove '{complex_name}'.")

@bot.command(name='add-layout')
async def add_layout(ctx, layout_name: str, complex_name: str):
    result = await apartment_db.add_layout(layout_name, complex_name)

    if result:
        await ctx.send(f"Layout '{layout_name}' added to '{complex_name}' successfully.")
    else:
        await ctx.send(f"An error occured while trying to add '{layout_name} to {complex_name}'.")

@bot.command(name='remove-layout')
async def remove_layout(ctx, layout_name: str, complex_name: str):
    result = await apartment_db.remove_layout(layout_name, complex_name)

    if result:
        await ctx.send(f"Layout '{layout_name}' removed from '{complex_name}' successfully.")
    else:
        await ctx.send(f"An error occured while trying to remove '{layout_name}' from '{complex_name}'.")

@bot.command(name='list-layouts')
async def list_layouts(ctx):
    complex_layouts = await apartment_db.list_all_layouts()

    if complex_layouts == False:
        await ctx.send('Failed to retrieve layouts.')
    else:
        message = ["Complexes and their layouts:"]
        for complex_name, layouts in complex_layouts.items():
            layouts_str = ', '.join(layouts)
            message.append(f"{complex_name}: {layouts_str}")
        await ctx.send('\n'.join(message))

@bot.command(name='list-complexes')
async def list_complexes(ctx):
    complexs = await apartment_db.list_all_complex()

    if complexs == False:
        await ctx.send('Failed to retrieve complexes.')
    else:
        message = ["Complexes:"]
        for complex_name, url in complexs.items():
            message.append(f"{complex_name}: {url}")
        await ctx.send('\n'.join(message))

# Demo get apartments command
@bot.command(name='get-available-apartments')
async def get_available_apartments(ctx, complex_name):
    url = await apartment_db.get_complex_url(complex_name)
    url = str(url)
    loop = asyncio.get_running_loop()

    print('Getting available apartments...')
    await ctx.send('Getting available apartments...')
    available_apartments = await loop.run_in_executor(None, apartment_web_scraper.get_available_apartments_from_url, url)

    # Formatting the table such that there is consistant whitespace inbetween columns.
    message = [
        "```",
        f"{'Unit':<6} | {'Layout':<15} | {'Cost':<8} | {'Sq Ft':<6} | {'Available':<8}",
        "-"*60,
    ]

    for apt in available_apartments:
        message.append(apt.get_formatted_string_for_discord_table())

    message.append("```")

    await ctx.send('\n'.join(message))

print('Running bot...')
bot.run(discord_bot_config['discord_bot_token'])

    