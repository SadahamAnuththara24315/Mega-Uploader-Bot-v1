from telethon import TelegramClient, events, Button
from mega import Mega
import glob, bitly_api, shutil

def login():
    global m
    mega = Mega()
    m = mega.login(EMAIL.message, PASSWORD.message)
    details = m.get_user()
    space = m.get_storage_space(giga=True)

    global acc_name
    acc_name = details['name']
    acc_email = details['email']
    acc_total_space = "{:.2f}".format(space['total'])
    acc_used_space = "{:.2f}".format(space['used'])
    
    global msg1
    msg1 = f'Successfuly login!\n\nAccount Name - {acc_name}\nEmail - {acc_email}\nSpace :-\n    Total - {acc_total_space}GB\n    Used :- {acc_used_space}GB'

API_ID = 16804073
API_HASH = '2987ccbbc4d989e610675106783c558c'
BOT_TOKEN = '5593479120:AAEgPupFb4QBJiuCYzADD995a8Eejl2AMsU'

client = TelegramClient('user', API_ID, API_HASH).start(bot_token = BOT_TOKEN)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    chat = await event.get_chat()
    await event.reply(f'Hey {chat.first_name} {chat.last_name}\n\nI can upload your files to your Mega account and get public link of that.\nsend /help to know how to use this bot!')

@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.reply('Hey I can upload your files to Mega and get it\'s public link. Before that I want to access to your Mega account. Because I upload files to your own Mega cloud storage.\n\nFirst you want to create a Mega account. If you done it send /upload command.')

@client.on(events.NewMessage(pattern='/upload'))
async def upload(event):
    global EMAIL
    global PASSWORD
    global chat
    chat = await event.get_chat()
    msg = await event.reply(f'Send your Mega account\'s Email:')
    async with client.conversation(chat.id) as conv:
        EMAIL = await conv.get_response(msg.id)
    msg = await event.reply(f'Send your Mega account\'s Password:')
    async with client.conversation(chat.id) as conv:
        PASSWORD = await conv.get_response(msg.id)
    login()
    await event.reply(msg1)

    uploadFile = await event.reply('Send file you want to upload...')
    async with client.conversation(chat.id) as conv:
        file = await conv.get_response(uploadFile.id)
        path = await client.download_media(file.media, "./down/file")
        for file in glob.glob("./down/file.*"):
            upFile = m.upload(file)
            link = m.get_upload_link(upFile)
            
            ACCESS_TOKEN = '69dd6739d96b407b8e78950b192bf09c19cbf202'
            connection = bitly_api.Connection(access_token=ACCESS_TOKEN)
            shortlink = connection.shorten(link).get('url')
            longlink = connection.shorten(link).get('long_url')
        
        shutil.rmtree('./down')

    await event.reply(f'Long url - {longlink}\n\nShort link - {shortlink}')
    
client.start()
client.run_until_disconnected()
