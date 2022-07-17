import discord
from discord.ext import commands
import asyncio
import random
import configs

intents = discord.Intents.default()
intents.members = True
token = configs.Token()
bot = commands.Bot(intents=intents, command_prefix="!")
prefixo = "!"
botimage = "https://s2.glbimg.com/g5ZxDqRORBmMoW2h1WPkHdT9pCs=/0x0:1465x916/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2021/c/1/nGOd5lQbOCz8BbFU3QXA/paimon-genshin.jpg"
command_channel = 923236110744830032
        
@bot.event
async def on_ready():
    await bot.change_presence(activity = discord.Game(name = 'Project Sekai: Colourfull Stage'))
    print(bot.user.name, 'está Online')

    
@bot.event
async def on_member_join(member):
    guild = member.guild #guild = server
    welcome_channel = bot.get_channel(911058863774654517)

    embed3 = discord.Embed(description=f":partying_face: Bem vindo ao servidor, {member.mention}.\n Espero que se divirta por aqui.")
    embed3.add_field(name='Integrantes', value=f'você é o {len(guild.members)}* integrante do total de {len(guild.members)} participantes do servidor.', inline=False)
    embed3.set_author(name=member.display_name, icon_url=member.display_avatar)
    embed3.add_field(name='ID', value=member.id, inline=False)
    embed3.set_image(url="https://cdn.discordapp.com/attachments/996151321096892636/997995707615162388/tenor.gif")
    await welcome_channel.send(embed=embed3)


#Verifica se o canal eh realmente o de comando no momento em que o member mandar a mensagem!
@bot.event
async def on_command(ctx, member: discord.Member = None):
    message_channel_id = bot.get_channel(' ')
    command_channel = bot.get_channel(923236110744830032)
    if message_channel_id == command_channel:
        return
    elif message_channel_id != command_channel:
        embed = discord.Embed(description=f"Voce nao pode mandar comandos por aqui {ctx.author.mention}")
        await ctx.send(embed=embed)
        asyncio.sleep(10)
        await message_channel_id.delete(ctx.author, ctx.message)
        
        
@bot.command()
async def twitch(ctx):
    channel_live = bot.get_channel(988883848060354620)
    allowed_mentions = discord.AllowedMentions(everyone = True)
    admin = bot.get_user(911000560109514752)
    message = ctx.channel.id
    
    command_channel = bot.get_channel(923236110744830032)
    print(f"{ctx.author}, {command_channel}, {channel_live}")
    
    if ctx.author == admin and ctx.channel == command_channel:
        print(f"{ctx.author}, {command_channel}, {channel_live}")
        embed = discord.Embed(descripition=f"ESTOU EM LIVE!")
        embed.add_field(name="Venha ver agora!", value="https://www.twitch.tv/ezdeterno", inline="False")
        embed.add_field(name="Quer ter sua mensagem vista na live? mande-a pelo pix!", value="Chave: thiagobeleren@gmail.com")
        embed.set_image(url='https://i.pinimg.com/564x/b7/c6/e5/b7c6e50a80b89476537711767aa677dd.jpg')
        await channel_live.send(embed=embed, content = '@everyone', allowed_mentions = allowed_mentions)
        print(f'mensagem de live enviada ao canal {channel_live}')
        
#Show random images or gifs to a embed !working on!
@bot.command()
async def musica(ctx):
    
    playlist = random.randint(1, 2)
    if playlist == 1:
        embed1 = discord.Embed(
        description=f'Album recomendado de hoje!'
        )
        embed1.add_field(name='Title',
                        value=f'Beyondcore Evangelix')
        await ctx.message.send(embed=embed1)
        await ctx.message.send("https://open.spotify.com/album/4YMCeV11IVZR4G5KJIoZTJ?si=ff6db3bfbfbd43c2")

    elif playlist == 2:
        embed2 = discord.Embed(
            description=f'Album recomendado de hoje!'
        )
        embed2.add_field(name='Title',
                            value=f'Encore Emotion Vocal Pop: 02')
        await ctx.send(embed=embed2)
        await ctx.send("https://open.spotify.com/album/4YMCeV11IVZR4G5KJIoZTJ?si=ff6db3bfbfbd43c2")


#Nao esta funcionando! nao sei pq?, isso iria mostrar oque o user mencionado estava ouvindo!
@bot.command(aliases=['whois', 'user'])
async def userinfo(ctx, member: discord.Member = None):
    if member:
        if not member.id in [923236110744830032, 988887114634629130]:
            if member.activity == None:
                activity = 'Inactive'

            elif type(member.activity) == discord.Spotify:
                activity = 'Spotify' \
                           f'\n{member.activity.artist} - {member.activity.title}' \
                           f'\n aus [{member.activity.album}]({member.activity.album_cover_url})'

            else:
                activity = f'{member.activity.name}'

            embed = discord.Embed(color=member.top_role.color.value, title=f'Musica que {member} esta ouvindo :headphones:')
            embed.add_field(name='**Activity**', value=f'{activity}', inline=True)
            await ctx.send(embed=embed)


@bot.command()
async def regras(ctx):
    command_channel = bot.get_channel(923236110744830032)
    membro = bot.get_user(' ')
    if ctx.channel.id == 923236110744830032:
        embed4 = discord.Embed(title=f'Regras de conduta no servidor', color=10181046)
        embed4.set_author(name=bot.user.name, icon_url=botimage)
        embed4.set_image(url="https://images2.alphacoders.com/117/1171852.png")
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
        embed1.set_thumbnail(url=botimage)
        embed1.add_field(name="-" + "music" " nome da musica", value=f"para o bot tocar a musica {bot_de_musica.mention}", inline=False)
        embed1.add_field(name="!" + "rpg", value="Informacoes sobre o rpg", inline=True)
        embed1.add_field(name="!" + "flip", value="Tirar cara ou coroa", inline=False)
        embed1.add_field(name="!" + "regras", value="Ler as regras do servidor")
        embed1.add_field(name="!" + "sobre", value="sobre o bot e talz")
        embed1.add_field(name="!"+ "userinfo" "nomedouser", value="mostra os status do spotfy do user mencionado")
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

        await channel.send('A face da moeda eh {} {.author}!, :partying_face:'.format(moeda, msg))

        print(moeda)

    elif ctx.channel.id != 923236110744830032:
        await ctx.channel.send(
            'Voce nao tem permissao para digitar comando aqui bobinho! :stuck_out_tongue_closed_eyes:')


@bot.command()
async def sobre(ctx):
    if ctx.channel.id == 923236110744830032:
        autor = bot.get_user(911000560109514752)
        embed = discord.Embed(
            title="Sobre mim", description="Entusiasta de bots, desenvolvedor back-end das linguagens Python e Javascript.\n"
                                            "Estou sempre disposto a ouvir sugestoes :man_mage:, meu discord esta no link acima :wink:",
            url="https://discord.gg/ZtDpVNzq94"
            )
        embed.add_field(name="Sobre o Bot", value=f"O bot e de uso livre, criador por {autor.mention}")
        embed.set_thumbnail(url="https://s2.glbimg.com/g5ZxDqRORBmMoW2h1WPkHdT9pCs=/0x0:1465x916/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_08fbf48bc0524877943fe86e43087e7a/internal_photos/bs/2021/c/1/nGOd5lQbOCz8BbFU3QXA/paimon-genshin.jpg")
        await ctx.channel.send(embed=embed)

        
    
    
    
    

bot.run(token)