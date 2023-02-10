from utils import slash_command
import discord
from discord.commands import slash_command
from discord.ext import commands

class Weather(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='weather', description='return bot latency')
    async def weather(
        self,
        ctx: discord.ApplicationContext
    ):
        await ctx.respond(f"pong! ({self.bot.latency*1000:.2f} ms)")

def setup(bot):
    bot.add_cog(Weather(bot))
