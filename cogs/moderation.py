import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Por favor preencha todos os argumentos :rolling_eyes:.')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Voce nao tem todas as permissoes :angry:")


    @commands.slash_command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        await ctx.kick(reason=reason)
        await ctx.send(reason)
        print(member.display_name, member.id, reason)


    @commands.slash_command()
    @commands.has_permissions(ban_members=True, administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        await member.ban(reason=reason)
        await ctx.respond(f'O {member.name} foi banido por {reason}')
        print(member.display_name, member.id, reason)


    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
        print(user.display_name, user.id)

    @commands.slash_command(aliases=['shutdown'])
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx: commands.Context):
        await ctx.respond('Desligando o bot...')
        await self.bot.close()


    @commands.slash_command(aliases=['userinfo'])
    @commands.has_permissions(administrator=True)
    async def userinfo(self, ctx: commands.Context, member: discord.Member=None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"Informacoes sobre o {member.name}", description=f"*User id:* `{member.id}` \n "
                                                                                      f"*User real name* `{member.name}#{member.discriminator}` \n"
                                                                                      f"*User Nickname* `{member.display_name}` \n")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))