import discord
from store import message_store

# Update the role id to the you want to use in discord
# Set up a private channel which only includes people with that role
role_id = 928052176578830437

description = '''
React to this message with a 🤖 to be added to the bot discussion channel.  Unreact to be removed.

This way, if you want to chat about the bot, you can do so without disturbing everyone who doesn't.
'''

async def create_message(client: discord.Client, message: discord.Message):

    if message.content.startswith('$bot'):

        # Delete original message
        await message.delete()

        # Create the card with title and description, send the message, add reaction
        embed = discord.Embed(title='Bot Channel', color=discord.Color.dark_blue(), description=description)
        new_message = await message.channel.send(embed=embed)
        await new_message.add_reaction('🤖')

        # Add the new message id to the message store
        message_store.add('bot_message_id', new_message.id)



async def reaction_add(client: discord.Client, payload: discord.RawReactionActionEvent):

    # Do nothing if the message doesn't have the correct the correct messageid
    if message_store.get('bot_message_id') != str(payload.message_id): return

    # Do nothing if the reaction isn't the correct emoji
    if payload.emoji.name != '🤖': return
    
    # Add the role to the user who made the reaction
    guild = await client.fetch_guild(payload.guild_id)
    role = guild.get_role(role_id)
    await payload.member.add_roles(role)



async def reaction_remove(client: discord.Client, payload: discord.RawReactionActionEvent):

    # Do nothing if the message doesn't have the correct messageid
    if message_store.get('bot_message_id') != str(payload.message_id): return

    # Do nothing if the reaction isn't the correct emoji
    if payload.emoji.name != '🤖': return

    # Remove the role from the user who removed the reaction
    guild = await client.fetch_guild(payload.guild_id)
    role = guild.get_role(role_id)
    member = await guild.fetch_member(payload.user_id)
    await member.remove_roles(role)