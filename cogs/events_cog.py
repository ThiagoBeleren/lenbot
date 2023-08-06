import discord
from discord.ext import commands


class Events(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_member_join(self, member):
    guild = member.guild  # guild = server
    welcome_channel = member.guild.system_channel
    
    if guild.id == 1135982907043889192: #Server jogadinhas
      embed = discord.Embed(
        description=f":partying_face: Bem vindo ao servidor, {member.mention}. \n"
        f"Espero que se divirta por aqui. \n"
        f"Você é o **{len(guild.members)}** participante do servidor. \n")
      embed.set_author(name=member.display_name, icon_url=member.display_avatar)
      embed.set_footer(text="ID \n"
                      f"{member.id}")
      embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1135982909237493853/1135990644536512562/tenor.gif"
      )
      await welcome_channel.send(embed=embed)
      print(f'{member.mention}, entrou no servidor')
      
    else:
      embed = discord.Embed(
          description=f":partying_face: Bem vindo ao servidor, {member.mention}. \n"
          f"Espero que se divirta por aqui. \n"
          f"Você é o **{len(guild.members)}** participante do servidor. \n")
      embed.set_author(name=member.display_name, icon_url=member.display_avatar)
      embed.set_footer(text="ID \n"
                        f"{member.id}")
      embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/996151321096892636/997995707615162388/tenor.gif"
      )
      await welcome_channel.send(embed=embed)
      print(f'{member.mention}, entrou no servidor')

  @commands.Cog.listener()
  @commands.has_permissions(administrator=True)
  async def on_raw_reaction_add(self, payload):
    member = payload.member
    guild = member.guild
    emoji = payload.emoji.name
    role_message_id = 999072734954921994 
    role_message_id2 = 0#jogadinhas
     
    if role_message_id == payload.message_id:

      if emoji == '💻':
        role = discord.utils.get(guild.roles, name="Programadores 💻")

      if emoji == '👑':
        role = discord.utils.get(guild.roles, name="Anime_Fan 👑")

      if emoji == '🎶':
        role = discord.utils.get(guild.roles, name="Just_Chill 🎶")

      if emoji == "🏠":
        role = discord.utils.get(guild.roles, name="Rioters 🏠")

      if emoji == "🏆":
        role = discord.utils.get(guild.roles, name="Indie 🏆")

      if emoji == '🎵':
        role = discord.utils.get(guild.roles, name="Rhythm_Games 🎵")

      if emoji == '🕹️':
        role = discord.utils.get(guild.roles, name='Casual 🕹️')

      if emoji == '⚔️':
        role = discord.utils.get(guild.roles, name='Competitivo ⚔️')

      if emoji == '🔫':
        role = discord.utils.get(guild.roles, name="FPS 🔫")

      if emoji == '🎲':
        role = discord.utils.get(guild.roles, name="RPG 🎲")

    await member.add_roles(role)

  @commands.Cog.listener()
  @commands.has_permissions(administrator=True)
  async def on_raw_reaction_remove(self, payload):
    role_message_id = 999072734954921994
    if role_message_id == payload.message_id:
      guild = await (self.bot.fetch_guild(payload.guild_id))
      emoji = payload.emoji.name

      if emoji == '💻':
        role = discord.utils.get(guild.roles, name="Programadores 💻")

      if emoji == '👑':
        role = discord.utils.get(guild.roles, name="Anime_Fan 👑")

      if emoji == '🎶':
        role = discord.utils.get(guild.roles, name="Just_Chill 🎶")

      if emoji == "🏠":
        role = discord.utils.get(guild.roles, name="Rioters 🏠")

      if emoji == "🏆":
        role = discord.utils.get(guild.roles, name="Indie 🏆")

      if emoji == '🎵':
        role = discord.utils.get(guild.roles, name="Rhythm_Games 🎵")

      if emoji == '🕹️':
        role = discord.utils.get(guild.roles, name='Casual 🕹️')

      if emoji == '⚔️':
        role = discord.utils.get(guild.roles, name='Competitivo ⚔️')

      if emoji == '🔫':
        role = discord.utils.get(guild.roles, name="FPS 🔫")

      if emoji == '🎲':
        role = discord.utils.get(guild.roles, name="RPG 🎲")

      member = await (guild.fetch_member(payload.user_id))

      if member is not None:
        await member.remove_roles(role)
      else:
        print('Usuario Nao encontrado! :(')


def setup(bot):
  bot.add_cog(Events(bot))
