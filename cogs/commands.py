import discord
from discord.ext import commands
from discord import option #app_commands
import asyncio
import random
from discord import option
from discord.ui import Button, View

class Commands(commands.Cog):
    def __init__ (self, bot: commands.Bot):
        self.bot = bot
        intents = discord.Intents.all()
        intents.members = True
        commands.Bot(intents=intents, permissions=8)

    @commands.slash_command()
    async def regras(self, ctx: commands.Context):
        member = ctx.author
        command_channel = self.bot.get_channel(member)
        embed4 = discord.Embed(title=f'Regras de conduta no servidor', color=10181046)
        embed4.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        embed4.set_thumbnail(url=self.bot.user.avatar.url)
        embed4.add_field(name=":one:",
                         value="E proibido qualquer tipo descriminacao e apologia que viole os direitos humanos",
                         inline=False)
        embed4.add_field(name=":two:", value="Qualquer projeto criado deve ter seus devidos creditos dados ao usa-lo",
                         inline=False)
        embed4.add_field(name=":three:",
                         value="Nao e permitido o spam de mensagem nos canais de texto e em qualquer usuario deste servidor",
                         inline=False)
        embed4.add_field(name=":four:", value=f"Comandos so serao permitidos na aba de **Comandos**")
        await ctx.respond(embed=embed4)


    @commands.slash_command(description="Tira cara ou coroa")
    async def flip(self, ctx: commands.Context):
        channel = ctx.channel
        moeda = random.randint(1, 2)
        await channel.send('[1] para cara \n'
                            '[2] para coroa')

        def check(m):
            return m.content == '1' or '2' and m.channel == channel

        msg = await self.bot.wait_for('message', check=check, timeout=60.0)

        if moeda == 1:
            moeda = 'cara'
        elif moeda == 2:
            moeda = 'coroa'

        await channel.send(f'A face da moeda eh {moeda} {ctx.author.mention}! :partying_face:')
        print(moeda)


    @commands.slash_command(description="Alguns comandos usados por mim")
    async def ajuda(self, ctx: commands.Context):
        #buttons
        buttoninvitebot = Button(label="Convidar o bot",
                                 style=discord.ButtonStyle.url,
                                 url="https://discord.com/api/oauth2/authorize?client_id=991165635356794881&permissions=8&scope=bot")
        buttonbotserver = Button(label="Meu Servidor",
                                style=discord.ButtonStyle.url,
                                url="https://discord.gg/trRtuX97ch")
        buttonaboutme = Button(label="Sobre Mim",
                               style=discord.ButtonStyle.green,
                               )
        buttoniniviteguild = Button(label="Convite para seu servidor",
                                    style=discord.ButtonStyle.blurple)
        #add_buttons
        view = View()
        view.add_item(buttoninvitebot)
        view.add_item(buttonbotserver)
        view.add_item(buttonaboutme)
        view.add_item(buttoniniviteguild)

        #buttons callback
        async def buttonaboutmecallback(interaction: discord.Interaction):
            await interaction.response.send_message(embed=embed, ephemeral=True)
        buttonaboutme.callback = buttonaboutmecallback

        async def buttoninviteguildcallback(interaction: discord.Interaction):
            for guild in self.bot.guilds:
                discord_guild = self.bot.get_guild(int(guild.id))
                link = await discord_guild.text_channels[0].create_invite(max_uses=0, unique=False)
                await interaction.response.send_message(link)
                print(link)
        buttoniniviteguild.callback = buttoninviteguildcallback

        #vars
        autor = self.bot.get_user(911000560109514752)

        embed = discord.Embed(
            title="Sobre mim",
            description="Fui criado para ajudar em moderacoes de servidor, music e varias outras funcoes. A cada dia evoluindo mais e mais para todos os servidores.\n",
            url="https://github.com/ThiagoBeleren/lenbot"
        )
        embed.add_field(name="Sobre o Bot", value=f"O bot e de uso livre, criador por {autor.display_name}")
        embed.set_author(name=self.bot.user.name)
        embed.set_thumbnail(url=self.bot.user.avatar.url)

        embed1 = discord.Embed(title="Comandos usados por mim")
        embed1.add_field(name="Musica",
                         value=f"`tocar` `parar` `pausar` `retornar` `pular` `volume` `entrar` `sair` `tocando agora` `proucurarmusica` `fila`",
                         inline=False)
        embed1.add_field(name="Comandos Disponiveis", value="`flip` `regras` `sobre` `status` `twitch`", inline=False)
        embed1.add_field(name="Moderacao", value="`ban` `kick` `unban`", inline=False)
        embed1.set_author(name=self.bot.user.name, url="")
        embed1.set_thumbnail(url=self.bot.user.avatar.url)

        await ctx.respond(embed=embed1, view=view)


    @commands.slash_command(description="Mostra o status de um membro")
    async def status(self, ctx: commands.Context, member: discord.Member):
        if member:
                if member.activity == None:
                    activity = 'Inactive'
                    await ctx.respond(activity)

                elif type(member.activity) == discord.Spotify:
                        activity = 'Spotify'
                        embed = discord.Embed(color=member.top_role.color.value,
                                            title=f'Atividade que {member} esta fazendo :headphones:',
                                            url=member.activity.track_url)
                        embed.add_field(name="**Nome da Musica**",
                                        value=member.activity.title)
                        embed.add_field(name='**Activity**',
                                        value={activity},
                                        inline=True)
                        embed.set_image(url=member.activity.album_cover_url)
                        embed.add_field(name="**Album**",
                                        value=member.activity.album,
                                        inline=False)
                        embed.add_field(name='**Artista(s)**',
                                        value=member.activity.artist,
                                        inline=False)
                        await ctx.respond(embed=embed)

                elif type(member.activity) == discord.Streaming:
                    activity = 'Streaming'
                    embed = discord.Embed(title=f"{member.activity.twitch_name} esta ao vivo em {member.activity.platform}! 🔴",
                                                   color=member.color)
                    embed.add_field(name="**Titulo**",
                                    value=f"{member.activity.name}")
                    embed.add_field(name="**Game: **",
                                    value=f"{member.activity.game}")
                    embed.set_thumbnail(url=f"{member.activity.url}")
                    embed.set_image(url=f"{member.display_avatar}")
                    await ctx.respond(embed=embed)

                else:
                        activity = f'{member.activity.name}'
                        embed = discord.Embed(color=member.top_role.color.value,
                                            title=f'Atividade que {member} esta fazendo')
                        embed.add_field(name='**Activity**',
                                        value=f'{activity}',
                                        inline=True)
                        await ctx.respond(embed=embed)

    """
    @bot.slash_command(guild_ids=[911058863774654514])
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

def setup(bot):
    bot.add_cog(Commands(bot))