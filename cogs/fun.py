from discord.ext import commands
import discord
from discord import Member
import random
import traceback
import sys
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def message(self, ctx, userid:int, *, message):
        """Message another person (Use a!userid person to find their userid)"""
        person = self.bot.get_user(userid)
        await person.send(f"{ctx.author}: {message}\nBy the way, use `a!message {ctx.author.id} yourmessagehere` to message them back")
        await ctx.send(f"Succesfully sent {message}")

    @commands.command(hidden=True)
    async def secret(self, ctx):
        """I wonder what this does...."""
        secret = """
            Never gonna give you up
        Never gonna let you down
        Never gonna run around and desert you
        Never gonna make you cry
        Never gonna say goodbye
        Never gonna tell a lie and hurt you
        """
        em = discord.Embed(description=secret, color=discord.Color.blue())
        await ctx.send(embed = em)

    @commands.command()
    async def messageowner(self, ctx, *, arg:str):
       """Sends the owner a message! """
       owner = self.bot.get_user(self.bot.owner_id)
   #    await owner.send(f"{ctx.message.channel} ({ctx.message.guild})\n{ctx.author} ({ctx.author.id}) has sent you a message!\n{arg}")
       await owner.send(f"{ctx.author} ({ctx.author.id}): {arg}")
       await ctx.send(f"Succesfully sent {arg}")

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format. Example: a!roll 1d2"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command()
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def calc(self, ctx, left:int, operator, right:int):
        """Calculates 2 numbers. (No fractions)"""
        if operator == '/':
            return await ctx.send(left / right)

        if operator == '*':
            return await ctx.send(left * right)

        if operator == '+':
            return await ctx.send(left + right)

        if operator == '-':
            return await ctx.send(left - right)

        else:
            await ctx.send("Invalid operation!")
            error = "".join(traceback.format_exception(type(e), e, e.__traceback__, 1))
            return await ctx.send(f"Error. Here's the traceback:\n```{error}```")

    @commands.command()
    async def say(self, ctx, *, msg):
        """Repeats what you say."""
        #print(f'{ctx.author} used a!say to say {msg}')
        await ctx.send(f"{msg}")

    @commands.command(hidden = True)
    async def specialsay(self, ctx, *, msg):
        """something"""

        if len(msg) > 20:
            time = 2
        if len(msg) <= 20:
            time = 1
        if len(msg) < 10:
            time = 0.5
        if len(msg) < 5:
            time = 0.25

        if ctx.author.id == 224513210471022592 or ctx.author.id == 714554283026153554:
            await ctx.message.delete()

            async with ctx.typing():
                await asyncio.sleep(time)
                await ctx.send(f"{msg}")
        else:
            await ctx.message.delete()

            async with ctx.typing():
                await asyncio.sleep(time)
                await ctx.send(f"{ctx.author}: {msg}")

    @commands.command()
    async def rng(self, ctx, num1: int, num2: int):
        """Picks a random number between the two values"""
        value = random.randint(min(num1, num2), max(num1, num2))
        await ctx.send(f"You got {value}.")

    @commands.command()
    async def dpy_docs(self, ctx):
        """Sends the link to the discord.py documentation"""

        await ctx.send("Most of the stuff: <https://discordpy.readthedocs.io/en/latest/api.html#>\nMain page: https://discordpy.readthedocs.io/en/latest/index.html")

def setup(bot):
    bot.add_cog(Fun(bot))
