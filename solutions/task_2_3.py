from collections.abc import Iterable
from typing import Any


class YetAnotherRingBuffer:
    """
    Класс реализация циклического буфера FIFO

    Атрибуты
    ----
    _buffer: dict
        Словарь для хранения данных
    _maxsize: int
        Максимальный размер буфера
    _oldest_element: int
        Указатель на ячейку, из которой необходимо достать запись
    _newest_cell: int
        Указатель на ячейку, в которую необходимо произвести запись
    _size: int
        Текущая заполненность буфера

    Методы
    ----
    put(self, element: Any)
        Добавить элемент в буфер
    extend(self, iterable: Iterable[Any])
        Добавить последовательность элементов
    pop(self) -> Any
        Получить самый старый элемент (с удалением из буфера)
    get(self) -> Any
        Получить самый старый элемент (без удаления из буфера)
    clear(self)
        Удалить из буфера все элементы
    get_size(self) -> int
        Получить текущую заполненность буфера
    get_maxsize(self) -> int
        Получить максимальный размер буфера
    set_maxsize(self, size: int)
        Изменить максимальный размер буфера. Если новый размер меньше первоначального - буфер уменьшится с удалением
        самых старых данных
    """

    def __init__(self, size: int, iterable: Iterable[Any] = ()):
        if size <= 0:
            raise ValueError('Size must be greater than zero')
        self._maxsize = size
        self._oldest_cell = 0
        self._newest_cell = 0
        self._size = 0
        self._buffer = self._create_buffer()
        if iterable:
            self.extend(iterable)

    def put(self, element: Any):
        """
        Добавить элемент в буфер

        :param element: Объект, который необходимо добавить в буфер
        :type element: Any

        :return: None
        """
        self._buffer[self._newest_cell] = element
        self._shift_after_put()

    def extend(self, iterable: Iterable[Any]):
        """
        Добавить последовательность элементов

        :param iterable: Добавляемая итерируемая последовательность
        :type iterable: Iterable[Any]

        :return: None
        """
        for element in iterable:
            self.put(element)

    def pop(self) -> Any:
        """
        Получить самый старый элемент (с удалением из буфера)

        :rtype: Any
        :return: Самый старый элемент. Если буфер пуст - то None
        """
        element = self._buffer[self._oldest_cell]
        self._buffer[self._oldest_cell] = None
        self._shift_after_pop()
        return element

    def get(self) -> Any:
        """
        Получить самый старый элемент (без удаления из буфера)

        :rtype: Any
        :return: Самый старый элемент. Если буфер пуст - то None
        """
        return self._buffer[self._oldest_cell]

    def clear(self):
        """
        Удалить из буфера все элементы

        :return: None
        """
        self._buffer = self._create_buffer()
        self._oldest_cell = 0
        self._newest_cell = 0
        self._size = 0

    def get_size(self) -> int:
        """
        Получить текущую заполненность буфера

        :rtype: int
        :return: Текущее количество элементов внутри буфера
        """
        return self._size

    def get_maxsize(self) -> int:
        """
        Получить максимальный размер буфера

        :rtype: int
        :return: Максимальный размер буфера
        """
        return self._maxsize

    def set_maxsize(self, size: int):
        """
        Изменить максимальный размер буфера. Если новый размер меньше первоначального - буфер уменьшится с удалением
        самых старых данных

        :param size: Новый максимальный размер буфера
        :type size: int
        :return: None
        """
        if self._maxsize > size >= 0:
            self._cut_buffer(size)
        elif self._maxsize < size:
            self._extend_buffer(size)

    def _cut_buffer(self, size: int):
        """
        Создать новый буфер меньшего размера с переносом данных

        :param size: Новый максимальный размер буфера
        :type size: int
        :return: None
        """
        old_buffer = []
        while self._size >= size:
            old_buffer.append(self.pop())
        self.__init__(size, old_buffer)

    def _extend_buffer(self, size: int):
        """
        Создать новый буфер большего размера с переносом данных

        :param size: Новый максимальный размер буфера
        :type size: int
        :return: None
        """
        old_buffer = []
        while self._size != 0:
            old_buffer.append(self.pop())
        self.__init__(size, old_buffer)

    def _create_buffer(self):
        """
        Создать пустой буфер

        :rtype: dict
        :return: Словарь с ключами от 0 до maxsize-1 заполненный None
        """
        return {key: None for key in range(self._maxsize)}

    def _increment_size(self):
        """
        Увеличить текущую заполненность буфера на 1

        :return: None
        """
        if self._size < self._maxsize:
            self._size += 1

    def _decrement_size(self):
        """
        Уменьшить текущую заполненность буфера на 1

        :return: None
        """
        if self._size > 0:
            self._size -= 1

    def _increment_oldest(self):
        """
        Циклически сдвинуть указатель на ячейку для удаления вправо

        :return: None
        """
        self._oldest_cell = (self._oldest_cell + 1) % self._maxsize

    def _increment_newest(self):
        """
        Циклически сдвинуть указатель на ячейку для записи вправо

        :return: None
        """
        self._newest_cell = (self._newest_cell + 1) % self._maxsize

    def _shift_after_put(self):
        """
        Сдвиг указателя на ячейку для записи, увеличение показателя размера буфера,
        сдвиг указателя на ячейку для удаления если буфер заполнен

        :return: None
        """
        self._increment_newest()
        if self._size == self._maxsize:
            self._increment_oldest()
        self._increment_size()

    def _shift_after_pop(self):
        """
        Уменьшение показателя размера буфера, сдвиг указателя на ячейку для удаления если буфер не пуст

        :return: None
        """
        if self._size != 0:
            self._increment_oldest()
        self._decrement_size()

    def __str__(self):
        return f'{list(self._buffer.values())}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self._buffer}, maxsize={self._maxsize})'
