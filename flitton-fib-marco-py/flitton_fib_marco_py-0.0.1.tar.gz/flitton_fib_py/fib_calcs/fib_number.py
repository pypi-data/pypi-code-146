from typing import Optional


def recurring_fibonacci_number(number: int) -> Optional[int]:
    if number < 0:
        return None
    elif number <= 1:
        return number
    else:
        return recurring_fibonacci_number(number - 1) + recurring_fibonacci_number(number - 2)
