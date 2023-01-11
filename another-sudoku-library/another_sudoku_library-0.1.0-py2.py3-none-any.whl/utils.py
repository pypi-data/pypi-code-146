"""Utilities for accessing and manipulating sudoku boards """

import random


def getEmptyBoard():
    """Returns empty board, a 9x9 2D list structure. Empty cells are represented as zeros."""
    out = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return out


def printBoard(board, hidezeros=True):
    """Pretty print a board to console"""
    for y, x in fullGen():
        # print every number
        if board[y][x] == 0 and hidezeros:
            print(" ", end=" ")
        else:
            print(board[y][x], end=" ")

        # formatting & separators
        if x == 8:
            print()
            if y == 2 or y == 5:
                print("----------------------")

        if x == 2 or x == 5:
            print("| ", end="")


def copyBoard(board):
    """Deep copy--creates and returns copy as an entirely new board structure."""
    copy = getEmptyBoard()
    for y, x in fullGen():
        copy[y][x] = board[y][x]
    return copy


def getBitmap(board):
    """Returns board with 1 for all provided cells, 0 for undecided cells.

    This is useful for implementing a UI, for instance to separately style provided cells,
    or to prevent user from changing provided cells.
    """
    out = getEmptyBoard()
    for y, x in fullGen():
        if board[y][x] != 0:
            out[y][x] = 1
    return out


def getOrigPermutation(board, bitmap):
    """Returns original problem board based on bitmap"""
    out = getEmptyBoard()
    for y, x in fullGen():
        out[y][x] = board[y][x] * bitmap[y][x]
    return out


def rotateNormal(board):
    """Rotates board so heaviest side is on bottom. Goal is consistency--identical puzzles should end up
    the same, regardless of initial orientation (identical meaning *normal* versions of the puzzle are identical).

    I want to take a given puzzle and rotate it, so that different permutations always end up in the same
    orientation. I cannot use the values of the cells, because these will also be normalized. So, I have to
    consider only the *locations* of filled vs unfilled cells--we're essentially figuring out which side
    is the heaviest.

    If I only counted all the values on a given side (eg the top is every cell in first three rows), sides
    would frequently have the same weight. So, we scale each row (and each square) slightly differently.
    The scaling should be the same between different sides, so the same side gets the same weighted score
    regardless of whether it's currently on top, left, bottom or right. But specific *cells* within that side
    are weighted differently, to try to give differentiation.

    We still have problem of a completely symmetrical puzzle being non-rotateable. But giving these funky
    weights decreases the chance of that (hopefully)

    """
    a, b, c, d = 0, 0, 0, 0  # these hold sum of weights for each side

    t1 = sum(1.114 for y, x in rowGen(0, 4) if board[y][x] != 0)
    t2 = sum(1.326 for y, x in rowGen(1, 4) if board[y][x] != 0)
    t3 = sum(1.453 for y, x in rowGen(2, 4) if board[y][x] != 0)
    t4 = sum(1.242 for y, x in sqrGen(0, 0) if board[y][x] != 0)
    t5 = sum(1.141 for y, x in sqrGen(0, 3) if board[y][x] != 0)
    t6 = sum(1.242 for y, x in sqrGen(0, 6) if board[y][x] != 0)
    a = t1 + t2 + t3 + t4 + t5 + t6

    t1 = sum(1.114 for y, x in colGen(4, 8) if board[y][x] != 0)
    t2 = sum(1.326 for y, x in colGen(4, 7) if board[y][x] != 0)
    t3 = sum(1.453 for y, x in colGen(4, 6) if board[y][x] != 0)
    t4 = sum(1.242 for y, x in sqrGen(0, 8) if board[y][x] != 0)
    t5 = sum(1.141 for y, x in sqrGen(3, 8) if board[y][x] != 0)
    t6 = sum(1.242 for y, x in sqrGen(6, 8) if board[y][x] != 0)
    b = t1 + t2 + t3 + t4 + t5 + t6

    t1 = sum(1.114 for y, x in rowGen(8, 4) if board[y][x] != 0)
    t2 = sum(1.326 for y, x in rowGen(7, 4) if board[y][x] != 0)
    t3 = sum(1.453 for y, x in rowGen(6, 4) if board[y][x] != 0)
    t4 = sum(1.242 for y, x in sqrGen(8, 0) if board[y][x] != 0)
    t5 = sum(1.141 for y, x in sqrGen(8, 3) if board[y][x] != 0)
    t6 = sum(1.242 for y, x in sqrGen(8, 6) if board[y][x] != 0)
    c = t1 + t2 + t3 + t4 + t5 + t6

    t1 = sum(1.114 for y, x in colGen(4, 0) if board[y][x] != 0)
    t2 = sum(1.326 for y, x in colGen(4, 1) if board[y][x] != 0)
    t3 = sum(1.453 for y, x in colGen(4, 2) if board[y][x] != 0)
    t4 = sum(1.242 for y, x in sqrGen(0, 0) if board[y][x] != 0)
    t5 = sum(1.141 for y, x in sqrGen(3, 0) if board[y][x] != 0)
    t6 = sum(1.242 for y, x in sqrGen(6, 0) if board[y][x] != 0)
    d = t1 + t2 + t3 + t4 + t5 + t6

    if a > b and a > c and a > d:
        return board
    elif b > a and b > c and b > d:
        return rotate(board)
    elif c > a and c > b and c > d:
        return rotate(board, rotates=2)
    elif d > a and d > b and d > c:
        return rotate(board, rotates=3)
    else:
        print("error, two values collide")
        print("a: ", a, "b: ", b, "c: ", c, "d: ", d)
        return getEmptyBoard()


