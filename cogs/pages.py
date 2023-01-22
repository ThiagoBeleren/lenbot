import discord
from discord.ext import commands
from discord.ui import Button, View


class Pages(commands.Cog):
  current_page = 0
  buttons = []

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"Cog pages Ready!")

  async def send(self, ctx):
    self.message = await ctx.respond(view=self)
    await self.update_message(self.data[:self.sep])

  def create_embed(self, data):
    embed = discord.Embed(title="example")
    for item in data:
      embed.add_field(name=item, value=item, inline=False)
    return embed

  async def update_message(self, data):
    await self.message.edit(embed=self.create_embed(data), view=self)

  def update_buttons(self):
    if self.current_page == 1:
      self.home.disabled = True
      self.back.disabled = True
    else:
      self.home.disabled = False
      self.back.disabled = False

  @discord.ui.button(emoji='⏮️', style=discord.ButtonStyle.primary)
  async def home(self, interaction: discord.Interaction,
                 button: discord.ui.button):
    await interaction.response.defer()
    self.current_page = 1
    until_item = self.current_page * self.sep
    from_item = until_item - self.sep
    await self.update_message(self.data[:until_item])

  @discord.ui.button(emoji='⏪', style=discord.ButtonStyle.primary)
  async def back(self, interaction: discord.Interaction,
                 button: discord.ui.button):
    await interaction.response.defer()
    self.current_page -= 1
    until_item = self.current_page * self.sep
    from_item = until_item - self.sep
    await self.update_message(self.data[from_item:until_item])

  @discord.ui.button(emoji='⏩', style=discord.ButtonStyle.primary)
  async def next(self, interaction: discord.Interaction,
                 button: discord.ui.button):
    await interaction.response.defer()
    self.current_page += 1
    until_item = self.current_page * self.sep
    from_item = until_item - self.sep
    await self.update_message(self.data[from_item:until_item])

  @discord.ui.button(emoji='⏭️', style=discord.ButtonStyle.primary)
  async def end(self, interaction: discord.Interaction,
                button: discord.ui.button):
    await interaction.response.defer()
    self.current_page = int(len(self.data / self.sep)) + 1
    until_item = self.current_page * self.sep
    from_item = until_item - self.sep
    await self.update_message(self.data[from_item:])

  @commands.slash_command()
  async def page(self, interaction):
    page1 = discord.Embed(title="page 1", description="page 1")
    page2 = discord.Embed(title="page 2", description="page 2")
    page3 = discord.Embed(title="page 3", description="page 3")


def setup(bot):
  bot.add_cog(Pages(bot))
