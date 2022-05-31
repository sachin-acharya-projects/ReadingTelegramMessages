# Reading Telegram Messages
This simple program reads Messages from telegram using Telegram API and Telethon Python Package (It cannot read personal messages, yet!)
_____________________________________________________
### Configurations
````ini
[Telegram]
    # Structure for config.ini file
    # quote, "" can be ommited
    # Get API FROM
    # https://my.telegram.org/apps
    api_id = YOUR_API_ID_FROM_TELEGRAM
    api_hash = YOUR_API_HASH_FROM_TELEGRAM

    phone = YOUR_TELEGRAM_PHONE_NUMBER_WITH_COUNTRY_CODE(+91 XXX XXXXXXX)
    username = YOUR_TELEGRAM_USERNAME

    channels = CHANNEL_ID_OR_URL_FROM_TELEGRAM_TO_READ_MESSAGE_SEPARATED_WITH_SPACES (https://t.me/channelid, channelid)
````
[Get API here](https://my.telegram.org/apps)  
[Reference](https://betterprogramming.pub/how-to-get-data-from-telegram-82af55268a4b)
