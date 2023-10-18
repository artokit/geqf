import asyncio
from aiogram import Router, F
from aiogram.types import ContentType, Message
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from db import BotMessage
from handlers.admin.panel import get_admin_panel
from message_db import send_message_db
import keyboards
from states import EditMessage

router = Router()


@router.callback_query(F.data == 'get_all_messages')
async def get_all_messages(call: CallbackQuery):
    await call.message.delete()
    for i in await BotMessage.get_all():
        i = list(i)
        i[2] = keyboards.get_default_edit_message(i[0])

        await send_message_db(tuple(i), call.message)


@router.callback_query(F.data.startswith('check_keyboard'))
async def check_keyboard(call: CallbackQuery):
    message_id = int(call.data.split(':')[-1])
    bot_message = await BotMessage.get(pk=message_id)
    keyboard = keyboards.build_keyboard(eval(bot_message[0][2]))
    await call.message.edit_reply_markup(reply_markup=keyboard)

    await asyncio.sleep(5)
    default_keyboard = keyboards.build_keyboard(keyboards.get_default_edit_message(message_id))
    await call.message.edit_reply_markup(reply_markup=default_keyboard)


@router.callback_query(F.data.startswith('edit_content'))
async def edit_content(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        'Отправьте новый текст, который вы хотели бы видеть',
        reply_markup=keyboards.admin_cancel.as_markup()
    )
    await state.set_data({'message_id': int(call.data.split(':')[-1])})
    await state.set_state(EditMessage.edit_content)


@router.callback_query(F.data.startswith('edit_attachment'))
async def edit_attachment(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_data({'message_id': int(call.data.split(':')[-1])})
    await call.message.answer('Отправьте новую фотографию или видео', reply_markup=keyboards.admin_cancel.as_markup())
    await state.set_state(EditMessage.edit_attachment)


@router.message(EditMessage.edit_content, F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO, ContentType.TEXT]))
async def edit_content(message: Message, state: FSMContext):
    data = await state.get_data()

    try:
        await BotMessage.update_text(data['message_id'], message.html_text)
        await message.answer('Текст успешно изменён')
    except Exception as e:
        print(str(e))
        await message.answer('Что-то пошло не так. Текст не был изменён')

    await state.clear()
    await get_admin_panel(message)


@router.message(EditMessage.edit_attachment, F.content_type.in_([ContentType.PHOTO, ContentType.VIDEO]))
async def get_attachment(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data['message_id']

    if message.video:
        video = message.video.file_id
        await BotMessage.update_video(message_id, video)

    elif message.photo:
        photo = message.photo[-1].file_id
        await BotMessage.update_photo(message_id, photo)

    await message.answer('Данные были успешно изменены')
    await state.clear()
    await get_admin_panel(message)
