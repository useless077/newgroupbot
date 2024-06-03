from pyrogram import filters
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from MyTgBot import bot
from telegraph import Telegraph
from telegraph import upload_file

# telegraph page account 
telegraph = Telegraph()
telegraph.create_account(short_name="@CuteSerenaBot")

@bot.on_message(filters.command("txt", ["/", ".", "?", "!"]))
async def txt(_, message):
  try:
    reply = message.reply_to_message

    if not reply or not reply.text:
        return await message.reply("Reply to a text message")

    if len(message.command) < 2:
        return await message.reply("**Usage:**\n /txt [Page name]")

    page_name = message.text.split(None, 1)[1]
    page = telegraph.create_page(
        page_name, html_content=(reply.text.html).replace("\n", "<br>")
    )
    return await message.reply(
        f"**Posted:** {page['url']}",reply_markup=InlineKeyboardMarkup([ 
        [InlineKeyboardButton('View 💫' , url=f"{page['url']}")]
    ]),disable_web_page_preview=True,
    )
  except Exception as e:
       await message.reply_text(f"**ERROR**: {e}")
    
        

@bot.on_message(filters.command(["tm", "tgm"], ["/", ".", "?", "!"]))
def tm(_,message):
  try:
     reply = message.reply_to_message
     if not reply:
          return message.reply_text("Reply to a **Media** to get a permanent telegra.ph link.")
     if reply.text:
          return message.reply_text("Reply to a **Media** to get a permanent telegra.ph link.")
     if reply.media:
        path = reply.download()
        msg = message.reply_text("**downloading...**")
        fk = upload_file(path)
        for x in fk:
           url = "https://telegra.ph" + x
     msg.edit_text("**uploading....**")
     buttons = [[InlineKeyboardButton('View 💫' , url=f"{url}")]] 
     if url.endswith("jpg"):
           message.reply_photo(url,caption=f"{url}",reply_markup=InlineKeyboardMarkup(buttons))
     elif url.endswith("mp4"):
          message.reply_animation(url,caption=f"{url}",reply_markup=InlineKeyboardMarkup(buttons))
     msg.delete()
  except Exception as e:
       msg.edit_text(f"**ERROR**: {e}")
