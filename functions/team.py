from utils import slash_command
import discord
from discord.commands import slash_command, Option
from discord.ext import commands

import utils.Team as my_ts
from utils.info import teams_dict

class Team_manage(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="create_team",description="Create team")
    async def create_team(self, ctx,  team_name: Option(str, "The team name", required = True)):
        if (team_name in teams_dict):
            await ctx.respond("The team name is already exist.")
            return
        else:
            teams_dict[team_name] = my_ts.Team()

            teams_dict[team_name].leader.append(ctx.author)
            teams_dict[team_name].leader_ids.append(ctx.author.id)

            await ctx.respond(f"Create [{team_name}] success !!\nHint:\n\t-You can use `/set_public` to let all the user in this server can see your team.\n\t-Use `/set_confirm` to allow users to join your team without the consent of the leader.")

    @slash_command(name="set_public",description="whether the team is public or not")
    async def set_public(self, ctx,  team_name: Option(str, "The team name", required = True), status: Option(bool, "Is public or not.", required = True)):
        if (team_name not in teams_dict):
            await ctx.respond("The team name is not exist.")
            return


        if (ctx.author.id not in teams_dict[team_name].leader_ids):
            await ctx.respond("Your are not the leader")
            return
        else:
            teams_dict[team_name].is_public = status
            await ctx.respond(f"Set the team  [{team_name}]  is_public to {status}")


    @slash_command(name="set_confirm",description="Can users join your team without the consent of the leader.")
    async def set_confirm(self, ctx,  team_name: Option(str, "The team name", required = True), status: Option(bool, "Is public or not.", required = True)):
        if (team_name not in teams_dict):
            await ctx.respond("The team name is not exist.")
            return

        if (ctx.author.id not in teams_dict[team_name].leader_ids):
            await ctx.respond("Your are not the leader")
            return
        else:
            teams_dict[team_name].need_per = status
            await ctx.respond(f"Set the team  [{team_name}]  set_confirm to {status}")

    @slash_command(name="invite_button",description="Let users join your team.(If `/set_confirm` is True, your consent is still required)")
    async def invite_button(self, ctx,  team_name: Option(str, "The team name", required = True), timeout_min = Option(int, "Time out (min)", required = False, default = 5)):
        if (team_name not in teams_dict):
            await ctx.respond("The team name is not exist.")
            return

        if (ctx.author.id not in teams_dict[team_name].leader_ids):
            await ctx.respond("Your are not the leader")
            return
        else:
            await ctx.send(f"Team {team_name} is hiring, press the button to try to join")
            Invite_bottun = my_ts.InviteUser(ctx.author, teams_dict[team_name])
            await ctx.respond(view=Invite_bottun)

    # 看 今日 check in out 紀錄
    @slash_command(name="get_checkinout_recent",description="Get users recent checkin")
    async def get_checkinout_recent(self, ctx, team_name: Option(str, "The team name", required = True)):
        if (team_name not in teams_dict):
            await ctx.respond("The team name is not exist.")
            return

        if (ctx.author.id not in teams_dict[team_name].leader_ids):
            await ctx.respond("Your are not the leader")
            return

        name_txt, checkin_txt, checkout_txt = '','',''

        for each_member in teams_dict[team_name].member:
            name_txt = name_txt + f"{each_member.name}" + '\n'
            if (each_member.id not in User_dict):
                checkin_txt  = checkin_txt  + f"no record" + '\n'
                checkout_txt = checkout_txt + f"no record" + '\n'
            else:   
                checkin_arr , checkout_arr = User_dict[each_member.id].get_user_check_in_record() , User_dict[each_member.id].get_user_check_ou_record()
                if (len(checkin_arr)!=0 and checkin_arr[-1]):
                    checkin_txt  = checkin_txt  + f"{checkin_arr[-1].strftime('%m-%d %X')}" + '\n'
                else:
                    checkin_txt  = checkin_txt  + f"No record" + '\n'


                if (len(checkout_arr)!=0 and checkout_arr[-1]):
                    checkout_txt  = checkout_txt + f"{checkout_arr[-1].strftime('%m-%d %X')}" + '\n'
                else:
                    checkout_txt  = checkout_txt  + f"No record" + '\n'


        embed = discord.Embed( title="Check in out record ")
        embed.add_field(name='Members'  , value=name_txt    ,inline=True)
        embed.add_field(name='Check in' , value=checkin_txt ,inline=True)
        embed.add_field(name='Check out', value=checkout_txt,inline=True)
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Team_manage(bot))


