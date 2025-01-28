import pytest

from solutions.task_1 import my_is_even


def test_my_is_even():
    assert my_is_even(1) == False
    assert my_is_even(2) == True
    assert my_is_even(0) == True
    assert my_is_even(-2) == True
    assert my_is_even(-11) == False