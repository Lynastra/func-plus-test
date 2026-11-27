import math

import pytest

from main import compress_numbers


# 1. Примеры из задания
@pytest.mark.parametrize(
    "data, expected",
    [
        ([1, 1, 2, 2, 3], [1, 2, 3]),
        ([0, 0, 1, 1, 0], [0, 1, 0]),
    ],
    ids=["example_1", "example_2"],
)
def test_examples_from_task(data, expected):
    assert compress_numbers(data) == expected


# 2. Граничные размеры входа
@pytest.mark.parametrize(
    "data, expected",
    [
        ([], []),
        ([5], [5]),
        ([7, 7], [7]),
        ([7, 8], [7, 8]),
    ],
    ids=["empty", "single", "two_equal", "two_different"],
)
def test_boundary_sizes(data, expected):
    assert compress_numbers(data) == expected


# 3. Расположение серий дубликатов
@pytest.mark.parametrize(
    "data, expected",
    [
        ([1, 2, 3, 4], [1, 2, 3, 4]),                   # дубликатов нет
        ([9, 9, 9, 9], [9]),                            # все одинаковые
        ([1, 1, 2, 3], [1, 2, 3]),                      # серия в начале
        ([1, 2, 3, 3], [1, 2, 3]),                      # серия в конце
        ([1, 2, 2, 2, 3], [1, 2, 3]),                   # серия в середине
        ([1, 1, 2, 2, 2, 3, 3, 1, 1], [1, 2, 3, 1]),    # несколько серий разной длины
        ([0, 0, 0], [0]),                               # нули
    ],
    ids=["no_dups", "all_same", "run_at_start", "run_at_end",
         "run_in_middle", "many_runs", "zeros"],
)
def test_run_positions(data, expected):
    assert compress_numbers(data) == expected


# 4. Неподряд идущие повторы удалять нельзя
@pytest.mark.parametrize(
    "data",
    [
        [1, 2, 1, 2, 1, 2],
        [1, 2, 1],
        [0, 1, 0, 1, 0],
    ],
    ids=["alternating", "palindrome_like", "binary_alternating"],
)
def test_non_adjacent_duplicates_are_kept(data):
    assert compress_numbers(data) == data


# 5. Разные виды чисел
@pytest.mark.parametrize(
    "data, expected",
    [
        ([-1, -1, 0, 0, -1], [-1, 0, -1]),
        ([1.1, 1.1, 2.2, 2.2], [1.1, 2.2]),
        ([10**30, 10**30, 10**30 + 1], [10**30, 10**30 + 1]),
        ([math.inf, math.inf, -math.inf], [math.inf, -math.inf]),
    ],
    ids=["negative", "float", "big_int", "infinity"],
)
def test_number_kinds(data, expected):
    assert compress_numbers(data) == expected


def test_int_and_float_equal_values_are_duplicates():
    # В Python 1 == 1.0, поэтому это дубликаты. Фиксируем поведение явно.
    assert compress_numbers([1, 1.0, 2]) == [1, 2]


def test_nan_is_never_equal_to_itself():
    # NaN != NaN по стандарту IEEE 754, поэтому подряд идущие NaN не схлопываются.
    # Тест документирует это поведение, чтобы оно не было неожиданностью.
    result = compress_numbers([math.nan, math.nan])
    assert len(result) == 2
    assert all(math.isnan(x) for x in result)


# 6. Контракт функции: не мутирует вход, возвращает новый список
def test_input_is_not_mutated():
    data = [1, 1, 2, 2, 3]
    snapshot = list(data)
    compress_numbers(data)
    assert data == snapshot


def test_returns_new_list_object():
    data = [1, 2, 3]
    result = compress_numbers(data)
    assert result == data
    assert result is not data


def test_accepts_any_iterable():
    assert compress_numbers((1, 1, 2)) == [1, 2]
    assert compress_numbers(x for x in [3, 3, 4]) == [3, 4]


# 7. Большой вход: линейная сложность, нет квадратичной деградации
def test_large_input_all_same():
    assert compress_numbers([42] * 1_000_000) == [42]


def test_large_input_no_duplicates():
    data = list(range(1_000_000))
    assert compress_numbers(data) == data
