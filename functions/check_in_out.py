from utils import slash_command
import discord
from discord.commands import slash_command
from discord.ext import commands
from utils.info import User_dict
import utils.User as my_Us

class Check(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="checkin",description="check in")
    async def checkin(self, ctx): 
        print(f'[*] {ctx.author.name} try to check in')
        if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = my_Us.User(ctx.author)

        if (await User_dict[ctx.author.id].checkin()):

            await ctx.respond(f"{ ctx.author.name} check_in !")
        else:  
            await ctx.respond(f"you didn't check out last time")


    @slash_command(name="checkout",description="check out")
    async def checkout(self, ctx): 
        print(f'[*] {ctx.author.name} try to check out')
        if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = my_Us.User(ctx.author)

        if (await User_dict[ctx.author.id].checkout()):
            await ctx.respond(f"{ ctx.author.name} check out !")
        else:
            await ctx.respond(f"No check in record!!")
def setup(bot):
    bot.add_cog(Check(bot))
