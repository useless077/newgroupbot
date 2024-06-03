import io
import sys
import speedtest
import traceback
from contextlib import redirect_stdout
from subprocess import getoutput as run
from pyrogram import filters
from pyrogram import Client 
from MyTgBot import bot
from datetime import datetime


DEV_USERS = [5696053228, 5015417782, 7019511932, 1666544436, 5965055071, 5690711835, 5597384270, 5102929777]


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def convert(speed):
    return round(int(speed) / 1_000_000, 3)

@bot.on_message(filters.user(DEV_USERS) & filters.command("speedtest", ["/", "!", "?", "."]))
async def speedtest_func(client, message):
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    speedtest_image = speed.results.share()

    result = speed.results.dict()
    msg = f"""
    **Download**: {convert(result['download'])}Mb/s
    **Upload**: {convert(result['upload'])}Mb/s
    **Ping**: {result['ping']}
    """
    await message.reply_photo(speedtest_image, caption=msg)


@bot.on_message(filters.user(DEV_USERS) & filters.command(["run","eval"],["?","!",".","*","/","$"]))
async def eval(client, message):
    if len(message.text.split()) <2:
          return await message.reply_text("`Input Not Found!`")
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(None, 1)[1]
    start = datetime.now()
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    end = datetime.now()
    ping = (end-start).microseconds / 1000
    final_output = "<b>📎 Input</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>📒 Output</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n\n"
    final_output += f"<b>✨ Taken Time</b>: {ping}<b>ms</b>"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await status_message.edit_text(final_output)


@bot.on_message(filters.user(DEV_USERS) & filters.command(["sh","shell"],["?","!",".","*","/","$"]))
async def sh(client, message):
          code = message.text.replace(message.text.split(" ")[0], "")
          await message.reply_text("`No Input Found!`")
          x = run(code)
          string = f"**📎 Input**: `{code}`\n\n**📒 Output **:\n`{x}`"
          try:
             await message.reply_text(string) 
          except Exception as e:
              with io.BytesIO(str.encode(string)) as out_file:
                 out_file.name = "shell.text"
                 await message.reply_document(document=out_file, caption=e)

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)
