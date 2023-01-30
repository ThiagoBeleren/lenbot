import discord
import wavelink
import typing 
import asyncio
import os

from threading import Thread
from discord.ext import commands
from discord.ui import Button, View

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.position = 0
        self.queue = []
        self.playingTextChannel = 0
        bot.loop.create_task(self.create_nodes())
        
    async def create_nodes(self):
        await self.bot.wait_until_ready()
        node = await wavelink.NodePool.create_node(bot = self.bot,
                                                   host = "127.0.0.1",
                                                   port = 2333,
                                                   password = "lenbot123",
                                                   )
    
    async def buttons(self):
        pause_btn = Button(style=discord.ButtonStyle.gray,
                           emoji="⏯️")
        view = View()
        view.add_item(pause_btn)
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Music COG is ready!')
        
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node '{node.identifier}' is ready!")
        
    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        try:
            self.queue.pop(0)
        except:
            pass
      
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        if reason == 'FINISHED':
            if not len(self.queue) == 0:
                next_track: wavelink.Track = self.queue[0]
                channel = self.bot.get_channel(923236110744830032)
                
                try:
                    await player.play(next_track)
                except:
                    return await channel.send(embed=discord.Embed(title="Algo deu errado ao tocar a musica"))
                
                await channel.send(embed=discord.Embed(title="Tocando Agora 🎶", description=f"{next_track.title}"))
                
            else:
                pass
        else:
            print(reason)
            
    @commands.slash_command(description="plays a song (youtube)")
    async def play(self, ctx: commands.Context, *, search: str):
        try:
            search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        except:
            await ctx.respond('nao achei nenhum resultado')
            return self.queue[0]
        
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if not vc.is_playing():
            try:
                await vc.play(search)
                await ctx.respond(embed=discord.Embed(title="Tocando Agora 🎶", description=f"{search.title}", url=f"{search.uri}")
                                  .add_field(name="Author", value=f"{search.author}")
                                  .add_field(name="Duração", value=f"`{search.length/60}m`")
                                  .set_footer(text=f"adicionado por {ctx.author}", icon_url=ctx.author.display_avatar))
            except:
                pass
        else:
            self.queue.append(search)
            await ctx.respond(embed=discord.Embed(title="Adicionado a fila: ", description=f"{search.title}", url=f"{search.uri}")
                                                    .add_field(name="Author", value=f"{search.author}")
                                                    .add_field(name="Duração", value=f"`{search.length/60}m`")
                                                    .set_footer(text=f"adicionado por {ctx.author}", icon_url=ctx.author.display_avatar))
            
    @commands.slash_command(description="Pauses the song")
    async def pause(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if player is None:
            ctx.send('Nao estou conectado a nenhum canal de voz!')
            
        if not player.is_paused():
            if player.is_playing():
                await player.pause()
                await ctx.respond(embed=discord.Embed(title='Musica Pausada!'))
                    
        if player.is_paused():
            await player.resume()
            await ctx.edit(embed=discord.Embed(title='Musica Despausada!'))
                
        else:
            await ctx.send('Nao a musicas na playlist 😔')
            
    @commands.slash_command(description="Stops the song")
    async def stop(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if player is None:
            ctx.send('Nao estou conectado a nenhum canal de voz!')
            
        self.queue.clear()
        
        try:
            if player.is_playing():
                await player.stop()
                await ctx.respond(embed=discord.Embed(title="Playlist Parada!"))
        except:
            await ctx.respond("Nao ha nada tocando agora! ")

    @commands.slash_command(description="Skips the song")
    async def skip(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if player is None:
            ctx.send('Nao estou conectado a nenhum canal de voz!')
        
        if not len(self.queue) == 0:
            next_track: wavelink.Track = self.queue[0]
            
            if player.is_playing():
                try:
                    await player.play(next_track)
                except:
                    await ctx.respond('Nao a musicas na playlist 😔')
                
            await ctx.respond(embed=discord.Embed(title="Tocando Agora 🎶", description=f"{next_track.title}", url=f"{next_track.uri}")
                                .add_field(name="Author", value=f"{next_track.author}")
                                .add_field(name="Duração", value=f"`{next_track.length/60}m`")
                                .set_footer(text=f"adicionado por {ctx.author}", icon_url=ctx.author.display_avatar))
      
    @commands.slash_command(description="Shows the queue")
    async def queue(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if not len(self.queue) == 0:
            mbed = discord.Embed(
                title=f"Tocando Agora 🎶: {player.track}" 
                if player.is_playing() 
                else "Queue: ",
                description = "\n".join(f"**{i+1}. `{track}`" for i, 
                                        track in enumerate(self.queue[:20])) 
                                            if not player.is_playing() else "**Queue: **\n" + "\n".join(f"**{i+1}. `{track}`" for i, 
                                                track in enumerate(self.queue[:20])),
                color=discord.Color.from_rgb(255, 255, 255)
            )

            return await ctx.respond(embed=mbed)
        else:
            return await ctx.respond(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))
        
    """
    @commands.slash_command(name="searchs for a song")
    async def search(self, ctx: commands.Context, *, search: str):
        try:
            tracks = await wavelink.YouTubeTrack.search(query=search)
        except:
            return await ctx.respond(embed=discord.Embed(title="Something went wrong while searching for this track", color=discord.Color.from_rgb(255, 255, 255)))

        if tracks is None:
            return await ctx.respond("No tracks found")

        mbed = discord.Embed(
            title="Select the track: ",
            description=("\n".join(f"**{i+1}. {t.title}**" for i, t in enumerate(tracks[:5]))),
            color = discord.Color.from_rgb(255, 255, 255)
        )
        msg = await ctx.respond(embed=mbed)

        emojis_list = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '❌']
        emojis_dict = {
            '1️⃣': 0,
            "2️⃣": 1,
            "3️⃣": 2,
            "4️⃣": 3,
            "5️⃣": 4,
            "❌": -1
        }

        for emoji in list(emojis_list[:min(len(tracks), len(emojis_list))]):
            await msg.add_reaction(emoji)

        def check(res, user):
            return(res.emoji in emojis_list and user == ctx.author and res.message.id == msg.id)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
            return
        else:
            await msg.delete()

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        try:
            if emojis_dict[reaction.emoji] == -1: return
            choosed_track = tracks[emojis_dict[reaction.emoji]]
        except:
            return

        vc: wavelink.Player = ctx.voice_client or await ctx.author.voice.channel.connect(cls=wavelink.Player)

        if not player.is_playing() and not player.is_paused():
            try:
                await vc.play(choosed_track)
            except:
                return await ctx.respond(embed=discord.Embed(title="Something went wrong while playing this track", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            self.queue.append(choosed_track)
        
        await ctx.respond(embed=discord.Embed(title=f"Added {choosed_track.title} to the queue", color=discord.Color.from_rgb(255, 255, 255)))
        """

def setup(bot):
    bot.add_cog(Music(bot))
    
            
        