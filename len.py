import discord
import os
import platform
import configs

from discord.ext import commands
from colorama import Fore


intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(intents=intents, permissions=8, command_prefix="/")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Project Sekai: Colourfull Stage'))
    print(f"{Fore.BLUE} {bot.user.name} esta online!")
    print(f"{Fore.BLUE} Bot identifier: {str(bot.user.id)}")
    print(f"{Fore.BLUE} Discord Version: {str(discord.__version__)}")
    print(f"{Fore.BLUE} Python Version: {str(platform.python_version())}")

# Cogs / Modules
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(configs.Token())
