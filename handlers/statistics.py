from aiogram import Router, F
from aiogram.types import ChatMemberUpdated, CallbackQuery

import keyboards
from db import UserInfo, Admin
import datetime

router = Router()


@router.my_chat_member()
async def f(member_update: ChatMemberUpdated):
    if member_update.new_chat_member.status == 'kicked':
        await UserInfo.add_block_user(member_update.chat.id)


@router.callback_query(F.data == 'check_statistics')
async def send_statistics(call: CallbackQuery):
    if not await Admin.check_admin(call.message.chat.id):
        return

    s = datetime.datetime.now().strftime('%Y-%m-%d')
    users = await UserInfo.get_all()
    count = 0
    blocked_count = 0

    for user in users:
        if user[1].split()[0] == s:
            count += 1
        if user[2]:
            if user[2].split()[0] == s:
                blocked_count += 1

    await call.message.edit_text(
        f'Общее количество пользователей: {len(users)}\n'
        f'Новых пользователей за сегодня: {count}\n'
        f'Заблочили бота за сегодня: {blocked_count}',
        reply_markup=keyboards.admin.as_markup()
    )
