from twothousand_forty_eight.board import Board, check_move
from twothousand_forty_eight.board.tile import Tile
from twothousand_forty_eight.direction import Direction


def main():
    board = Board(4, 4)
    board.set_tile(0, 0, 2)
    board.set_tile(3, 0, 2)
    print(board)
    res = check_move(board, Direction.DOWN)
    print(res.possible, res.score_gain)
    board.tiles = res.tiles
    res = check_move(board, Direction.LEFT)
    print(res.possible, res.score_gain)
    board.tiles = res.tiles
    print(board)
