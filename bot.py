import discord
import os

from events.messages import on_message
from events.reactions import on_raw_reaction_add, on_raw_reaction_remove

class BotClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    
    async def on_message(self, message: discord.Message):
        await on_message(self, message)
    
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await on_raw_reaction_add(self, payload)
    
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await on_raw_reaction_remove(self, payload)
    
client = BotClient()

client.run(os.environ.get('token'))