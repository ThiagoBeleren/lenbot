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
        command_channel = self.bot.get_channel(ctx.guild)
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
        embed4.add_field(name=":four:", value=f"Comandos so serao permitidos na aba {command_channel.mention}")
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
        buttonservidor = Button(label="Meu Servidor",
                                style=discord.ButtonStyle.url,
                                url="https://discord.gg/trRtuX97ch")
        buttonaboutme = Button(label="Sobre Mim",
                               style=discord.ButtonStyle.green,
                               )

        #add_buttons
        view = View()
        view.add_item(buttoninvitebot)
        view.add_item(buttonservidor)
        view.add_item(buttonaboutme)

        #buttons callback
        async def buttonaboutmecallback(interaction: discord.Interaction):
            await interaction.response.send_message(embed=embed, ephemeral=True)
        buttonaboutme.callback = buttonaboutmecallback

        #vars
        autor = self.bot.get_user(911000560109514752)

        embed = discord.Embed(
            title="Sobre mim",
            description="Fui criado para ajudar em moderacoes de servidor, music e varias outras funcoes. A cada dia evoluindo mais e mais para todos os servidores.\n"
                        "Estou sempre disposto a ouvir sugestoes :man_mage:, contatos do meu criador esta no link abaixo :wink:",
            url="https://github.com/ThiagoBeleren/lenbot"
        )
        embed.add_field(name="Sobre o Bot", value=f"O bot e de uso livre, criador por {autor.mention}")
        embed.set_author(name=self.bot.user.name, url="")
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
    async def status(self, ctx: commands.Context, member: discord.Member=None):
        if member:
            if member == None:
                member = ctx.author
                if member.activity == None:
                    activity = 'Inactive'
                    await ctx.respond(activity)

                elif type(member.activity) == discord.Spotify:
                        activity = 'Spotify'
                        embed = discord.Embed(color=member.top_role.color.value,
                                            title=f'Atividade que {member} esta fazendo :headphones:',
                                            url=member.activity.track_url, timestamp=ctx.message.created_at)
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

                else:
                        activity = f'{member.activity.name}'
                        embed = discord.Embed(color=member.top_role.color.value,
                                            title=f'Atividade que {member} esta fazendo')
                        embed.add_field(name='**Activity**',
                                        value=f'{activity}',
                                        inline=True)
                        await ctx.respond(embed=embed)


    @commands.slash_command()
    async def twitch(self, ctx: commands.Context):
        channel_live = self.bot.get_channel(988883848060354620)
        allowed_mentions = discord.AllowedMentions(everyone=True)

        command_channel = self.bot.get_channel(923236110744830032)
        print(f"{ctx.author}, {command_channel}, {channel_live}")

        if ctx.author.is_owner(911000560109514752):
            print(f"{ctx.author}, {command_channel}, {channel_live}")
            embed = discord.Embed(description=f"ESTOU EM LIVE!")
            embed.add_field(name="Venha ver agora!", value="https://www.twitch.tv/ezdeterno", inline="False")
            embed.add_field(name="Quer ter sua mensagem vista na live? mande-a pelo pix!",
                            value="Chave: thiagobeleren@gmail.com")
            embed.set_image(url='https://i.pinimg.com/564x/b7/c6/e5/b7c6e50a80b89476537711767aa677dd.jpg')
            await channel_live.send(embed=embed, content='@everyone', allowed_mentions=allowed_mentions)
            print(f'mensagem de live enviada ao canal {channel_live}')


    @commands.slash_command()
    async def invite(self, ctx: commands.Context):
        for guild in self.bot.guilds:
            discord_guild = self.bot.get_guild(int(guild.id))
            link = await discord_guild.text_channels[0].create_invite(max_uses=0, unique=False)
            await ctx.respond(link)
            print(link)


def setup(bot):
    bot.add_cog(Commands(bot))