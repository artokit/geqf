import asyncio
from settings import dp, bot
from handlers import users, statistics, postback_channel
from handlers.admin import admins_manager, panel, message_editor, sender, keyboard_editor


async def main():
    dp.include_routers(users.router, admins_manager.router, panel.router, statistics.router,
                       postback_channel.router, message_editor.router, keyboard_editor.router)
    sender.set_bot(dp, bot)
    sender.init_handlers()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
 