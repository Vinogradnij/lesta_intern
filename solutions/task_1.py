# Данный пример
def isEven(value):
    return value % 2 == 0


# Моё решение
def my_is_even(value):
    return not (value & 0b1)

