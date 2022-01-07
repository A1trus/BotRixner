import discord
import json
from store import message_store



error_message = '''
Unable to parse the message body as JSON.  The message must be in the following format (there can be up to 10 choices):
```
$poll {
    "title": "Sample Poll",
    "description": "This is a sample poll with 10 choices",
    "choices": [
        "Choice one",
        "Choice two",
        "Choice three",
        "Choice four",
        "Choice five",
        "Choice six",
        "Choice seven",
        "Choice eight",
        "Choice nine",
        "Choice ten"
    ]
}
```
Remove the lines you don't need and ensure the last element doesn't have a trailing comma
'''



emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']



def create_description(choices: dict) -> str:
    output = ''
    if 'description' in choices:
        output += choices['description'] + '\n'
    for i, choice in enumerate(choices['choices']):
        output += f'{emojis[i]}: {choice}\n'
    return output



async def create_message(client: discord.Client, message: discord.Message):

    # Do nothing if the message does not start with $poll
    if not message.content.startswith('$poll '): return

    # Fail if the message was posted in a DM
    if message.channel.type != discord.ChannelType.text:
        await message.author.send('You can only create events in text channels')
        return
    
    # Delete the original message
    await message.delete()

    # Parse the body of the message as JSON
    try:
        choices = json.loads(message.content[6:])
    except:
        await message.author.send(error_message)
        return

    # Fail if the number of choices isn't correct
    if not (2 <= len(choices['choices']) <= 10):
        await message.author.send('The number of choices must be between 2 and 10, inclusive')
        return
    
    # Create the card with all the choices, send the message, and add the reactions
    embed = discord.Embed(title=choices['title'], description=create_description(choices), color=discord.Color.purple())
    new_message = await message.channel.send(embed=embed)
    for i in range(len(choices['choices'])):
        await new_message.add_reaction(emojis[i])

    # Add the message_id to the message store
    message_store.add('poll_' + str(new_message.id), new_message.id)

    # Send confirmation to the creator of the poll, including instructions for deleting
    await message.author.send('Poll was successfully created.  Paste the following to delete the poll:')
    await message.author.send(f'```\n$delete poll {new_message.id}\n```')



async def delete_message(client: discord.Client, message: discord.Message):

    # Do nothing if the message does not start with $delete poll
    if not message.content.startswith('$delete poll '): return

    # Extract the message_id
    message_id = message.content[13:]

    # Fail if the message was posted in a DM
    if message.channel.type != discord.ChannelType.text:
        await message.author.send('You need to run the delete command in the channel in which the poll is located')
        return

    # Delete the original message
    await message.delete()

    # Do nothing if the supplied message_id isn't in the message_store
    if not message_store.includes(message_id, 'poll_'):
        await message.author.send(f'Poll with id {message_id} doesn\'t exist.  No need to delete')
        return

    # Delete the poll
    partial_message = message.channel.get_partial_message(message_id)
    try:
        await partial_message.delete()
    except:
        await message.author.send('There was a problem, the poll was not deleted.  Did you paste the `$delete poll` instruction in the correct channel?')
        return
    
    # Remove from the message store
    message_store.remove('poll_' + message_id)

    # Send confirmation message
    await message.author.send('The poll was successfully deleted')



async def reaction_add(client: discord.Client, payload: discord.RawReactionActionEvent):
    
    # Do nothing if the message_id is not in the message_store
    if not message_store.includes(str(payload.message_id), 'poll_'): return

    # Remove all reactions from the user on the message, except for
    # the one they just added (if it's one of the reactions we're tracking)
    channel = client.get_channel(payload.channel_id)
    partial_message = channel.get_partial_message(payload.message_id)
    if payload.emoji.name in emojis:
        for emoji in emojis:
            if emoji == payload.emoji.name:
                continue
            await partial_message.remove_reaction(emoji, payload.member)