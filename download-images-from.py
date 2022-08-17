import configparser, json, os
from datetime import datetime
from sqlite3 import OperationalError
from colorama import init as init, Fore; init(autoreset=True)

from telethon import TelegramClient
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

try:
    client = TelegramClient(username, api_id=api_id, api_hash=api_hash)
except OperationalError:
    client = TelegramClient(None, api_id=api_id, api_hash=api_hash)

print(f"TelegramClient(username, api_id={api_id}, api_hash={api_hash})")
async def main():
    # await client.start()
    print(f"{Fore.CYAN}Connection has been initiated")

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
    
    counter = 0
    messages = client.iter_messages(myChannel)
    path = os.path.join(os.getcwd(), channel_title)
    if not os.path.exists(path):
        os.mkdir(path)
    old_l = 0 # Initial length of messages
    async for message in messages:
        # print(message.id, message.text)
        if message.photo:
            msg = f"{Fore.CYAN}>> Message ID {message.id}"
            
            diff = old_l - len(msg)
            if diff < 0:
                old_l = 0
            else:
                old_l = diff
            print(f"{msg}{'':<{old_l}}\r", end="")
            old_l = len(msg)
            await message.download_media(file=path) # 177
            counter += 1
    print(f"{'':<{old_l}}")
    await client.disconnect()
    print(f"{Fore.GREEN}Task has been completed. {counter} Images has been downloaded")

with client:
    client.loop.run_until_complete(main)