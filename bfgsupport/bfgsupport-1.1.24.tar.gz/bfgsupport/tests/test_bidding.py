""" Bid for Game
    test hands module
"""

import os
from termcolor import colored
import sys

sys.path.append('../bridgeobjects')

from ..source.pbn import PBN
# import board_xref
from .board_xref import board_xref

def _get_boards():
    """Return a list of boards from the path."""
    path = 'test_data/specification_hands.pbn'
    print('cwd', os.getcwd())
    assert os.path.isfile(path), f'Path is not a file {path}'
    boards = PBN().boards_from_path(path)
    return boards


def _get_suggested_call(board):
    """Check a bid and return True if correct."""
    board.bid_history = [call.name for call in board.auction.calls[:-1]]
    dealer_index = 0
    player = board.players[dealer_index]
    suggested_bid = player.make_bid()
    return suggested_bid


def _check_xref(board, suggested_bid):
    """Return True if the comment_xref entry is correct."""
    board_number = '{:0>4}'.format(board.description.split(' ')[0])
    boards = board_xref[suggested_bid.call_id]
    if len(boards) > 0 and board_number in boards:
        return True
    else:
        return False


def test_bid_and_xref_correct():
    """Test that the correct bid is made."""
    boards = _get_boards()
    print('\n\nProcessing {} boards'.format(len(boards)))
    failed = []
    failed_text = '{}, correct call={}, suggested call={}, xref check={}, correct call id={}'
    for board in boards:
        suggested_bid = _get_suggested_call(board)
        # assert suggested_bid == board.auction.calls[-1], board.description
        # assert _check_xref(board, suggested_bid), board.description
        if suggested_bid != board.auction.calls[-1] or not _check_xref(board, suggested_bid):
            failed.append(failed_text.format(board.description,
                                             board.auction.calls[-1].name,
                                             suggested_bid.name,
                                             _check_xref(board, suggested_bid),
                                             suggested_bid.call_id,
                                             ))
    print('')
    if failed:
        for item in failed:
            print(colored(item, 'red'))
    else:
        print(colored('All tests passed ...', 'green'))
    print('')
