import discord
import asyncio
import re
import os
import json 

from discord.ext import commands
from asyncio import run_coroutine_threadsafe
from discord import option
from discord.ui import Button, View, Select
from urllib import parse, request
from youtube_dl import YoutubeDL

class Music(commands.Cog):
  def ___init__(self, bot):
    self.bot = bot
    bot = commands.Bot(command_prefix="/")

    self.is_playing = {}
    self.is_paused = {}
    self.music_queue = {}
    self.queue_index = {}

    self.YTDL_OPTIONS = {'format': 'bestaudio', 'nonplaylist' : 'True'}
    self.FFMPEG_OPTIONS = {'before_options': 'reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    self.vc = {}

  @commands.Cog.listener()
  async def on_ready(self):
    for guild in self.bot.guilds:
      id = self.bot.get_guild(int(guild.id))
      self.music_queue[id] = []
      self.queue_index[id] = 0
      self.vc[id] = None
      self.is_paused[id] = self.is_playing[id] = False

  async def join(self, ctx, channel):
    try: 
      id = int(ctx.guild.id)
      if self.vc[id] == None or not self.vc[id].is_connected():
        self.vc[id] = await channel.connect()
        await self.vc[id].move_to(channel)
    except: 
      await ctx.respond("Nao foi possivel conectar ao canal de voz")

  def search(self, search):
    query = parse.urlenconde({'search_query': search})
    htmlContent = request.urlopen('https://www.youtube.com/results?' + query)
    searchResults = re.findall(f"/watch\?v=(.{11})", htmlContent.read().decode())
    return searchResults[0:10]

  def extract(self, url):
    with YoutubeDL(self.YTDL_OPTIONS) as ydl:
      try:
        info = ydl.extract_info(url, download=False)
      except:
        return False
    return {
      'link': 'https://www.youtube.com/watch?v=' + url,
      'thumbnail': 'https://i.ytimg.com/vi/' + url + '/hqdefault.jpg?sqp=-oaymwEcCOADEI4CSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD5uL4xKN-IUfez6KIW_j5y70mlig',
      'source': info['formats'][0]['url'],
      'title': info['title']
    }

  def play_next(self, ctx):
    id = int(ctx.guild.id)
    if not self.playing[id]:
      return
    if self.queue_index[id] + 1 < len(self.music_queue[id]):
      self.isplaying = True
      self.queue_index[id] += 1

      song = self.music_queue[id][self.queue_index[id]][0]
      embed = discord.Embed(title="Tocando agora: ", description=f"{song}")
      coro = ctx.send(embed=embed)
      fut = run_coroutine_threadsafe(coro, self.bot.loop)
      try:
        fut.result()
      except:
        pass

      self.vc[id].play(discord.FFmpegPCMAudio(
        song['source'], **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
    else:
      self.queue_index[id] += 1
      self.is_playing[id] = False                       

    
  async def play_music(self, ctx):
    id = int(ctx.guild.id)
    if self.queue_index[id] < len(self.music_queue[id]):
      self.is_playing[id] = True
      self.is_paused[id] = False

      await self.join(ctx, self.music_queue[id][self.queue_index[id]][1])

      song = self.music_queue[id][self.queue_index[id]][0]
      embed = discord.Embed(title="Tocando agora: ", description=f"{song}")
      await ctx.respond(embed=embed)

      self.vc[id].play(discord.FFmpegPCMAudio(
        song['source'], **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx)
      )
    else:
      await ctx.send("nao tem sons na lista!")
      self.queue_index[id] += 1
      self.is_playing = False




      
def setup(bot):
  bot.add_cog(Music(bot))
