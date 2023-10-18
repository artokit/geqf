import aiosqlite
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from db import User, BotMessage, UserInfo, Postback
from message_db import send_message_db

router = Router()


@router.message(Command('start'))
async def start(message: Message):

    try:
        await User.add(message.chat.id, message.from_user.username)
        await UserInfo.add(message.chat.id)
    except aiosqlite.IntegrityError:
        pass

    messages_db = await BotMessage.get_all()
    await send_message_db(messages_db[0], message, user_id=message.chat.id)


@router.callback_query(F.data == 'check_reg')
async def check_reg(call: CallbackQuery):
    if await Postback.get(user_id=call.message.chat.id):
        bot_message = await BotMessage.get(pk=2)
    else:
        bot_message = await BotMessage.get(pk=1)

    await send_message_db(bot_message[0], call.message, user_id=call.message.chat.id)
