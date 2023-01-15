import discord
from discord.ext import commands
from discord import option
from discord.ui import Button
import json
import io
# import keep_alive
import os
import asyncio
import random
import configs
import wavelink
#pip install PyNaCl
import platform

intents=discord.Intents.all()
bot = commands.Bot(intents=intents, permissions=8, command_prefix="/")
intents.members = True
connections = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Project Sekai: Colourfull Stage'))
    print(f"{bot.user.name} esta online!")
    print(f"Bot identifier: {str(bot.user.id)}")
    print(f"Discord Version: {str(discord.__version__)}")
    print(f"Python Version: {str(platform.python_version())}")

#Cogs / Modules
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(configs.Token())


# keep_alive.keep_alive()

# Mandar mensagem que ira receber as roles!


