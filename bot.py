import logging
import logging.config

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

import os 
import sys
from dotenv import load_dotenv

load_dotenv("./dynamic.env", override=True, encoding="utf-8")

from pyrogram import idle
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_inlinedb import Media2, Media3, Media4, Media5
from database.users_chats_db import db
from database.join_reqs import JoinReqs, JoinReqs2
from info import *
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types

from aiohttp import web
from plugins import web_server
from plugins.index import index_files_to_db, incol
PORT = environ.get("PORT", "8080")
name = "main"

async def restart_index(bot):
    progress_document = incol.find_one({"_id": "index_progress"})
    if progress_document:
        last_indexed_file = progress_document.get("last_indexed_file", 0)
        last_msg_id = progress_document.get("last_msg_id")
        chat_id = progress_document.get("chat_id")           
        temp.CURRENT = int(last_indexed_file)
        msg = await bot.send_message(chat_id=int(LOG_CHANNEL), text="Restarting Index...")
        await index_files_to_db(last_msg_id, chat_id, msg, bot)                    


class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()        
        if REQ_CHANNEL == None:
            with open("./dynamic.env", "wt+") as f:
                req = await JoinReqs().get_fsub_chat()
                if req is None:
                    req = False
                else:
                    req = req['chat_id']
                f.write(f"REQ_CHANNEL={req}\n")
            logging.info("Loading REQ_CHANNEL from database...")
            os.execl(sys.executable, sys.executable, "bot.py")
            return
        if REQ_CHANNEL2 == None:
            with open("./dynamic.env", "wt+") as f:
                req = await JoinReqs2().get_fsub_chat()
                if req is None:
                    req = False
                else:
                    req = req['chat_id']
                f.write(f"REQ_CHANNEL2={req}\n")
            logging.info("Loading CHANNEL_REQ from database...")
            os.execl(sys.executable, sys.executable, "bot.py")
            return 
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} 𝖶𝗂𝗍𝗁 𝖥𝗈𝗋 𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆 v{__version__} (Layer {layer}) 𝖲𝗍𝖺𝗋𝗍𝖾𝖽 𝖮𝗇 @{me.username}")
        await self.send_message(chat_id=LOG_CHANNEL, text=f"{me.first_name} 𝖶𝗂𝗍𝗁 𝖥𝗈𝗋 𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆 v{__version__} (Layer {layer}) 𝖲𝗍𝖺𝗋𝗍𝖾𝖽 𝖮𝗇 @{me.username}")
        logging.info(LOG_STR)
       
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()       

        await restart_index(self)
    
    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")
    
    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat sequentially.
        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_messages` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat messages with a
        single call.
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                
            limit (``int``):
                Identifier of the last message to be returned.
                
            offset (``int``, *optional*):
                Identifier of the first message to be returned.
                Defaults to 0.
        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.
        Example:
            .. code-block:: python
                for message in app.iter_messages("pyrogram", 1, 15000):
                    print(message.text)
        """
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1

if name == "main":
    app = Bot()
    app.run()
    
