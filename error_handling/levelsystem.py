import discord
import json
import os
import requests
import sqlite3

from datetime import datetime
from discord import File
from discord.ext import commands
from discord.ui import Button
from typing import Optional
from easy_pil import Editor, load_image_async, Font

# give role

# #role name
# level = ["level5", "level8", "level9"]
#
# #level amount to get that role
# level_num = [5, 10, 15]

# if you want to give role to the user at any specific level upgrade then you can do like this
# enter the name of the role in a list
level = ["Newbie", "Dona do Scat", "Dona Saori"]

# add the level number at which you want to give the role
level_num = [5, 10, 15]


class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'`LevelSystem cog` is ready')

    # this will increase the user's xp everytime they message
    @commands.Cog.listener()
    async def on_message(self, message):
        # the bot's prefix is ? that's why we are adding this statement so user's xp doesn't increase when they use any commands
        if not message.content.startswith("/"):
            # checking if the bot has not sent the message
            if not message.author.bot:
                with open("levels.json", "r") as read_file:
                    data = json.load(read_file)

                # checking if the user's data is already there in the file or not
                if str(message.author.id) in data:
                    xp = data[str(message.author.id)]["xp"]
                    lvl = data[str(message.author.id)]["level"]
                    money = data[str(message.author.id)]["money"]

                    # increase the xp by the number which has 100 as its multiple
                    increased_xp = xp + 25
                    new_level = int(increased_xp / 100)

                    data[str(message.author.id)]["xp"] = increased_xp

                    with open("levels.json", "w") as f:
                        json.dump(data, f)

                    if new_level > lvl:
                        await message.channel.send(
                            f"{message.author.mention} Aumentou seu Nivel para **{new_level}** :partying_face: !!!"
                        )

                        data[str(message.author.id)]["level"] = new_level
                        data[str(message.author.id)]["xp"] = 0
                        data[str(message.author.id)]["money"] = money

                        with open("levels.json", "w") as f:
                            json.dump(data, f)

                        for i in range(len(level)):
                            if new_level == level_num[i]:
                                await message.author.add_roles(
                                    discord.utils.get(message.author.guild.roles, name=level[i]))

                                mbed = (discord.Embed(
                                    title=f"{message.author} Voce conseguiu o cargo **{level[i]}**!",
                                    color=message.author.colour))
                                mbed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.respond(embed=mbed)

                            else:
                                data[str(message.author.id)] = {}
                                data[str(message.author.id)]["xp"] = 0
                                data[str(message.author.id)]["level"] = 1
                                data[str(message.author.id)]["money"] = 1

                            with open("levels.json", "w") as f:
                                json.dump(data, f)

    @commands.slash_command(description="rank")
    async def rank(self, ctx: commands.Context, user: discord.Member):
        userr = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)

            xp = data[str(userr.id)]["xp"]
            lvl = data[str(userr.id)]["level"]
            money = data[str(userr.id)]["money"]

            next_level_xp = (lvl + 1) * 100
            xp_need = next_level_xp
            xp_have = data[str(userr.id)]["xp"]

            percentage = int(((xp_have * 100) / xp_need))

            if percentage < 1:
                percentage = 0

            ## Rank card
            background = Editor(f"len_adolescence.jpg")
            profile = await load_image_async(str(userr.display_avatar))

            profile = Editor(profile).resize((150, 150)).circle_image()

            poppins = Font.poppins(size=40)
            poppins_small = Font.poppins(size=30)

            # you can skip this part, I'm adding this because the text is difficult to read in my selected image
            ima = Editor("zBLACK.png")
            background.blend(image=ima, alpha=.5, on_top=False)

            background.paste(profile.image, (30, 30))

            background.rectangle((30, 220),
                                 width=650,
                                 height=40,
                                 fill="#fff",
                                 radius=20)
            background.bar(
                (30, 220),
                max_width=650,
                height=40,
                percentage=percentage,
                fill="#ff9933",
                radius=20,
            )
            background.text((200, 40),
                            str(userr.name),
                            font=poppins,
                            color="#ff9933")
            background.rectangle((200, 100), width=350, height=2, fill="#ff9933")
            background.text(
                (200, 130),
                f"Level : {lvl}   " + f" XP : {xp} / {(lvl + 1) * 100} ",
                font=poppins_small,
                color="#ff9933",
            )
            background.text(
                (200, 180),
                f"Money: {money}",
                font=poppins_small,
                color="#ff9933",
            )
            card = File(fp=background.image_bytes, filename="zCARD.png")
            await ctx.send(file=card)

    @commands.slash_command(description="Tabela de rank do servidor ")
    async def servidorrank(self, ctx, range_num=10):
        with open("levels.json", "r") as f:
            data = json.load(f)

        l = {}
        total_xp = []

        for userid in data:
            xp = int(data[str(userid)]['xp'] +
                     (int(data[str(userid)]['level']) * 100))

            l[xp] = f"{userid};{data[str(userid)]['level']};{data[str(userid)]['xp']}"
            total_xp.append(xp)

        total_xp = sorted(total_xp, reverse=True)
        index = 1

        mbed = discord.Embed(title="Tabela de rank do servidor")

        for amt in total_xp:
            id_ = int(str(l[amt]).split(";")[0])
            level = int(str(l[amt]).split(";")[1])
            xp = int(str(l[amt]).split(";")[2])

            member = await self.bot.fetch_user(id_)

            if member is not None:
                name = member.name
                mbed.add_field(name=f"{index}. {name}",
                               value=f"**Level: {level} | XP: {xp}**",
                               inline=False)

                if index == range_num:
                    break
                else:
                    index += 1

        await ctx.respond(embed=mbed)

    @commands.slash_command(description="resetar seu rank do servidor")
    async def servidorresetarrank(self, ctx, user: discord.Member):
        member = user or ctx.author

        # this if statement will check that user who's using this command is trying to remove his data or any other user data
        # if she is trying to remove any other user's data then we are going to check that he has a specific role or not (in my case its 'Bot-Mod') so that only admins can remov any users data and not other people can remove other
        if not member == ctx.author:
            role = discord.utils.get(ctx.author.guild.roles, name="Moderadores")

            if not role in member.roles:
                await ctx.send(
                    f"Voce so pode resetar seu rank, somente {role.mention} podem alterar ranks de outros membros"
                )  # sunglasses emoji
                return

        with open("levels.json", "r") as f:
            data = json.load(f)

        del data[str(member.id)]

        with open("levels.json", "w") as f:
            json.dump(data, f)

        await ctx.respond(f"{member.mention}' Resetou seus dados")  # sad emoji

    @commands.slash_command(description="aumentar nivel")
    @commands.has_role("Moderador")
    async def aumentarnivel(self, ctx, increase_by: int,
                            user: discord.Member):
        member = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)

        data[str(member.id)]["level"] += increase_by

        with open("levels.json", "w") as f:
            json.dump(data, f)

        await ctx.respond(
            f"{member.mention}, Parabens , seu nivel aumentou para **{increase_by}**"
        )

    @commands.slash_command(description="aumentar xp")
    @commands.has_role("Moderador")
    async def aumentarxp(self, ctx, increase_by: int,
                         user: discord.Member):
        member = user or ctx.author

        with open("levels.json", "r") as f:
            data = json.load(f)

        data[str(member.id)]['xp'] += increase_by

        with open("levels.json", "w") as f:
            json.dump(data, f)

        await ctx.send(
            f"{member.mention}, Seu xp foi alterado para `{increase_by}`")


def setup(bot):
    bot.add_cog(LevelSystem(bot))
