from utils import slash_command
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from utils.info import teams_dict

class Alarm(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="team_alarm",description="Book a alram and let me notify everyone in the team")
    async def team_alarm(self, ctx,
                        team_name : Option(str, "The team name"  , required = True),
                        month     : Option(int,"month"           , required = True),
                        day       : Option(int,"day"             , required = True),
                        hour      : Option(int,"hour"            , required = True),
                        text      : Option(str, "text to notify" , required = True)):

        one_time = (month, day, hour)
        allmem   = teams_dict[team_name].member +  teams_dict[team_name].leader
        alarm_arr.append( my_ts.Alarm(allmem , one_time, text) )

        ## check if user is a team leader, set a alarm to user

        await ctx.respond(f" BookMeeting at {month}-{day} {hour}",ephemeral=True)

    async def loop_alarm():
        while True:
            result = False
            for each in range(len(alarm_arr)):
                result = await alarm_arr[each].check()
                if (result):
                    alarm_arr.pop(each)
                    break
            if (not result):
                await asyncio.sleep(10)

def setup(bot):
    bot.add_cog(Alarm(bot))
