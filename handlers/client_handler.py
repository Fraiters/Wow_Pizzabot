from aiogram import Bot, Dispatcher
from aiogram.types import Message
from keyboards.client_kb import ClientKb
from aiogram.types import ReplyKeyboardRemove


class ClientHandler:
    """Класс хендлеров для клиента"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.kb = ClientKb()

    async def commands_start(self, message: Message):
        """Хендлер для команд 'start', 'help' """
        try:
            await self.bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=self.kb.get_kb())
            await message.delete()
        except:
            await message.reply('Общение с ботом через лс, пожалуйста напишите ему: \n @Wow_Pizzabot')

    async def timetable(self, message: Message):
        """Хендлер для команды 'Режим_работы' """
        await self.bot.send_message(message.from_user.id, 'ПН-ПТ - с 10:00 до 22:00, СБ-ВС - с 12:00 до 00:00')

    async def location(self, message: Message):
        """Хендлер для команды 'Расположение' """
        await self.bot.send_message(message.from_user.id, 'г. Москва, ул. Ленина 43',
                                    reply_markup=ReplyKeyboardRemove())

    def registration(self, dp: Dispatcher):
        """Регистрация хендлеров для клиента"""
        dp.register_message_handler(callback=self.commands_start, commands=['start', 'help'])
        dp.register_message_handler(callback=self.timetable, commands=['Режим_работы'])
        dp.register_message_handler(callback=self.location, commands=['Расположение'])
