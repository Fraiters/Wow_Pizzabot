from aiogram import Bot, Dispatcher
from aiogram.types import Message
from keyboards.client_kb import ClientKb
from aiogram.types import ReplyKeyboardRemove
from db.db import Db


class ClientHandler:
    """Класс хендлеров для клиента"""

    def __init__(self, bot: Bot, db: Db):
        self.bot = bot
        self.client_cb = ClientKb()
        self.db = db

    async def commands_start(self, message: Message):
        """Хендлер для команд 'start', 'help' """
        try:
            await self.bot.send_message(message.from_user.id, 'Приятного аппетита',
                                        reply_markup=self.client_cb.get_kb())
            await message.delete()
        except:
            await message.reply('Общение с ботом через лс, пожалуйста напишите ему: \n @Wow_Pizzabot')

    async def timetable(self, message: Message):
        """Хендлер для команды 'Режим_работы' """
        await self.bot.send_message(message.from_user.id, 'ПН-ПТ - с 10:00 до 22:00, СБ-ВС - с 12:00 до 00:00')

    async def location(self, message: Message):
        """Хендлер для команды 'Расположение' """
        await self.bot.send_message(message.from_user.id,
                                    'г. Москва, ул. Ленина 43')  # , reply_markup=ReplyKeyboardRemove())

    async def menu(self, message: Message):
        """Хендлер для команды 'Меню' """
        menu_elements = await self.db.select_all_menu_record()
        for elem in menu_elements:
            await self.bot.send_photo(message.from_user.id, elem[0],
                                      f'{elem[1]}\nОписание: {elem[2]}\nЦена: {elem[3]} руб.')

    # async def empty(self, message: Message):
    #     await message.answer('Нет такой команды')
    #     await message.delete()

    def registration(self, dp: Dispatcher):
        """Регистрация хендлеров для клиента"""
        dp.register_message_handler(callback=self.commands_start, commands=['start', 'help'])
        dp.register_message_handler(callback=self.timetable, commands=['Режим_работы'])
        dp.register_message_handler(callback=self.location, commands=['Расположение'])
        dp.register_message_handler(callback=self.menu, commands=['Меню'])
