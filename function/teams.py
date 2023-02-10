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

    @discord.ui.button(label="不同意", row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await  self.user.send("Your invitations have been reject")




class InviteUser(discord.ui.View):
    def __init__(self, author, team_class, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.author     = author
        self.team_class = team_class


    @discord.ui.button(label="我要加入!!", style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        if (interaction.user.id in self.team_class.leader_ids or interaction.user.id in self.team_class.member_ids):
            await interaction.response.send_message("You are already in the team !!",ephemeral=True)
            return
        if (self.team_class.need_per):
            comfirm_button = ComfirmUserJoin(self.author, self.team_class, interaction.user)
            await self.author.send(f"User {interaction.user.name} wants to join you team", view=comfirm_button)
            await interaction.response.send_message("Has sent invitations for you",ephemeral=True)
        else:
            self.team_class.member.append(interaction.user)
            self.team_class.member_ids.append(interaction.user.id)
            await interaction.response.send_message("You have joined the team !!",ephemeral=True)


        