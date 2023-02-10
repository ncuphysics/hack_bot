from utils import slash_command
import discord
from discord.commands import slash_command
from discord.ext import commands


class Help(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="help", description="Shows help for the bot")
    async def help(self, ctx):
        # embed = discord.Embed( title="Command", description="I'm a bot that could help you to works with your teams")
        # embed.add_field(name= "checkin"     , value="Check in"                 , inline=True)
        # embed.add_field(name= "checkout"    , value="Check out"                , inline=True)
        # embed.add_field(name= "order_drink" , value="Create a drink order"                  )
        # embed.add_field(name= "record"      , value="record yor meeting sound"              )
        text = """:sun_with_face:  `/CHECKIN` :first_quarter_moon_with_face: `\CHECKOUT`
\t\t-The Check in out function can provide automated registration, login and logout services, and provide detailed login records
\t\t-Allowing the team to manage and monitor user activities more easily.
\t\t-Allowing you to manage and monitor user activities more effectively.
:champagne_glass: `/ORDER DRINK`
\t\t-You can create a drink order.
\t\t-Other users can enter what they want to drink.
\t\t-In the end you will receive all the drinks entered by the user.
:speaking_head: `/RECORD`
\t\t-You can record your meeting sound, and get the summarize of the meeting.
\t\t-private record       : Start a private recording, and the subsequent summary will only be available to those in the voice room (it is recommended to lock the room)
\t\t-public record        : Open a public recording, everyone in this server can access.
\t\t-check record summary : Can check all your accessible recordings, and call up the summary conclusion.
\t\t-check record file    : Can check all your accessible recordings, and download the audio.
:office_worker: `/get_checkinout`
\t\t-The team leader can check the team member check in-out record.
:man_teacher: `/Team`
\t\tYou can create your team, manage your team members, assign tasks, check in and out status.
\t\t-get checkinout       : The team leader can check the team member check in-out record.
\t\t-teamwork             : You can use this command to let the robot help you assign tasks to team members.
\t\t-member current tasks : Do you find it troublesome to private message each team member? Let the robot help you ask, and I can help you ask every member under you.
\t\t-teamkick             : Remove member.
\t\t-anonymous_opinion    : Each member has the ability to express their opinions anonymously, which makes a team grow.
"""
        await ctx.send(text)

        
def setup(bot):
    bot.add_cog(Help(bot))