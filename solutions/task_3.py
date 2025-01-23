from collections import deque


def merge_sort(array, low, high):
    if low < high:
        middle = int((low + high) / 2)
        merge_sort(array, low, middle)
        merge_sort(array, middle + 1, high)

        _merge(array, low, middle, high)


def _merge(array, low, middle, high):
    left_array = deque(array[low:middle + 1])
    right_array = deque(array[middle + 1:high + 1])

    i = low

    while left_array and right_array:
        if left_array[0] <= right_array[0]:
            array[i] = left_array.popleft()
            i += 1
        else:
            array[i] = right_array.popleft()
            i += 1

    while left_array:
        array[i] = left_array.popleft()
        i += 1

    while right_array:
        array[i] = right_array.popleft()
        i += 1
