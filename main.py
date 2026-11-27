from collections.abc import Iterable


def compress_numbers(numbers: Iterable[float]) -> list[float]:
    """Удаляет подряд идущие дубликаты из последовательности чисел.

    Возвращает новый список, исходные данные не изменяются.
    Сложность: O(n) по времени и памяти.

    >>> compress_numbers([1, 1, 2, 2, 3])
    [1, 2, 3]
    >>> compress_numbers([0, 0, 1, 1, 0])
    [0, 1, 0]
    """
    result: list[float] = []
    for number in numbers:
        # Пустой result обрабатывается тем же условием, отдельная ветка не нужна.
        if not result or number != result[-1]:
            result.append(number)
    return result
