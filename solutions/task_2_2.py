from collections.abc import Iterable
from typing import Any


class AnotherRingBuffer:
    """
    Класс реализация циклического буфера FIFO

    Атрибуты
    ----
    _buffer: list
        Список для хранения данных
    _maxsize: int
        Максимальный размер буфера
    _pointer: int
        Указатель на самый старый элемент буфера

    Методы
    ----
    put(self, element: Any)
        Добавить элемент в буфер
    extend(self, iterable: Iterable)
        Добавить последовательность элементов
    pop(self) -> Any
        Получить самый старый элемент (с удалением из буфера)
    get(self) -> Any
        Получить самый старый элемент (без удаления из буфера)
    clear(self)
        Удалить из буфера все элементы
    get_maxsize(self) -> int
        Получить максимальный размер буфера
    set_maxsize(self, size: int)
        Изменить максимальный размер буфера. Если новый размер меньше первоначального - буфер уменьшится с удалением
        самых старых данных
    """

    def __init__(self, size: int, iterable: Iterable[Any] = ()):
        """
        Создать буфер с заданным размером size (обязателен) из последовательности iterable (может отсутствовать)

        :param size: Максимальное количество элементов буфера
        :type size: int
        :param iterable: Последовательность, которую необходимо занести в буфер
        :type iterable: Iterable[Any]
        """
        self._maxsize = size
        self._pointer = 0
        self._buffer = []
        if iterable:
            self.extend(iterable)

    def put(self, element: Any):
        """
        Добавить элемент в буфер

        :param element: Объект, который необходимо добавить в буфер
        :type element: Any

        :return: None
        """
        if self._is_not_full_buffer():
            self._buffer.append(element)
        else:
            self._buffer[self._pointer] = element
            self._increment_pointer()

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
        if self._is_not_empty_buffer():
            element = self._buffer.pop(self._pointer)
            if self._is_outside_pointer():
                self._pointer = 0
            return element
        else:
            return None

    def get(self) -> Any:
        """
        Получить самый старый элемент (без удаления из буфера)

        :rtype: Any
        :return: Самый старый элемент. Если буфер пуст - то None
        """
        if self._is_not_empty_buffer():
            return self._buffer[self._pointer]
        else:
            return None

    def clear(self):
        """
        Удалить из буфера все элементы

        :return: None
        """
        self._buffer.clear()
        self._pointer = 0

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
            self._maxsize = size

    def _cut_buffer(self, size: int):
        """
        Уменьшить размер буфера и удалить лишние элементы

        :param size:
        :type size: int
        :return: None
        """
        while len(self._buffer) > size:
            self.pop()
        self._maxsize = size

    def _increment_pointer(self):
        """
        Циклически сдвинуть указатель вправо

        :return: None
        """
        self._pointer = (self._pointer + 1) % self._maxsize

    def _is_not_empty_buffer(self) -> bool:
        """
        Проверить, что в буфере есть хотя бы один элемент

        :rtype: bool
        :return: True, если в буфере есть данные. Иначе False
        """
        return bool(self._buffer)

    def _is_not_full_buffer(self) -> bool:
        """
        Проверить, что буфер не переполнен

        :rtype: bool
        :return: True, если в буфере осталось неиспользованное место. Иначе False
        """
        return len(self._buffer) < self._maxsize

    def _is_outside_pointer(self) -> bool:
        """
        Проверить, что указатель на элементы превысил количество хранимых элементов

        :rtype: bool
        :return: True, если указатель превысил количество хранимых элементов. Иначе False
        """
        return self._pointer >= len(self._buffer)

    def __str__(self):
        return f'{self._buffer}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self._buffer}, maxsize={self._maxsize})'
