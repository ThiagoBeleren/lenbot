import discord
from discord.ext import commands
import os
import asyncio
import random
import configs

#intents.members = True
token = configs.Token()
bot = commands.Bot(intents= discord.Intents.all(), command_prefix="-", permissions=8)
prefixo = "-"

@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = 'Project Sekai: Colourful Stage'))
    print(bot.user.name, 'está Online')


@bot.event
async def on_member_join(member):
    guild = member.guild #guild = server
    welcome_channel = bot.get_channel(911058863774654517)
    role_channel = bot.get_channel(911064432472367154)

    embed3 = discord.Embed(description=f":partying_face: Bem vindo ao servidor, {member.mention}.\n Espero que se divirta por aqui.")
    embed3.add_field(name='Integrantes', value=f'você é o {len(guild.members)}* participante do servidor. Nao se esquece de pegar um cargo no {role_channel.mention}', inline=False)
    embed3.set_author(name=member.display_name, icon_url=member.display_avatar)
    embed3.add_field(name='ID', value=member.id, inline=False)
    embed3.set_image(url="https://cdn.discordapp.com/attachments/996151321096892636/997995707615162388/tenor.gif")
    await welcome_channel.send(embed=embed3)
    print(f'{member.mention}, entrou no servidor')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")
        
#Verifica se o canal eh realmente o de comando no momento em que o member mandar a mensagem!
@bot.event
async def on_command(ctx, member: discord.Member = None):
    channel_id = ctx.channel.id
    print(f"o {ctx.author.mention}, digitou no canal certo! ({channel_id})")
    
    if channel_id != 923236110744830032:
        embed = discord.Embed(description=f"Voce nao pode mandar comandos por aqui {ctx.author.mention}")
        await ctx.send(embed=embed)
        print(f'{ctx.author.mention} digitou o comando no canal errado')
        #delete message
        
    elif channel_id == 923236110744830032:
        return 

@bot.event
@commands.has_permissions(administrator=True)
async def on_raw_reaction_add(payload):

    member = payload.member
    guild = member.guild
    emoji = payload.emoji.name
    role_message_id = 999072734954921994
    if role_message_id == payload.message_id:
        
        if emoji == '💻':
            role = discord.utils.get(guild.roles, name="Programadores 💻")
        
        if emoji == '👑':
            role = discord.utils.get(guild.roles, name="Anime fan 👑")
            
        if emoji == '🎶':
            role = discord.utils.get(guild.roles, name="Just Chill 🎶")
            
        if emoji == "🏠":
            role = discord.utils.get(guild.roles, name="Rioters 🏠")
            
        if emoji == "🏆":
            role = discord.utild.get(guild.roles, name="Indie 🏆")
            
        if emoji == '🕹️':
            role = discord.utils.get(guild.roles, name='Casual 🕹️')
            
        if emoji == '🔫':
            role = discord.utils.get(guild.roles, name="FPS 🔫")
            
        if emoji == '🎲':
            role = discord.utils.get(guild.roles, name="RPG 🎲")
            
        await member.add_roles(role)
    

@bot.event
@commands.has_permissions(administrator=True)
async def on_raw_reaction_remove(payload):
    role_message_id = 999072734954921994
    if role_message_id == payload.message_id:
        guild = await(bot.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        
        if emoji == '💻':
            role = discord.utils.get(guild.roles, name="Programadores 💻")
        
        if emoji == '👑':
            role = discord.utils.get(guild.roles, name="Anime fan 👑")
            
        if emoji == '🎶':
            role = discord.utils.get(guild.roles, name="Just Chill 🎶")
            
        if emoji == "🏠":
            role = discord.utils.get(guild.roles, name="Rioters 🏠")
            
        if emoji == "🏆":
            role = discord.utild.get(guild.roles, name="Indie 🏆")
            
        if emoji == '🕹️':
            role = discord.utils.get(guild.roles, name='Casual 🕹️')
            
        if emoji == '🔫':
            role = discord.utils.get(guild.roles, name="FPS 🔫")
            
        if emoji == '🎲':
            role = discord.utils.get(guild.roles, name="RPG 🎲")
        
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print('Member not found! :(')
#https://www.youtube.com/watch?v=0Yr4ddt7vbI&t=230s, exceedcoding credits.
    
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *,reason = None):
    guild = discord.utils.get(guild.roles, name="Moderadores")
    if ctx.author == 911000560109514752 or guild:
        await ctx.kick(reason = reason)
        
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member, *,reason = None):
    guild = discord.utils.get(guild.roles, name="Moderadores")
    if ctx.author == 911000560109514752 or guild:
        await ctx.ban(reason = reason)
        
@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    guild = discord.utils.get(guild.roles, name="Moderadores")
    if ctx.author == 911000560109514752 or guild:
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
        
