"""The dealer object for the bridgeobjects module."""

import random

from bridgeobjects import (SEATS, SHAPES, BALANCED_SHAPES, SEMI_BALANCED_SHAPES,
                           Call, SUITS)

from .board import Auction
from .dealer_engine import DealerEngine
from .board import Board


class Dealer(object):
    """The dealer object for the bridgeobjects module."""
    DEFAULT_POINTS_RANGE = [12, 14]
    #: the maximum number of points allowed in a hand
    MAX_POINTS = 26

    #: shapes suitable for single suited rebids
    SINGLE_SUITED_SHAPES = [
        [6, 3, 3, 1], [6, 3, 2, 2], [7, 2, 2, 2],
        [7, 3, 3, 0], [7, 3, 2, 1], [5, 4, 3, 1],
        [5, 4, 2, 2], [5, 4, 4, 0], [5, 5, 2, 1],
        [5, 5, 3, 0], [6, 5, 1, 1], [6, 5, 2, 0],
        [6, 4, 2, 1], [6, 4, 3, 0], [7, 4, 1, 1],
        [7, 4, 2, 0], [7, 5, 1, 0], [6, 6, 1, 0],
        [8, 4, 1, 0], [7, 6, 0, 0], [7, 3, 2, 1],
        [6, 3, 2, 2], [6, 3, 3, 1], [7, 2, 2, 2],
        [7, 3, 3, 0], [8, 2, 2, 1], [8, 3, 1, 1],
        [8, 3, 2, 0], [9, 2, 1, 1], [9, 3, 1, 0],
        [9, 2, 2, 0]
    ]

    #: shapes suitable for single suited rebids
    TWO_SUITED_SHAPES = [
            [5, 4, 3, 1], [5, 4, 2, 2], [6, 4, 2, 1],
            [5, 5, 2, 1], [6, 4, 3, 0], [5, 4, 4, 0],
            [7, 4, 1, 1], [5, 5, 3, 0], [6, 5, 1, 1],
            [6, 5, 2, 0], [7, 4, 2, 0], [7, 5, 1, 0],
            [6, 6, 1, 0], [8, 4, 1, 0], [7, 6, 0, 0],
            [6, 5, 2, 0]
    ]

    #: Weak two shapes
    WEAK_TWO_SHAPES = [
        [6, 3, 3, 1], [6, 3, 2, 2], [7, 2, 2, 2],
        [7, 3, 3, 0], [7, 3, 2, 1], [6, 5, 1, 1],
        [6, 5, 2, 0], [6, 4, 2, 1], [6, 4, 3, 0],
        [7, 4, 1, 1], [7, 4, 2, 0], [7, 5, 1, 0],
        [6, 6, 1, 0]
    ]

    def __init__(self, dealer=None, allow_overcalls=True):
        if not dealer:
            dealer = random.choice(SEATS)
        self.dealer = dealer
        self.engine = DealerEngine(dealer)
        self.allow_overcalls = allow_overcalls

    def deal_random_hand(self, points_range=None):
        """Return a randomly dealt hand."""
        if not points_range:
            points_range = [0, self.MAX_POINTS]
        hand = self.engine.get_hand_from_points_and_shape(points_range)
        return hand

    def deal_random_board(self, points_range=None):
        """Return a board of randomly dealt hands."""
        hand = self.deal_random_hand(points_range)
        board = None
        if self.dealer:
            seat = self.dealer
        else:
            seat = SEATS[random.choice(range(4))]
        valid_overcalls = False
        while not valid_overcalls:
            hands = {0: hand}
            board = self.engine.create_board_from_hands(hands, seat)
            auction = self._generate_auction_calls(board)
            valid_overcalls = self._valid_overcalls(auction)
        return board

    def deal_balanced_hand(self, points_range=None):
        """Return a board with balanced hand in the given points range."""
        hand = self.engine.get_hand_from_points_and_shape(points_range,
                                                          BALANCED_SHAPES)
        return hand

    def deal_balanced_board(self, points_range=None):
        """Return a board with balanced hand in the given points range."""
        hand = self.deal_balanced_hand(points_range)
        hands = {0: hand}
        board = self.engine.create_board_from_hands(hands)
        return board

    def deal_balanced_opposite(self, openers_hand, points_range=None, support=False):
        """Return a board with balanced hand opposite."""
        shape = self.engine.select_random_shape(BALANCED_SHAPES)
        hand = self.engine.get_hand_from_points_and_shape(points_range, shape)
        hands = {0: openers_hand, 2: hand}
        board = self.engine.create_board_from_hands(hands)
        return board

    def deal_single_suited_hand(self, points_range=None):
        """Return a board with single long suit in the given points range."""
        get_hand = self.engine.get_hand_from_points_and_shape
        hand = get_hand(points_range, self.SINGLE_SUITED_SHAPES)
        return hand

    def deal_single_suited_board(self, points_range=None):
        """Return a board with single suited hand in the given points range."""
        hand = self.deal_single_suited_hand(points_range)
        hands = {0: hand}
        board = self.engine.create_board_from_hands(hands)
        return board

    def deal_two_suited_hand(self, points_range=None):
        """Return a board with single long suit in the given points range."""
        shape_list = [shape for shape in SHAPES if shape[0] <= 6]
        exclusions = [shape for shape in BALANCED_SHAPES]
        exclusions.extend(self.SINGLE_SUITED_SHAPES)
        for shape in exclusions:
            if shape in shape_list:
                shape_list.remove(shape)
        hand = self.engine.get_hand_from_points_and_shape(points_range, shape_list)
        return hand

    def deal_two_suited_board(self, points_range=None):
        """Return a board with single suited hand in the given points range."""
        hand = self.deal_two_suited_hand(points_range)
        hands = {0: hand}
        board = self.engine.create_board_from_hands(hands)
        return board

    def deal_opening_one_hand(self):
        """Return a hand suitable for an opening one."""
        get_hand = self.engine.get_hand_from_points_and_shape
        found = False
        loop = 0
        openers_hand =  None
        while not found:
            loop += 1
            openers_hand = get_hand([12, 22])
            responders_hand = get_hand([0, 22], None, openers_hand)
            hands = {0: openers_hand, 2: responders_hand}
            board = self.engine.create_board_from_hands(hands)
            auction = self._generate_auction_calls(board)
            openers_bid = auction[0]
            if openers_bid.level == 1 and self._valid_overcalls(auction):
                found = True
        return openers_hand

    @staticmethod
    def _openers_bid(hand):
        """Return an opening bid on the hand."""
        board = Board()
        board.hands[0] = hand
        board.players[0].hand = hand
        bid = board.players[0].make_bid(board)
        return bid

    def deal_positive_one_nt_board(self):
        """Return a board with 1NT opener and positive response."""
        openers_hand = self.deal_balanced_hand([12, 14])
        get_hand = self.engine.get_hand_from_points_and_shape
        found = False
        responders_hand = None
        while not found:
            responders_hand = get_hand([3, 20], None, openers_hand)
            if responders_hand.hcp >= 11:
                found = True
            elif responders_hand.shape[0] >= 6:
                found = True
            elif (responders_hand.spades >= 5 or
                    responders_hand.hearts >= 5):
                found = True
        hands = {0: openers_hand, 2: responders_hand}
        board = self.engine.create_board_from_hands(hands)
        return board

    def deal_defence_to_one_nt_board(self):
        """Return a board with 1NT opponents and positive response."""
        dealer = random.choice([1, 3])
        openers_hand = self.deal_balanced_hand([12, 14])
        hands = {0: openers_hand}
        board = self.engine.create_board_from_hands(hands)
        found = False
        while not found:
            hand_one = board.hands[1]
            hand_three = board.hands[3]
            if (hand_one.hcp >= 16 or
                    hand_three.hcp >= 16):
                found = True
        self.engine.rotate_hands(1)
        return board

    @staticmethod
    def is_jump(first_bid, second_bid):
        """Return True if second bid is a jump over first."""
        result = False
        if second_bid.is_value_call and first_bid.is_value_call:
            jump_level = second_bid.level - first_bid.level
            if jump_level > 1:
                result = True
            elif jump_level == 1:
                if second_bid.is_suit_call and first_bid.is_suit_call:
                    if second_bid.denomination > first_bid.denomination:
                        result = True
                elif second_bid.is_no_trumps:
                    result = True
            else:
                result = False
        return result

    def _generate_auction_calls(self, board):
        """Return the auction calls as a list."""
        board.auction = Auction()
        player_index = SEATS.index(board.dealer)
        while not self._three_passes(board.bid_history):
            player = board.players[player_index]
            player.make_bid(board)
            player_index = (player_index + 1) % 4
        board.auction.calls = [Call(bid) for bid in board.bid_history]
        return board.auction.calls

    @staticmethod
    def _three_passes(calls):
        """Return True if there have been three consecutive passes."""
        three_passes = False
        if len(calls) >= 4:
            if calls[-3:] == ['P', 'P', 'P']:
                three_passes = True
        return three_passes

    def _valid_overcalls(self, auction):
        """Return True if the overcalls in the auction match self.allow_overcalls."""
        if self.allow_overcalls == 1:
            return True
        elif self.allow_overcalls == 0:
            return self._no_overcall_present(self._strip_auction(auction))
        elif self.allow_overcalls == 2:
            return self._overcall_present(self._strip_auction(auction))
        else:
            assert False, 'Invalid value for allow_overcalls: %s' % str(self.allow_overcalls)

    @staticmethod
    def _strip_auction(auction):
        """Return the auction, removing leading passes."""
        strip_auction = [call for call in auction]
        is_pass = True
        while is_pass and len(strip_auction) > 0:
            if strip_auction[0].is_pass:
                strip_auction.pop(0)
            else:
                is_pass = False
        return strip_auction

    @staticmethod
    def _no_overcall_present(auction):
        """Return True if there is no overcall in the auction."""
        value = True
        for call in auction[1::2]:
            if not call.is_pass:
                value = False
                break
        return value

    @staticmethod
    def _overcall_present(auction):
        """Return True if there is an overcall in the auction."""
        value = False
        for call in auction[1::2]:
            if not call.is_pass:
                value = True
                break
        return value