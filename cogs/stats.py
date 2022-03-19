from discord.ext import commands
import discord
from discord import Member
import datetime
import humanize
from humanize import precisedelta

class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ["update"])
    async def updatelog(self, ctx):
        """Update log for the bot!"""
        await ctx.send ("*https://github.com/Streakwind/Monke/commits/main")

    @commands.command()
    async def prefix(self, ctx):
        """Prefixes for the bot"""
        await ctx.send(f"Prefixes: {self.bot.command_prefix}")
    
    @commands.command(aliases=["latency"])
    async def ping(self, ctx):
        """The bots ping/latency"""
        await ctx.send(f"My ping is {self.bot.latency * 1000}ms")
    
    @commands.command()
    async def sourcecode(self, ctx):
        """Source code for the bot"""
        await ctx.send("<https://github.com/Streakwind/Monke>")
    
    @commands.command()
    async def uptime(self, ctx):
        uptime_before = datetime.datetime.utcnow() - self.bot.uptime
        
        uptime = precisedelta(uptime_before)
        
        await ctx.send(f"I booted up {uptime} ago")

    @commands.command(aliases = ["issue", "reportissue"])
    async def report(self, ctx):
        await ctx.send("Problem with the bot? Report issues here! <https://github.com/Streakwind/Monke/issues>")

def setup(bot):
    bot.add_cog(Statistics(bot))

