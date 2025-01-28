import pytest
import random

from solutions.task_3 import merge_sort


def test_positive_sort():
    actual_list = [x for x in range(0, 100)]
    expected_list = [x for x in range(0, 100)]
    random.shuffle(actual_list)
    assert actual_list != expected_list
    merge_sort(actual_list, 0, len(actual_list) - 1)
    assert actual_list == expected_list

    actual_list = [x for x in range(-100, 100)]
    expected_list = [x for x in range(-100, 100)]
    random.shuffle(actual_list)
    assert actual_list != expected_list
    merge_sort(actual_list, 0, len(actual_list) - 1)
    assert actual_list == expected_list
