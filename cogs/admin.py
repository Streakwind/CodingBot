from discord.ext import commands
import discord
import traceback
import asyncio
import datetime
import humanize
from humanize.time import precisedelta

class Admin (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await commands.is_owner().predicate(ctx)

    @commands.command(hidden=True)
    async def reload(self, ctx, extension):
        """Reload an extension"""

        try:
            self.bot.reload_extension(extension)
            print(f"{extension} successfully reloaded.")
            emoji = '\N{THUMBS UP SIGN}'
            await ctx.message.add_reaction(emoji)
        except Exception as e:
            # this next line formats the traceback and sends it
            error = "".join(traceback.format_exception(type(e), e, e.__traceback__, 1))
            return await ctx.send(f"Failed to reload extension {extension}:\n```{error}```")

    # @reload.command()
    # async def all(self, ctx):
    #     """Reload all extensions"""
    #     try:
    #         self.bot.load_extension(cogs.admin)
    #         self.bot.load_extension(cogs.fun)
    #         self.bot.load_extension(cogs.information)
    #         self.bot.load_extension(cogs.log)
    #         self.bot.load_extension(cogs.moderation)
    #         self.bot.load_extension(cogs.music)
    #         self.bot.load_extension(cogs.stats)
    #     except Exception as e:
    #         error = "".join(traceback.format_exception(type(e), e, e.__traceback__, 1))
    #         return await ctx.send(f"Failed to reload extensions {extension}:\n```{error}```")

    @commands.command(hidden=True)
    async def changeactidle(self, ctx):
        """Changed the status to idle."""
        await self.bot.change_presence(status=discord.Status.idle)
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)

    @commands.command(hidden=True)
    async def changeactdnd(self, ctx):
        """Changed the status to DND."""
        await self.bot.change_presence(status=discord.Status.do_not_disturb)
        #await ctx.send ("Success!")
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)

    @commands.command(hidden=True)
    async def changeactoff(self, ctx):
        """Changed the status to invisible."""
        await self.bot.change_presence(status=discord.Status.invisible)
        #await ctx.send ("Success!")
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)

    @commands.command(hidden=True)
    async def resetact(self, ctx):
        """Reset the status."""
        await self.bot.change_presence(status=discord.Status.online)
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)


    @commands.command(hidden=True)
    async def setplay(self, ctx, *, thing):
        """Set's a play status"""
        await self.bot.change_presence(activity = discord.Game(thing))
        #await ctx.send ("Success!")
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)


    @commands.command(hidden=True)
    async def setwatch(self, ctx, *, thing):
        """Set's a watch status"""
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=thing))
        #await ctx.send ("Success!")
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)


    @commands.command(hidden=True)
    async def setlisten(self, ctx, *, thing):
        """Set's a listen status"""
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=thing))
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)


    @commands.command(hidden=True)
    async def repeat(self, ctx, times: int, *, content='repeating...'):
        """Admin-only command for purge testing."""
        for i in range(times):
            await ctx.send(content)

            await asyncio.sleep(1)

    #JSK is better
    #@commands.command()
    #@commands.is_owner()
    #async def changeactplay(self, ctx, status, game):
    #    """Lets the bot play a game."""
    #    await self.bot.change_presence(status=discord.Status.{status} activity={game})
    #    await ctx.send ("Success!")

    @commands.command(hidden=True)
    async def troll(self, ctx, userid:int, *, message):
        """troll"""
        person = self.bot.get_user(userid)
        await person.send(f"{message}")
        await ctx.send(f"Succesfully sent {message}")

   # @commands.command(hidden = True)
    #async def reply(self, ctx, msgid, msg):
     #   """something"""
      #  message = ctx.channel.fetch_message(msgid)

       # if len(msg) > 20:
       #     time = 2
       # if len(msg) <= 20:
        #    time = 1
       # if len(msg) < 10:
       #     time = 0.5
       # if len(msg) < 5:
       #     time = 0.25

       # await ctx.message.delete()

      #  async with ctx.typing():
       #     await asyncio.sleep(time)
        #    await message.reply(f"{msg}", mentionauthor = False)

    @commands.command()
    async def debug_mode(self, ctx):
        """Turn debug mode on/off"""
        if self.bot.debugMode:
            self.bot.debugMode=False
            emoji = '\N{THUMBS UP SIGN}'
            await ctx.message.add_reaction(emoji)

        else:
            self.bot.debugMode=True
            emoji = '\N{THUMBS UP SIGN}'
            await ctx.message.add_reaction(emoji)
    @commands.command()
    async def adv_mode(self, ctx):
        """Turn advanced mode on/off"""
        if self.bot.advMode:
            self.bot.advMode=False
            emoji = '\N{THUMBS UP SIGN}'
            await ctx.message.add_reaction(emoji)

        else:
            self.bot.advMode=True
            emoji = '\N{THUMBS UP SIGN}'
            await ctx.message.add_reaction(emoji)

    @commands.command()
    async def blacklist(self, ctx, id):
        """Blacklist"""
        self.bot.blacklist.append(id)
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)

    @commands.command()
    async def whitelist(self, ctx, id):
        """Whitelist"""
        self.bot.blacklist.remove(id)
        emoji = '\N{THUMBS UP SIGN}'
        await ctx.message.add_reaction(emoji)

    @commands.command()
    async def blacklisted(self, ctx):
        """List"""
        for x in self.bot.blacklist:
            await ctx.send(x)


def setup(bot):
    bot.add_cog(Admin(bot))
