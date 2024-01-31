import myarenaapi
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from auth import aut_cgt, auth
from clear_msg import process_msgkey_delete
from config import API_TOKEN, arena_token, arena_token_сss

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

api_data_CS = myarenaapi.MyApiArena(arena_token)
api_data_CSS = myarenaapi.MyApiArena(arena_token_сss)

info_bot = """

bot_add - Добавить бота в команду, где игроков меньше.
bot_add_ct - добавить бота-спецназовца
bot_add_t - Добавить бота-террориста
bot_kick - Кикнуть всех
bot_kill - Убить всех

"""


async def info_server_req(status_server, callback_query):
    if status_server:
        status = status_server.get('status', 'Unknown Status')
        message = status_server.get('message', 'No Message')
        await process_msgkey_delete(callback_query.message, f"Server response:\nStatus: {status}\nMessage: {message}",
                                    10)
    else:
        await process_msgkey_delete(callback_query.message, "Не удалось получить ответ от сервера", 10)
    await callback_query.answer()


@dp.message_handler(commands=['restart_cs', 'restart_css'])
@auth
async def restart_server(message: types.Message):
    status_server = None
    name_server = ''
    command_text = message.get_command()
    if command_text == '/restart_cs':
        name_server = 'Counter-Strike 1.6'
        status_server = api_data_CS.auth_server_user('restart')
    elif command_text == '/restart_css':
        name_server = 'Counter-Strike: Source v34'
        status_server = api_data_CSS.auth_server_user('restart')

    await message.delete()
    await process_msgkey_delete(message, f"Перезагрузка сервера {name_server}\nожидайте ответ..", 10)

    if status_server:
        status = status_server.get('status', 'Unknown Status')
        response_message = status_server.get('message', 'No Message')
        await process_msgkey_delete(message, f"Server response:\nStatus: {status}\nMessage: {response_message}", 10)
    else:
        await process_msgkey_delete(message, "Не удалось получить ответ от сервера", 10)


@dp.message_handler(commands=['infoserver_cs', 'infoserver_css'])
@aut_cgt()
async def info_server(message: types.Message):
    server_info = ''
    command_text = message.get_command()
    if command_text == '/infoserver_cs':
        server_info = api_data_CS.get_server_info()
    elif command_text == '/infoserver_css':
        server_info = api_data_CSS.get_server_info()

        await message.delete()

    await process_msgkey_delete(message, f"*{server_info}*", 20, parse_mode='markdown')


@dp.message_handler(commands=['nextmap_cs', 'nextmap_css'])
@aut_cgt()
async def next_map_server(message: types.Message):
    server = ''
    maps_text = ''
    map_qery = ''
    command_text = message.get_command()
    if command_text == '/nextmap_cs':
        server = 'CS-1.6'
        map_qery = "choose_map_cs"
        maps_text = api_data_CS.get_server_maps()
    elif command_text == '/nextmap_css':
        server = 'CSS-v34'
        map_qery = "map_css"
        maps_text = api_data_CSS.get_server_maps()
    await message.delete()

    maps_list = [map_name.strip() for map_name in maps_text.strip().split("\n")]
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=map_name, callback_data=f'{map_qery}{map_name}')
        for map_name in maps_list
    ]
    inline_keyboard.add(*buttons)

    await process_msgkey_delete(message, f"Карты на сервере {server}:", 45, inline_keyboard)


@dp.callback_query_handler(lambda css: css.data and css.data.startswith('map_css'))
async def process_callback_map_css(callback_query: types.CallbackQuery):
    user_name = callback_query.from_user.full_name
    await process_msgkey_delete(callback_query.message,
                                f"✅Кнопки работают✅\n\n{user_name} Выбрал карту на сервере CSSv34: {callback_query.data[7:]}",
                                10)

    status_server = api_data_CSS.change_level_server("changelevel", f"{callback_query.data[7:]}")

    await info_server_req(status_server, callback_query)


@dp.callback_query_handler(lambda cs: cs.data and cs.data.startswith('choose_map_cs'))
async def process_callback_map_cs(callback_query: types.CallbackQuery):
    user_name = callback_query.from_user.full_name
    await process_msgkey_delete(callback_query.message,
                                f"✅Кнопки работают✅\n\n{user_name} Выбрал карту на сервере CS1.6: {callback_query.data[13:]}",
                                10)

    status_server = api_data_CS.change_level_server("changelevel", f"{callback_query.data[13:]}")

    await info_server_req(status_server, callback_query)


@dp.message_handler(commands=['changebot'])
@aut_cgt()
async def change_bot_server(message: types.Message):
    await message.delete()
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text="bot_add", callback_data=f'change_bot_bot_add'),
        InlineKeyboardButton(text="bot_add_ct", callback_data=f'change_bot_bot_add_ct'),
        InlineKeyboardButton(text="bot_add_t", callback_data=f'change_bot_bot_add_t'),
        InlineKeyboardButton(text="bot_kick", callback_data=f'change_bot_bot_kick'),
        InlineKeyboardButton(text="bot_kill", callback_data=f'change_bot_bot_kill'),
    ]
    inline_keyboard.add(*buttons)
    await process_msgkey_delete(message, f'Управление ботами:\n{info_bot}', 45, inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('change_bot_'))
async def process_callback_bot_cg(callback_query: types.CallbackQuery):
    user_name = callback_query.from_user.full_name
    await process_msgkey_delete(callback_query.message,
                                f"✅Кнопки работают✅\n\n{user_name} Выполнил: {callback_query.data[11:]}", 10)

    status_server = api_data_CSS.change_bot_server("consolecmd", f"{callback_query.data[11:]}")
    await info_server_req(status_server, callback_query)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
