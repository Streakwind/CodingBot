from discord.ext import commands
import discord
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, banreason=None):
      """Bans a specified user from the guild"""
      await member.ban(reason=banreason)
      await ctx.send(f"{member} has been banned by {ctx.author}. Reason: {banreason}")
      
    @commands.Cog.listener('on_command_error')
    async def command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You can't do that!")
            
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, kickreason=None):
      """Kicks a specified user from the guild"""
      await member.kick(reason=kickreason)
      await ctx.send(f"{member} has been kicked by {ctx.author}. Reason: {kickreason}")
            
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount: int):
        #for i in range(amount + 1):
         # await ctx.channel.purge(limit=1)

          #await asyncio.sleep(1.5)
        
        await ctx.channel.purge(limi=amount+1)
        
        await ctx.send(f"Successfully purged {amount} messages.")

def setup(bot):
    bot.add_cog(Moderation(bot))