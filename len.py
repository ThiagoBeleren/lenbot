import discord
from discord.ext import commands
from discord import option
from discord.ui import Button
import json
#from PIL import Image, ImageFont, ImageDraw, ImageOps
import io
# import keep_alive
import os
import asyncio
import random
import configs
#py -3.9 -m pip install -U Wavelink
import wavelink
#pip install PyNaCl

intents=discord.Intents.all()
bot = commands.Bot(intents=intents, permissions=8, command_prefix="/")
intents.members = True
lenbot = bot.get_user(991165635356794881)
connections = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Project Sekai: Colourfull Stage'))
    print(f"{bot.user.name} esta online!")

#Cogs / Modules
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(configs.Token())


# keep_alive.keep_alive()

# Mandar mensagem que ira receber as roles!

"""
@bot.slash_command()
@commands.has_permissions(administrator=True)
async def roles(ctx):
    
        role_channel = bot.get_channel(911064432472367154)
        embed = discord.Embed(description="**Pegue algum cargo!** \n Mencione algum destes cargos para interagir com membros de mesmo gosto", colour=15844367)
        embed.set_image(url="https://cdn.discordapp.com/attachments/996151321096892636/999071769279353023/tenor_1.gif")
        embed.add_field(name="💻- Programadores", value="Gosta de criar")
        embed.add_field(name="👑- Anime Fan", value='Anime fan')
        embed.add_field(name="🎶- Just Chill", value="Gosta de interajir")
        embed.add_field(name="🏠- Jogador da dona RIOT", value='Jogar jogos da Riot')
        embed.add_field(name="🎵- Rhythm Games", value="Jogos de Musica")
        embed.add_field(name="🏆- Jogador de Indies", value="Jogos Independentes")
        embed.add_field(name="🕹️- Jogador Casual", value="Companhia pra jogar")
        embed.add_field(name="⚔️- Jogador de ranked", value="Companhia pra ranked")
        embed.add_field(name="🔫- Jogador de FPS", value="Jogar jogos de tiro")
        embed.add_field(name="🎲- Jogador de RPG", value="Jogador de RPG de mesa, grupo ou video-game")
        reaction = await role_channel.send(embed=embed)
    
        await reaction.add_reaction('💻')
        await reaction.add_reaction('👑')
        await reaction.add_reaction('🎶')
        await reaction.add_reaction('🏠')
        await reaction.add_reaction('🏆')
        await reaction.add_reaction('🎵')
        await reaction.add_reaction('🕹️')
        await reaction.add_reaction('⚔️')
        await reaction.add_reaction('🔫')
        await reaction.add_reaction('🎲')
"""
