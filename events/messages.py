import discord
from modules import bot_role, events, polls



async def on_message(client: discord.Client, message: discord.Message):
    
    # Do nothing if the message was written by the bot
    if message.author == client.user: return

    # Functions from the modules that need to be run for this event
    await bot_role.create_message(client, message)
    await events.create_message(client, message)
    await events.edit_message(client, message)
    await events.delete_message(client, message)
    await polls.create_message(client, message)
    await polls.delete_message(client, message)
        