from utils import slash_command
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
import random

class Roll(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='roll', description='Roll a number!')
    async def roll(self,ctx, uppperlimit: Option(int, "upperbound", required = False, default = 6)):
        x = random.randint(1, uppperlimit)
        await ctx.respond(f"You roll {x}!")

def setup(bot):
    bot.add_cog(Roll(bot))