@bot.command()
@commands.has_permissions(administrator=True)
async def roles(ctx):
    
    if ctx.author.is_owner(911000560109514752):
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
    
    
@bot.command()
async def twitch(ctx):
    channel_live = bot.get_channel(988883848060354620)
    allowed_mentions = discord.AllowedMentions(everyone = True)
    
    command_channel = bot.get_channel(923236110744830032)
    print(f"{ctx.author}, {command_channel}, {channel_live}")
    
    if ctx.author.is_owner():
        print(f"{ctx.author}, {command_channel}, {channel_live}")
        embed = discord.Embed(description=f"ESTOU EM LIVE!")
        embed.add_field(name="Venha ver agora!", value="https://www.twitch.tv/ezdeterno", inline="False")
        embed.add_field(name="Quer ter sua mensagem vista na live? mande-a pelo pix!", value="Chave: thiagobeleren@gmail.com")
        embed.set_image(url='https://i.pinimg.com/564x/b7/c6/e5/b7c6e50a80b89476537711767aa677dd.jpg')
        await channel_live.send(embed=embed, content = '@everyone', allowed_mentions = allowed_mentions)
        print(f'mensagem de live enviada ao canal {channel_live}')
        
        
#Show random images or gifs to a embed !working on!
'''
@bot.command()
async def images(ctx):
    '''

@bot.command(aliases=['whois', 'user'])
async def status(ctx, member: discord.Member = None):
    if member:
        if not member.id in [923236110744830032, 988887114634629130]:
            if member.activity == None:
                activity = 'Inactive'

            elif type(member.activity) == discord.Spotify:
                activity = 'Spotify'
                           
            else:
                activity = f'{member.activity.name}'

            embed = discord.Embed(color=member.top_role.color.value, title=f'Atividade que {member} esta fazendo :headphones:', url=member.activity.track_url)
            embed.add_field(name="**Nome da Musica**", value=member.activity.title)
            embed.add_field(name='**Activity**', value={activity}, inline=True)
            embed.set_image(url=member.activity.album_cover_url)
            embed.add_field(name="**Album**", value=member.activity.album, inline=False)
            embed.add_field(name='**Artista(s)**', value=member.activity.artist, inline=False)
            
            await ctx.send(embed=embed)


@bot.command()
async def regras(ctx):
    command_channel = bot.get_channel(923236110744830032)
    if ctx.channel.id == 923236110744830032:
        embed4 = discord.Embed(title=f'Regras de conduta no servidor', color=10181046)
        embed4.set_author(name=bot.user.name, icon_url=bot.user.avatar.url)
        embed4.set_thumbnail(url=bot.user.avatar.url)
        embed4.add_field(name=":one:", value="E proibido qualquer tipo descriminacao e apologia que viole os direitos humanos", inline=False)
        embed4.add_field(name=":two:", value="Qualquer projeto criado deve ter seus devidos creditos dados ao usa-lo", inline=False)
        embed4.add_field(name=":three:", value="Nao e permitido o spam de mensagem nos canais de texto e em qualquer usuario deste servidor", inline=False)
        embed4.add_field(name=":four:", value=f"Comandos so serao permitidos na aba {command_channel.mention}")
        await ctx.send(embed=embed4)        
    
    
@bot.command()
async def ajuda(ctx):
    bot_de_musica = bot.get_user(923228100714696704)
    if ctx.channel.id == 923236110744830032:
        embed1 = discord.Embed(title="Alguns comandos usados por mim", url="", description="", color=0x109319)
        embed1.set_author(name=bot.user.name, url="")
        embed1.set_thumbnail(url=bot.user.avatar.url)
        embed1.add_field(name=prefixo + "play" " nomedamusica", value=f"para o bot tocar a musica {bot_de_musica.mention}", inline=False)
        embed1.add_field(name=prefixo + "rpg", value="Informacoes sobre o rpg", inline=False)
        embed1.add_field(name=prefixo + "flip", value="Tirar cara ou coroa", inline=False)
        embed1.add_field(name=prefixo + "regras", value="Ler as regras do servidor", inline=False)
        embed1.add_field(name=prefixo + "sobre", value="sobre o bot e talz", inline=False)
        embed1.add_field(name=prefixo + "status" " nomedouser", value="mostra os status do user mencionado", inline="false")
        #embed1.add_field(name=prefixo + "roles", value="Para pegar algum cargo!")
        await ctx.channel.send(embed=embed1)


@bot.command()
async def flip(ctx):
    if ctx.channel.id == 923236110744830032:
        channel = ctx.channel
        moeda = random.randint(1, 2)
        await channel.send('[1] para cara \n'
                            '[2] para coroa')

        def check(m):
            return m.content == '1' or '2' and m.channel == channel
        msg = await bot.wait_for('message', check=check, timeout=60.0)

        if moeda == 1:
            moeda = 'cara'
        elif moeda == 2:
            moeda = 'coroa'

        await channel.send(f'A face da moeda eh {moeda} {ctx.author.mention}! :partying_face:')

        print(moeda)


@bot.command()
async def sobre(ctx):
    if ctx.channel.id == 923236110744830032:
        autor = bot.get_user(911000560109514752)
        embed = discord.Embed(
            title="Sobre mim", description="Entusiasta de bots, desenvolvedor back-end da linguagem Python e bibliotecas py-cord e tkinter.\n"
                                            "Estou sempre disposto a ouvir sugestoes :man_mage:, meus contatos esta no link abaixo :wink:",
            url="https://thiagobeleren.github.io/mylinktree/"
            )
        embed.add_field(name="Sobre o Bot", value=f"O bot e de uso livre, criador por {autor.mention}")
        embed.set_thumbnail(url=bot.user.avatar.url)
        await ctx.channel.send(embed=embed)

    
    

bot.run(token)