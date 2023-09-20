import discord
import time
import sqlite3

from discord.ext import commands
from colorama import Fore


class BotModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Fore.YELLOW}`Bot Moderation cog` is ready!")


def setup(bot):
    bot.add_cog(BotModeration(bot))
