from typing import Union
from fomat_variables import format_text
from settings import bot
from aiogram.types import Message
from db import BotMessage


async def send_message_db(data_db: tuple, message: Union[Message | int], **kwargs):
    m = BotMessage.get_kwarg_answer(data_db, **kwargs)

    if isinstance(message, Message):
        user_id = message.chat.id

    else:
        user_id = message

    if m.get('text'):
        m['text'] = format_text(m['text'], user_id=user_id)
    if m.get('caption'):
        m['caption'] = format_text(m['caption'], user_id=user_id)

    if m.get('photo'):
        return await bot.send_photo(user_id, **m)

    if m.get('video'):
        return await bot.send_video(user_id, **m)

    return await bot.send_message(user_id, disable_web_page_preview=True, **m)
