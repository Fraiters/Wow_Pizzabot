from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.db import Db
from keyboards.admin_kb import AdminKb

ID = None


class FsmAdmin(StatesGroup):
    """Класс машины состояний для админа"""
    photo = State()
    name = State()
    description = State()
    price = State()


class AdminHandler:
    """Класс хендлеров для админа"""

    def __init__(self, bot: Bot, db: Db):
        self.bot = bot
        self.db = db
        self.fsm_admin = FsmAdmin()
        self.admin_kb = AdminKb()

    async def make_changes(self, message: Message):
        """Получение ID текущего модератора"""
        global ID
        ID = message.from_user.id
        await self.bot.send_message(chat_id=ID, text='Хозяин, рад вас видеть', reply_markup=self.admin_kb.get_kb())
        await message.delete()

    async def start_load(self, message: Message):
        """Хендлер для команды 'Загрузить' (начало загрузки нового пункта меню)"""
        if message.from_user.id == ID:
            await self.fsm_admin.photo.set()
            await message.reply('Загрузите фото')

    async def cancel(self, message: Message, state: FSMContext):
        """Выход из машины состояний"""
        if message.from_user.id == ID:
            current_state = await state.get_state()
            if current_state is None:
                return
            await state.finish()
            await message.reply('OK')

    async def load_photo(self, message: Message, state: FSMContext):
        """Ловится первый ответ и пишется в словарь (загрузка фото)"""
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id
            await self.fsm_admin.next()
            await message.reply('Введите название')

    async def load_name(self, message: Message, state: FSMContext):
        """Ловится второй ответ и пишется в словарь (загрузка названия)"""
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['name'] = message.text
            await self.fsm_admin.next()
            await message.reply('Введите описание')

    async def load_description(self, message: Message, state: FSMContext):
        """Ловится третий ответ и пишется в словарь (загрузка описания)"""
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['description'] = message.text
            await self.fsm_admin.next()
            await message.reply('Укажите цену')

    async def load_price(self, message: Message, state: FSMContext):
        """Ловится четвертый ответ и пишется в словарь (загрузка цены)"""
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['price'] = float(message.text)

            await self.db.add_menu_record(state=state)
            await state.finish()

    def registration(self, dp: Dispatcher):
        """Регистрация хендлеров для админа"""
        dp.register_message_handler(callback=self.start_load, commands=['Загрузить'],
                                    state=None)
        dp.register_message_handler(callback=self.cancel, commands=['Отмена'],
                                    state='*')
        dp.register_message_handler(self.cancel, Text(equals='Отмена', ignore_case=True),
                                    state='*')
        dp.register_message_handler(callback=self.load_photo, content_types=['photo'],
                                    state=self.fsm_admin.photo)
        dp.register_message_handler(callback=self.load_name,
                                    state=self.fsm_admin.name)
        dp.register_message_handler(callback=self.load_description,
                                    state=self.fsm_admin.description)
        dp.register_message_handler(callback=self.load_price,
                                    state=self.fsm_admin.price)
        dp.register_message_handler(callback=self.make_changes, commands=['moderator'], is_chat_admin=True)
