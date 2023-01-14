from typing import Generator, Iterable

from reljicd_utils.collections import chunks
from reljicd_utils.logger import get_logger

LOGGER = get_logger(__name__)


def iter_counter(iterable: Iterable,
                 total: int = None,
                 print_step: int = 1000,
                 print_message: str = 'Working on obj') -> Generator:
    total_message = f'/{_formatted(total)}' if total else ''
    if total and print_step > total:
        print_step = total

    for i, iter_chunk in enumerate(chunks(iterable, print_step), 1):
        yield from iter_chunk
        LOGGER.info(f'{print_message}: '
                    f'{_formatted(i * print_step)}' + total_message)


def _formatted(number: int) -> str:
    return format(number, ",").replace(",", " ")
