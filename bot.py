import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.client.default import DefaultBotProperties

from backend import *

from tools.content import TOKEN
from tools.user import router as user_router
from tools.admin import router as admin_router

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(admin_router)


@dp.message(CommandStart())
async def start_command(message: Message):
    save_user_to_db(message.from_user.id, message.from_user.username)
    role_id = get_user_role(message.from_user.id)

    if role_id == 1:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="/get_all_users")],
                [KeyboardButton(text="/delete_user <telegram_id>")],
                [KeyboardButton(text="/edit_user <telegram_id> <новое_имя> <возраст> <телефон>")],
                [KeyboardButton(text="/view_user <telegram_id>")]
            ], resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Создать профиль")],
                [KeyboardButton(text="Изменить профиль")],
                [KeyboardButton(text="Удалить профиль")],
                [KeyboardButton(text="Просмотреть профиль")]
            ], resize_keyboard=True
        )

    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=keyboard)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())