import aiosqlite
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from db import Admin
import keyboards
import states
from handlers.admin.panel import get_admin_panel

router = Router()


@router.callback_query(F.data == 'add_admin')
async def add_admin(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(states.AdminListManage.add_admin)
    await call.message.answer('Выбрано действие: добавить админа', reply_markup=keyboards.admin_cancel.as_markup())
    await call.message.answer(
        'Отправьте контакт человека, которого хотите поставить на данную должность',
        reply_markup=keyboards.request_admin
    )


@router.message(states.AdminListManage.add_admin, F.user_shared)
async def get_admin_contact(message: Message, state: FSMContext):
    try:
        await Admin.add(message.user_shared.user_id)
        await message.answer('Админ добавлен в базу данных', reply_markup=ReplyKeyboardRemove())
        await state.clear()

    except aiosqlite.IntegrityError:
        return await message.answer('Данный пользователь уже есть в БД', reply_markup=ReplyKeyboardRemove())

    await get_admin_panel(message)


@router.callback_query(F.data == 'cancel_admin_action')
async def cancel_admin_action(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer('Действие отменено!', reply_markup=ReplyKeyboardRemove())
    await get_admin_panel(call.message)


@router.callback_query(F.data == 'get_admins')
async def get_admins(call: CallbackQuery):
    text = 'Вот список id админов: \n'

    for i in await Admin.get_all():
        text += f'{i[0]}\n'

    await call.message.edit_text(text, reply_markup=keyboards.admin.as_markup())


@router.callback_query(F.data == 'delete_admin')
async def delete_admin(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        'Введите айди админа, которого хотите удалить.',
        reply_markup=keyboards.admin_cancel.as_markup()
    )
    await state.set_state(states.AdminListManage.delete_admin)


@router.message(states.AdminListManage.delete_admin)
async def delete_admin(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer(
            '❌Ошибка!❌\n Нужно ввести ID',
            reply_markup=keyboards.admin_cancel.as_markup()
        )

    if not await Admin.check_admin(int(message.text)):
        return await message.answer(
            '❌Ошибка!❌\n Данного пользователя нету в БД',
            reply_markup=keyboards.admin_cancel.as_markup()
        )

    await Admin.delete(user_id=int(message.text))
    await state.clear()
    await message.answer('Админ успешно удалён из БД!')
    await get_admin_panel(message)
