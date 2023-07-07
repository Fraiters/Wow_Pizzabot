from keyboards.button import Button


class ClientKb:
    """Класс для управления клавиатурой "клиента" """
    names_buttons = ['/Меню', '/Режим_работы', '/Расположение']
    kb = ...

    def __init__(self):
        self.button = Button()

    def add(self):
        """Добавление кнопок "клиента" """
        self.button.add(names=self.names_buttons)
        self.kb = self.button.kb

    def get_kb(self):
        self.add()
        return self.kb
