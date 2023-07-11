import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from handlers.admin_handler import AdminHandler
from handlers.client_handler import ClientHandler
from handlers.other_handler import OtherHandler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db.db import Db


class TelegramBot:
    """Класс для запуска телеграм бота"""
    bot = Bot(token=os.getenv('TOKEN'))
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)
    db = Db()

    async def on_startup(self, _):
        print('Бот вышел в онлайн')
        self.db.create_table_menu()

    def run(self):
        admin_handler = AdminHandler(bot=self.bot, db=self.db)
        client_handler = ClientHandler(bot=self.bot, db=self.db)
        other_handler = OtherHandler()

        admin_handler.registration(dp=self.dp)
        client_handler.registration(dp=self.dp)
        other_handler.registration(dp=self.dp)

        executor.start_polling(dispatcher=self.dp, skip_updates=True, on_startup=self.on_startup)


if __name__ == '__main__':
    telegram_bot = TelegramBot()
    telegram_bot.run()
