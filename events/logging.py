def setup(bot):
    # Debug
    @bot.event
    async def on_ready():
        print(f"{bot.user} is online and listening to all channels!")

    @bot.event
    async def on_message(message):
        print(f"Received message: '{message.content}' in #{message.channel.name}")

        if message.author == bot.user:
            return  # Ignore its own messages

        await bot.process_commands(message)