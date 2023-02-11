from utils import slash_command
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
import utils.Team as my_ts

class Vote(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="vote",description="Create a vote")
    async def vote(self, ctx, timeout_min : Option(int, "Time out (min)", required = False, default = 5)):
        # Choose vote
        my_vote = my_ts.DecideVote(ctx.channel, timeout_min, title='Votes')
        await ctx.response.send_modal(my_vote)

def setup(bot):
    bot.add_cog(Vote(bot))


