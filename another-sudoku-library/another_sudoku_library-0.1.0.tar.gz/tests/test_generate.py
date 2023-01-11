from another_sudoku_library.generate import getPuzzle
from another_sudoku_library.utils import fullGen
from another_sudoku_library.solve import checkConsistent


def test_getPuzzle():
    result = getPuzzle()
    assert checkConsistent(result) == True
    for y, x in fullGen():
        assert result[y][x] in range(0, 10)