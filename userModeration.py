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
        db = sqlite3.connect("warning.sqlite")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS userwarning(user, guild, date, hour, time, reason)")
        
        db2 = sqlite3.connect("userlist.sqlite")
        cursor2 = db2.cursor()
        cursor2.execute("CREATE TABLE IF NOT EXISTS userlist(user, guild, date, hour, banned kicked by, reason)")
        
        print(f"SQL server READY!")
    
    async def addembed(self, ctx, member: discord.Member, reason, type):
        embed = discord.Embed(title=f"Um membro foi {type} deste servidor! 😔")
        embed.add_field(name="Motivo", value=f"`User: {member.mention} ` \n"
                        f"*Relatorio: {reason}* \n")
        embed.set_footer(text=f"{type} por {ctx.author} \n"
                         f"em _{self.date}_ as {self.hour}")
        await ctx.respond(embed=embed)
        
    async def addwarn(self, ctx, member, reason, time):
        await self.addembed(ctx, member, reason, type = 'advertido')
        db = sqlite3.connect("warning.sqlite")
        cursor = db.cursor()
        cursor.execute("INSERT INTO userwarning(user, guild, date, hour, time, reason) VALUES (?, ?, ?, ?, ?, ?)", (member.id, ctx.guild.id, self.date, self.hour, time, reason))
        db.commit()
    
    async def addkick(self, ctx, member: discord.Member, reason: str, time: int):
        await member.kick(reason=reason)
        await self.addembed(ctx, member, reason, type = 'expulso')
        db = sqlite3.connect("userlist.sqlite")
        cursor = db.cursor()
        cursor.execute("INSERT INTO userlist(user, guild, date, hour, banned kicked by, reason) VALUES (?, ?, ?, ?, ?, ?)", (member.id, ctx.guild.id, self.date, self.hour, ctx.author.id, reason))
        
        cursor.execute("SELECT * FROM userwarning WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        data = cursor.fetchall()
        
        if len(data) >= 3:
            muteRole = discord.utils.get(ctx.guild.roles, name="muted")
            await member.add_roles("muted")
            await ctx.respond(f"Voce tem {len(data)} advertencias, o maximo permitido neste servidor, entao uma penalidade sera aplicada") 
            await asyncio.sleep(time*60)
            await member.remove_roles(muteRole)
            await ctx.respond(f"{member.mention} has been umuted")
        
        db.commit()
        
        
    @commands.slash_command(description="Expulse um membro do servidor")
    @commands.has_permissions(kick_members=True)
    async def kickuser(self, ctx, member: discord.Member, reason: str):
        await self.addkick(ctx, member, reason)
        
        
    @commands.slash_command()
    @commands.has_permissions(manage_roles=True)
    async def warnuser(self, ctx, member: discord.Member, reason: str, time: int):
        await self.addwarn(ctx, member, reason, time)
        
        
    @commands.slash_command()
    @commands.has_permissions(kick_members=True, manage_roles=True)
    async def removewarn(self, ctx, member: discord.Member):
        db = sqlite3.connect("userinfo.sqlite")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM userwarning WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
        data = cursor.fetchone()
        if data:
            cursor.execute("DELETE FROM userwarning WHERE user = ? AND guild = ?", (member.id, ctx.guild.id))
            await ctx.respond(f"Advertencias de {member.mention} foram removidos!")
        
        else:
            await ctx.respond(f"{member.mention} nao tem advertencias!")
            
        db.commit()
        
def setup(bot):
    bot.add_cog(userModeration(bot))