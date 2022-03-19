from discord.ext import commands
import discord
import traceback
import config
import aiohttp
import sys
from discord import Webhook, AsyncWebhookAdapter
import datetime

class Log (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def direct_message(self, message):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.logging_webhook, adapter=AsyncWebhookAdapter(session))
            if message.guild is None:
                if message.author.id != self.bot.bot_id:
                    if message.author.id != self.bot.owner_id:
                        embed = discord.Embed(title="DIRECT MESSAGE")
                        embed.add_field(name="TIME (UTC)", value=f"<t:{int(message.created_at.timestamp())}>")
                        embed.add_field(name="FROM", value=f"{message.author} ({message.author.id})")
                        embed.add_field(name="MESSAGE", value=f"{message.content}")
                        embed.set_thumbnail(url=message.author.avatar_url)
                        #await webhook.send(f"```DIRECT MESSAGE\nTIME: {message.created_at}UTC\nFROM: {message.author} ({message.author.id})\nMESSAGE: {message.content}```", username='Direct Message Log')
                        await webhook.send(embed = embed, username = "Direct Message Log")

    @commands.Cog.listener('on_command')
    async def logging(self, message):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.logging_webhook, adapter=AsyncWebhookAdapter(session))
       #     channel = bot.get_channel(849678967639638057)

            #channel.send("something")
            destination = None
            if message.guild != None:
                if message.author.id != self.bot.owner_id:
                    destination = f"#{message.channel} ({message.guild})"

                    embed = discord.Embed(title=f"{destination}")
                    embed.add_field(name="TIME (UTC)", value=f"<t:{int(message.created_at.timestamp())}>")
                    embed.add_field(name="FROM", value=f"{message.author} ({message.author.id})")
                    embed.add_field(name="MESSAGE", value=f"{message.content}")
                    embed.set_thumbnail(url=message.author.avatar_url)
                    #await webhook.send(f"```{destination}\nTIME: {ctx.message.created_at}UTC\nFROM: {message.author} ({message.author.id})\nMESSAGE: {ctx.message.content}```", username= 'Log')
                    await webhook.send(embed=embed, username="Log")

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.guild_webhook, adapter=AsyncWebhookAdapter(session))

            if message_before.author.id != self.bot.bot_id:

                embed = discord.Embed(title=f"{message_after.author} has edited a message!")
                embed.add_field(name="TIME (UTC)", value=f"<t:{int(datetime.timestamp(datetime.now()))}")
                embed.add_field(name="LINK", value=f"{message_after.jump_url}")
                embed.add_field(name="BEFORE", value=f"{message_before.content}", inline=True)
                embed.add_field(name="AFTER", value=f"{message_after.content}", inline=True)
                embed.set_thumbnail(url=message_after.author.avatar_url)

                #await webhook.send(f"{message_after.author} has edited a message.\n{message_after.jump_url}\nPrevious: {message_before.content}\nNew: {message_after.content}", username = 'Guild Log')
                await webhook.send(embed=embed, username="Guild Log")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.guild_webhook, adapter=AsyncWebhookAdapter(session))

            if message.author.id != self.bot.bot_id:
                embed = discord.Embed(title=f"{message.author} has deleted a message!")
                embed.add_field(name="TIME (UTC)", value=f"<t:{int(datetime.timestamp(datetime.now()))}")
                embed.add_field(name="MESSAGE", value=f"{message.content}")
                embed.set_thumbnail(url=message.author.avatar_url)
               # await webhook.send(f"{message.author} has deleted a message.\nMessage: {message.content}", username = 'Guild Log')
                await webhook.send(embed=embed, username="Guild Log")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.logging_webhook, adapter=AsyncWebhookAdapter(session))

            """The event triggered when an error is raised while invoking a command.
            Parameters
            ------------
            ctx: commands.Context
                The context used for command invocation.
            error: commands.CommandError
                The Exception raised.
            """
            if hasattr(ctx.command, 'on_error'):
                return

            cog = ctx.cog
            if cog:
                if cog._get_overridden_method(cog.cog_command_error) is not None:
                    return

            #ignored = (commands.CommandNotFound, )
            error = getattr(error, 'original', error)

            #if isinstance(error, ignored):
                #return

            embed = discord.Embed(title=f"Command Error - Time (UTC): <t:{int(ctx.message.created_at.timestamp())}>", description=f"Ignoring exception in command {ctx.command}", color=discord.Color.blue())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="Error", value=f"`{str(error)}`")
            embed.add_field(name="Command User", value=f"{ctx.author} - {ctx.author.id}")

            #guild = self.bot.get_guild(ctx.message.guild_id)
            guild = ctx.message.guild
            embed.add_field(name="Guild", value=guild)

            await webhook.send(embed=embed)

            if self.bot.debugMode:
                embed_1 = discord.Embed(title="Command Error", description=f"Ignoring exception in command {ctx.command}", color=discord.Color.blue())
                embed_1.add_field(name="Error", value=f"`{str(error)}`")

                await ctx.send(embed=embed_1)
                return

            if isinstance(error, commands.CommandNotFound):
                if not self.bot.debugMode:
                    return await ctx.send(":x: Command not found")

            if isinstance(error, commands.DisabledCommand):
                if not self.bot.debugMode:
                    return await ctx.send(f'{ctx.command} has been disabled.')

            elif isinstance(error, commands.NoPrivateMessage):
                if not self.bot.debugMode:
                    try:
                        return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
                    except discord.HTTPException:
                        pass

            elif isinstance(error, commands.BadArgument):
                if not self.bot.debugMode:
                    if ctx.command.qualified_name == 'tag list':
                        return await ctx.send('I could not find that member. Please try again.')

            if not self.bot.debugMode:
                return await ctx.send("An unknown error occured. Add an issue at <https://github.com/Streakwind/Monke/issues> and press the \"New Issue\" button! Thanks!")

def setup(bot):
    bot.add_cog(Log(bot))
