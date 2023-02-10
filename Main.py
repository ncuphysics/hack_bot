from discord.commands     import Option
from discord.ext          import commands
from datetime             import datetime
from pathlib              import Path

import OrderDrink   as my_od # my class
import Record       as my_rd # my class
import User         as my_Us # my class

import discord
import time
import glob
import os

# pip install py-cord   

testing_guild = [597757976920588288, 1071431018701144165]
client = commands.Bot()

User_dict   = {}  ##   {userid : userclass }k
orders      = {}
teams       = {}

PRIVATE_RECORD_FOLDER = "private_recorded"
PUBLIC_RECORD_FOLDER = "public_recorded"
os.makedirs(PRIVATE_RECORD_FOLDER, exist_ok=True)
os.makedirs(PUBLIC_RECORD_FOLDER , exist_ok=True)

TEAM_FILE_NAME = "teams.json"

print("Start server")

@client.event
async def on_ready():
    print('目前登入身份：', client.user)


@client.slash_command(name="checkin",description="check in",guild_ids=testing_guild)
async def checkin(ctx): 
    print(f'[*] {ctx.author.name} try to check in')
    if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = my_Us.User(ctx.author)

    if (await User_dict[ctx.author.id].checkin()):

        await ctx.respond(f"{ ctx.author.name} check_in !")
    else:  
        await ctx.respond(f"you didn't check out last time")



@client.slash_command(name="checkout",description="check out",guild_ids=testing_guild)
async def checkout(ctx): 
    print(f'[*] {ctx.author.name} try to check out')
    if (ctx.author.id not in User_dict):User_dict[ctx.author.id] = my_Us.User(ctx.author)

    if (await User_dict[ctx.author.id].checkout()):
        await ctx.respond(f"{ ctx.author.name} check out !")
    else:
        await ctx.respond(f"No check in record!!")


@client.slash_command(name="order_drink",description="Order a drink (default 5 minute time out)",guild_ids=testing_guild)
async def order_drink(ctx,  timeout_min: Option(int, "Time out (min)", required = False, default = 5)):


    ## send menu
    await ctx.send('======= Menu =======')
    with open("menu.png", "rb") as fh:
        f = discord.File(fh, filename='menu.png')
    await ctx.send(file=f)



    print(f"[*] {ctx.author.name} initialize a drink order with timeout :",timeout_min )

    ## 按鈕
    this_order = my_od.OrderDrink(author = ctx.author, timeout=timeout_min*60)
    orders[ctx.author.id] = this_order

    await ctx.response.send_message(f"{ctx.author.mention} :exclamation: You can use a :stop_button: /stop_order_drink :stop_button:  command to close the order anytime you want.", ephemeral=True)
    await ctx.send(f"@everyone!!  {ctx.author.mention} open a drink order", view=this_order)



############################################################ Record ############################################################

@client.slash_command(name="stop_order_drink",description="Stop the drink order",guild_ids=testing_guild)
async def stop_order_drink(ctx):
    if (ctx.author.id not in orders):
        await ctx.response.send_message('You didn\'t open any drink order',ephemeral=True)
    await orders[ctx.author.id].on_timeout()
    await ctx.response.send_message(f"You have stop the order", ephemeral=True)
    del orders[ctx.author.id]


@client.slash_command(name="public_record",description="Start a public record",guild_ids=testing_guild)
async def public_record(ctx, name: Option(str, "The name of meeting", required = False, default = None)):
    voice = ctx.author.voice
    if not voice:
        await ctx.respond("You aren't in a voice channel!")
        return
    vc = await voice.channel.connect()
    # connections.update({ctx.guild.id: vc})

    SRS = my_rd.StopRecordSave(os.path.join(PUBLIC_RECORD_FOLDER,str(ctx.guild.id)),name)

    vc.start_recording(
        discord.sinks.WaveSink(),  # The sink type to use.
        # discord.Sink(encoding='wav', filters={'time': 0}),
        SRS.once_done,  # What to do once done.
        ctx.channel  # The channel to disconnect from.
    )

    await ctx.respond("====== Start a public recording ====== :speaking_head: :speech_balloon:\n",view=my_rd.StopRecordButton(voice_channel=vc,text_channel=ctx.channel,timeout=None))

