from math import floor
from typing import List, Tuple

MatrixType = Tuple[Tuple[int, ...], ...]

MULTIPLICATION: MatrixType = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
)

PERMUTATION: MatrixType = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
)

INVERSE = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)

ARC4_INITIAL_STATE: List[int] = [i for i in range(256)]


def checksum_verhoeff(num: str, digits: int) -> str:
    """
    Calculate the Verhoeff checksum over the provided number, iterating a given number of `times`.
    The checksum is returned as an int. Valid numbers should have a checksum of 0.
    """

    for i in range(digits, 0, -1):  # Repeat validation n times
        check = 0
        length = len(str(num))

        for i in range(length - 1, -1, -1):
            check = MULTIPLICATION[check][
                PERMUTATION[((length - i) % 8)][int(str(num)[i])]
            ]
        num = f"{num}{INVERSE[check]}"

    return num


def arc4_encrypt(data: str, key: str) -> str:
    """Encrypt a piece of data using RC4 (Rivest's Cipher version 4)"""

    state = ARC4_INITIAL_STATE.copy()

    # Sign initial state with the key
    j: int = 0
    for i in range(256):
        j = (j + state[i] + ord(key[i % len(key)])) % 256
        temp = state[i]
        state[i] = state[j]
        state[j] = temp

    x: int = 0
    y: int = 0

    output: str = ""

    for i in range(len(data)):
        x = (x + 1) % 256
        y = (state[x] + y) % 256
        temp = state[x]
        state[x] = state[y]
        state[y] = temp
        output += format(ord(data[i]) ^ state[(state[x] + state[y]) % 256], "02x")

    return output.upper()


def base10to64(number: int) -> str:
    result = ""
    dictionary = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

    while number > 0:
        result = dictionary[int(number % 64)] + result
        number = floor(number // 64)

    return result


def round_half_up(n: float, decimals: int = 0) -> float:
    """Round a float value to half or up."""
    multiplier: int = 10**decimals
    return floor(n * multiplier + 0.5) / multiplier
