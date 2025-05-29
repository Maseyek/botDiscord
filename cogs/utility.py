from discord.ext import commands
import config

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # !commands
    @commands.command(name="commands")
    async def command_list(self, ctx):
        help_message = """
        **Available Commands:**

        `!los40` - Starts playing the Los 40 Classic radio stream in the voice channel.
        `!leave` - Makes the bot leave the voice channel.
        `!patch` - Display last three patch notes
        `!github` - Display link to repository

        Type `!<command>` to execute any of these commands.
        """

        await ctx.send(help_message)

    # !patch
    @commands.command()
    async def patch(self, ctx):
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

    @commands.command()
    async def github(self, ctx):
        await ctx.send(f"Source code: {config.GITHUB_URL}")

async def setup(bot):
    await bot.add_cog(Utility(bot))