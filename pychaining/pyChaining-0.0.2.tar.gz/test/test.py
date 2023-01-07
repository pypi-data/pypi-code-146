# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 11:08:45 2021

@author: xethhung
"""

# import sys
# # caution: path[0] is reserved for script path (or '' in REPL)
# sys.path.insert(1, '..')

from src.pyChaining import Chains


def test_chain():
    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]).list()
    assert xx == [1, 2, 3, 4, 5, 6, 7]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]).filter(lambda x: x % 2 == 1).list()
    assert xx == [1, 3, 5, 7]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]).filter(lambda x: x % 2 == 1).map(lambda x: x * 2).list()
    assert xx == [2, 6, 10, 14]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]).filter(lambda x: x % 2 == 1).map(lambda x: x * 2) \
        .skip(1).list()
    assert xx == [6, 10, 14]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]).filter(lambda x: x % 2 == 1).map(lambda x: x * 2) \
        .skip(2).list()
    assert xx == [10, 14]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]).filter(lambda x: x % 2 == 1).map(lambda x: x * 2) \
        .first()
    assert xx == 2

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]).filter(lambda x: x % 2 == 1).map(lambda x: x * 2) \
        .last()
    assert xx == 14

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]) \
        .skipUntil(lambda x: x == 2).list()
    assert xx == [2, 3, 4, 5, 6, 7]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]) \
        .stopBefore(lambda x: x == 5).list()
    assert xx == [1, 2, 3, 4]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]) \
        .stopAt(lambda x: x == 5).list()
    assert xx == [1, 2, 3, 4, 5]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]) \
        .stopAfter(lambda x: x == 5, 1).list()
    assert xx == [1, 2, 3, 4, 5, 6]

    xx = Chains.of([1, 2, 3, 4, 5, 6, 7]) \
        .flatMap(lambda x: [x, x]).list()
    assert xx == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]

    xx = Chains.of([[1, 2, 3], [4, 5], [6, 7]]) \
        .flatten().list()
    assert xx == [1, 2, 3, 4, 5, 6, 7]

    # xx = Chains.of([1, 2, 3]) \
    #     .zip([4, 5, 6]).get()
    # assert xx == [[1, 4], [2, 5], [3, 6]]


if __name__ == "__main__":
    test_chain()
