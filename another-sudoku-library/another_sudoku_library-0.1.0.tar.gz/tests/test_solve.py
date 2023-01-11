import pytest
from another_sudoku_library.solve import _getRowVals, _getColVals, _getSqrVals, solve, check
from . import sample_boards


def test_getRowVals():
    assert _getRowVals(sample_boards.t1, 3, 7, inclusive=False) == [6, 5, 7]


def test_getColVals():
    assert _getColVals(sample_boards.t1, 1, 1, inclusive=False) == [2, 4, 5]


def test_getSqrVals():
    assert _getSqrVals(sample_boards.t1, 4, 4, inclusive=False) == [5, 7]


@pytest.mark.parametrize(
    "pz",
    (
        {"problem": sample_boards.t2_problem, "solution": sample_boards.t2_solution},
        {"problem": sample_boards.t3_problem, "solution": sample_boards.t3_solution},
    ),
)
def test_solve(pz):
    assert solve(pz["problem"]) == pz["solution"]


@pytest.mark.parametrize("solution", (
    sample_boards.t2_solution,
    sample_boards.t3_solution,
)
)
def test_check(solution):
    assert check(solution) == True

    solution[0][0] = (solution[0][0] % 9) + 1   # make a cell incorrect
    assert check(solution) == False

    solution[0][0] = 0                          # make a cell empty
    assert check(solution) == False
