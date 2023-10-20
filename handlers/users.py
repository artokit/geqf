import aiosqlite
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import keyboards
from db import User, BotMessage, UserInfo, Postback
from message_db import send_message_db
import random

router = Router()
users = {

}


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
        bot_message = await BotMessage.get(pk=6)
    else:
        bot_message = await BotMessage.get(pk=4)

    await send_message_db(bot_message[0], call.message, user_id=call.message.chat.id)


@router.callback_query(F.data.startswith('next'))
async def next_message(call: CallbackQuery):
    message_id = call.data.split('-')[-1]
    bot_message = await BotMessage.get(pk=int(message_id))
    await send_message_db(bot_message[0], call.message, user_id=call.message.chat.id)


@router.callback_query(F.data == 'start_demo')
async def start_demo(call: CallbackQuery):
    if call.message.chat.id not in users:
        users[call.message.chat.id] = 0

    if users[call.message.chat.id] > 2:
        return await call.message.answer_photo(
            'AgACAgIAAxkBAAPKZTDoQmPFDcTdZoICG3e6PCsFePcAApfNMRtGD4lJXxZ7Me2E0VIBAAMCAAN5AAMwBA',
            caption='YOU ARE USING DEMO BOT VERSION ⚠️\n'
            'TO START USING PRO MODE CONTACT ADMINISTRATOR 🧑🏽‍💻',
            reply_markup=keyboards.end_demo.as_markup()
        )

    users[call.message.chat.id] += 1

    await call.message.answer_photo(
        'AgACAgIAAxkBAAPJZTDmkSZ1oKi5aCiVUi14XIabkR4AAovNMRtGD4lJdy_abLFSQfQBAAMCAAN5AAMwBA',
        caption='ACCESS: DEMO MODE ✈️\n\n'
        f'✅ BET {random.randint(100, 300)}₹, coeff {random.randint(120, 300)/100}',
        reply_markup=keyboards.demo.as_markup()
    )
