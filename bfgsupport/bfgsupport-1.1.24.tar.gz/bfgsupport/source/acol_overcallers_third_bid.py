""" Bid for Game
    Acol OverCallersBid module
"""

import inspect
from .bridge_tools import Pass, Double
from .hand import Hand


class OverCallersThirdBid(Hand):
    """BfG OverCallersRebid class."""
    def __init__(self, hand_cards, board):
        super(OverCallersThirdBid, self).__init__(hand_cards, board)
        self.trace = 0

    def suggested_bid(self):
        """Direct control to relevant method and return a Bid object."""
        if self._advancer_supports_major_after_stayman():
            if self.hcp >= 16:
                bid = self.next_level_bid(self.bid_two.denomination, '0842')
            else:
                bid = Pass('0843')
        elif self._can_show_second_major_after_stayman():
            bid = self.next_level_bid(self.spade_suit, '0216')
        elif self._has_thirteen_points_advancer_supports_second_suit():
            bid = self.next_level_bid(self.bid_two.denomination, '0844')
        elif self._has_fifteen_points_advancer_bids_two_suits():
            bid = self._fifteen_points_advancer_bids_two_suits()
        elif self._is_very_strong_and_five_four():
            if self.second_suit not in self.opponents_suits:
                suit = self.second_suit
            else:
                suit = self.longest_suit
            bid = self.next_level_bid(suit, '0846')
        elif self._is_strong_and_advancer_bids():
            bid = self._strong_hand()
        elif self._three_suits_have_been_bid():
            bid = self._three_suits_bid()
        elif self._has_two_card_support_for_advancers_major():
            bid = self.next_level_bid(self.partner_bid_one.denomination, '0324')
        elif self._has_six_card_suit_advancer_repeats_suit():
            bid = self.next_level_bid(self.longest_suit, '0850')
        elif self._is_strong_advancer_bids_nt_after_stayman():
            bid = self.nt_bid(3, '0000')
        else:
            bid = Pass('0851')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_hand(self):
        """Return bid with strong hand."""
        if self.bid_one.is_double and self.bid_two.is_double:
            bid = Pass('0132')
        elif self._support_for_advancer():
            bid = self.next_level_bid(self.advancer_bid_one.denomination, '0658')
        elif self.is_balanced and self.nt_level <= 3:
            bid = self.next_nt_bid('0852')
        elif self.five_five and self.second_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.second_suit, '0853')
        elif self.five_four and self.second_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.second_suit, '0854')
        elif (self.partner_bid_one.denomination != self.partner_last_bid.denomination and
                self.longest_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.longest_suit, '0855')
        elif (not self.partner_bid_one.is_pass and
                self.suit_length(self.partner_bid_one.denomination) >= 3):
            bid = self.next_level_bid(self.partner_bid_one.denomination, '0857')
        else:
            bid = Pass('0858')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _three_suits_bid(self):
        """Return bid after 3 suits have been bid."""
        suit_to_bid = self._select_suit_after_three_suits_bid()
        if self._suit_is_minor(suit_to_bid):
            bid = self.next_nt_bid('0847')
        elif suit_to_bid not in self.opponents_suits:
            bid = self.next_level_bid(suit_to_bid, '0848')
        else:
            bid = Pass('0849')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _fifteen_points_advancer_bids_two_suits(self):
        """Return bid if strong and advancer bids two suits."""
        if self.bidding_above_game:
            bid = Double('0912')
        elif self._advancer_has_passed_after_double():
            bid = Pass('0913')
        elif (self.suit_length(self.opener_bid_one.denomination) >= 3 and
                self.suit_points(self.opener_bid_one.denomination) >= 5):
            bid = Pass('0427')
        else:
            suit = self._suit_preference()
            bid = self.next_level_bid(suit, '0845')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    # Various utility functions

    def _suit_preference(self):
        """Return preference (if any) for partner's suits."""
        suit = None
        if (self.partner_bid_one.denomination.is_major or
                self.partner_bid_one.denomination.is_minor):
            suit_one = self.partner_bid_one.denomination
            if self.suit_length(suit_one) >= 3:
                suit = suit_one
        if (self.partner_last_bid.denomination.is_major or
                self.partner_last_bid.denomination.is_minor):
            suit_two = self.partner_last_bid.denomination
            if (self.suit_length(suit_two) >= 4 or
                    not suit):
                suit = suit_two
        if not suit:
            suit = self.no_trumps
        return suit

    def _select_suit_after_three_suits_bid(self):
        if self.suit_length(self.partner_last_bid.denomination) >= 4:
            suit_to_bid = self.partner_last_bid.denomination
        elif self.five_five:
            suit_to_bid = self.second_suit
            if suit_to_bid in self.opponents_suits:
                suit_to_bid = self.longest_suit
        else:
            suit_to_bid = self.longest_suit
        return suit_to_bid

    # Various boolean functions

    def _advancer_supports_major_after_stayman(self):
        """Return True if advancer supports major after Stayman."""
        result = (self.bid_one.name == '1NT' and
                  self.partner_bid_one.name == '2C' and
                  self.partner_last_bid.denomination == self.bid_two.denomination and
                  self.partner_last_bid.level == 3)
        return result

    def _can_show_second_major_after_stayman(self):
        """Return True if got 4 spades and 4 hearts."""
        result = (self.bid_one.name == '1NT' and
                  self.partner_bid_one.name == '2C' and
                  self.bid_two.name == '2H' and
                  self.partner_last_bid.name == '2NT' and
                  self.spades >= 4 and
                  self.spade_suit not in self.opponents_suits)
        return result

    def _has_thirteen_points_advancer_supports_second_suit(self):
        """Return True if 13 points and advancer support second suit."""
        result = (self.partner_last_bid.denomination == self.bid_two.denomination and
                  self.partner_last_bid.is_suit_call and
                  not self.partner_last_bid.is_game and
                  self.hcp >= 13 and
                  not self.singleton_honour)
        return result

    def _has_fifteen_points_advancer_bids_two_suits(self):
        """Return True if fifteen points and advancer bids two suits."""
        result = (self.partner_bid_one.denomination != self.partner_last_bid.denomination and
                  not self.bid_one.is_nt and
                  not self.partner_last_bid.is_nt and
                  not self.partner_last_bid.is_game and
                  self._suit_preference().is_suit and
                  self.hcp >= 15)
        return result

    def _is_very_strong_and_five_four(self):
        """Return True if strong and 5/4."""
        result = (self.hcp >= 19 and
                  self.five_four_or_better and
                  not self.bid_two.is_nt and
                  not self.bidding_above_game and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _is_strong_and_advancer_bids(self):
        """Return True if strong and advancer bids."""
        result = (self.hcp >= 16 and
                  not self.partner_last_bid.is_pass and
                  not self.partner_last_bid.is_game)
        return result

    def _three_suits_have_been_bid(self):
        """Return True if 3 suits bid."""
        my_suits = [self.bid_one.denomination, self.bid_two.denomination]
        result = (self.partner_bid_one.denomination != self.partner_last_bid.denomination and
                  self.partner_bid_one.is_suit_call and
                  self.partner_last_bid.level == 3 and
                  self.bid_one.denomination != self.partner_last_bid.denomination and
                  not self.partner_last_bid.is_game and
                  self.partner_last_bid.denomination not in my_suits)
        return result

    def _advancer_has_passed_after_double(self):
        """Return True if advancer passes after double."""
        result = (self.bid_one.is_double and
                  (self.partner_bid_one.is_pass or
                   self.partner_last_bid.is_pass))
        return result

    def _has_two_card_support_for_advancers_major(self):
        """Return True if 2 card support for advancers major."""
        result = (self.partner_bid_one.denomination == self.partner_last_bid.denomination and
                  self.partner_bid_one.is_value_call and
                  self.partner_bid_one.denomination.is_major and
                  self.suit_length(self.partner_bid_one.denomination) >= 2 and
                  self.hcp >= 15 and
                  not self.partner_last_bid.is_game)
        return result

    def _has_six_card_suit_advancer_repeats_suit(self):
        """Return True if 6 card suit and advancer repeats their suit."""
        result = (self.partner_bid_one.denomination == self.partner_last_bid.denomination and
                  self.partner_bid_one.is_value_call and
                  self.shape[0] >= 6 and
                  not self.partner_last_bid.is_game and
                  self.longest_suit not in self.opponents_suits and
                  self.hcp >= 12)
        return result

    def _is_strong_advancer_bids_nt_after_stayman(self):
        """Return True if strong and advancer bids NT after stayman."""
        result = (self.bid_one.name == '1NT' and
                  self.partner_bid_one.name == '2C' and
                  self.partner_last_bid.name == '2NT' and
                  self.hcp >= 17 and
                  self.nt_level <= 3)
        return result

    def _suit_is_minor(self, suit_to_bid):
        """Return True if suit is minor."""
        result = (self.nt_level <= 3 and
                  (suit_to_bid.is_minor or
                   suit_to_bid in self.opponents_suits))
        return result

    def _support_for_advancer(self):
        """Return True if xxx."""
        if not self.advancer_bid_two:
            result = False
        else:
            result = (self.advancer_bid_one.denomination == self.advancer_bid_two.denomination and
                      self.suit_length(self.advancer_bid_one.denomination) >= 3)
        return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result

