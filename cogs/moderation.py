import nextcord
from nextcord.ext import commands
import time


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'`Moderation Cog` is ready!')

    @nextcord.slash_command(description="Informacoes do membro do servidor")
    @commands.has_permissions(administrator=True)
    async def userinfo(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        if member is None:
            member = interaction.user
        roles = [role for role in member.roles]

        embed = nextcord.Embed(
          title=f"Informacoes sobre o {member.name}",
          description=f"*Membro id:* `{member.id}` \n "
        )
        embed.add_field(
            name="Status",
            value=f"{member.status}"
        )

        if member.activity is None:
            activity = f"{member.status}"
        else:
            activity = f"{member.status} & {member.activity.name}"

        embed.add_field(
          name="*Atividade *",
          value=f"{activity}"
        )
        embed.add_field(
          name="*Entrou em *",
          value=f"{member.joined_at.strftime('%a, %B %d, %Y, %I:%M %p')}"
        )
        embed.add_field(
          name=f"Roles ({len(roles)})",
          value=" ".join(role.mention for role in member.roles)
        )

        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(description="Informacoes sobre o servidor")
    @commands.has_permissions(administrator=True)
    async def serverinfo(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
          title="Informacoes do servidor",
          description=
            f"Nome: **{interaction.guild.name}** \n"
            f"Quantidade de Membros: ({interaction.guild.member_count}) \n"
            f"Canais: {len(interaction.guild.channels)} | Canais de Voz: {len(interaction.guild.voice_channels)} \n"
            f"Dono do servidor: {interaction.guild.owner.name}",
          color=nextcord.Color.red()
        )
        embed.set_thumbnail(
          url=f"{interaction.guild.icon}"
        )
        embed.add_field(
          name="Server descricao",
          value=f"{interaction.guild.description}"
        )
        embed.set_footer(
          text=f"Server criado em: {interaction.guild.created_at.strftime('%a, %B %d, %Y, %I:%M %p')} UK "
        )
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
