import discord
import wavelink
import random

from discord.ext import commands
from discord.ui import Button, View


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.position = 0
        self.playingTextChannel = 0
        self.queue = []
        bot.loop.create_task(self.create_nodes())
        
    async def create_nodes(self):
        await self.bot.wait_until_ready()
        node: wavelink.Node = wavelink.Node(
            uri = "127.0.0.1:2333",
            password = "youshallnotpass",
        )
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music COG is ready!')
        
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node '{node.id}' is ready!")
        
    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.YouTubeTrack):
        try:
            self.queue.pop(0)
        except:
            pass
      
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.YouTubeTrack, reason):
        if reason == 'FINISHED':
            if not len(self.queue) == 0:
                next_track: wavelink.YouTubeTrack = self.queue[0]
                channel = self.bot.get_channel(923236110744830032)
                ctx = commands.Context
                
                try:
                    await player.play(next_track)
                except:
                    return await channel.respond(embed=discord.Embed(title="Algo deu errado ao tocar a musica"))
                
                await self.music_embed(ctx, search=next_track, title="Tocando Agora")
                await self.music_buttons(ctx)
                
            else:
                pass
        else:
            print(reason)
    
    async def music_embed(self, ctx, search, title):
        embed = discord.Embed(title=f"{title} 🎶", description=f"{search.title}", url=f"{search.uri}")
        embed.add_field(name="Author", value=f"{search.author}")
        embed.add_field(name="Duração", value=f"`{round(search.length/60, 2)}m`")
        embed.set_footer(text=f"adicionado por {ctx.author}")# icon_url=ctx.author.display_avatar)
        embed.set_image(url=f"{search.thumb}")
        await ctx.respond(embed=embed)

    async def music_buttons(self, ctx):
        back_btn = Button(style=discord.ButtonStyle.gray,
                          emoji="⏪",
                          disabled=True,
                          )
        pause_btn = Button(style=discord.ButtonStyle.gray,
                           emoji="⏯️",
                           )
        skip_btn = Button(style=discord.ButtonStyle.gray,
                           emoji="⏩",
                           )
        shuffle_btn = Button(style=discord.ButtonStyle.secondary,
                             emoji="🔀",
                             disabled=False,
                             )
        stop_btn = Button(style=discord.ButtonStyle.red,
                          emoji="⏹️",
                          )
        repeat_btn = Button(style=discord.ButtonStyle.secondary,
                            emoji="🔁",
                            disabled=False,
                            )
        
        view = View()
        view.add_item(back_btn) 
        view.add_item(pause_btn)
        view.add_item(skip_btn)
        view.add_item(shuffle_btn)
        view.add_item(stop_btn)
        view.add_item(repeat_btn)
        
        async def backBTN(interaction: discord.Interaction):
            return
        
        async def pauseBTN(interaction: discord.Interaction):
            await self.pause_add(ctx)
        pause_btn.callback = pauseBTN
        
        async def skipBTN(interaction: discord.Interaction):
            await self.skip_add(ctx)
        skip_btn.callback = skipBTN
        
        async def shuffleBTN(interaction: discord.Interaction):
            await self.shuffle_add(ctx)
        shuffle_btn.callback = shuffleBTN
        
        async def stopBTN(interaction: discord.Interaction):
            await self.stop_add
        stop_btn.callback = stopBTN
        
        async def repeatBTN(interaction: discord.Interaction):
            await self.repeat_add(ctx)
        repeat_btn.callback = repeatBTN
        
        await ctx.respond(view=view)

    @commands.slash_command(description="plays a song (youtube)")
    async def play_add(self, ctx: commands.Context, *, search: str):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        query = await wavelink.YouTubeTrack.search(search)
        await vc.play(query)

        
    async def pause_add(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        msg = await ctx.send("Pausando... ⏸️")
        
        if player is None:
            msg.edit('Nao estou conectado a nenhum canal de voz!')
            
        if player.is_paused():
            await player.resume()
            await msg.edit(embed=discord.Embed(title='Musica Despausada!'))
                    
        elif not player.is_paused():
            if player.is_playing():
                await player.pause()
                await msg.edit(embed=discord.Embed(title='Musica Pausada!'))
                    
        else:
            await msg.edit('Nao a musicas na playlist 😔')

    async def stop_add(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        msg = await ctx.send("Parando... ⏹️")
        
        if player is None:
            msg.edit('Nao estou conectado a nenhum canal de voz!')
            
        self.queue.clear()
        
        try:
            if player.is_playing():
                await player.stop()
                await msg.edit(embed=discord.Embed(title="Playlist Parada!"))
        except:
            await msg.edit("Nao ha nada tocando agora! ")

    async def skip_add(self, ctx):
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
                
            await self.music_embed(ctx, search=next_track, title="Tocando agora")
            await self.music_buttons(ctx)
    
    async def shuffle_add(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if not len(self.queue) == 0:
            random.shuffle(self.queue)
            msg = await ctx.respond("Ordem de reproducao aleatoria ativada! 🕺")
            
            mbed = discord.Embed(
                title=f"Tocando Agora 🎶: {player.track}" 
                if player.is_playing() 
                else "Queue: ",
                description = "\n".join(f"**{i+1}**. `{track}`" for i, 
                                        track in enumerate(self.queue[:20])) 
                                            if not player.is_playing() else "**Queue: **\n" + "\n".join(f"**{i+1}. `{track}`" for i, 
                                                track in enumerate(self.queue[:20])),
                color=discord.Color.from_rgb(255, 255, 255)
            )

            return await msg.reply(embed=mbed)
        else:
            return await msg.reply(embed=discord.Embed(title="The queue is empty", color=discord.Color.from_rgb(255, 255, 255)))
        
    async def repeat_add(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        return

    async def queue_add(self, ctx):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if not len(self.queue) == 0:
            mbed = discord.Embed(
                title=f"Tocando Agora 🎶: {player.track}" 
                if player.is_playing() 
                else "Queue: ",
                description = "\n".join(f"**{i+1}**. `{track}`" for i, 
                                        track in enumerate(self.queue[:20])) 
                                            if not player.is_playing() else "**Queue: **\n" + "\n".join(f"**{i+1}. `{track}`" for i, 
                                                track in enumerate(self.queue[:20])),
                color=discord.Color.from_rgb(255, 255, 255)
            )

            return await ctx.respond(embed=mbed)
        else:
            return await ctx.respond(embed=discord.Embed(title="A lista esta vazia", color=discord.Color.from_rgb(255, 255, 255)))

    """
    @commands.slash_command(description="plays a song (youtube)")
    async def play(self, ctx: commands.Context, search: str):
        await self.play_add(ctx, search)

    """
    @commands.slash_command(description="Pauses the song")
    async def pause(self, ctx: commands.Context):
        await self.pause_add(ctx)
            
    @commands.slash_command(description="Stops the song")
    async def stop(self, ctx: commands.Context):
        await self.stop_add(ctx)

    @commands.slash_command(description="Skips the song")
    async def skip(self, ctx: commands.Context):
        await self.skip_add(ctx)  
      
    @commands.slash_command(description="Shuffle a playlist")
    async def shuffle(self, ctx: commands.Context):
        await self.shuffle_add(ctx)
        
    @commands.slash_command(description="Shows the queue")
    async def queue(self, ctx: commands.Context):
        await self.queue_add(ctx)
    
    @commands.slash_command(description="Repeats the current song of the queue")
    async def repeat(self, ctx: commands.Context):
        await self.repeat_add(ctx)
        
    @commands.slash_command(description="Adds your youtube playlist")
    async def playlist(self, ctx: commands.Context):
        return
        
        
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
    
            
        