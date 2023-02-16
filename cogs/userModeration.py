import sqlite3
import asyncio
import discord

from datetime import datetime
from discord.ext import commands
from pytz import timezone
    
class userModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.date = datetime.now()
        self.hour = 2

      
    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("warnings.sqlite")
        cursorwarn = db.cursor()
        cursorwarn.execute("CREATE TABLE IF NOT EXISTS userwarnings(user, guild, date, hour, time, reason)")
        
        db2 = sqlite3.connect("kicks.sqlite")
        cursorkick = db2.cursor()
        cursorkick.execute("CREATE TABLE IF NOT EXISTS userkicks(user, guild, date, hour, kicked by, reason)")

        dbban = sqlite3.connect("bans.sqlite")
        cursorban = dbban.cursor()
        cursorban.execute("CREATE TABLE IF NOT EXISTS userbans(user, guild, date, hour, banned by, reason)")
      
        print("SQL server READY!")
    
    async def addembed(self, ctx, member: discord.Member, reason, type):
        embed = discord.Embed(title=f"Um membro foi {type} deste servidor! 😔")
        embed.add_field(name="Motivo", value=f"`User: {member.mention} ` \n"
                        f"*Relatorio: {reason}* \n")
        embed.set_footer(text=f"{type} por {ctx.author} \n"
                         f"em _{self.date}_ as {self.hour}")
        await ctx.send(embed=embed)
    
    async def addwarn(self, ctx, member, reason, time, warnings):
        await self.addembed(ctx, member, reason, type = 'advertido')
        db = sqlite3.connect("warning.sqlite")
        cursor = db.cursor()
        cursor.execute("INSERT INTO userwarnings(user, guild, warns, date, hour, time, reason) VALUES (?, ?, ?, ?, ?, ?)", (member.id, ctx.guild.id, self.date, self.hour, time, reason))

        cursor.execute("SELECT warnings FROM userwarnings WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        data = cursor.fetchall()
        
        if len(data) >= 3:
            muteRole = discord.utils.get(ctx.guild.roles, name="muted")
            await member.add_roles("muted")
            await ctx.respond(f"Voce tem {len(data)} advertencias, o maximo permitido neste servidor, entao uma penalidade sera aplicada") 
            await asyncio.sleep(time*60)
            await member.remove_roles(muteRole)
            await ctx.respond(f"{member.mention} has been umuted")
        
        db.commit()

    async def addkick(self, ctx, member: discord.Member, reason: str):
        await member.kick(reason=reason)
        await self.addembed(ctx, member, reason, type = 'expulso')
        db = sqlite3.connect("kicks.sqlite")
        cursor = db.cursor()
        cursor.execute("INSERT INTO userkicks(user, guild, date, hour, kicked by, reason) VALUES (?, ?, ?, ?, ?, ?)", (member.id, ctx.guild.id, self.date, self.hour, ctx.author.id, reason))
        db.commit()
      
    async def addban(self, ctx, member: discord.Member, reason: str):
        await member.ban(reason=reason)
        db = sqlite3.connect("bans.sqlite3")
        cursor = db.cursor()
        cursor.execute("INSERT INTO userbans(user, guild, date, hour, banned by, reason) VALUES (?, ?, ?, ?. ?, ?)", (member.id, ctx.guild.id, self.date, self.hour, ctx.author.id, reason))
        db.commit()

    async def removewarn(self, ctx, member: discord.Member, reason : str):
        db = sqlite3.connect("warnings.sqlite")
        cursor = db.cursor()
        cursor.execute("SELECT warnings FROM userwarnings WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        data = cursor.fetchone()
        if data:
            cursor.execute("DELETE FROM userwarnings WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
            await ctx.respond(f"Advertencias de {member.mention} foram removidos!")
        
        else:
            await self.addembed(ctx, member, reason, type='desbanido')
            
        db.commit()

    async def removeban(self, ctx, member: discord.Member, reason: str):
        db = sqlite3.connect("bans.connect")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM userbans WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        cursor.execute("DELETE FROM userbans WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        
    @commands.slash_command(description="Expulse um membro ")
    @commands.has_permissions(kick_members=True)
    async def kickuser(self, ctx, member: discord.Member, reason: str):
        await self.addkick(ctx, member, reason)

      
    @commands.slash_command(description="Mande uma advertencia a um membro")
    @commands.has_permissions(manage_roles=True)
    async def warnuser(self, ctx, member: discord.Member, reason: str, time: int, warnings: int):
        await self.addwarn(ctx, member, reason, time, warnings)

      
    @commands.slash_command(description="Bana um membro")
    @commands.has_permissions(ban_members=True)
    async def banuser(self, ctx, member: discord.Member, reason: str):
      await self.addban(ctx, member, reason)


    @commands.slash_command(description="Remova uma advertecia de um membro")
    @commands.has_permissions(kick_members=True, manage_roles=True)
    async def removewarnuser(self, ctx, member: discord.Member, reason : str):
        await self.removewarn(ctx, member)


    @commands.slash_command(description="Remova o ban de um membro")
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
      banned_users = await ctx.guild.bans()
      member_name, member_discriminator = member.split("#")
  
      for ban_entry in banned_users:
        user = ban_entry.user
  
        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
          await ctx.guild.unban(user)
          await ctx.send(f'Unbanned {user.mention}')
          return
      print(user.display_name, user.id)
      
def setup(bot):
    bot.add_cog(userModeration(bot))