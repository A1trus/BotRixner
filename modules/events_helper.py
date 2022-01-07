import json



reactions = ['✅', '❌', '❔']



reaction_descriptions = ['I plan to attend', 'I do not plan to attend', 'I don\'t know']



react_message = ''
for reaction, description in zip(reactions, reaction_descriptions):
    react_message += f'{reaction}: {description}\n'



error_message = '''
The JSON you supplied was unable to be parsed.  The message must be in the following format:
```
$event {
    "title": "Event Title",
    "description": "This is the description of the event.  This is where you want to place all the long form text",
    "day": "Monday, January 10, 2022",
    "time": "9pm",
    "location": "RMC"
}
```
'''



def create_description(event_params: dict) -> str:
    params = ['day', 'time', 'location', 'description']
    output = ''
    for param in params:
        if param not in event_params: continue
        output += f'**{param.upper()}**: {event_params[param]}\n'
    return output



def create_edit_text(event_params: dict) -> str:
    return f'''
To edit the event:
```
$edit event {json.dumps(event_params, indent=4)}
```
To delete the event:
```
$delete event {event_params['event_id']}
```
'''