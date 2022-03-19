from discord.ext import commands
import discord
from discord import Member
import random
import traceback
import sys
#import humanize
#from humanize import precisedelta
from typing import Union
import datetime

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joined(self, ctx, member: discord.Member = None):
        """Tells you when a member joined."""

        if not member:
            member = ctx.author

        await ctx.send('{0.name} joined in {0.joined_at} UTC'.format(member))

    @commands.command()
    async def avatar(self, ctx, member: discord.User = None):
       """Displays a specified users avatar"""
       if not member:
           member = ctx.author
       em = discord.Embed(title = str(member))
       em.set_image(url=member.avatar_url)
       await ctx.send(embed=em)

    @commands.command()
    async def userid(self, ctx, member: discord.User = None):
        """Tells you the user ID for a certain user"""

        if not member:
            member = ctx.author
        await ctx.send(f"{member}'s user id is {member.id}")

    @commands.command(aliases = ["ui"])
    async def userinfo(self, ctx, *, member: Union[discord.Member, discord.User] = None):
        """Information about a certain user"""

        if not member:
            member = ctx.author

        time_1 = str(ctx.message.created_at)[:19]

        embed = discord.Embed(title=f"{member}", description="", color=discord.Color.blue())
        embed.set_author(name=f"{member} - {member.id}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(icon_url="https://images-ext-2.discordapp.net/external/dAn5X2wnC6ZXQ1R2Gc-KR4cTBiKv7gTxQlWQZXIq0xc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/736380975025619025/ab9e6644e42342400080d8dc3ce6afd3.webp?width=80&height=80", text=f"Monke | {time_1} ")

        #time=precisedelta(member.created_at, minimum_unit="hours")
        #time = member.created_at.timestamp()

        embed.add_field(name="User created at (UTC)", value=f"<t:{int(member.created_at.timestamp())}>", inline=True)

        if ctx.guild:
            if member in ctx.guild.members:
                #time_2=precisedelta(member.joined_at, minimum_unit="hours")
                #time_2 = member.joined_at.timestamp()

                embed.add_field(name="User joined at (UTC)", value=f"<t:{int(member.joined_at.timestamp())}>", inline=True)
            else:
                embed.description += f"This user ({member}) is not in the guild"

            if member in ctx.guild.members:
                if member.id == ctx.guild.owner.id:
                    embed.description += f"\nThis user owns this server ({ctx.guild.name})"

        if member.bot:
            embed.description += "This user is a bot"

     #   embed.author.icon_url(url=member.avatar_url)

       # if member.bot == true:
          #  isbot = "YES"
 #       await ctx.send(f"{member}\nUSERID:{member.id}\nBOT:{isbot}\nAVATAR:{member.avatar_url}")
        await ctx.send(embed = embed)

    @commands.command(aliases = ["gi"])
    async def guildinfo(self, ctx):

        guild = ctx.guild

        if ctx.guild:
            embed = discord.Embed(title="", description="", color=discord.Color.blue())
            embed.set_author(name=f"{guild} - {guild.id}", icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)
            embed.add_field(name="Guild Owner", value=guild.owner, inline=True)
            embed.set_footer(icon_url="https://images-ext-2.discordapp.net/external/dAn5X2wnC6ZXQ1R2Gc-KR4cTBiKv7gTxQlWQZXIq0xc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/736380975025619025/ab9e6644e42342400080d8dc3ce6afd3.webp?width=80&height=80", text=f"Monke")
            embed.add_field(name="Guild created at", value=f"<t:{int(guild.created_at.timestamp())}>", inline=True)
            embed.add_field(name="Members", value=guild.member_count, inline=True)
            embed.add_field(name="Emojis", value=guild.emojis, inline=True)
            embed.add_field(name="Emoji limit", value=guild.emoji_limit, inline=True)
            embed.add_field(name="Text channels", value=guild.text_channels, inline=True)
            embed.add_field(name="Voice channels", value=guild.voice_channels, inline=True)
      #      embed.timestamp(str(ctx.message.created_at)[:19])
            await ctx.send(embed = embed)

        else:
            await ctx.send("This command can only be used in guilds/servers!")

def setup(bot):
    bot.add_cog(Information(bot))
