# Bot Rixner

A Discord bot which uses [discord.py](https://discordpy.readthedocs.io/en/stable/index.html) to implement a few features intended to be used in the CVX @ Rice Discord server

---
## Capabilities

- Manages permissions to the bot discussion channel
- Manages events and RSVPs through reactions
- Polling via reactions

# Documentation: Events
To create an event in a channel, copy, edit, then paste the following message in a text channel:
```
$event {
    "title": "Event Title",
    "description": "This is the description of the event.  This is where you want to place all the long form text",
    "day": "Monday, January 10, 2022",
    "time": "9pm",
    "location": "RMC"
}
```

The bot looks for the text "$event " followed by JSON.  Title is required, but all other parameters are optional and can be removed. 

Once the event is created, the bot will DM the creator with details on how to edit or delete the event card.

The event card will create space for people to RSVP via reactions and ensures that people don't RSVP to more than one option by removing past reactions when they add a new one

# Documentation: Polls

To create a poll, copy, edit, and post the following into a text channel:
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
The bot looks for the text $poll followed by JSON.  The title and the choices are required, but the description is optional

# Development

Required packages are noted in the `requirements.txt` file

For the bot to be able to login there will need to be a `token` environment variable set.  You can read more about the discord API [here](https://discord.com/developers/docs/intro)
