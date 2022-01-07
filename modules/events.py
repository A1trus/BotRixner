import discord
import json
from store import message_store
from .events_helper import reactions, react_message, error_message, create_description, create_edit_text



async def create_message(client: discord.Client, message: discord.Message):
    
    # Do nothing if the message does not start with $event
    if not message.content.startswith('$event '): return

    # Fail if the message was posted in a DM
    if message.channel.type != discord.ChannelType.text:
        await message.author.send('You can only create events in text channels')
        return

    # Delete original message
    await message.delete()
    
    # Parse body of message as JSON
    try:
        event_params = json.loads(message.content[7:])
    except:
        await message.author.send(error_message)
        return
    
    # Create the card with title and descriptions, send the message, add reactions
    embed = discord.Embed(title=event_params['title'], description=create_description(event_params), color=discord.Color.dark_blue())
    embed.add_field(name='RSVP', value=react_message)
    new_message = await message.channel.send(embed=embed)
    for reaction in reactions:
        await new_message.add_reaction(reaction)

    # Add the messageid to the message_store
    message_store.add('event_' + str(new_message.id), new_message.id)

    # Send confirmation to the creator of the event, including instructions for how to edit or delete the event
    await message.author.send('Event was successfully created. Edit and paste the messages below in the channel to edit or delete the event')
    event_params['event_id'] = str(new_message.id)
    await message.author.send(create_edit_text(event_params))



async def edit_message(client: discord.Client, message: discord.Message):
    
    # Do nothing if the message does not start with $edit event
    if not message.content.startswith('$edit event '): return

    # Fail if the message was posted in a DM
    if message.channel.type != discord.ChannelType.text:
        await message.author.send('You need to run the delete command in the channel in which the event exists')
        return
    
    # Delete original message
    await message.delete()

    # Parse body of message as JSON
    try:
        event_params = json.loads(message.content[12:])
    except:
        await message.author.send(error_message)
        return
    
    # Do nothing if the supplied message_id isn't in the message_store
    message_id = event_params.pop('event_id')
    if not message_store.includes(message_id, 'event_'):
        await message.author.send(f'Event of id {message_id} doesn\'t exist.  cannot edit')
        return

    # Create the card with the newly supplied parameters
    embed = discord.Embed(title=event_params['title'], description=create_description(event_params), color=discord.Color.dark_blue())
    embed.add_field(name='RSVP', value=react_message)

    # Edit the event message
    partial_message = message.channel.get_partial_message(message_id)
    try:
        await partial_message.edit(embed=embed)
    except:
        await message.author.send('There was a problem, the event was not edited.  Did you paste the `$edit event` instruction in the correct channel?')
        return
    await message.author.send('The event was successfully edited')



async def delete_message(client: discord.Client, message: discord.Message):

    # Do nothing if the message does not start with $delete event
    if not message.content.startswith('$delete event '): return

    # Fail if the message was posted in a DM
    if message.channel.type != discord.ChannelType.text:
        await message.author.send('You need to run the delete command in the channel in which the event exists')
        return

    # Extract the message_id
    message_id = message.content[14:]

    # Delete original message
    await message.delete()

    # Do nothing if the supplied message_id isn't in the message_store
    if not message_store.includes(message_id, 'event_'):
        await message.author.send(f'Event of id {message_id} doesn\'t exist.  No need to delete')
        return

    # Delete the message
    partial_message = message.channel.get_partial_message(message_id)
    try:
        await partial_message.delete()
    except:
        await message.author.send('There was a problem, the event was not deleted.  Did you paste the `$delete event` instruction in the correct channel?')
        return

    # Remove from the message_store
    message_store.remove('event_' + message_id)

    # Send confirmation message
    await message.author.send('The event was successfully deleted')
    


async def reaction_add(client: discord.Client, payload: discord.RawReactionActionEvent):
    
    # Do nothing if the message_id id not in the message_store
    if not message_store.includes(str(payload.message_id), 'event_'): return

    # Remove all reactions from the user on the message, except for
    # the one they just added (if it's one of the reactions we're tracking)
    channel = client.get_channel(payload.channel_id)
    partial_message = channel.get_partial_message(payload.message_id)
    if payload.emoji.name in reactions:
        for reaction in reactions:
            if reaction == payload.emoji.name:
                continue
            await partial_message.remove_reaction(reaction, payload.member)
