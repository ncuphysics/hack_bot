from datetime import datetime


import threading 
import asyncio
import discord
import time



## Modal after button pushed
class Drink_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="飲料品項"))
        self.add_item(discord.ui.InputText(label="客製化(甜度冰塊)", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="價格", style=discord.InputTextStyle.long))

        self.all_drinks  = []
        self.total_price = 0

    async def callback(self, interaction: discord.Interaction):
        if  (not self.children[2].value.isnumeric()):
            await interaction.response.send_message(content=':no_entry_sign: Error : The price should be a number !!!', ephemeral=True)
            return


        embed = discord.Embed(title="你的飲料 :tropical_drink: ")
        embed.add_field(name="飲料"   , value=self.children[0].value)
        embed.add_field(name="客製化" , value=self.children[1].value)
        embed.add_field(name="價格" , value=self.children[2].value)

        self.all_drinks.append([interaction.user.name,self.children[0].value, self.children[1].value,int(self.children[2].value)])
        self.total_price += eval(self.children[2].value)

        await interaction.user.send(embeds=[embed]) # 思訓 
        await interaction.response.send_message(content=':white_check_mark:  You have successfully order your drink :tropical_drink: , please check your message', ephemeral=True)




## button for order drink
class OrderDrink(discord.ui.View):

    def __init__(self, author, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.modal  = Drink_modal(title='Drinks')
        self.author = author

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        text = ""

        embed = discord.Embed( title="飲料單:tropical_drink: ")

        name_text = ""
        drin_text = ""
        pric_text = ""
        for order in self.modal.all_drinks:
            name_text = name_text + order[0] + '\n'
            drin_text = drin_text + f'{order[1]}-{order[2]}\n'
            pric_text = pric_text + f'{order[3]}' + '\n'

        embed.add_field(name='名稱', value=name_text,inline=True)
        embed.add_field(name='飲料', value=drin_text,inline=True)
        embed.add_field(name='價格', value=pric_text,inline=True)


        embed.add_field(name='總價格 $$', value=f'{self.modal.total_price }')
        await self.author.send(embed = embed)


        await self.message.edit(content="The drink order is finish. :sob: :sob: :sob: ", view=self)


    @discord.ui.button(label="我要訂飲料!!", style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        # await interaction.user.send('Please enter the drink you want to drink')
        await interaction.response.send_modal(self.modal)
        # await interaction.response.send(f"A drink order is initiated !!", view=self)