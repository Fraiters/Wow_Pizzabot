from keyboards.button import Button


class AdminKb:
    """Класс для управления клавиатурой "админа" """
    names_buttons = ['/Загрузить', '/Удалить']
    kb = ...

    def __init__(self):
        self.button = Button()

    def add(self):
        """Добавление кнопок "админа" """
        self.button.add(names=self.names_buttons)
        self.kb = self.button.kb

    def get_kb(self):
        self.add()
        return self.kb
