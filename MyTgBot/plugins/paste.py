import requests
import datetime
import os
from MyTgBot import bot
from pyrogram import filters


async def spacebin(text: str):
    url = "https://spaceb.in/api/v1/documents/"
    response = requests.post(url, data={"content": text, "extension": "txt"})
    id = response.json().get('payload').get('id')
    res = requests.get(f"https://spaceb.in/api/v1/documents/{id}").json()
    created_at = res.get("payload").get("created_at")
    link = f"https://spaceb.in/{id}"
    raw = f"https://spaceb.in/api/v1/documents/{id}/raw"
    string = f"""\u0020
**Here's the link**: **[Paste link]({link})**
**Here's the link**: **[Raw View]({raw})**
"""
    return string

@bot.on_message(filters.command("paste", ["/", "!", ".", "?"]))
async def paste(_, message):
    #share your codes on https://spacebin.in
    if not message.reply_to_message:
          try:
              text = message.text.split(None,1)[1]
          except:
               await message.reply_text("=> Input text to paste else reply.")
               return 

          link = await spacebin(text)
          return await message.reply(link)

    elif bool(message.reply_to_message.text or message.reply_to_message.caption):

           if message.reply_to_message.text:
                 text = message.reply_to_message.text
           elif message.reply_to_message.caption:
                 text = message.reply_to_message.caption
        
           link = await spacebin(text)
           return await message.reply(link)

    elif (message.reply_to_message.document and bool(message.reply_to_message.document.mime_type.startswith("text/"))):
           path = await bot.download_media(message.reply_to_message)
           file = open(path, "r")
           text = file.read()
           file.close()
           os.remove(path)
           link = await spacebin(text)
           return await message.reply(link)
    else:
         return await message.reply_text("=> I am unable to paste this.")
