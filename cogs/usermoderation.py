import sqlite3
import asyncio
import nextcord
import colorama

from datetime import datetime
from nextcord.ext import commands
from colorama import Fore


class UserModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.date = datetime.now()
        self.hour = datetime.hour

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{Fore.YELLOW}`UserModeration cog` is READY!")

        db = sqlite3.connect("warnings.sqlite")
        cursorwarn = db.cursor()
        cursorwarn.execute("CREATE TABLE IF NOT EXISTS userwarnings(user, guild, date, hour, time, reason)")

        db2 = sqlite3.connect("kicks.sqlite")
        cursorkick = db2.cursor()
        cursorkick.execute("CREATE TABLE IF NOT EXISTS userkicks(user, guild, date, hour, kicked by, reason)")

        dbban = sqlite3.connect("bans.sqlite")
        cursorban = dbban.cursor()
        cursorban.execute("CREATE TABLE IF NOT EXISTS userbans(user, guild, date, hour, banned by, reason)")

    async def addembed(self, interaction: nextcord.Interaction, member: nextcord.Member, reason, type):
        embed = nextcord.Embed(
            title=f"Um membro foi {type} deste servidor! 😔")
        embed.add_field(
            name="Motivo",
            value=f"`User: {member.mention} `\n"
                  f"*Relatorio: {reason}* \n"
        )
        embed.set_footer(
            text=f"{type} por {interaction.user} \n"
                 f"em _{self.date}_ as {self.hour}"
        )
        await interaction.response.send_messge(embed=embed)

    async def addwarn(self, interaction: nextcord.Interaction, member, reason, time, warnings):
        await self.addembed(interaction, member, reason, type='advertido')
        db = sqlite3.connect("warning.sqlite")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO userwarnings(user, guild, warnings, date, hour, time, reason) VALUES (?, ?, ?, ?, ?, ?)",
            (member.id, interaction.guild.id, self.date, self.hour, time, reason))

        cursor.execute("SELECT warnings FROM userwarnings WHERE user = ? AND guild = ?", (member.id, interaction.guild.id))
        data = cursor.fetchall()

        if len(data) >= 3:
            muteRole = nextcord.utils.get(interaction.guild.roles, name="muted")
            await member.add_roles("muted")
            await interaction.response.send_message(
                f"Voce tem {len(data)} advertencias, o maximo permitido neste servidor, entao uma penalidade sera aplicada")
            await asyncio.sleep(time * 60)
            await member.remove_roles(muteRole)
            await interaction.response.send_message(f"{member.mention} has been umuted")
        db.commit()

    async def addkick(self, ctx, member: nextcord.Member, reason: str):
        await member.kick(reason=reason)
        await self.addembed(ctx, member, reason, type='expulso')
        db = sqlite3.connect("kicks.sqlite")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO userkicks(user, guild, date, hour, kicked by, reason) VALUES (?, ?, ?, ?, ?, ?)",
            (member.id, ctx.guild.id, self.date, self.hour, ctx.author.id, reason)
        )
        db.commit()

    async def addban(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
        await member.ban(reason=reason)
        db = sqlite3.connect("bans.sqlite3")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO userbans(user, guild, date, hour, banned by, reason) VALUES (?, ?, ?, ?. ?, ?)",
            (member.id, interaction.guild.id, self.date, self.hour, interaction.user.id, reason)
        )
        db.commit()

    async def removewarn(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
        db = sqlite3.connect("warnings.sqlite")
        cursor = db.cursor()
        cursor.execute(
            "SELECT warnings FROM userwarnings WHERE user = ? AND guild = ?",
            (member.id, interaction.guild.id)
        )

        data = cursor.fetchone()

        if data:
            cursor.execute(
                "DELETE FROM userwarnings WHERE user = ? AND guild = ?",
                (member.id, interaction.guild.id)
            )
            await interaction.response.send_message(
                f"Advertencias de {member.mention} foram removidos!")

        else:
            await self.addembed(interaction, member, reason, type='desbanido')

        db.commit()

    async def removeban(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
        db = sqlite3.connect("bans.connect")
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM userbans WHERE user = ? AND guild = ?",
            (member.id, interaction.guild.id)
        )
        cursor.execute(
            "DELETE FROM userbans WHERE user = ? AND guild = ?",
            (member.id, interaction.guild.id)
        )

        banned_users = interaction.guild.bans()

        for ban_entry in banned_users:
            user = ban_entry.user
            await interaction.guild.unban(user)
            await interaction.send(f'Unbanned {user.mention}')
            print(user.display_name, user.id)

            return

    @nextcord.slash_command(description="Expulse um membro ")
    @commands.has_permissions(kick_members=True)
    async def kickuser(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
        await self.addkick(interaction, member, reason)

    @nextcord.slash_command(description="Mande uma advertencia a um membro")
    @commands.has_permissions(manage_roles=True)
    async def warnuser(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str, time: int, warnings: int):
        await self.addwarn(interaction, member, reason, time, warnings)

    @nextcord.slash_command(description="Bana um membro")
    @commands.has_permissions(ban_members=True)
    async def banuser(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
        await self.addban(interaction, member, reason)

    @nextcord.slash_command(description="Remova uma advertecia de um membro")
    @commands.has_permissions(kick_members=True, manage_roles=True)
    async def removewarnuser(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
        await self.removewarn(interaction, member, reason)

    @nextcord.slash_command(description="Remova o ban de um membro")
    @commands.has_permissions(administrator=True)
    async def unban(self, interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
        await self.removeban(interaction, member, reason)


def setup(bot):
    bot.add_cog(UserModeration(bot))
