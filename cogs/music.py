import discord
import typing
import wavelink
import asyncio

from discord import option
from discord.ui import Button, View
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.position = 0
        self.repeat = False
        self.repeatMode = "NONE"
        self.playingTextChannel = 0
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.bot.wait_until_ready()  # wait until the bot is ready
        node = await wavelink.NodePool.create_node(
            bot=self.bot,
            host='127.0.0.1',
            port=2333,
            password="password123",
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog de musica ativado!")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is now ready")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        try:
            self.queue.pop(0)
        except:
            pass

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, ctx: commands.Context, player: wavelink.Player, track: wavelink.Track, reason):
        if str(reason) == "FINISHED":
            node = wavelink.NodePool.get_node()

            if not len(self.queue) == 0:
                next_track: wavelink.Track = self.queue[0]
                channel = self.bot.get_channel(ctx.author)

                try:
                    await player.play(next_track)
                except:
                    return await channel.respond(embed=discord.Embed(title=f"Algo de errado aconteceu ao tocar a musica **{next_track.title}**",
                                              color=discord.Color.from_rgb(255, 255, 255)))

                await channel.respond(embed=discord.Embed(title=f"Tocando agora: {next_track.title}",
                                                       color=discord.Color.from_rgb(255, 255, 255)))
            else:
                pass
        else:
            print(reason)


    @commands.slash_command(description="Entrar no canal de voz")
    #@option("channel", description="escolher um canal de voz")
    async def entrar(self, ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            channel = ctx.author.voice.channel

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is not None:
            if player.is_connected():
                return await ctx.send("Estou conectado a um canal de voz")

        await channel.connect(cls=wavelink.Player)
        print(f"{channel.name}")

    @commands.slash_command(description="tocar musica")
    #@option("search", description="Digite o nome da musica")
    async def tocar(self, ctx: commands.Context, *, search: str):
        try:
            search = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        except:
            return await ctx.send(embed=discord.Embed(title="Algo de errado aconteceu ao tocar a musica",
                                                       color=discord.Color.from_rgb(255, 255, 255)))

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            try:
                await vc.play(search)
            except:
                return await ctx.send(embed=discord.Embed(title="Algo de errado aconteceu ao tocar a musica",
                                                           color=discord.Color.from_rgb(255, 255, 255)))
        else:
            self.queue.append(search)

        button_pause = Button(label="a",
                              style=discord.ButtonStyle.grey,
                              emoji="⏸️")

        view = View()
        view.add_item(button_pause)

        async def buttonpausecallback(interaction: discord.Interaction):
            await interaction.response.send_message('cabo')
        button_pause.callback = buttonpausecallback
        ctx.respond(
            view=view
        )

        @commands.slash_command()
        async def pausar(self, ctx: commands.Context):
                    node = wavelink.NodePool.get_node()
                    player = node.get_player(ctx.guild)

                    if player is None:
                        return await ctx.send("Nao estou conectado a nenhum canal de voz no momento")

                    if not player.is_paused():
                        if player.is_playing():
                            await player.pause()
                            mbed = discord.Embed(title="Musica pausada", color=discord.Color.from_rgb(255, 255, 255))
                            return await ctx.send(embed=mbed)
                        else:
                            return await ctx.send("Nao ha nada tocando agora")
                    else:
                        return await ctx.send("Musica ja esta pausada")


        mbed = discord.Embed(title=f"Adicionado *{search}* na fila", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.respond(embed=mbed) #view=view)

    @commands.slash_command(description="Parar a musica")
    async def parar(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Nao estou conectado a nenhum canal de voz no momento")

        self.queue.clear()

        if player.is_playing():
            await player.stop()
            mbed = discord.Embed(title="Musica parada", color=discord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=mbed)
        else:
            return await ctx.send("Nao ha nada tocando agora")



    @commands.slash_command(description="despausa a musica")
    async def retornar(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Nao estou conectado a nenhum canal de voz no momento!")

        if player.is_paused():
            await player.resume()
            mbed = discord.Embed(title="Musica despausada", color=discord.Color.from_rgb(255, 255, 255))
            return await ctx.send(embed=mbed)
        else:
            if not len(self.queue) == 0:
                track: wavelink.Track = self.queue[0]
                player.play(track)
                return await ctx.send(embed=discord.Embed(title=f"Tocando agora: {track.title}"))
            else:
                return await ctx.send("Musica nao esta pausada")

    @commands.slash_command(description="aumenta ou diminui a musica")
    async def volume(self, ctx: commands.Context, to: int):
        if to > 100:
            return await ctx.send("Volume deve estar entre 0 e 100")
        elif to < 1:
            return await ctx.send("Volume deve estar entre 0 e 100")

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        await player.set_volume(to)
        mbed = discord.Embed(title=f"Alterou o volume para {to}", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)

    @commands.slash_command(description="Mostra o que esta tocando agora")
    async def tocandoagora(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Nao estou conectado a nenhum canal de voz no momento!")

        if player.is_playing():
            mbed = discord.Embed(
                title=f"Tocando agora: {player.track}",
                color=discord.Color.from_rgb(255, 255, 255)
            )

            t_sec = int(player.track.length)
            hour = int(t_sec / 3600)
            min = int((t_sec % 3600) / 60)
            sec = int((t_sec % 3600) % 60)
            length = f"{hour}hr {min}min {sec}sec" if not hour == 0 else f"{min}min {sec}sec"

            mbed.add_field(name="Artista", value=player.track.info['author'], inline=False)
            mbed.add_field(name="Duracao", value=f"`{length}`", inline=False)
            mbed.add_field(name="Url", value=player.track.info['uri'])
            return await ctx.send(embed=mbed)
        else:
            await ctx.send("Nao esta tocando nada no momento")

    @commands.slash_command(description="exibe 5 resultados da musica")
    async def proucurarmusica(self, ctx: commands.Context, *, search: str):
        try:
            tracks = await wavelink.YouTubeTrack.search(query=search)
        except:
            return await ctx.send(embed=discord.Embed(title="Algo deu de errado ao tocar a musica :disappointed_relieved:",
                                                       color=discord.Color.from_rgb(255, 255, 255)))

        if tracks is None:
            return await ctx.send("Nao achei nenhum resultado")

        mbed = discord.Embed(
            title="Escolha uma musica: ",
            description=("\n".join(f"**{i + 1}. {t.title}**" for i, t in enumerate(tracks[:5]))),
            color=discord.Color.from_rgb(255, 255, 255)
        )
        msg = await ctx.send(embed=mbed)

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
            return (res.emoji in emojis_list and user == ctx.author and res.message.id == msg.id)

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
                return await ctx.send(embed=discord.Embed(title="Algo deu de errado ao tocar a musica :disappointed_relieved:",
                                                           color=discord.Color.from_rgb(255, 255, 255)))
        else:
            self.queue.append(choosed_track)

        await ctx.send(embed=discord.Embed(title=f"Adicionado {choosed_track.title} para a fila",
                                            color=discord.Color.from_rgb(255, 255, 255)))

    @commands.slash_command(description="Pula para a proxima musica da lista")
    async def pular(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not len(self.queue) == 0:
            next_track: wavelink.Track = self.queue[0]
            try:
                await player.play(next_track)
            except:
                return await ctx.send(embed=discord.Embed(title="Algo deu de errado ao tocar a musica :disappointed_relieved:",
                                                           color=discord.Color.from_rgb(255, 255, 255)))

            await ctx.send(embed=discord.Embed(title=f"Tocando Agora: {next_track.title}",
                                                color=discord.Color.from_rgb(255, 255, 255)))
        else:
            await ctx.send("A playlist esta vazia :guitar:")

    # this command would queue a song if some args(search) is provided else it would just show the queue
    @commands.slash_command(description="Exibe a lista de espera")
    async def fila(self, ctx: commands.Context, *, search=None):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if search is None:
            if not len(self.queue) == 0:
                mbed = discord.Embed(
                    title=f"Tocando Agora: {player.track}" if player.is_playing else "Fila: ",
                    description="\n".join(f"**{i + 1}. {track}**" for i, track in enumerate(
                        self.queue[:10])) if not player.is_playing else "**Fila: **\n" + "\n".join(
                        f"**{i + 1}. {track}**" for i, track in enumerate(self.queue[:10])),
                    color=discord.Color.from_rgb(255, 255, 255)
                )

                return await ctx.send(embed=mbed)
            else:
                return await ctx.send(
                    embed=discord.Embed(title="A playlist esta vazia :guitar:", color=discord.Color.from_rgb(255, 255, 255)))
        else:
            try:
                track = await wavelink.YoutubeTrack.search(query=search, return_first=True)
            except:
                return await ctx.send(embed=discord.Embed(title="Algo deu de errado ao tocar a musica :disappointed_relieved:",
                                                           color=discord.Color.from_rgb(255, 255, 255)))

            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel(cls=wavelink.Player)
                await player.connect(ctx.author.voice.channel)
            else:
                vc: wavelink.Player = ctx.voice_client

            if not vc.isp_playing():
                try:
                    await vc.play(track)
                except:
                    return await ctx.send(embed=discord.Embed(title="Algo deu de errado ao tocar a musica :disappointed_relieved:",
                                                               color=discord.Color.from_rgb(255, 255, 255)))
            else:
                self.queue.append(track)

            await ctx.send(embed=discord.Embed(title=f"Adicionado {track.title} na fila :musical_note:",
                                                color=discord.Color.from_rgb(255, 255, 255)))


    @commands.slash_command(description="Desconectar o bot")
    async def sair(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Nao estou conectado a nenhum canal de voz!")

        await player.disconnect()
        mbed = discord.Embed(title="Disconectado, ate mais!", color=discord.Color.from_rgb(255, 255, 255))
        await ctx.send(embed=mbed)


def setup(bot):
    bot.add_cog(Music(bot))


