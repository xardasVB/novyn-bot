import asyncio
import numpy
import json
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
import os

# Remember to use your own values from my.telegram.org!
api_id = 14662326
api_hash = '36e8b76c2226d987be720fa64c880b6d'
client = TelegramClient('test', api_id, api_hash)

async def main():    
    channel = await client.get_entity('novynyar')

    messages = await client.get_messages(channel, limit=5000)
    lst = [] 
    for m in messages:
        if m.message:
            lst.append(m.message)
    
    print(len(messages))
    print(len(lst))
    
    with open("novynyarDB.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(lst))
        
    #with open("novyny.txt", "w", encoding="utf-8") as f:
        #for m in messages:
        #    if m.message != None:
        #        f.write(m.message)
        #        f.write("\n\n")
        
    with open("novynyarDB.txt", "r", encoding="utf-8") as f:
       messages = json.loads(f.read())
        
    while True:
        id = numpy.random.randint(0, len(messages) - 1)
        print(messages[id])
        sec = input('Show next?.\n')
        os.system('cls')
    

    #message = await client.send_message(
    #    'shadygray',
    #    'This message has **bold**, `code`, __italics__ and '
    #    'a [nice website](https://example.com)!',
    #    link_preview=False)
    #await message.reply('Cool!')
    
with client:
    client.loop.run_until_complete(main())
