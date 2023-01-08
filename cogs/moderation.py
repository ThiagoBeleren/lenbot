import discord
from discord.ext import commands
import time


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Por favor preencha todos os parametros :rolling_eyes:.')
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
    #@discord.member
    async def userinfo(self, ctx: commands.Context, member: discord.Member=None):
        if member == None:
            member = ctx.author
        roles = [role for role in member.roles]
        embed = discord.Embed(title=f"Informacoes sobre o {member.name}", description=f"*User id:* `{member.id}` \n "
                                                                                      f"*User real name* `{member.name}#{member.discriminator} {member.mention}` \n"
                                                                                      f"*User Nickname* `{member.display_name}` \n")
        embed.add_field(name="*Activity*", value=f"{member.status} & {member.activity.name}")
        embed.add_field(name="*joined at*", value=f"{member.joined_at.strftime('%a, %B %d, %Y, %I:%M %p')}")
        embed.add_field(name="twitch", value=f"{member}")
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join(role.mention for role in member.roles))
        embed.add_field(name=f"Bot owner?", value=f"{member.bot}")
        embed.set_thumbnail(url=member.avatar)
        await ctx.respond(embed=embed)


    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def serverinfo(self, ctx: commands.Context):
        embed = discord.Embed(title="Server Info",
                              description=f"Name : {ctx.guild.name} \n"
                                          f"Members Count ({ctx.guild.member_count}) \n"
                                          f"Channels: {len(ctx.guild.channels)} | Voice Channels {len(ctx.guild.voice_channels)} \n"
                                          f"Server`s Owner: {ctx.guild.owner.name}#{ctx.guild.owner.discriminator}",
                              color=discord.Color.red())
        embed.set_thumbnail(url=f"{ctx.guild.icon}")
        embed.add_field(name="server description", value=f"{ctx.guild.description}")
        embed.set_footer(text=f"Server created at: {ctx.guild.created_at.strftime('%a, %B %d, %Y, %I:%M %p')} UK ")
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))