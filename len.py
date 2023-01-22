import discord
from discord.ext import commands
import os
import platform

intents = discord.Intents.all()
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


bot.run(os.environ['TOKEN'])

