import discord
from discord.ext import commands

'''
class SurveyModal(discord.ui.Modal, title="Survey"):
        name = discord.ui.InputText(label="Name")
        answer = discord.ui.InputText(label="Reason for joining", style=discord.InputTextStyle.paragraph)
        async def on_submit(self, interaction=discord.Interaction):
            await interaction.response.send_message(f"Submission sent, {self.name}", ephemeral=True)
'''
class SelectMenu(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Blue", emoji="👍", value="1",description="This is a blue label"),
            discord.SelectOption(label="Red", emoji="👍", value="2",description="This is a blue label"),
            discord.SelectOption(label="Green", emoji="👍", value="3",description="This is a blue label")
        ]
        super().__init__(placeholder="Choose a option", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "1":
            await interaction.response.send_message("VC escolheu a opcao Blue")
        elif self.values[0] == "2":
            await interaction.response.edit_message("VC escolheu a opcao Red")
        elif self.values[0] == "3":
            await interaction.response.send_message("VC escolheu a opcao Green")
        #await interaction.response.send_modal(SurveyModal())

class SelectView(discord.ui.View):
    def __init__(self, *, timeout=100):
        super().__init__(timeout=timeout)
        self.add_item(SelectMenu())

class MenuSelect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('COG MenuSelect READY!')

    @commands.slash_command(description="Select a option")
    async def option(self, ctx):
        await ctx.respond("choose an option", view=SelectView(), delete_after=15)

def setup(bot):
    bot.add_cog(MenuSelect(bot))