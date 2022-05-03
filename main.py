import configparser, json, os
from getpass import getpass
from datetime import datetime
from textwrap import indent

from colorama import init as colorInit, Fore
colorInit(autoreset=True)

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import PeerChannel
from telethon.tl.functions.channels import GetFullChannelRequest

# Some functions to parse json date

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)

# Reading credentials from config.ini file

config = configparser.ConfigParser()
config.read('config.ini')

api_id = config['Telegram']['api_id']
api_hash = str(config['Telegram']['api_hash'])

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Creating Client Object and connecting using these credentials

client = TelegramClient(username, api_id=api_id, api_hash=api_hash)
async def main(phone):
    await client.start()
    print(f"{Fore.CYAN}Connection has been initiated")

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone=phone, code=input("Enter Verification Code: "))
        except SessionPasswordNeededError:
            await client.sign_in(password=getpass(prompt="Enter (Telegram) Password: "))

    user_input_channel = input("Enter Channel (ID, URL or Name): ")
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel
    
    myChannel = await client.get_input_entity(entity)
    if 'user_id' in myChannel.stringify():
        chn = await client(GetFullUserRequest(myChannel.user_id))
        user_details = chn.user
        channel_title = user_details.first_name + " " + user_details.last_name
    elif 'channel_id' in myChannel.stringify():
        chn = await client(GetFullChannelRequest(myChannel.channel_id))
        channel_title = chn.chats[0].title
    else:
        channel_title = 'Personal (ME)'
        
    # Reading messages from channels

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0

    while True:
        print("""{}Informations
            Channel: {}
            Current Offset ID: {}
            Total Messages: {}
            """.format(Fore.CYAN, channel_title, offset_id, total_messages))
        history = await client(GetHistoryRequest(
            peer=myChannel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages)-1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break   
        try:
            output_file = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                "telegram_{}".format(str(channel_title).lower().replace(' ', '_'))
                )
        except:
            output_file = "telegram_personal_me"
        with open(f'{output_file}.json', 'w') as outfile:
            if input("Sort? [Y/N]: ").lower() == 'y':
                json.dump(all_messages.sort(lambda x:x['id']), outfile, cls=DateTimeEncoder, indent=4)
            else:
                json.dump(all_messages, outfile, cls=DateTimeEncoder, indent=4)
    print(f"{Fore.GREEN}Messages has been retrived and saved in {output_file}.json file successfully")
    
with client:
    client.loop.run_until_complete(main(phone))