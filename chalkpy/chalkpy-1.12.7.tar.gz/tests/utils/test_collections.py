from chalk.utils.collections import chunks


def test_chunks_size_1():
    seq = range(10)
    i = -1
    for i, chunk in enumerate(chunks(seq, 1)):
        assert list(chunk) == [i]
    assert i == 9


def test_chunks_not_evenly_divisible():
    seq = range(10)
    i = -1
    for i, chunk in enumerate(chunks(seq, 3)):
        if i == 0:
            assert list(chunk) == [0, 1, 2]
        if i == 1:
            assert list(chunk) == [3, 4, 5]
        if i == 2:
            assert list(chunk) == [6, 7, 8]
        if i == 3:
            assert list(chunk) == [9]
    assert i == 3


def test_chunks_evenly_divisible():
    seq = range(10)
    i = -1
    for i, chunk in enumerate(chunks(seq, 5)):
        if i == 0:
            assert list(chunk) == [0, 1, 2, 3, 4]
        if i == 1:
            assert list(chunk) == [5, 6, 7, 8, 9]
    assert i == 1
