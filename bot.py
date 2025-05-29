import asyncio

import discord
import os
from dotenv import load_dotenv
import config
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# Shared state
import events.logging

events.logging.setup(bot)

async def main():
    await bot.load_extension("cogs.radio")
    await bot.load_extension("cogs.utility")
    await bot.start(TOKEN)

asyncio.run(main())

