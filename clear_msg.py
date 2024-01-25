import asyncio
from aiogram import Bot, types

from config import API_TOKEN

bot = Bot(token=API_TOKEN)


async def msg_del_time(message: types.Message, delay: int):
    try:
        await asyncio.sleep(delay)
        await message.delete()
    except:
        print("Сообщение уже было удалено!")


async def process_msgkey_delete(message, text, delay, keyboard=None, parse_mode=None):
    reply_msg = await message.answer(text, reply_markup=keyboard, parse_mode=parse_mode)
    if reply_msg is not None:
        _ = asyncio.create_task(msg_del_time(reply_msg, delay))
