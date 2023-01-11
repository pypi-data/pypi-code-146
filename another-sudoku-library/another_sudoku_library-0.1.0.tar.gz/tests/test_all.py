from another_sudoku_library import getPuzzle, check, solve

def test_all():

    pz = getPuzzle()
    assert check(pz) == False

    solved = solve(pz)
    assert check(solved) == True