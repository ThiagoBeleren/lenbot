import discord
from discord.ext import commands
from discord.ui import Button, View

class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def button(self, ctx: commands.Context):
        #buttons
        button1 = Button(label="Click here",
                         style=discord.ButtonStyle.green,
                         emoji="👍")

        button2 = Button(label="Click here",
                         style=discord.ButtonStyle.green,
                         emoji="👍")
        view = View()
        view.add_item(button1)
        view.add_item(button2)

        #embeds
        E_button1 = discord.Embed(title="Esse eh o botao 1",
                                  description="botao 1")

        E_button2 = discord.Embed(title="Esse eh o botao 2",
                                  description="Botao 2")

        #buttons callback
        async def button1callback(interaction: discord.Interaction):
            await interaction.response.send_message(embed=E_button1)
        button1.callback = button1callback

        async def button2callback(interaction: discord.Interaction):
            await interaction.response.send_message(embed=E_button2, ephemeral=False)
        button2.callback = button2callback

        await ctx.respond(
            view=view
        )



def setup(bot):
  bot.add_cog(Buttons(bot))


