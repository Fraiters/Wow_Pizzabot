import sqlite3
from sqlite3 import Cursor
from sqlite3 import Connection
from aiogram.dispatcher import FSMContext


class Db:
    """Класс работы с БД"""

    def __init__(self):
        self.connection = sqlite3.connect('wow_pizza.db')  # type: Connection
        self.cursor = self.connection.cursor()  # type: Cursor
        if self.connection:
            print("База данных подключена")

    def create_table_menu(self):
        """Создание таблицы меню в БД"""
        command = 'CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)'
        self.connection.execute(command)
        self.connection.commit()

    async def add_menu_record(self, state: FSMContext):
        """Добавление записи в меню"""
        async with state.proxy() as data:
            command = 'INSERT INTO menu VALUES (?, ?, ?, ?)'
            self.cursor.execute(command, tuple(data.values()))
            self.connection.commit()

    async def select_all_menu_record(self):
        """Выбор всех позиций в меню"""
        command = 'SELECT * FROM menu'
        table_elements = self.cursor.execute(command).fetchall()
        return table_elements
