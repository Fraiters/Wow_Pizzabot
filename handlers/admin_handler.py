from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FsmAdmin(StatesGroup):
    """Класс машины состояний для админа"""
    photo = State()
    name = State()
    description = State()
    price = State()


class AdminHandler:
    """Класс хендлеров для админа"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.fsm_admin = FsmAdmin()

    async def start_load(self, message: Message):
        """Хендлер для команды 'Загрузить' (начало загрузки нового пункта меню)"""
        await self.fsm_admin.photo.set()
        await message.reply('Загрузите фото')

    async def load_photo(self, message: Message, state: FSMContext):
        """Ловится первый ответ и пишется в словарь (загрузка фото)"""
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await self.fsm_admin.next()
        await message.reply('Введите название')

    async def load_name(self, message: Message, state: FSMContext):
        """Ловится второй ответ и пишется в словарь (загрузка названия)"""
        async with state.proxy() as data:
            data['name'] = message.text
        await self.fsm_admin.next()
        await message.reply('Введите описание')

    async def load_description(self, message: Message, state: FSMContext):
        """Ловится третий ответ и пишется в словарь (загрузка описания)"""
        async with state.proxy() as data:
            data['description'] = message.text
        await self.fsm_admin.next()
        await message.reply('Укажите цену')

    async def load_price(self, message: Message, state: FSMContext):
        """Ловится четвертый ответ и пишется в словарь (загрузка цены)"""
        async with state.proxy() as data:
            data['price'] = float(message.text)

        async with state.proxy() as data:
            await message.reply(str(data))

        await state.finish()

    def registration(self, dp: Dispatcher):
        """Регистрация хендлеров для админа"""
        dp.register_message_handler(callback=self.start_load, commands=['Загрузить'],
                                    state=None)
        dp.register_message_handler(callback=self.load_photo, content_types=['photo'],
                                    state=self.fsm_admin.photo)
        dp.register_message_handler(callback=self.load_name, content_types=['name'],
                                    state=self.fsm_admin.name)
        dp.register_message_handler(callback=self.load_description, content_types=['description'],
                                    state=self.fsm_admin.description)
        dp.register_message_handler(callback=self.load_price, content_types=['price'],
                                    state=self.fsm_admin.price)
