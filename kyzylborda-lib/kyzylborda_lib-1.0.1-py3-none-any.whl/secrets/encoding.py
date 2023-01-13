from __future__ import annotations

# We really really really want to use tokens for filenames, database names, transfer them over the
# wire and serialize and deserialize them in various formats, but, generally speaking, there is no
# guarantee that the token provided by the user satisfies all of these requirements; moreover, it
# might be *deliberate* that various subsystems can be exploited by using unsafe tokens. All in all,
# this means we want to encode arbitrary strings to a very safe format while not sacrificing
# human-readability (or, in a bad case, at least machine readability) to enable easier debugging.
# The implementation used here is loosely based on the idea behind punycode.

# TODO: Would it be reasonable to sanitize language keywords too?


import hashlib
import string
from typing import Optional


__all__ = ("encode_token", "try_decode_token")


SAFE_CHARACTERS = "".join(sorted(string.ascii_lowercase + string.digits))

THRESHOLD = 6  # choosen by fair dice roll

MAX_LENGTH = 48  # 63 for Postgres, 64 for MySQL; this might be unrelated, but gives a good estimate

HASH_LENGTH = 26  # in bytes. Maximize so that the assertion below passes


def encode_number(num: int) -> str:
    s = SAFE_CHARACTERS[num % THRESHOLD]
    num //= THRESHOLD
    base = len(SAFE_CHARACTERS) - THRESHOLD
    while num > 0:
        s += SAFE_CHARACTERS[THRESHOLD + num % base]
        num //= base
    return s


def decode_numbers(s: str) -> list[int]:
    nums = []
    cur_coeff = 0

    for c in s:
        value = SAFE_CHARACTERS.index(c)
        if value < THRESHOLD:
            nums.append(value)
            cur_coeff = THRESHOLD
        else:
            nums[-1] += (value - THRESHOLD) * cur_coeff
            cur_coeff *= len(SAFE_CHARACTERS) - THRESHOLD

    return nums


assert len("long_" + encode_number(2 ** (HASH_LENGTH * 8) - 1)) <= MAX_LENGTH


def encode_token(token: str) -> str:
    # An empty string is "nil", "nil" itself is "nil_nil", and so on
    if token == "":
        safe_token = "nil"
    elif len(token) % 4 == 3 and token == "nil" + "_nil" * (len(token) // 4):
        safe_token = "nil_" + token
    else:
        unsafe_chars = [(i, c) for i, c in enumerate(token) if c not in SAFE_CHARACTERS]
        safe_token = "".join(c for c in token if c in SAFE_CHARACTERS)

        if unsafe_chars:
            original_len = len(safe_token)

            if safe_token == "":
                safe_token = "esc"
            elif safe_token in ("nil", "pad", "long", "esc"):
                # Tokens used elsewhere
                safe_token = "esc_" + safe_token

            safe_token += "_"
            prev_location = -1
            for j, (i, c) in enumerate(unsafe_chars):
                code = ord(c)
                for c in SAFE_CHARACTERS[::-1]:
                    if code > ord(c):
                        code -= 1
                num = code * (original_len + j - prev_location) + (i - prev_location - 1)
                safe_token += encode_number(num)
                prev_location = i
        else:
            # No need to escape anything but "nil", which is already handled, and identifiers
            # starting with digits, for which we add pad_ to the beginning.
            if safe_token[0].isdigit():
                safe_token = "pad_" + safe_token

    if len(safe_token) > MAX_LENGTH:
        hash_ = hashlib.sha512(token.encode()).digest()[:HASH_LENGTH]
        safe_token = "long_" + encode_number(int.from_bytes(hash_, "little"))

    return safe_token


# Makes a good faith attempt at decoding the token, returns None if it the encoding was
# irrecoverable. May crash or hang on invalid input.
def try_decode_token(safe_token: str) -> Optional[str]:
    if len(safe_token) % 4 == 3 and safe_token == "nil" + "_nil" * (len(safe_token) // 4):
        return safe_token[4:]

    if safe_token.startswith("long_"):
        # Hashes are not reversible :(
        return None

    if safe_token.startswith("pad_"):
        return safe_token[4:]

    if "_" not in safe_token:
        return safe_token

    if safe_token.startswith("esc_"):
        safe_token = safe_token[4:]

    parts = safe_token.split("_")
    if len(parts) == 1:
        token, encoded = "", parts[0]
    elif len(parts) == 2:
        token, encoded = parts
    else:
        return None

    prev_location = -1
    for num in decode_numbers(encoded):
        base = len(token) - prev_location
        i = num % base + prev_location + 1
        code = num // base
        for c in SAFE_CHARACTERS:
            if code >= ord(c):
                code += 1
        c = chr(code)
        token = token[:i] + c + token[i:]
        prev_location = i

    return token


for token in ["", "nil", "pad", "long", "esc", "nil!", "pad!", "long!", "esc!", "nil_nil", "The quick brown fox."] + [chr(c) for c in range(256)]:
    assert try_decode_token(encode_token(token)) == token, token