@client.slash_command(name="private_record",description="Start a private record",guild_ids=testing_guild)
async def private_record(ctx, name: Option(str, "The name of meeting", required = False, default = None)):
    voice = ctx.author.voice
    if not voice:
        await ctx.respond("You aren't in a voice channel!")
        return
    vc = await voice.channel.connect()
    # connections.update({ctx.guild.id: vc})

    SRS = my_rd.StopRecordSave(os.path.join(PRIVATE_RECORD_FOLDER,str(ctx.guild.id)), name)

    vc.start_recording(
        discord.sinks.WaveSink(),  # The sink type to use.
        # discord.Sink(encoding='wav', filters={'time': 0}),
        SRS.once_done,  # What to do once done.
        ctx.channel  # The channel to disconnect from.
    )

    await ctx.respond("====== Start a private recording ====== :speaking_head: :speech_balloon:\n",view=my_rd.StopRecordButton(voice_channel=vc,text_channel=ctx.channel,timeout=None))

@client.slash_command(name="check_record_summary",description="Check summarized record",guild_ids=testing_guild)
async def check_record_summary(ctx):
    guild_id = str(ctx.guild.id)
    user_id  = ctx.author.id


    private_folders  = os.path.join(PRIVATE_RECORD_FOLDER,guild_id )
    public_folders   = os.path.join(PUBLIC_RECORD_FOLDER,guild_id  )

    availble_time         = []
    corresponding_folders = []

    if os.path.isdir(public_folders): 
        availble_time = os.listdir(public_folders)
        corresponding_folders = [os.path.join(public_folders,i) for i in availble_time]


    if os.path.isdir(private_folders): 
        # find avalible private
        for each_private_time in os.listdir(private_folders):
            this_time_folder = os.path.join(private_folders,each_private_time)
            if (f'{user_id}.wav' in os.listdir(this_time_folder)):
                availble_time.append(each_private_time)
                corresponding_folders.append(this_time_folder)

    

    if (len(availble_time) == 0):
        await ctx.respond("you haven't recorded any audio")
        return

    CRM = my_rd.CheckRecordMenu(availble_time, corresponding_folders,False)
    

    await ctx.respond("Choose a record!   🟢:Public    🔴:Private", view=CRM.view, ephemeral=True)
    # await ctx.respond("====== check_record ======")


@client.slash_command(name="check_record_file",description="Check record file",guild_ids=testing_guild)
async def check_record_file(ctx):
    guild_id = str(ctx.guild.id)
    user_id  = ctx.author.id


    private_folders  = os.path.join(PRIVATE_RECORD_FOLDER,guild_id )
    public_folders   = os.path.join(PUBLIC_RECORD_FOLDER,guild_id  )

    availble_time         = []
    corresponding_folders = []

    if os.path.isdir(public_folders): 
        availble_time = os.listdir(public_folders)
        corresponding_folders = [os.path.join(public_folders,i) for i in availble_time]


    if os.path.isdir(private_folders): 
        # find avalible private
        for each_private_time in os.listdir(private_folders):
            this_time_folder = os.path.join(private_folders,each_private_time)
            if (f'{user_id}.wav' in os.listdir(this_time_folder)):
                availble_time.append(each_private_time)
                corresponding_folders.append(this_time_folder)

    

    if (len(availble_time) == 0):
        await ctx.respond("you haven't recorded any audio")
        return

    CRM = my_rd.CheckRecordMenu(availble_time, corresponding_folders)
    

    await ctx.respond("Choose a record!   🟢:Public    🔴:Private", view=CRM.view, ephemeral=True)


#######################################################################################################################




##################################################### Team ############################################################


# 開始一個 team
# 提供所有人加入  

@client.slash_command(name="create_team",description="Create team",guild_ids=testing_guild)
async def create_team(ctx,  team_name: Option(str, "The team name", required = True)):
    ## Create a team  
    ## check if teamname exist

    await ctx.respond("====== Create team ======")

# 看check in out 紀錄
@client.slash_command(name="get_checkinout",description="Get users checkin",guild_ids=testing_guild)
async def get_checkinout(ctx):
    ## check if user is any team leader
    ## choose each team


    await ctx.respond("====== checkin_record ======")


