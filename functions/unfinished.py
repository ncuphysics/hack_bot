from utils import slash_command
import discord
from discord.commands import slash_command, Option
from discord.ext import commands

class Not_Finished(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="joke",description="Talk a joke")
    async def joke(self, ctx):
        await ctx.respond("Let me think ...")
        await ctx.send( my_rd.prompt_openai('Q:請你說個笑話\nA:'))


    @slash_command(name="chickensoul",description="Chicken Soup for the Soul")
    async def ChickenSoul(self, ctx):
        await ctx.respond("Let me think ...")
        await ctx.send( my_rd.prompt_openai('Q:請你說個一句心靈雞湯\nA:'))


    @slash_command(name="ask",description="Ask me anything")
    async def ask(self, ctx,  text      : Option(str, "Question" , required = True)):
        await ctx.respond("Let me think ...")
        await ctx.send( my_rd.prompt_openai(f'你是心靈捕手,一個團隊協作的AI,同時也是我們的私人秘書。\nQ:{text}\nA:'))

    @slash_command(name="get_covid",description="Number of confirmed cases in Taiwan")
    async def get_covid(self, ctx):
        await ctx.respond(my_Cd.get_covid())

def setup(bot):
    bot.add_cog(Not_Finished(bot))
