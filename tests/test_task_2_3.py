import pytest
from solutions.task_2_3 import YetAnotherRingBuffer as RingBuffer


def test_initialize_without_iterable():
    buffer = RingBuffer(5)
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 0
    assert buffer._size == 0
    expected_dict = {0: None, 1: None, 2: None, 3: None, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'


def test_initialize_with_iterable():
    buffer = RingBuffer(5, [1, 2, 3])
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 3
    assert buffer._size == 3
    expected_dict = {0: 1, 1: 2, 2: 3, 3: None, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'


def test_initialize_with_overflow():
    buffer = RingBuffer(3, [1, 2, 3, 4, 5])
    assert buffer._oldest_cell == 2
    assert buffer._newest_cell == 2
    assert buffer._size == 3
    expected_dict = {0: 4, 1: 5, 2: 3}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=3)'


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

    buffer = RingBuffer(3, [1, 2, 3])
    assert buffer.get_maxsize() == 3


def test_clear():
    buffer = RingBuffer(5, [1, 2, 3])
    buffer.clear()
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 0
    assert buffer._size == 0
    expected_dict = {key: None for key in range(5)}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'


def test_put():
    buffer = RingBuffer(5, [1, 2, 3])
    buffer.put(4)
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 4
    assert buffer._size == 4
    expected_dict = {0: 1, 1: 2, 2: 3, 3: 4, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'

    buffer = RingBuffer(5)
    buffer.put(1)
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 1
    assert buffer._size == 1
    expected_dict = {0: 1, 1: None, 2: None, 3: None, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'


def test_put_with_overflow():
    buffer = RingBuffer(5, [1, 2, 3, 4, 5])
    buffer.put(6)
    assert buffer._oldest_cell == 1
    assert buffer._newest_cell == 1
    assert buffer._size == 5
    expected_dict = {0: 6, 1: 2, 2: 3, 3: 4, 4: 5}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'


def test_put_after_pop():
    buffer = RingBuffer(5, [1, 2, 3])
    buffer.pop()
    buffer.put(4)
    assert buffer._oldest_cell == 1
    assert buffer._newest_cell == 4
    assert buffer._size == 3
    expected_dict = {0: None, 1: 2, 2: 3, 3: 4, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'

    buffer = RingBuffer(5, [1, 2, 3, 4, 5])
    buffer.pop()
    buffer.put(6)
    assert buffer._oldest_cell == 1
    assert buffer._newest_cell == 1
    assert buffer._size == 5
    expected_dict = {0: 6, 1: 2, 2: 3, 3: 4, 4: 5}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'

    buffer = RingBuffer(5, [1, 2, 3, 4, 5])
    buffer.pop()
    buffer.pop()
    buffer.put(6)
    buffer.put(7)
    assert buffer._oldest_cell == 2
    assert buffer._newest_cell == 2
    assert buffer._size == 5
    expected_dict = {0: 6, 1: 7, 2: 3, 3: 4, 4: 5}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'


def test_pop():
    buffer = RingBuffer(5, [1, 2, 3])
    assert buffer.pop() == 1
    assert buffer._oldest_cell == 1
    assert buffer._newest_cell == 3
    assert buffer._size == 2
    expected_dict = {0: None, 1: 2, 2: 3, 3: None, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'

    assert buffer.pop() == 2
    assert buffer._oldest_cell == 2
    assert buffer._newest_cell == 3
    assert buffer._size == 1
    expected_dict = {0: None, 1: None, 2: 3, 3: None, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'


def test_pop_after_put():
    buffer = RingBuffer(3, [1, 2])
    buffer.put(3)
    assert buffer.pop() == 1
    assert buffer._oldest_cell == 1
    assert buffer._newest_cell == 0
    assert buffer._size == 2
    expected_dict = {0: None, 1: 2, 2: 3}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=3)'


def test_pop_after_overflow():
    buffer = RingBuffer(3, [1, 2, 3])
    buffer.put(4)
    assert buffer.pop() == 2
    assert buffer._oldest_cell == 2
    assert buffer._newest_cell == 1
    assert buffer._size == 2
    expected_dict = {0: 4, 1: None, 2: 3}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=3)'


def test_pop_with_empty_buffer():
    buffer = RingBuffer(3)
    assert buffer.pop() is None
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 0
    assert buffer._size == 0
    expected_dict = {0: None, 1: None, 2: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=3)'


def test_extend():
    buffer = RingBuffer(3, [1, 2])
    buffer.extend([3, 4])
    assert buffer._oldest_cell == 1
    assert buffer._newest_cell == 1
    assert buffer._size == 3
    expected_dict = {0: 4, 1: 2, 2: 3}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=3)'


def test_extend_empty_iterable():
    buffer = RingBuffer(3, [1, 2])
    buffer.extend([])
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 2
    assert buffer._size == 2
    expected_dict = {0: 1, 1: 2, 2: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=3)'


def test_get():
    buffer = RingBuffer(3, [1, 2])
    assert buffer.get() == 1
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 2
    assert buffer._size == 2
    expected_dict = {0: 1, 1: 2, 2: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=3)'


def test_set_maxsize():
    buffer = RingBuffer(3, [1, 2])
    buffer.set_maxsize(5)
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 2
    assert buffer._size == 2
    expected_dict = {0: 1, 1: 2, 2: None, 3: None, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'

    buffer = RingBuffer(3, [1, 2, 3])
    buffer.set_maxsize(5)
    assert buffer._oldest_cell == 0
    assert buffer._newest_cell == 3
    assert buffer._size == 3
    expected_dict = {0: 1, 1: 2, 2: 3, 3: None, 4: None}
    assert repr(buffer) == f'{buffer.__class__.__name__}({expected_dict}, maxsize=5)'
