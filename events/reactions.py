import discord
from modules import bot_role, events, polls



async def on_raw_reaction_add(client: discord.Client, payload: discord.RawReactionActionEvent):

    # Do nothing if the reaction came from the bot
    if payload.member == client.user: return

    # Functions from the modules that need to be run for this event
    await bot_role.reaction_add(client, payload)
    await events.reaction_add(client, payload)
    await polls.reaction_add(client, payload)



async def on_raw_reaction_remove(client: discord.Client, payload: discord.RawReactionActionEvent):

    # Do nothing if the reaction came from the bot
    if payload.member == client.user: return

    # Functions from the modules that need to be run for this event
    await bot_role.reaction_remove(client, payload)