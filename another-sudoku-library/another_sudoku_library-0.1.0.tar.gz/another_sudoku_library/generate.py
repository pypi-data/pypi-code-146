"""Function to generate a new Sudoku puzzle"""

import random
from .utils import fullGen, exclusiveGen, getEmptyBoard, copyBoard
from .solve import _generateCache, _uniqueCheck, checkComplete, checkConsistent, solve


def _picker(board, y, x, cache=None):
    """Returns value for cell on board. First checks for existing value, 
    
    then checks if there's only one possible value, finally chooses randomly
    among valid possibilities.
    """
    if board[y][x] != 0:
        return board[y][x]

    if cache == None:
        cache = _generateCache(board)

    solve = _uniqueCheck(board, y, x, cache=cache)
    if solve != 0:
        return solve

    else:
        options = list(cache[y][x])
        return options[random.randint(0, len(options) - 1)]


def _generate():
    """Randomly generates a completely solved, logically consistent Sudoku board. 
    
    This doesn't work every time, so 'while not done:' loop continues trying until a 
    consistent board is generated.
    """
    done = False
    while not done:
        n = getEmptyBoard()
        for y, x in fullGen():
            n[y][x] = _picker(n, y, x)

            if y > 5:  # heuristic: try to solve once board is mostly full
                n = solve(n, nest=4)
                if checkComplete(n):
                    break

        if checkConsistent(n):
            done = True
    return n


def _removable(board, y, x, nest=4):
    """Tests if board can be solved without given cell. Returns bool. """
    test = copyBoard(board)
    test[y][x] = 0
    test = solve(test, nest=nest)  
    return checkComplete(test) and checkConsistent(test)


def _rm(wb, forbid, ry, rx, nest=4):
    """Checks if cell is removable or not. If yes, removes it from wb. If not, adds 
    
    that cell to the forbid list. Return True if removed, False if not. Nest arg controls
    how hard it tries to solve puzzle without the given cell--higher nest is slower, but
    removes more cells.
    """
    if wb[ry][rx] == 0 or forbid[ry][rx] == 1: # skip
        return 0

    if _removable(wb, ry, rx, nest=nest): 
        wb[ry][rx] = 0
        return True
    else:
        forbid[ry][rx] = 1
        return False


def _carve(board, count=60):
    """Takes a full board, and removes cells so that puzzle is still solveable. 
    
    Removes up to count cells. Note that there is a limit, you typically can't remove
    more than ~60 cells without making puzzle unsolveable. More cells removed = harder
    puzzle.
    """
    wb = copyBoard(board)
    forbid = getEmptyBoard()  # cache cells that are necessary to solve puzzle
    removes = 0
    attempts = 0

    # stage one: try removing random coords
    while removes < count and attempts < 50:
        attempts += 1
        ry = random.randint(0, 8)
        rx = random.randint(0, 8)
        if _rm(wb, forbid, ry, rx): 
            removes += 1

    # stage two: crawl entire board and try remove
    if removes < count:
        for ry, rx in exclusiveGen():
            if _rm(wb, forbid, ry, rx):
                removes += 1
                if removes == count:
                    break

    return wb


def getPuzzle(diff=40):
    """Generates completed puzzle, then carves off cells to create puzzle. 
    
    Diff argumnet is the number of cells to remove. 60 is hard, 25 is easy"""
    return _carve(_generate(), count=diff)
