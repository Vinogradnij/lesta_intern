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
    _pointer: int
        Указатель на самый старый элемент буфера
    _len: int
        Количество хранимых элементов

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
    get_size(self) -> int
        Получить текущее количество элементов внутри буфера
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
        self._pointer = 0
        self._len = 0
        self._buffer = self._create_buffer()
        if iterable:
            self.extend(iterable)

    def put(self, element: Any):
        """
        Добавить элемент в буфер

        Если в буфере есть свободное место - записываем на основе размера, иначе - с помощью указателя на
        старейший элемент

        :param element: Объект, который необходимо добавить в буфер
        :type element: Any

        :return: None
        """
        if self._is_not_full_buffer():
            self._buffer[self._len] = element
            self._increment_len()
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
        element = self._buffer[self._pointer]
        self._buffer[self._pointer] = None
        self._decrement_len()
        return element

    def get(self) -> Any:
        """
        Получить самый старый элемент (без удаления из буфера)

        :rtype: Any
        :return: Самый старый элемент. Если буфер пуст - то None
        """
        return self._buffer[self._pointer]

    def clear(self):
        """
        Удалить из буфера все элементы

        :return: None
        """
        self._buffer = self._create_buffer()
        self._pointer = 0
        self._len = 0

    def get_size(self) -> int:
        """
        Получить текущее количество элементов внутри буфера

        :rtype: int
        :return: Текущее количество элементов внутри буфера
        """
        return self._len

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
            self._expand_buffer(size)

    def _cut_buffer(self, size: int):
        """
        Создать новый буфер меньшего размера с переносом данных

        :param size:
        :type size: int
        :return: None
        """
        old_buffer = []
        while self._len >= size:
            old_buffer.append(self.pop())
        self.__init__(size, old_buffer)

    def _expand_buffer(self, size: int):
        """
        Создать новый буфер большего размера с переносом данных

        :param size:
        :type size: int
        :return: None
        """
        old_buffer = []
        while self._len != 0:
            old_buffer.append(self.pop())
        self.__init__(size, old_buffer)

    def _create_buffer(self):
        """
        Создать пустой буфер

        :rtype: dict
        :return: Словарь с ключами от 0 до maxsize-1 заполненный None
        """
        return {key: None for key in range(self._maxsize)}

    def _increment_len(self):
        """
        Увеличить показатель количества хранимых элементов

        :return: None
        """
        self._len += 1

    def _decrement_len(self):
        """
        Уменьшить показатель количества хранимых элементов, если это возможно. В этом же случае сместить
        указатель на самый старый элемент буфера. Если элементов больше нет - сбросить указатель на самый
        старый элемент буфера

        :return: None
        """
        if self._len > 0:
            self._len -= 1
            self._increment_pointer()
        if self._len == 0:
            self._pointer = 0

    def _increment_pointer(self):
        """
        Циклически сдвинуть указатель вправо

        :return: None
        """
        self._pointer = (self._pointer + 1) % self._maxsize

    def _is_not_full_buffer(self) -> bool:
        """
        Проверить, что буфер не переполнен

        :rtype: bool
        :return: True, если в буфере осталось неиспользованное место. Иначе False
        """
        return self._len < self._maxsize

    def __str__(self):
        return f'{list(self._buffer.values())}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self._buffer}, maxsize={self._maxsize})'
