from aiogram.fsm.state import State, StatesGroup


class AdminListManage(StatesGroup):
    add_admin = State()
    delete_admin = State()


class SenderStates(StatesGroup):
    send_media = State()
    send_caption = State()
    send_urls = State()
    final = State()


class EditMessage(StatesGroup):
    edit_content = State()
    edit_attachment = State()
    edit_keyboard = State()


class EditKeyboardMessage(StatesGroup):
    send_buttons = State()
    agree = State()
