from django.core.management import BaseCommand
from dotenv import load_dotenv

import os
from aiogram import Bot, Dispatcher, types
from aiogram import executor

load_dotenv(dotenv_path='.env')


def get_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton("Done", callback_data="done"),
                 types.InlineKeyboardButton("Not Done", callback_data="not_done"))
    return keyboard


class Command(BaseCommand):

    def handle(self, *args, **options):
        bot = Bot(os.getenv('TELEGRAM_TOKEN'))
        dp = Dispatcher(bot)

        @dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            """Handle the /start command."""
            user_id = message.from_user.id
            await message.reply(f"Hello! Your Telegram ID is {user_id}.")

        @dp.message_handler(commands=['remind'])
        async def remind(message: types.Message):

            await message.reply("Ваше напоминание установлено. Вы выполнили задание?",
                                reply_markup=get_inline_keyboard())

        @dp.callback_query_handler(lambda c: c.data == 'done')
        async def done(callback_query: types.CallbackQuery):

            pass
        @dp.callback_query_handler(lambda c: c.data == 'no done')
        async def not_done(callback_query: types.CallbackQuery):
            pass

        executor.start_polling(dp, skip_updates=True)

# 2. crons: every minute: run sender and run parser

# 3. sender: db::whereNull(message_id)->where(notification_date,today())->time()

