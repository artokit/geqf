import aiosqlite
from aiogram import Router, F
from aiogram.types import Message
from message_db import send_message_db
from db import Postback, BotMessage

router = Router()

CHANNEL = -1001887378505


@router.channel_post(F.chat.id == CHANNEL)
async def channel_post_handler(message: Message):
    if message.text.endswith('RU-reg'):
        user_id = int(message.text.split(':')[0])

        try:
            await Postback.add(user_id)
            message_db = await BotMessage.get(pk=6)
            await send_message_db(message_db[0], user_id)
        except aiosqlite.IntegrityError:
            pass
