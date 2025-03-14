import discord
import os
from dotenv import load_dotenv
import config
from discord.ext import commands

load_dotenv()
TOKEN=os.getenv("BOT_TOKEN")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")

intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

active_client = {}

#Commands

#!los40
@bot.command()
async def los40(ctx):
    text_channel = ctx.channel
    member = ctx.guild.get_member(ctx.author.id)
    if member is None:
        await ctx.send("Error: Could not retrieve member info. Please check bot permissions or enter voice channel if you are not in one already.")
        return

    if member.voice and member.voice.channel:
        channel = member.voice.channel
        if ctx.guild.id in active_client:
            await ctx.send("Already streaming radio!")
            return

        try:
            vc = await channel.connect()
            active_client[ctx.guild.id] = vc
            await ctx.send(f"Joined {channel.name} and started streaming radio!")

            vc._text_channel = text_channel
            #vc.play(discord.FFmpegPCMAudio(config.RADIO_URL, executable=FFMPEG_PATH))
            vc.play(discord.FFmpegPCMAudio(config.RADIO_URL))

        except discord.ClientException:
            await ctx.send("Error: Failed to connect to voice channel")
        except Exception as e:
            await ctx.send(f"Unexpected error! Can't execute this. {e}")
    else:
        await ctx.send("You need to be in voice channel to use command!")

#!leave
@bot.command()
async def leave(ctx):
    if ctx.guild.id in active_client:
        vc = active_client.pop(ctx.guild.id)
        await vc.disconnect()
        await ctx.send("Skibidi out!!!")
    else:
        await ctx.send("Not in channel")

#!commands
@bot.command()
async def commands(ctx):
    help_message = """
    **Available Commands:**

    `!los40` - Starts playing the Los 40 Classic radio stream in the voice channel.
    `!leave` - Makes the bot leave the voice channel.
    `!patch` - Display last three patch notes

    Type `!<command>` to execute any of these commands.
    """

    await ctx.send(help_message)

#!patch
@bot.command()
async def patch(ctx):
    try:
        with open("patch_notes.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
        last_three_commits = lines[-3:] if len(lines) >= 3 else lines

        if not last_three_commits:
            await ctx.send("No patch notes available yet")
            return

        response = "**Last Patches:**\n" + "".join(f"- {line}" for line in last_three_commits)
        await ctx.send(response)

    except FileNotFoundError:
        await ctx.send("Patch notes file not found")


#Event
#Empty channel
@bot.event
async def on_voice_state_update(member, before, after):
    for guild_id, vc in list(active_client.items()):
        if vc.channel and len(vc.channel.members) == 1:
            await vc._text_channel.send("Skibidi out!!!")
            await vc.disconnect()
            active_client.pop(guild_id, None)


#Debug
@bot.event
async def on_ready():
    print(f"{bot.user} is online and listening to all channels!")

@bot.event
async def on_message(message):
    print(f"Received message: '{message.content}' in #{message.channel.name}")

    if message.author == bot.user:
        return  # Ignore its own messages

    await bot.process_commands(message)


bot.run(TOKEN)