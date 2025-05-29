import discord
from discord.ext import commands
import config
import os

active_client = {}

class Radio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ffmpeg_path = os.getenv("FFMPEG_PATH")

    # !los40
    @commands.command()
    async def los40(self, ctx):
        text_channel = ctx.channel
        member = ctx.guild.get_member(ctx.author.id)
        if member is None:
            await ctx.send(
                "Error: Could not retrieve member info. Please check bot permissions or enter voice channel if you are not in one already.")
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
                # vc.play(discord.FFmpegPCMAudio(config.RADIO_URL, executable=FFMPEG_PATH))
                vc.play(discord.FFmpegPCMAudio(config.RADIO_URL, before_options='-reconnect 1 -reconnect_streamed 1 '
                                                                                '-reconnect_delay_max 5',
                                               options='-vn'))

            except discord.ClientException:
                await ctx.send("Error: Failed to connect to voice channel")
            except Exception as e:
                await ctx.send(f"Unexpected error! Can't execute this. {e}")
        else:
            await ctx.send("You need to be in voice channel to use command!")

    # !leave
    @commands.command()
    async def leave(self, ctx):
        if ctx.guild.id in active_client:
            vc = active_client.pop(ctx.guild.id)
            await vc.disconnect()
            await ctx.send("Skibidi out!!!")
        else:
            await ctx.send("Not in channel")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        for guild_id, vc in list(active_client.items()):
            if vc.channel and len(vc.channel.members) == 1:
                await vc._text_channel.send("Skibidi out!!!")
                await vc.disconnect()
                active_client.pop(guild_id, None)


async def setup(bot):
    await bot.add_cog(Radio(bot))