from aiogram.filters import Command
from aiogram.types import Message
from db import Admin
import keyboards
from aiogram import Router

router = Router()


@router.message(Command('admin'))
async def get_admin_panel(message: Message):
    if await Admin.check_admin(message.chat.id):
        await message.answer('Админ-панель', reply_markup=keyboards.admin.as_markup())
