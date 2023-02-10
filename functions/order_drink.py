from utils import slash_command
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from utils.OrderDrink  import OrderDrink
from utils.info import orders

class Order_drink(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="order_drink",description="Order a drink (default 5 minute time out)")
    async def order_drink(self, ctx,  timeout_min: Option(int, "Time out (min)", required = False, default = 5)):


        ## send menu
        await ctx.send('======= Menu =======')
        menu_id = 1
        with open(f"data/drink_menu/{menu_id}.png", "rb") as fh:
            f = discord.File(fh, filename='menu.png')
        await ctx.send(file=f)



        print(f"[*] {ctx.author.name} initialize a drink order with timeout :",timeout_min )

        ## 按鈕
        this_order = OrderDrink(author = ctx.author, timeout=timeout_min*60)
        orders[ctx.author.id] = this_order

        await ctx.response.send_message(f"{ctx.author.mention} :exclamation: You can use a :stop_button: /stop_order_drink :stop_button:  command to close the order anytime you want.", ephemeral=True)
        await ctx.send(f"@everyone!!  {ctx.author.mention} open a drink order", view=this_order)


def setup(bot):
    bot.add_cog(Order_drink(bot))
