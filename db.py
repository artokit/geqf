from typing import Union
import aiosqlite
import asyncio
import keyboards
connect: Union[None | aiosqlite.Connection] = None
cursor: Union[None | aiosqlite.Cursor] = None


class BaseDBObject:
    table_name: str = None

    @classmethod
    async def add(cls, *args):
        q = '?,'*len(args)
        q = q[:-1]
        await cursor.execute(f'INSERT INTO {cls.table_name} VALUES({q})', args)
        await connect.commit()

    @classmethod
    async def get(cls, **kwargs):
        kwargs_string = ' AND '.join([f'{i}={kwargs[i]}' for i in kwargs])
        return await (await cursor.execute(f'SELECT * FROM {cls.table_name} WHERE {kwargs_string}')).fetchall()

    @classmethod
    async def get_all(cls):
        return await (await cursor.execute(f'SELECT * FROM {cls.table_name}')).fetchall()

    @classmethod
    async def delete(cls, **kwargs):
        kwargs_string = ' AND '.join([f'{i}={kwargs[i]}' for i in kwargs])
        await cursor.execute(f'DELETE FROM {cls.table_name} WHERE {kwargs_string}')
        await connect.commit()


class User(BaseDBObject):
    table_name = 'users'


class UserInfo(BaseDBObject):
    table_name = 'users_info'

    @classmethod
    async def add(cls, *args):
        try:
            await cursor.execute('INSERT INTO USERS_INFO VALUES(?, datetime("now", "localtime"), ?)', (args[0], None))
            await connect.commit()
        except aiosqlite.IntegrityError:
            pass

    @classmethod
    async def add_block_user(cls, user_id):
        await cursor.execute(
            'UPDATE USERS_INFO SET BLOCKED_BOT = datetime("now", "localtime") WHERE user_id = ?',
            (user_id,)
        )
        await connect.commit()


class Admin(BaseDBObject):
    table_name = 'admins'

    @classmethod
    async def check_admin(cls, user_id):
        if user_id in [i[0] for i in await cls.get_all()]:
            return True
        return False


class Postback(BaseDBObject):
    table_name = 'postbacks'


class BotMessage(BaseDBObject):
    table_name = 'messages'

    @classmethod
    async def update_text(cls, message_id, text):
        await cursor.execute(f'UPDATE {cls.table_name} SET text = ? where pk = ?', (text, message_id))
        await connect.commit()

    @classmethod
    async def delete_attachments(cls, message_id):
        await cursor.execute(
            f'UPDATE {cls.table_name} SET photo = ?, video = ? where pk = ?',
            (None, None, message_id)
        )
        await connect.commit()

    @classmethod
    async def update_photo(cls, message_id, photo_id):
        await cls.delete_attachments(message_id)
        await cursor.execute(f'UPDATE {cls.table_name} SET PHOTO = ? where pk = ?', (photo_id, message_id))
        await connect.commit()

    @classmethod
    async def update_video(cls, message_id, video_id):
        await cls.delete_attachments(message_id)
        await cursor.execute(f'UPDATE {cls.table_name} SET VIDEO = ? where pk = ?', (video_id, message_id))
        await connect.commit()

    @classmethod
    async def update_keyboard(cls, message_id, keyboard):
        await cursor.execute('UPDATE messages SET buttons = ? where pk = ?', (str(keyboard), message_id))
        await connect.commit()

    @staticmethod
    def get_kwarg_answer(message_args, **kwargs):
        pk, text, buttons, photo, video = message_args
        reply_markup = None

        if buttons:
            if isinstance(buttons, str):
                buttons = eval(buttons)

            reply_markup = keyboards.build_keyboard(buttons, **kwargs)

        if photo:
            return {'caption': text, 'reply_markup': reply_markup, 'photo': photo, 'parse_mode': 'html'}

        if video:
            return {'caption': text, 'reply_markup': reply_markup, 'video': video, 'parse_mode': 'html'}

        return {'text': text, 'reply_markup': reply_markup, 'parse_mode': 'html'}


async def connect_database():
    global connect, cursor
    connect = await aiosqlite.connect('db.sqlite')
    cursor = await connect.cursor()
    await connect.commit()


loop = asyncio.get_event_loop()
tasks = asyncio.wait([loop.create_task(connect_database())])
loop.run_until_complete(tasks)
