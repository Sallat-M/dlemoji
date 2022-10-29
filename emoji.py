import shutil
import os

from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message


API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
Bot_Token = os.environ.get("BOT_TOKEN")
Session = os.environ.get("Session_String")


bot = Client("Emoji", api_id=API_ID, api_hash=API_HASH, bot_token=Bot_Token, session_string=Session)


@bot.on_message(filters.private & filters.incoming & filters.text)
async def main(_, msg: Message):
    All = list(set([i.custom_emoji_id for i in msg.entities if i.type == MessageEntityType.CUSTOM_EMOJI]))
    result = await bot.get_custom_emoji_stickers(All)
    os.mkdir(str(msg.id))
    for n, i in enumerate(result):
        await bot.download_media(i.file_id, file_name=os.path.join(str(msg.id), f"{All[n]}.tgs"))
    shutil.make_archive(str(msg.id), 'zip', str(msg.id))
    await msg.reply_document(f"{msg.id}.zip")
    shutil.rmtree(str(msg.id))
    os.remove(f"{msg.id}.zip")


bot.run()
