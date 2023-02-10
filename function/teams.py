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






















