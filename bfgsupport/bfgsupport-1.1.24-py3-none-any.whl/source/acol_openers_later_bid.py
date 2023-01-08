""" Bid for Game
    Acol OpenersLaterBid module
"""

import inspect
from .bridge_tools import Bid, Pass
from .blackwood import Blackwood
from .hand import Hand


class OpenersLaterBid(Hand):
    """BfG OpenersLaterBid class."""
    def __init__(self, hand_cards, board):
        super(OpenersLaterBid, self).__init__(hand_cards, board)
        self.my_last_bid = Bid(self.bid_history[-4], '')
        self.my_penultimate_bid = Bid(self.bid_history[-8], '')
        self.partners_last_bid = Bid(self.bid_history[-2], '')
        self.partners_penultimate_bid = Bid(self.bid_history[-6], '')
        self.trace = 0

    def suggested_bid(self):
        """Direct control to relevant method and returns a Bid object."""
        if self.my_last_bid.name == '4NT':
            bid = self.bid_after_4nt()
        elif self.my_last_bid.name == '5NT':
            bid = Blackwood(self.cards, self.board).select_contract()
        elif self.partners_last_bid.name == '4NT':
            bid = Blackwood(self.cards, self.board).count_aces()
        elif self.partners_last_bid.name == '5NT':
            bid = Blackwood(self.cards, self.board).count_kings()
        elif (self.responder_bid_one.denomination != self.responder_bid_two.denomination and
              self.responder_bid_three.denomination == self.opener_bid_one.denomination and
              self.responder_bid_one.denomination.is_major and
              self.suit_length(self.responder_bid_one.denomination) >= 3 and
              not Bid(self.bid_history[-2]).is_game):
            bid = self.bid_to_game(self.responder_bid_one.denomination, '0936')
        elif self._responder_supports_last_bid_suit():
            bid = self.bid_to_game(self.partners_last_bid.denomination, '0536')
        elif (self.hcp >= 23 and
                self.responder_bid_two.denomination.is_suit and
                self.responder_bid_two.denomination != self.responder_bid_one.denomination and
                self.next_level(self.responder_bid_two.denomination) < 6):
            bid = self._strong_and_responder_changes_suit()
        else:
            bid = Pass('0537')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def bid_after_4nt(self):
        """Return bid after response to 4NT."""
        four_aces = Blackwood(self.cards, self.board).four_aces
        if four_aces and self.kings != 4:
            bid = self.nt_bid(5, '0538')
        elif (Blackwood(self.cards, self.board).has_three_aces and
              self.kings == 4 and self._suit_fit()):
            bid = self.suit_bid(6, self._suit_fit(), '0709')
        else:
            bid = Blackwood(self.cards, self.board).select_contract()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_and_responder_changes_suit(self):
        """Return bid after responder changes suit, showing 5/5."""
        if self.suit_length(self.responder_bid_one.denomination) >= 3:
            bid = self.suit_bid(6, self.responder_bid_one.denomination, '0000')
        elif self.suit_length(self.responder_bid_two.denomination) >= 3:
            bid = self.suit_bid(6, self.responder_bid_two.denomination, '0867')
        else:
            bid = self.nt_bid(6, '0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid


    # Various utility functions
    def _suit_fit(self):
        """Return the suit if a fit is found."""
        suits = []
        our_bids = [bid for bid in self.bid_history[::-1][1::2]]
        responders_bids = our_bids[::2]
        for bid in responders_bids:
            call = Bid(bid)
            if call.level <= 4 and call.is_suit_call:
                if call.denomination != self.club_suit:
                    suits.append(call.denomination)
                elif call.denomination == self.club_suit and Bid(self.bid_history[0]).is_suit_call:
                    suits.append(call.denomination)
        for suit in suits:
            if self.suit_length(suit) >= 4:
                return suit
        return None

    # Various boolean functions

    def _responder_supports_last_bid_suit(self):
        """Return True if zzz."""
        result = (self.my_last_bid.denomination != self.my_penultimate_bid.denomination and
                  (self.partners_last_bid.denomination == self.my_last_bid.denomination or
                   self.partners_last_bid.denomination == self.my_penultimate_bid.denomination) and
                  self.partners_last_bid.denomination.is_suit and
                  not self.bidding_above_game)
        return result

    # def xxx(self):
    #     """Return True if zzz."""
    #     result = False
    #     return result
    #
    # def xxx(self):
    #     """Return True if zzz."""
    #     result = False
    #     return result
