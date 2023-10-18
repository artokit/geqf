from aiogram.types import InlineKeyboardButton, KeyboardButtonRequestUser, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup
from fomat_variables import format_text


def build_keyboard(data: list[list[tuple]], **kwargs):
    keyboard = InlineKeyboardBuilder()

    for row in data:
        buttons = []
        for column in row:
            if column[1].startswith('url'):
                buttons.append(
                    InlineKeyboardButton(
                        text=format_text(column[0], user_id=kwargs.get('user_id')),
                        url=format_text(column[1].split(':', maxsplit=1)[1], user_id=kwargs.get('user_id')))
                )
            if column[1].startswith('call'):
                buttons.append(InlineKeyboardButton(text=column[0], callback_data=column[1].split(':', maxsplit=1)[1]))
        keyboard.row(*buttons)

    return keyboard.as_markup()


admin = InlineKeyboardBuilder()
admin.row(InlineKeyboardButton(text='🔽Действия с админитрацией🔽', callback_data='none'))
admin.row(
    InlineKeyboardButton(text='📋Список📋', callback_data='get_admins'),
    InlineKeyboardButton(text='➕Добавить➕', callback_data='add_admin'),
    InlineKeyboardButton(text='❌Удалить❌', callback_data='delete_admin'),
)
admin.row(InlineKeyboardButton(text='🔽Взаимодействие с аудиторией🔽', callback_data='none'))
admin.row(
    InlineKeyboardButton(text='📨Рассылка📨', callback_data='start_send_messages'),
    InlineKeyboardButton(text='📊Узнать статистику📊', callback_data='check_statistics')
)
admin.row(InlineKeyboardButton(text='💬Получить все сообщения💬', callback_data='get_all_messages'))

admin_cancel = InlineKeyboardBuilder()
admin_cancel.add(InlineKeyboardButton(text='Отмена', callback_data='cancel_admin_action'))

request_admin = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(
        text='Отправить пользователя',
        request_user=KeyboardButtonRequestUser(request_id=0)
    )]],
    resize_keyboard=True,
)
admin_choice = InlineKeyboardBuilder()
admin_choice.row(InlineKeyboardButton(text='Сохранить', callback_data='agree'))
admin_choice.row(InlineKeyboardButton(text='Не сохранять', callback_data='disagree'))


def get_default_edit_message(message_id: int):
    return [
        [('🎹Посмотреть клавиатуру🎹', f'call:check_keyboard:{message_id}')],
        [('🎹Изменить клавиатуру🎹', f'call:edit_keyboard:{message_id}')],
        [('💬Изменить текст💬', f'call:edit_content:{message_id}')],
        [('📸Поставить новое изображение или видео📸', f'call:edit_attachment:{message_id}')],
    ]