def orderNormal(board):
    """Re-orders values in puzzle, without changing logic. Goal is consistency"""

    temp = copyBoard(board)
    for digit in range(1, 9):  # go through 1 - 9, to ensure puzzle is in order
        for y, x in fullGen():  # check through entire board
            if (
                temp[y][x] < digit
            ):  # if cell is 0 or smaller number, ignore since already in order
                continue
            elif (
                temp[y][x] == digit
            ):  # if next cell we come to is our digit, break since already in order
                break
            else:  # if cell is out of order, swap all occurences of number w digit
                old = 1 * temp[y][x]  # get old, out of order num
                for y1, x1 in fullGen():  # new loop through board
                    if temp[y1][x1] == old:  # swap
                        temp[y1][x1] = digit
                    elif temp[y1][x1] == digit:
                        temp[y1][x1] = old
                break
    return temp


def normalize(board):
    """returns normalized form of board--all permutations should result in same normal form"""
    return orderNormal(rotateNormal(board))


def shuffle(board):
    """Shuffle a normalized board to return a random permutation"""
    digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    out = copyBoard(board)

    for old in range(1, 10):
        digit = digits[random.randint(0, len(digits) - 1)]
        digits.remove(digit)
        for y, x in fullGen():
            if out[y][x] == old:
                out[y][x] = digit
            elif out[y][x] == digit:
                out[y][x] = old

    r = random.randint(0, 3)
    return rotate(out, rotates=r)


def stringify(board):
    """Serializes board (a 2D list) into a flat string separated by semicolons"""
    outString = ""
    for y, x in fullGen():
        outString += str(board[y][x])
        if x == 8 and y != 8:
            outString += ";"
    return outString


def unstringify(boardString):
    """Unserializes board (a 2D list) from a flat string"""
    out = getEmptyBoard()
    temp = boardString.split(";")
    for y, x in fullGen():
        out[y][x] = int(temp[y][x])
    return out


def rowGen(y, x, inclusive=True):
    """Return generator that gives coord tuples (y,x) for the row of the argument coordinate.

    By default, generator returns the argument coordinate. Set inclusive=False to exclude
    the argument.
    """
    return ((y, x1) for x1 in range(9) if (inclusive) or (x1 != x))


def colGen(y, x, inclusive=True):
    """Return generator that gives coord tuples (y,x) for the column of the argument coordinate.

    By default, generator returns the argument coordinate. Set inclusive=False to exclude
    the argument.
    """
    return ((y1, x) for y1 in range(9) if (inclusive) or (y1 != y))


def sqrGen(y, x, inclusive=True):
    """Return generator that gives coord tuples (y,x) for the square of the argument coordinate.

    By default, generator returns the argument coordinate. Set inclusive=False to exclude
    the argument.
    """
    cY = (y // 3) * 3  # calculate top-left corner of square, for
    cX = (x // 3) * 3  # the provided cell
    return (
        (y1, x1)
        for y1 in range(cY, cY + 3)
        for x1 in range(cX, cX + 3)
        if (inclusive) or (y1 != y) or (x1 != x)
    )


def fullGen():
    """Returns generator that gives coord tuples (y,x) for whole board"""
    return ((y1, x1) for y1 in range(9) for x1 in range(9))


def exclusiveGen():
    """Returns generator that gives coord tuples (y,x) for whole board. Coords are

    given in order to get maximum distance between consecutive tuples."""
    a = lambda x, y: ((x * 3 + x // 3 + y) % 9)
    return ((a(y1, x1), x1) for y1 in range(9) for x1 in range(9))


def funnyGen():
    """Returns generator that gives coord tuples (y,x) for whole board. Coords fill

    out one square at a time."""
    xs = [0, 1, 2, 0, 1, 2, 0, 1, 2]
    ys = [0, 1, 2, 2, 0, 1, 1, 2, 0]
    for sqr in range(9):
        cornerY = ys[sqr] * 3
        cornerX = xs[sqr] * 3
        for cel in range(9):
            yield cornerY + ys[cel], cornerX + xs[cel]


def rotate(start, rotates=1):
    """spins board clockwise 90 degrees for each 'rotate'. Returns new board"""
    workboard = copyBoard(start)
    for i in range(rotates):
        temp = getEmptyBoard()
        for y, x in fullGen():
            y1 = x
            x1 = abs(8 - y)
            temp[y1][x1] = workboard[y][x]
        workboard = temp
    return workboard
