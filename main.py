import discord
import dotenv
import os
from traceback import format_exception

dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))
# import asyncio

bot = discord.Bot(intents=discord.Intents.all(),)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    # while True:
    #     await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='A nice game'))
    #     await asyncio.sleep(60)




# extensions = [# load cogs
#     'functions.ping',
# ]

if __name__ == '__main__': # import cogs from cogs folder
    for filename in os.listdir("functions"):
        if filename.endswith(".py"):
            extension = f"functions.{filename[:-3]}"
            bot.load_extension(extension)
    # for extension in extensions:
    #     bot.load_extension(extension)

bot.run(token)