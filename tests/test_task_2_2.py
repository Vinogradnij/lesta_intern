import pytest
from solutions.task_2_2 import AnotherRingBuffer as RingBuffer


def test_initialize_without_iterable():
    buffer = RingBuffer(5)
    assert buffer.get_maxsize() == 5
    assert buffer._pointer == 0


def test_initialize_with_iterable():
    buffer = RingBuffer(5, [1, 2, 3])
    assert buffer.get_maxsize() == 5
    assert buffer.get_size() == 3
    assert buffer._pointer == 0
    assert str(buffer) == str([1, 2, 3])


def test_initialize_with_overflow():
    buffer = RingBuffer(3, [1, 2, 3, 4, 5])
    assert buffer.get_maxsize() == 3
    assert buffer.get_size() == 3
    assert buffer._pointer == 2
    assert str(buffer) == str([4, 5, 3])


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
    assert buffer._pointer == 0
    assert str(buffer) == str([])


def test_put():
    buffer = RingBuffer(5, [1, 2, 3])
    buffer.put(4)
    assert buffer._pointer == 0
    assert str(buffer) == str([1, 2, 3, 4])

    buffer = RingBuffer(5)
    buffer.put(1)
    assert buffer._pointer == 0
    assert str(buffer) == str([1])


def test_put_with_overflow():
    buffer = RingBuffer(5, [1, 2, 3, 4, 5])
    buffer.put(6)
    assert buffer._pointer == 1
    assert str(buffer) == str([6, 2, 3, 4, 5])


def test_put_after_pop():
    buffer = RingBuffer(5, [1, 2, 3])
    buffer.pop()
    buffer.put(4)
    assert buffer._pointer == 0
    assert str(buffer) == str([2, 3, 4])

    buffer = RingBuffer(5, [1, 2, 3, 4, 5])
    buffer.pop()
    buffer.put(6)
    assert buffer._pointer == 0
    assert str(buffer) == str([2, 3, 4, 5, 6])

    buffer = RingBuffer(5, [1, 2, 3, 4, 5])
    buffer.put(6)
    buffer.put(7)
    buffer.pop()
    buffer.pop()
    buffer.put(8)
    assert buffer._pointer == 2
    assert str(buffer) == str([6, 7, 5, 8])


def test_pop():
    buffer = RingBuffer(5, [1, 2, 3])
    assert buffer.pop() == 1
    assert buffer._pointer == 0
    assert str(buffer) == str([2, 3])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 5


def test_pop_after_put():
    buffer = RingBuffer(3, [1, 2])
    buffer.put(3)
    assert buffer.pop() == 1
    assert buffer._pointer == 0
    assert str(buffer) == str([2, 3])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 3

    buffer = RingBuffer(5, [1, 2, 3, 4, 5])
    buffer.extend([6, 7, 8, 9])
    assert buffer.pop() == 5
    assert buffer._pointer == 0
    assert str(buffer) == str([6, 7, 8, 9])
    assert buffer.get_size() == 4
    assert buffer.get_maxsize() == 5

def test_pop_after_overflow():
    buffer = RingBuffer(3, [1, 2, 3])
    buffer.put(4)
    assert buffer.pop() == 2
    assert buffer._pointer == 1
    assert str(buffer) == str([4, 3])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 3


def test_pop_with_empty_buffer():
    buffer = RingBuffer(3)
    assert buffer.pop() is None
    assert buffer._pointer == 0
    assert str(buffer) == str([])
    assert buffer.get_size() == 0
    assert buffer.get_maxsize() == 3


def test_extend():
    buffer = RingBuffer(3, [1, 2])
    buffer.extend([3, 4])
    assert buffer._pointer == 1
    assert str(buffer) == str([4, 2, 3])
    assert buffer.get_size() == 3
    assert buffer.get_maxsize() == 3


def test_extend_empty_iterable():
    buffer = RingBuffer(3, [1, 2])
    buffer.extend([])
    assert buffer._pointer == 0
    assert str(buffer) == str([1, 2])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 3


def test_get():
    buffer = RingBuffer(3, [1, 2])
    assert buffer.get() == 1
    assert buffer._pointer == 0
    assert str(buffer) == str([1, 2])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 3


def test_set_maxsize():
    buffer = RingBuffer(3, [1, 2])
    buffer.set_maxsize(5)
    assert buffer._pointer == 0
    assert str(buffer) == str([1, 2])
    assert buffer.get_size() == 2
    assert buffer.get_maxsize() == 5
