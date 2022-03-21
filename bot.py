import discord
from discord.ext import commands
from discord import Member
import random
import traceback
import sys
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import config
import logging
import datetime

description = ''''''

def get_prefix(bot, message):
  return ["a!", "coding ", "A!", "Coding "]

intents = discord.Intents.default()
intents.members = True

initial_extensions = (
    'cogs.admin',
    'cogs.moderation',
    'cogs.music',
    'cogs.fun',
    'cogs.information',
    'cogs.stats',
    'cogs.log',
    'cogs.reactionroles',
)

class CodingBot(commands.Bot):
    def __init__(self):
        self.debugMode=False
        self.uptime=datetime.datetime.utcnow()
        self.bot_id=954853701233836143
        self.bot_guild=871097075192954930
        self.blacklist=[0]

        super().__init__(
            command_prefix=get_prefix,
            description=description,
            owner_id=714554283026153554,
            intents=intents,
        )

        self.load_extension('jishaku')

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()


    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('TIME: %(asctime)s, LEVEL: %(levelname)s, NAME: %(name)s: %(message)s'))
    logger.addHandler(handler)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print ('Wuchu for life!11!!!1!!')
        print('------')
        await self.change_presence(activity=discord.Game('a!help'))


    async def on_disconnect(self):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.webhook, adapter=AsyncWebhookAdapter(session))
            await webhook.send('Disconnected from discord.', username='Status')

    async def on_connect(self):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.webhook, adapter=AsyncWebhookAdapter(session))
            await webhook.send('Connected to discord!', username='Status')

    async def on_resumed(self):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(config.webhook, adapter=AsyncWebhookAdapter(session))
            await webhook.send('Resumed connection to discord!', username='Status')

bot = CodingBot()

bot.help_command = commands.MinimalHelpCommand()

@bot.command(hidden=True)
async def hello(ctx):
    await ctx.send (f"Hello, {ctx.author.mention}. You can use `a!help` to get started.")

bot.run(config.token)
