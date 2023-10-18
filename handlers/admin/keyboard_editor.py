from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import keyboards
from .panel import get_admin_panel
from states import EditKeyboardMessage
from db import BotMessage

router = Router()


@router.callback_query(F.data.startswith('edit_keyboard'))
async def edit_keyboard(call: CallbackQuery, state: FSMContext):
    await state.set_data({'message_id': call.data.split(':')[1]})

    await call.message.answer(
        "Отправьте новые кнопки клавиатуры.\n"
        "Пример:\n\n"
        "Название кнопки 1\n"
        "Ссылка или колбэк 1\n"
        "Название кнопки 2\n"
        "Ссылка или колбэк 2\n",
        reply_markup=keyboards.admin_cancel.as_markup()
    )
    await call.message.answer(
        'Доступные колбэки:\n'
        '<b>check_reg</b>',
        parse_mode='html'
    )
    await call.message.answer(
        'Доступные переменные:\n'
        '<b>{user_id}</b>',
        parse_mode='html'
    )
    await state.set_state(EditKeyboardMessage.send_buttons)


@router.message(EditKeyboardMessage.send_buttons)
async def get_buttons_text(message: Message, state: FSMContext):
    if message.text.count('\n') % 2 == 0:
        return await message.answer('Ошибка!\nОтправляйте текст сообщения так же, как это указано в примере')

    buttons = message.text.split('\n')
    buttons = [[buttons[i], buttons[i+1]] for i in range(0, len(buttons), 2)]
    db_buttons = []

    for i in buttons:
        button_text, button_func = i

        if button_func.startswith('https://') or button_func.startswith('http://'):
            button_func = 'url:' + button_func
        else:
            button_func = 'call:' + button_func

        db_buttons.append([(button_text, button_func),])

    await state.update_data({'buttons': db_buttons})

    await message.answer(
        'Ваша клавиатура будет выглядть вот так:',
        reply_markup=keyboards.build_keyboard(db_buttons)
    )

    await state.set_state(EditKeyboardMessage.agree)
    await message.answer('Сохраняем данную клавиатуру в БД?', reply_markup=keyboards.admin_choice.as_markup())


@router.callback_query(F.data == 'agree')
async def agree_choice(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await BotMessage.update_keyboard(data['message_id'], data['buttons'])
    await call.message.answer('Клавиатура была успешно изменена')
    await state.clear()


@router.callback_query(F.data == 'disagree')
async def disagree_choice(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer('Действие отменено')
    await get_admin_panel(call.message)
