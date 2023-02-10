from utils import slash_command
import discord
from discord.commands import slash_command
from discord.ext import commands
import requests
import json
import glob
import os

api_key = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-65BFD2A8-AA98-4D34-881B-CE6060B65444&locationName='

two_day_weater_req = requests.get(api_key)

jason_weather_content = two_day_weater_req.content.decode('utf-8')
jason_weather_dict = json.loads(jason_weather_content)


city_weater=[]

for location in jason_weather_dict['records']['location']:
    city_locate=location['locationName']
    #天氣狀態
    noon_weater_status = location['weatherElement'][0]['time'][1]['parameter']["parameterName"]
    night_weater_status = location['weatherElement'][0]['time'][2]['parameter']["parameterName"]
    #氣溫資訊
    noon_Maxtmp =location['weatherElement'][4]['time'][1]['parameter']["parameterName"]
    noon_Mintmp = location['weatherElement'][2]['time'][1]['parameter']["parameterName"]
    noon_temp_status=location['weatherElement'][3]['time'][1]['parameter']["parameterName"]
    
    night_Maxtmp =location['weatherElement'][4]['time'][2]['parameter']["parameterName"]
    night_Mintmp = location['weatherElement'][2]['time'][2]['parameter']["parameterName"]
    night_temp_status=location['weatherElement'][3]['time'][2]['parameter']["parameterName"]
    
    #降雨機率
    noon_pop = location['weatherElement'][1]['time'][1]['parameter']["parameterName"]
    night_pop = location['weatherElement'][1]['time'][2]['parameter']["parameterName"]
    
    #print([city_locate])
    #print(["白天:"+noon_weater_status,"最高溫:"+noon_Maxtmp+"度C 最低溫:"+noon_Mintmp+"度C",
    #       "降雨機率"+noon_pop+"%"])
    #print(["晚上:"+night_temp_status,"最高溫:"+night_Maxtmp+"度C 最低溫:"+night_Mintmp+"度C",
    #       "降雨機率"+night_pop+"%"])
    #輸入每筆城市的氣候資料
    #(城市名, 白天天氣舒適度, 白天最高溫, 白天最低溫, 白天降雨機率, 夜晚天氣舒適度, 夜晚天最高溫, 夜晚天最低溫, 夜晚天降雨機率 )
    city_weater.append([city_locate ,noon_weater_status , noon_Maxtmp, noon_Mintmp, noon_pop,night_temp_status, night_Maxtmp,
                       night_Mintmp,night_pop])
#print(len(city_weater))


class CheckWeatherMenu():
    def __init__(self,*args, **kwargs):
        options =[]
        self.city_locate=[]
        for i in range(len(city_weater)):
            options.append(discord.SelectOption(
                label=city_weater[i][0],
                #description="You choose city is "+city_weater[i][0]
                )
            )
            self.city_locate.append(city_weater[i][0])
        self.select = discord.ui.Select(
            placeholder = "你想查看明天的天氣的地點 ?",
            min_values =1,
            max_values =1,
            options = options
        )
        print(city_locate)
        self.view = discord.ui.View()
        self.view.add_item(self.select)
        self.folder_arr = city_weater
        self.select.callback = self.city_callback
        #self.select.callback = 
    async def city_callback(self, interaction):
        which_chosen = self.city_locate.index(self.select.values[0])
        city_weater_arr_len=len(city_weater)
        if(which_chosen<=city_weater_arr_len):
            city_name=city_weater[which_chosen][0]
            noon_temp_status=city_weater[which_chosen][1]
            noon_Maxtmp=city_weater[which_chosen][2]
            noon_Mintmp=city_weater[which_chosen][3]
            noon_pop=city_weater[which_chosen][4]
            night_temp_status=city_weater[which_chosen][5]
            night_Maxtmp=city_weater[which_chosen][6]
            night_Mintmp=city_weater[which_chosen][7]
            night_pop=city_weater[which_chosen][8]

            await interaction.response.send_message(f"城市: "+city_name)
            await interaction.channel.send(f"白天: {noon_temp_status},最高溫: {noon_Maxtmp}度C,最低溫: {noon_Mintmp}度C, 降雨機率: {noon_pop}%")
            await interaction.channel.send(f"晚上: {night_temp_status},最高溫: {night_Maxtmp}度C,最低溫: {night_Mintmp}度C, 降雨機率: {night_pop}%")
            if(eval(noon_pop) >= 70 or eval(night_pop)>= 70):
                await interaction.channel.send(f"記得帶傘")
            else:
                await interaction.channel.send(f"早晚降雨機率極低")

        else:
            await interaction.channel.send(f"Code has BUG")
        
        



class Weather(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command(name="weather",description="Weather information for each region")
    async def weather(self, ctx):
        city_table = []
        weather_Meun = CheckWeatherMenu(city_table)
        await ctx.respond("====== weather ======", view=weather_Meun.view, ephemeral=True)

def setup(bot):
    bot.add_cog(Weather(bot))

