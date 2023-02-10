# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 14:32:06 2023

@author: user
"""

import discord

fun = ['Check in/out','Team','Record','Music','Whether','Order drink','Clock and Timer','Note','Joke','Travel']
fun2 = [
""":sun_with_face:  **CHECKIN** :first_quarter_moon_with_face: **CHECKOUT**
\t\t-The Check in out function can provide automated registration, login and logout services, and provide detailed login records.
\t\t-Allowing the team to manage and monitor user activities more easily.
\t\t-Allowing you to manage and monitor user activities more effectively.
""",
""":right_facing_fist::left_facing_fist: **Team**
\t\t-Leader can create the team and set whether it is free to join and public.
\t\t-Leader can view check-in/out records, conduct public opinion polls, send broadcast, set meeting time, and kick someone out.
\t\t-Member can set status, send anonymous comments, and leave the group.
""",
""":speaking_head:  **RECORD**
\t\t-You can record your meeting sound.
\t\t-You can get the summarize of the meeting.
""",
""":headphones:  **Music** 
\t\t-You can let the robot play music on the youtube.
\t\t-You can pause, play, list, leave, clear, skip, and loop any music.
""",
""":sunny:  **Weather**
\t\t-You can get the weather forecast for the day
""",
""":champagne_glass: **ORDER DRINK**
\t\t-You can create and stop a drink order.
\t\t-Other users can enter what they want to drink.
\t\t-In the end you will receive all the drinks entered by the user.
""",
""":alarm_clock:  **Alarm clock and Countdown timer**
\t\t-You can set the reminder at a certain time or countdown timer.
""",
""":ledger:  **Note**
\t\t-You can create and write your own notes.
""",
""":clown:  **Joke**
\t\t-You can get some jokes to relax.
""",
""":airplane:  **Travel**
\t\t-You can start a campaign and find out if anyone want to attend.
"""
]

class HelpSelection():
    def __init__(self,*args, **kwargs):
        options =[]
        self.city_locate=[]
        for i in range(len(fun)):
            options.append(discord.SelectOption(
                label=fun[i],
                #description="You choose city is "+city_weater[i][0]
                )
                )
            self.city_locate.append(fun[i])
        self.select = discord.ui.Select(
            placeholder = "Which function do you want to know?",
            min_values =1,
            max_values =1,
            options = options
        )

        self.view = discord.ui.View()
        self.view.add_item(self.select)
        self.select.callback = self.city_callback

    async def city_callback(self, interaction):
        which_chosen = self.city_locate.index(self.select.values[0])
        city_weater_arr_len=len(fun)
        if(which_chosen<=city_weater_arr_len):
            await interaction.response.send_message(fun2[which_chosen])
        else:
            await interaction.channel.send(f"Code has BUG")
