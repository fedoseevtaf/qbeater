from typing import Iterable

from fcalc import ratio


def octa(frequency: float | int) -> Iterable:
    for interval in range(9, -1, -1):
        yield frequency / ratio(interval)
    for interval in range(1, 3):
        yield frequency * ratio(interval)


def octc(frequency: float | int) -> Iterable:
    for interval in range(13):
        yield frequency * ratio(interval)


if __name__ == '__main__':
    notes = 0, 2, 4, 5, 7, 9, 11
    for i, freq in enumerate(octa(float(input()))):
        if i in notes:
            print(f'>>> {freq:.2f}')
        else:
            print(f'>   {freq:.2f}')