# 分派工作
@client.slash_command(name="teamwork",description="Assign work to users",guild_ids=testing_guild)
async def teamwork(ctx):

    ## check if user is any team leader
    ## choose each team

    await ctx.respond("====== teamwork ======")


# 問團隊隊員現在的任務
@client.slash_command(name="member_current_tasks",description="Ask the team members about their current tasks",guild_ids=testing_guild)
async def member_current_tasks(ctx):

    ## check if user is any team leader
    ## choose each team

    await ctx.respond("====== member_current_tasks ======")


@client.slash_command(name="teamkick",description="kick a member off the team",guild_ids=testing_guild)
async def teamkick(ctx):

    ## check if user is any team leader
    ## choose each team

    await ctx.respond("====== teamkick ======")



# 匿名回覆意見
@client.slash_command(name="anonymous_opinion",description="Allow members to comments anonymously",guild_ids=testing_guild)
async def anonymous_opinion(ctx):
    ctx.author.se
    ## check if user in any team

    await ctx.respond("====== anonymousopinion ======")


# 訂會議室
@client.slash_command(name="book_meeting",description="Let user book a meeting",guild_ids=testing_guild)
async def book_meeting(ctx):
    
    ## check if user is a team leader, set a alarm to user



    await ctx.respond("====== BookMeeting ======")


#######################################################################################################################



############################################################ Information ###############################################

# get weather
@client.slash_command(name="weather",description="Weather information for each region",guild_ids=testing_guild)
async def weather(ctx):
    await ctx.respond("====== weather ======")



# get stock
@client.slash_command(name="stock",description="Get stock information",guild_ids=testing_guild)
async def stock(ctx):

    

    await ctx.respond("====== stock ======")


# get earthquake
@client.slash_command(name="earthquake",description="Get earthquake information",guild_ids=testing_guild)
async def earthquake(ctx):

    

    await ctx.respond("====== earthquake ======")

########################################################################################################################



@client.slash_command(name="help",description="Shows help for the bot",guild_ids=testing_guild)
async def help(ctx):

    # embed = discord.Embed( title="Command", description="I'm a bot that could help you to works with your teams")

    # embed.add_field(name= "checkin"     , value="Check in"                 , inline=True)
    # embed.add_field(name= "checkout"    , value="Check out"                , inline=True)
    # embed.add_field(name= "order_drink" , value="Create a drink order"                  )
    # embed.add_field(name= "record"      , value="record yor meeting sound"              )

    text = """:sun_with_face:  **CHECKIN** :first_quarter_moon_with_face: **CHECKOUT**
\t\t-The Check in out function can provide automated registration, login and logout services, and provide detailed login records
\t\t-Allowing the team to manage and monitor user activities more easily.
\t\t-Allowing you to manage and monitor user activities more effectively.

:champagne_glass: **ORDER DRINK**
\t\t-You can create a drink order.
\t\t-Other users can enter what they want to drink.
\t\t-In the end you will receive all the drinks entered by the user.

:speaking_head: **RECORD**
\t\t-You can record your meeting sound, and get the summarize of the meeting.
\t\t-private record       : Start a private recording, and the subsequent summary will only be available to those in the voice room (it is recommended to lock the room)
\t\t-public record        : Open a public recording, everyone in this server can access.
\t\t-check record summary : Can check all your accessible recordings, and call up the summary conclusion.
\t\t-check record file    : Can check all your accessible recordings, and download the audio.

:office_worker: **get_checkinout**
\t\t-The team leader can check the team member check in-out record.

:man_teacher: **Team**
\t\tYou can create your team, manage your team members, assign tasks, check in and out status.
\t\t-get checkinout       : The team leader can check the team member check in-out record.
\t\t-teamwork             : You can use this command to let the robot help you assign tasks to team members.
\t\t-member current tasks : Do you find it troublesome to private message each team member? Let the robot help you ask, and I can help you ask every member under you.
\t\t-teamkick             : Remove member.
\t\t-anonymous_opinion    : Each member has the ability to express their opinions anonymously, which makes a team grow.


"""
    await ctx.send(text)


# client.run(os.getenv('DISCORD_TOKEN'))

client.run('')
