from utils import slash_command
import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from utils.info import connections
import os

import utils.Record       as my_rd

PRIVATE_RECORD_FOLDER = "data/private_recorded"
PUBLIC_RECORD_FOLDER  = "data/public_recorded"
os.makedirs(PRIVATE_RECORD_FOLDER, exist_ok=True)
os.makedirs(PUBLIC_RECORD_FOLDER , exist_ok=True)

class Record(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="public_record",description="Start a public record")
    async def public_record(self, ctx, name: Option(str, "The name of meeting", required = False, default = None)):
        voice = ctx.author.voice
        if not voice:
            await ctx.respond("You aren't in a voice channel!")
            return
        vc = await voice.channel.connect()
        connections.update({ctx.guild.id: vc})

        SRS = my_rd.StopRecordSave(os.path.join(PUBLIC_RECORD_FOLDER,str(ctx.guild.id)),name, self)

        vc.start_recording(
            discord.sinks.WaveSink(),  # The sink type to use.
            # discord.Sink(encoding='wav', filters={'time': 0}),
            SRS.once_done,  # What to do once done.
            ctx.channel  # The channel to disconnect from.
        )

        await ctx.respond("====== Start a public recording ====== :speaking_head: :speech_balloon:\n",view=my_rd.StopRecordButton(voice_channel=vc,text_channel=ctx.channel,timeout=None))

    @slash_command(name="private_record",description="Start a private record")
    async def private_record(self, ctx, name: Option(str, "The name of meeting", required = False, default = None)):
        voice = ctx.author.voice
        if not voice:
            await ctx.respond("You aren't in a voice channel!")
            return

        vc = await voice.channel.connect()
        connections.update({ctx.guild.id: vc})

        SRS = my_rd.StopRecordSave(os.path.join(PRIVATE_RECORD_FOLDER,str(ctx.guild.id)), name, self)

        vc.start_recording(
            discord.sinks.WaveSink(),  # The sink type to use.
            # discord.Sink(encoding='wav', filters={'time': 0}),
            SRS.once_done,  # What to do once done.
            ctx.channel  # The channel to disconnect from.
        )

        await ctx.respond("====== Start a private recording ====== :speaking_head: :speech_balloon:\n",view=my_rd.StopRecordButton(voice_channel=vc,text_channel=ctx.channel,timeout=None))

    @slash_command(name="check_record_summary",description="Check summarized record")
    async def check_record_summary(self, ctx):
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

        CRM = my_rd.CheckRecordMenu(availble_time, corresponding_folders,False, self)
        

        await ctx.respond("Choose a record!   🟢:Public    🔴:Private", view=CRM.view, ephemeral=True)
        # await ctx.respond("====== check_record ======")

    @slash_command(name="check_record_file",description="Check record file")
    async def check_record_file(self, ctx):
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

        CRM = my_rd.CheckRecordMenu(availble_time, corresponding_folders,True, self)
        

        await ctx.respond("Choose a record!   🟢:Public    🔴:Private", view=CRM.view, ephemeral=True)

def setup(bot):
    bot.add_cog(Record(bot))
