def ratio(interval: int) -> None:
    if interval == 0:
        return 1
    return 2 ** (interval / 12)


if __name__ == '__main__':
    print(ratio(int(input())))