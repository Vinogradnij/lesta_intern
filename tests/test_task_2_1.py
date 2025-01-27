import pytest
from solutions.task_2_1 import RingBuffer


def test_initialize_without_iterable():
    buffer = RingBuffer(5)
    assert buffer.get_maxsize() == 5


def test_initialize_with_iterable():
    buffer = RingBuffer(5, [1, 2, 3])
    assert buffer.get_maxsize() == 5
    assert buffer.get_size() == 3
    assert str(buffer) == str([1, 2, 3])


def test_initialize_with_overflow():
    buffer = RingBuffer(3, [1, 2, 3, 4, 5])
    assert buffer.get_maxsize() == 3
    assert buffer.get_size() == 3
    assert str(buffer) == str([3, 4, 5])


def test_initialize_value_error():
    with pytest.raises(ValueError):
        buffer = RingBuffer(-1)

    with pytest.raises(ValueError):
        buffer = RingBuffer(0)

    with pytest.raises(ValueError):
        buffer = RingBuffer(-1, [1, 2, 3])


def test_initialize_type_error():
    with pytest.raises(TypeError):
        buffer = RingBuffer([1, 2, 3], 5)

    with pytest.raises(TypeError):
        buffer = RingBuffer([1, 2, 3])


def test_get_size():
    buffer = RingBuffer(5, [1, 2, 3])
    assert buffer.get_size() == 3


def test_get_maxsize():
    buffer = RingBuffer(5)
    assert buffer.get_maxsize() == 5


def test_clear():
    buffer = RingBuffer(5, [1, 2, 3])
    buffer.clear()
    assert str(buffer) == str([])


def test_put():
    buffer = RingBuffer(5, [1, 2, 3])
    buffer.put(4)
    assert str(buffer) == str([1, 2, 3, 4])

    buffer = RingBuffer(5)
    buffer.put(1)
    assert str(buffer) == str([1])


def test_put_with_overflow():
    buffer = RingBuffer(5, [1, 2, 3, 4, 5])
    buffer.put(6)
    assert str(buffer) == str([2, 3, 4, 5, 6])


def test_pop():
    buffer = RingBuffer(5, [1, 2, 3])
    assert buffer.pop() == 1
    assert str(buffer) == str([2, 3])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 5


def test_pop_after_put():
    buffer = RingBuffer(3, [1, 2])
    buffer.put(3)
    assert buffer.pop() == 1
    assert str(buffer) == str([2, 3])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 3


def test_pop_after_overflow():
    buffer = RingBuffer(3, [1, 2, 3])
    buffer.put(4)
    assert buffer.pop() == 2
    assert str(buffer) == str([3, 4])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 3


def test_pop_with_empty_buffer():
    buffer = RingBuffer(3)
    assert buffer.pop() is None
    assert str(buffer) == str([])
    assert buffer.get_size() == 0
    assert buffer.get_maxsize() == 3


def test_extend():
    buffer = RingBuffer(3, [1, 2])
    buffer.extend([3, 4])
    assert str(buffer) == str([2, 3, 4])
    assert buffer.get_size() == 3
    assert buffer.get_maxsize() == 3


def test_extend_empty_iterable():
    buffer = RingBuffer(3, [1, 2])
    buffer.extend([])
    assert str(buffer) == str([1, 2])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 3
