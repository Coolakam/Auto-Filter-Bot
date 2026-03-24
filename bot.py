import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logging.getLogger('pyrogram').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

import os
import time
import asyncio

try:
    import uvloop
    uvloop.install()
except ImportError:
    pass

from pyrogram import types, Client, StopPropagation
from pyrogram.handlers import MessageHandler
from typing import Union, Optional, AsyncGenerator

from info import INDEX_CHANNELS, SUPPORT_GROUP, LOG_CHANNEL, API_ID, DATA_DATABASE_URL, API_HASH, BOT_TOKEN, PORT, ADMINS
from utils import temp, get_readable_time, check_premium
from database.users_chats_db import db


class Bot(Client):
    def __init__(self):
        super().__init__(
            name='Auto_Filter_Bot',
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"}
        )
        self.listeners: dict[tuple[int, int], asyncio.Future] = {}
        self.add_handler(MessageHandler(self._listener_handler), group=-1)

    async def _listener_handler(self, client: Client, message: types.Message):
        if not message.chat or not message.from_user:
            return

        listener_id = (message.chat.id, message.from_user.id)

        if listener_id in self.listeners:
            future = self.listeners[listener_id]
            if not future.done():
                future.set_result(message)
            raise StopPropagation

    async def listen(self, chat_id: int, user_id: int, timeout: int = 60) -> Optional[types.Message]:
        future = asyncio.get_running_loop().create_future()
        listener_id = (chat_id, user_id)

        if listener_id in self.listeners:
            old_future = self.listeners[listener_id]
            if not old_future.done():
                old_future.cancel()

        self.listeners[listener_id] = future

        try:
            message = await asyncio.wait_for(future, timeout)
            return message
        except asyncio.TimeoutError:
            return None
        finally:
            self.listeners.pop(listener_id, None)

    async def start(self, **kwargs):
        await super().start()

        temp.START_TIME = time.time()

        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats

        # Restart handling
        if os.path.exists('restart.txt'):
            with open("restart.txt") as file:
                chat_id, msg_id = map(int, file)

            try:
                await self.edit_message_text(
                    chat_id=chat_id,
                    message_id=msg_id,
                    text='Restarted Successfully!'
                )
            except Exception as e:
                logger.error(f"Restart message edit failed: {e}")

            os.remove('restart.txt')

        temp.BOT = self

        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name

        # Background task
        asyncio.create_task(check_premium(self))

        # Log startup
        try:
            await self.send_message(
                chat_id=LOG_CHANNEL,
                text=f"<b>{me.mention} Restarted! 🤖</b>"
            )
        except Exception as e:
            logger.error("Make sure bot is admin in LOG_CHANNEL")
            raise e

        logger.info(f"@{me.username} is started now ✓")

    async def stop(self, **kwargs):
        await super().stop()
        logger.info("Bot Stopped! Bye...")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0
    ) -> Optional[AsyncGenerator[types.Message, None]]:
        async for message in self.get_chat_history(chat_id, limit=limit, offset=offset):
            yield message


app = Bot()
app.run()
