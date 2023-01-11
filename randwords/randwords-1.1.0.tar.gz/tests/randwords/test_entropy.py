import pytest

from randwords.entropy import *

def test_calculate_corpus():
    assert calculate_corpus(100, 5) == math.log2(100) * 5
    assert calculate_corpus(100, 10) == math.log2(100) * 10
    assert calculate_corpus(1_000_000, 10) == math.log2(1_000_000) * 10
    assert calculate_corpus(1, 1) == 0
    assert calculate_corpus(1, 10) == 0

def test_calculate_chars():
    assert calculate_chars('abcd') == math.log2(26) * 4
    assert calculate_chars('ABCD') == math.log2(26) * 4
    assert calculate_chars('1234') == math.log2(10) * 4
    assert calculate_chars('abCD') == math.log2(52) * 4
    assert calculate_chars('Abcd12') == math.log2(62) * 6
    assert calculate_chars('Hello World') == math.log2(53) * 11

    