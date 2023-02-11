from datetime import datetime


import discord

class Team:
    def __init__(self):
        self.member = []
        self.leader = []

        self.member_ids = []
        self.leader_ids = []


        self.is_public = False
        self.need_per  = True

class ComfirmUserJoin(discord.ui.View):
    def __init__(self, author, team_class, user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.team_class = team_class
        self.author     = author
        self.user       = user

    @discord.ui.button(label="同意", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        self.team_class.member.append(self.user)
        self.team_class.member_ids.append(self.user.id)

        await self.user.send("Your invitations have been comfirm")
        await interaction.response.send_message("Sucessful !!")

    @discord.ui.button(label="不同意", row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await  self.user.send("Your invitations have been reject")
        await interaction.response.send_message("Reject !!")

class InviteUser(discord.ui.View):
    def __init__(self, author, team_class, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.author     = author
        self.team_class = team_class


    @discord.ui.button(label="我要加入!!", style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        # if (interaction.user.id in self.team_class.leader_ids or interaction.user.id in self.team_class.member_ids):
        #     await interaction.response.send_message("You are already in the team !!",ephemeral=True)
        #     return


        if (self.team_class.need_per):
            comfirm_button = ComfirmUserJoin(self.author, self.team_class, interaction.user)
            await self.author.send(f"User {interaction.user.name} wants to join you team", view=comfirm_button)
            await interaction.response.send_message("Has sent invitations for you",ephemeral=True)
        else:
            self.team_class.member.append(interaction.user)
            self.team_class.member_ids.append(interaction.user.id)
            await interaction.response.send_message("You have joined the team !!",ephemeral=True)

class CheckUsersInOut():
    def __init__(self, members, User_dict, isfile=True, *args, **kwargs):
        self.members   = members
        self.User_dict = User_dict
        self.member_name = [ self.members[i].name for i in range(len(self.members))]
        self.member_id = [ self.members[i].id for i in range(len(self.members))]


        options = [ discord.SelectOption(label=self.members[i].name)for i in range(len(self.members))]

        self.select = discord.ui.Select(
            placeholder = "All team member",
            min_values  = 1, 
            max_values  = 1,
            options = options
            )


        self.select.callback = self.callback

        self.view = discord.ui.View()
        self.view.add_item(self.select)


    async def callback(self, interaction):
        which_chosen = self.member_name.index(self.select.values[0])
        this_id      = self.member_id[which_chosen]

        checkin_arr , checkout_arr = self.User_dict[this_id].get_user_check_in_record() , self.User_dict[this_id].get_user_check_ou_record()
        checkin_txt  = ''
        checkout_txt = ''
        for ci, co in zip(checkin_arr , checkout_arr):


            if (ci):
                checkin_txt  = checkin_txt  + f"{ci.strftime('%m-%d %X')}" + '\n'
            else:
                checkin_txt  = checkin_txt  + f"No record" + '\n'


            if (co):
                checkout_txt  = checkout_txt + f"{co.strftime('%m-%d %X')}" + '\n'
            else:
                checkout_txt  = checkout_txt  + f"No record" + '\n'

        embed = discord.Embed( title=f"{self.member_name[which_chosen]} check in out record.")
        embed.add_field(name='Check in'  , value=checkout_txt    ,inline=True)
        embed.add_field(name='Check out' , value=checkout_txt ,inline=True)


        await interaction.response.send_message(embed=embed)

class VoteSection(discord.ui.View):
    def __init__(self, options, channel,*args, **kwargs):
        super().__init__(*args, **kwargs)

        self.channel        = channel
        self.all_vote       = {options[i]:0 for i in range(len(options))}
        self.options        = options
        self.vote_dict      = {}
        self.select_options = [ discord.SelectOption(label=options[i]) for i in range(len(options))]

        self.select = discord.ui.Select(
            placeholder = "All team member",
            min_values  = 1, 
            max_values  = 1,
            options = self.select_options
            )


        self.select.callback = self.this_callback

        self.add_item(self.select)

    async def on_timeout(self):
        # print('[*] timeout')
        for user, voted in self.vote_dict.items():
            self.all_vote[voted] += 1


        sorted_vote = sorted(self.all_vote.items(), key=lambda x:x[1],reverse=True)


        name, get = "", ""
        for i,j in sorted_vote:
            name = name + str(i) + '\n'
            get  = get  + str(j) + '\n'

        embed = discord.Embed( title=f"Vote result.")
        embed.add_field(name="Option"  , value=name    ,inline=True)
        embed.add_field(name="number of votes" , value=get ,inline=True)
        await self.channel.send(embed=embed)

    async def this_callback(self, interaction):
        # which_chosen = self.options.index(self.select.values[0])

        if (interaction.user.id in self.vote_dict):
            await interaction.response.send_message(f"Change your vote to {self.select.values[0]}", ephemeral=True)
        else:
            await interaction.response.send_message(f"You voted {self.select.values[0]}", ephemeral=True)

        self.vote_dict[interaction.user.id] = self.select.values[0]
        # self.all_vote[which_chosen] = self.all_vote[which_chosen] + 1 
        # self.vote_dict

class DecideVote(discord.ui.Modal):
    def __init__(self, channel, timeout_min ,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.timeout_min = timeout_min
        self.channel     = channel
        self.add_item(discord.ui.InputText(label="Vote Option (Split with chage line)", style=discord.InputTextStyle.long))


    async def callback(self, interaction: discord.Interaction):
        get_word = self.children[0].value.strip()
        if (len(get_word) == 0):
            await interaction.response.send_message(content=':white_check_mark: create a poll failed', ephemeral=True)
            return

        self.options = get_word.split("\n") 

        if (len(self.options) <= 1):
            await interaction.response.send_message(content=':white_check_mark: create a poll failed', ephemeral=True)
            return


        VoteS = VoteSection(self.options, self.channel, timeout=10)#self.timeout_min*60)

        await interaction.response.send_message(content=':white_check_mark:  You have successfully create a vote', view=VoteS)

        # await interaction.response.send_message(content=':white_check_mark:  You have successfully create a vote', ephemeral=True)

class AnoyOpion(discord.ui.Modal):
    def __init__(self, leader ,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.leader = leader
        self.add_item(discord.ui.InputText(label="Say anythings", style=discord.InputTextStyle.long))

    async def callback(self, interaction):
        get_word = self.children[0].value.strip()
        for each_leader in self.leader:
            await each_leader.send("From anonymous opinion:\n"+get_word)

        await interaction.response.send_message(content='Successful', ephemeral=True)

class Alarm:
    def __init__(self,member, ontime, text):
        self.member = member
        self.ontime = ontime
        self.text   = text
    async def check(self):
        today = datetime.now()

        today_mdh = today.month, today.day, today.hour

        if (today_mdh == self.ontime ):
            for each in self.member:
                await each.send(f"{today_mdh[0]}-{today_mdh[1]} {today_mdh[2]}  : {self.text} !!")
            return True
        return False

class KickMember:
    def __init__(self, members, teamname):
        self.members      = members
        self.member_name  = [ self.members[i].name for i in range(len(self.members))]
        self.member_name2 = [ self.members[i].name for i in range(len(self.members))]
        self.teamname     = teamname
        options = [ discord.SelectOption(label=self.member_name[i])for i in range(len(self.members))]

        self.select = discord.ui.Select(
            placeholder = "All team member",
            min_values  = 1, 
            max_values  = 1,
            options = options
            )
        self.select.callback = self.callback

        self.view = discord.ui.View()
        self.view.add_item(self.select)

    async def callback(self, interaction):
        if (self.select.values[0] not in self.member_name2):
            await interaction.response.send(f"{self.select.values[0]} has long been removed.")
            return
        which_chosen = self.member_name.index()
        self.options.pop(which_chosen)
        self.member_name2.remove(self.select.values[0] )

        await self.members[which_chosen].send(f'You were removed from {self.teamname}.')
        self.members.pop(which_chosen)
        self.members_ids.pop(which_chosen)

        await interaction.response.send(f"{self.select.values[0]} has been removed.")

class CheckAllTeam:
    def __init__(self, name, team_dict):
        self.team_dict = team_dict

        options = [ discord.SelectOption(label=name[i])for i in range(len(name))]

        self.select = discord.ui.Select(
            placeholder = "All public team",
            min_values  = 1, 
            max_values  = 1,
            options = options
            )


        self.select.callback = self.callback
        self.name = name
        self.view = discord.ui.View()
        self.view.add_item(self.select)

    async def callback(self,interaction):
        which_chosen = self.name.index(self.select.values[0])

        # if (not team_dict[self.select.values[0]].need_per):
        #     self.team_dict.member.append(interaction.user)
        #     await interaction.response.send(f"You joined {self.select.values[0]} successfully")
        #     return 

        # else:

        #     await interaction.response.send(f"You joined {self.select.values[0]} successfully")



        leader_ctx = self.team_dict[self.select.values[0]].leader[-1]
        team_class = self.team_dict[self.select.values[0]]

        if (team_class.need_per):
            comfirm_button = ComfirmUserJoin(leader_ctx , team_class, interaction.user)
            await leader_ctx.send(f"User {interaction.user.name} wants to join you team", view=comfirm_button)
            await interaction.response.send_message("Has sent invitations for you",ephemeral=True)
        else:
            team_class.member.append(interaction.user)
            team_class.member_ids.append(interaction.user.id)
            await interaction.response.send_message("You have joined the team !!",ephemeral=True)
