import myarenaapi
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from auth import aut_cgt, auth
from clear_msg import process_msgkey_delete
from config import API_TOKEN, arena_token

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

api_data = myarenaapi.MyApiArena(arena_token)


@dp.message_handler(commands=['s_restart'])
@auth
async def restart_server(message: types.Message):
    await message.delete()
    await process_msgkey_delete(message, "Перезагрузка сервера, ожидайте ответ..", 5)
    status_server = api_data.auth_server_user('restart')
    if status_server:
        status = status_server.get('status', 'Unknown Status')
        response_message = status_server.get('message', 'No Message')
        await process_msgkey_delete(message, f"Server response:\nStatus: {status}\nMessage: {response_message}", 10)
    else:
        await process_msgkey_delete(message, "Не удалось получить ответ от сервера", 10)


@dp.message_handler(commands=['infoserver'])
@aut_cgt()
async def info_server(message: types.Message):
    await message.delete()
    server_info = api_data.get_server_info()
    await process_msgkey_delete(message, f"*{server_info}*", 20, parse_mode='markdown')


@dp.message_handler(commands=['nextmap'])
@aut_cgt()
async def next_map_server(message: types.Message):
    await message.delete()
    maps_text = api_data.get_server_maps()
    maps_list = [map_name.strip() for map_name in maps_text.strip().split("\n")]
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=map_name, callback_data=f'choose_map_{map_name}')
        for map_name in maps_list
    ]
    inline_keyboard.add(*buttons)

    await process_msgkey_delete(message, "Карты на сервере:", 45, inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('choose_map'))
async def process_callback_map(callback_query: types.CallbackQuery):
    user_name = callback_query.from_user.full_name
    await process_msgkey_delete(callback_query.message,
                                f"✅Кнопки работают✅\n\n{user_name} Выбрал карту: {callback_query.data[11:]}", 10)

    status_server = api_data.change_level_server("changelevel", f"{callback_query.data[11:]}")

    if status_server:
        status = status_server.get('status', 'Unknown Status')
        message = status_server.get('message', 'No Message')
        await process_msgkey_delete(callback_query.message, f"Server response:\nStatus: {status}\nMessage: {message}",
                                    10)
    else:
        await process_msgkey_delete(callback_query.message, "Не удалось получить ответ от сервера", 10)
    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
