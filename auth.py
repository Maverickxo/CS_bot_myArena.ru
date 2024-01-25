from aiogram import types
from config import all_admin_ids, work_chat


def aut_cgt(chat_ids=work_chat):
    def decorator(func):
        async def wrapper(message: types.Message):
            if message.chat.id not in chat_ids:
                # Если сообщение не из нужных чатов, ничего не делаем
                return
            return await func(message)

        return wrapper

    return decorator


def auth(func):
    async def wrapper(message):
        if message['from']['id'] not in all_admin_ids:
            return await message.reply("Доступ запрещен, только для админов ", reply=False)
        return await func(message)

    return wrapper
