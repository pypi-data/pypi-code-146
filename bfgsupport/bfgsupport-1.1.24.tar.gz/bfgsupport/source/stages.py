"""Generate stages for BfG."""
import sys
from .dealer import Dealer
from .dealer_engine import DealerEngine

sys.path.append('../')


class Stage(object):
    """Stage returns Boards that meet stage criteria."""

    #: points range for two no trump opening
    TWO_NT_POINTS = [20, 22]
    OPENING_ONES_POINTS = [10, 22]

    def __init__(self, stage, dealer=None):
        """direct the request to appropriate function and return a board."""
        self.dealer_engine = DealerEngine(dealer)
        if stage == 'opening ones':
            self.board = self.opening_ones(dealer)
        elif stage == 'limit_bids':
            self.board = self.limit_bids(dealer)
        elif stage == 'balanced_rebids':
            self.board = self.balanced_rebids(dealer)
        elif stage == 'single_suited_rebids':
            self.board = self.single_suited_rebids(dealer)
        elif stage == 'support_for_responder':
            self.board = self.support_for_responder(dealer)
        elif stage == 'raise_responders_nt':
            self.board = self.raise_responders_nt(dealer)
        elif stage == 'response_to_weak_two':
            self.board = self.response_to_weak_two(dealer)
        elif stage == 'response_to_two_nt':
            self.board = self.response_to_two_nt(dealer)
        elif stage == 'response_to_two_clubs':
            self.board = self.response_to_two_clubs(dealer)
        else:
            self.board = Dealer(dealer).deal_random_board()

    @staticmethod
    def opening_ones(dealer):
        """Return a stage board appropriate for opening_ones."""
        return Dealer(dealer).deal_opening_one_board()

    @staticmethod
    def limit_bids(dealer):
        """Return a stage board appropriate for limit_bids."""
        return Dealer(dealer).deal_random_board()

    @staticmethod
    def balanced_rebids(dealer):
        """Return a stage board appropriate for balanced_rebids."""
        return Dealer(dealer).deal_random_board()

    @staticmethod
    def single_suited_rebids(dealer):
        """Return a stage board appropriate for single_suited_rebids."""
        return Dealer(dealer).deal_random_board()

    @staticmethod
    def support_for_responder(dealer):
        """Return a stage board appropriate for support_for_responder."""
        return Dealer(dealer).deal_random_board()

    @staticmethod
    def raise_responders_nt(dealer):
        """Return a stage board appropriate for raise_responders_nt."""
        return Dealer(dealer).deal_random_board()

    @staticmethod
    def response_to_weak_two(dealer):
        """Return a stage board appropriate for response_to_weak_two."""
        return Dealer(dealer).deal_random_board()

    @staticmethod
    def response_to_two_nt(dealer):
        """Return a stage board appropriate for response_to_two_nt."""
        return Dealer(dealer).deal_random_board()

    @staticmethod
    def response_to_two_clubs(dealer):
        """Return a stage board appropriate for response_to_two_clubs."""
        return Dealer(dealer).deal_random_board()


if __name__ == "__main__":
    for _ in range(100):
        board = Stage('opening_ones', 'S').board
        print('Dealer: {}.'.format(board.dealer))
        for hand in board.hands:
            print(hand, hand.shape, hand.hcp)
