from collections import deque
from collections.abc import Iterable
from typing import Any


class RingBuffer:
    """
    Класс реализация циклического буфера FIFO

    Атрибуты
    ----
    _buffer: deque
        Двусвязный список заданного размера для хранения данных

    Методы
    ----
    put(self, element: Any)
        Добавить элемент в буфер
    pop(self) -> Any
        Получить самый старый элемент (с удалением из буфера)
    extend(self, iterable: Iterable)
        Добавить последовательность элементов
    clear(self)
        Удалить из буфера все элементы
    get_size(self) -> int
        Получить максимальный размер буфера
    """

    def __init__(self, size: int, iterable: Iterable[Any] = ()):
        """
        Создать буфер с заданным размером size (обязателен) из последовательности iterable (может отсутствовать)

        :param size: Максимальное количество элементов буфера
        :type size: int
        :param iterable: Последовательность, которую необходимо занести в буфер
        :type iterable: Iterable[Any]
        """
        self._buffer = deque(iterable=iterable, maxlen=size)

    def put(self, element: Any):
        """
        Добавить элемент в буфер

        :param element: Объект, который необходимо добавить в буфер
        :type element: Any

        :return: None
        """
        self._buffer.append(element)

    def pop(self) -> Any:
        """
        Получить самый старый элемент (с удалением из буфера)

        :rtype: Any
        :return: Самый старый элемент. Если буфер пуст - то None
        """
        return self._buffer.popleft() if self._buffer else None

    def extend(self, iterable: Iterable[Any]):
        """
        Добавить последовательность элементов

        :param iterable: Добавляемая итерируемая последовательность
        :type iterable: Iterable[Any]

        :return: None
        """
        self._buffer.extend(iterable)

    def clear(self):
        """
        Удалить из буфера все элементы

        :return: None
        """
        self._buffer.clear()

    def get_size(self) -> int:
        """
        Получить максимальный размер буфера

        :rtype: int
        :return: Максимальный размер буфера
        """
        return self._buffer.maxlen

    def __str__(self):
        return f'{list(self._buffer)}'

    def __repr__(self):
        return f'{self._buffer}'
