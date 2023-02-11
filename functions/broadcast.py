from utils import slash_command
from utils.info import teams_dict
import discord
from discord.commands import slash_command, Option
from discord.ext import commands


class Broadcast(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="broadcast",description="A broadcast to all team member")
    async def broadcast(self, ctx, team_name: Option(str, "The team name", required = True), text:Option(str, "content", required = True)):

        if (team_name not in teams_dict):
            await ctx.respond("The team name is not exist.")
            return

        if (ctx.author.id not in teams_dict[team_name].leader_ids):
            await ctx.respond("Your are not the leader")
            return

        for each_member in teams_dict[team_name].member:
            await each_member.send(f"{team_name} team leader {ctx.author.name} :{text}")
        ## check if user is any team leader
        ## choose each team

        await ctx.respond("Broadcast success !",ephemeral=True)

def setup(bot):
    bot.add_cog(Broadcast(bot))

