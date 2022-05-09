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

#from Fyssions Clam
class GlobalUser(commands.Converter):
    async def convert(self, ctx, arg):
        try:
            if not ctx.guild:
                raise commands.BadArgument()  # blank to skip
            user = await commands.MemberConverter().convert(ctx, arg)

        except commands.BadArgument:
            try:
                user = await commands.UserConverter().convert(ctx, arg)

            except commands.BadArgument:
                try:
                    arg = int(arg)

                except ValueError:
                    arg = discord.utils.escape_mentions(arg)
                    raise commands.BadArgument(
                        f"Could not find a member or user `{arg}` with that name. Try with their ID instead."
                    )
                try:
                    user = await ctx.bot.fetch_user(arg)

                except discord.HTTPException:
                    raise commands.BadArgument(
                        f"Could not find a member or user with the ID of `{arg}`."
                    )

        return user
        
class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joined(self, ctx, member: discord.Member = None):
        """Tells you when a member joined."""

        if not member:
            member = ctx.author

        await ctx.send('{0.name} joined in {int(0.joined_at.timestamp())} UTC'.format(member)) #<t:{int(member.created_at.timestamp())}>

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

 #    @commands.command(aliases = ["ui"])
 #    async def userinfo(self, ctx, *, member: Union[discord.Member, discord.User] = None):
 #        """Information about a certain user"""
 #
 #        if not member:
 #            member = ctx.author
 #
 #        time_1 = str(ctx.message.created_at)[:19]
 #
 #        embed = discord.Embed(title=f"{member}", description="", color=discord.Color.blue())
 #        embed.set_author(name=f"{member} - {member.id}", icon_url=member.avatar_url)
 #        embed.set_thumbnail(url=member.avatar_url)
 #        embed.set_footer(icon_url="https://images-ext-2.discordapp.net/external/dAn5X2wnC6ZXQ1R2Gc-KR4cTBiKv7gTxQlWQZXIq0xc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/736380975025619025/ab9e6644e42342400080d8dc3ce6afd3.webp?width=80&height=80", text=f"Monke | {time_1} ")
 #
 #        #time=precisedelta(member.created_at, minimum_unit="hours")
 #        #time = member.created_at.timestamp()
 #
 #        embed.add_field(name="User created at (UTC)", value=f"<t:{int(member.created_at.timestamp())}>", inline=True)
 #
 #        if ctx.guild:
 #            if member in ctx.guild.members:
 #                #time_2=precisedelta(member.joined_at, minimum_unit="hours")
 #                #time_2 = member.joined_at.timestamp()
 #
 #                embed.add_field(name="User joined at (UTC)", value=f"<t:{int(member.joined_at.timestamp())}>", inline=True)
 #            else:
 #                embed.description += f"This user ({member}) is not in the guild"
 #
 #            if member in ctx.guild.members:
 #                if member.id == ctx.guild.owner.id:
 #                    embed.description += f"\nThis user owns this server ({ctx.guild.name})"
 #
 #        if member.bot:
 #            embed.description += "This user is a bot"
 #
 #     #   embed.author.icon_url(url=member.avatar_url)
 #
 #       # if member.bot == true:
 #          #  isbot = "YES"
 # #       await ctx.send(f"{member}\nUSERID:{member.id}\nBOT:{isbot}\nAVATAR:{member.avatar_url}")
 #        await ctx.send(embed = embed)

    #following  code imported from Fyssions clam;https://github.com/Fyssion/Clam/blob/main/clam/cogs/tools.py; minor modifications (getting rid of emojis)
    @commands.command(aliases=["memberinfo", "ui", "whois"])
    async def userinfo(self, ctx, *, user: GlobalUser = None):
        """Shows info about a user; credits to Clam"""

        user = user or ctx.author

        is_member = isinstance(user, discord.Member)

        badge_mapping = {
            discord.UserFlags.staff: emojis.DISCORD_DEVELOPER,
            discord.UserFlags.partner: emojis.PARTNER,
            discord.UserFlags.hypesquad: emojis.HYPESQUAD_EVENTS,
            discord.UserFlags.bug_hunter: emojis.BUG_HUNTER,
            discord.UserFlags.bug_hunter_level_2: emojis.BUG_HUNTER_2,
            discord.UserFlags.hypesquad_bravery: emojis.HYPESQUAD_BRAVERY,
            discord.UserFlags.hypesquad_brilliance: emojis.HYPESQUAD_BRILLIANCE,
            discord.UserFlags.hypesquad_balance: emojis.HYPESQUAD_BALANCE,
            discord.UserFlags.early_supporter: emojis.EARLY_SUPPORTER,
            discord.UserFlags.verified_bot_developer: emojis.EARLY_VERIFIED_DEVELOPER,
        }

        badges = []
        for f in user.public_flags.all():
            badge = badge_mapping.get(f)

            if badge:
                badges.append(badge)

        desc = " ".join(badges)
        if user.id == self.bot.owner_id:
            created_or_owns = "created" if user.id == self.bot.owner_id else "owns"
            desc += f"\n:gear: This user {created_or_owns} {self.bot.user.name}."
        if user == self.bot.user:
            desc += "\n:wave: Hey, that's me!"
        if user.bot is True:
            verified = "verified " if user.public_flags.verified_bot else ""
            desc += f"\n:robot: This user is a {verified}bot."
        if is_member and user.id == ctx.guild.owner_id:
            desc += "\nThis user is the server owner."
        if is_member and user.premium_since:
            formatted = user.premium_since.strftime("%b %d, %Y at %#I:%M %p")
            desc += (
                "\n<:boost:649644112034922516> "
                "This user has been boosting this server since "
                f"{formatted}."
            )

        author = str(user)
        if is_member and user.nick:
            author += f" ({user.nick})"
        author += f" - {str(user.id)}"

        icon = user.display_avatar
        try:
            color = await self.get_average_color(icon) if icon else None
        except discord.HTTPException:
            color = None
        color = color or (user.color if is_member and user.color else colors.PRIMARY)

        em = discord.Embed(description=desc, color=color)

        em.set_thumbnail(url=user.display_avatar.url)
        em.set_author(name=author, icon_url=user.display_avatar.url)

        created_fmt = humantime.fulltime(user.created_at, accuracy=2)
        em.add_field(
            name=":clock1: Account Created",
            value=created_fmt,
            inline=True,
        )

        if is_member:
            joined_fmt = humantime.fulltime(user.joined_at, accuracy=2)
            em.add_field(
                name="Joined Server",
                value=joined_fmt,
                inline=True,
            )

            members = ctx.guild.members
            members.sort(key=lambda x: x.joined_at)
            position = members.index(user)

            escape = discord.utils.escape_markdown
            joins = []

            if position > 0:
                joins.append(escape(f"{members[position - 1]} (#{position})"))

            user_pos = f"{user} (#{position + 1})"
            joins.append(f"**{escape(user_pos)}**")

            if position < len(members) - 1:
                joins.append(escape(f"{members[position + 1]} (#{position + 2})"))

            join_order = " \u2192 ".join(joins)
            em.add_field(name="Join Position and Order", value=join_order, inline=False)

            if user.roles[1:]:
                roles = ""
                for role in user.roles[1:]:
                    if len(roles + f"{role.mention} ") > 1012:
                        roles += "...and more"
                        break
                    roles += f"{role.mention} "
                em.add_field(name="Roles", value=roles, inline=False)

        shared = [
            g for g in self.bot.guilds if discord.utils.get(g.members, id=user.id)
        ]

        if not shared:
            em.set_footer(text=f"No servers shared with {self.bot.user.name}")

        else:
            em.set_footer(text=f"{plural(len(shared)):server} shared with {self.bot.user.name}")

        await ctx.send(embed=em)

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
