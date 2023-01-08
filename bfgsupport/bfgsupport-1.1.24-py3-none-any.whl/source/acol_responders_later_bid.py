""" Bid for Game
    Acol RespondersLaterBid module
"""
import inspect
from .bridge_tools import Bid, Pass
from .blackwood import Blackwood
from .hand import Hand


class RespondersLaterBid(Hand):
    """BfG RespondersLaterBid class."""
    def __init__(self, hand_cards, board):
        super(RespondersLaterBid, self).__init__(hand_cards, board)
        self.openers_last_bid = Bid(self.bid_history[-2])
        self.openers_penultimate_bid = Bid(self.bid_history[-6])
        self.trace = 0

    def suggested_bid(self):
        """Direct control to relevant method and return a Bid object."""
        suit = self.openers_last_bid.denomination

        if self.openers_penultimate_bid.name == '5NT':
            bid = Pass('0522')
        elif self.opener_bid_one.name == '2C':
            bid = self._two_club_opening()
        elif self.openers_last_bid.is_nt and self.openers_last_bid.level >= 4:
            bid = self._opener_bid_blackwood()
        elif self.previous_bid.is_nt and self.previous_bid.level >= 4:
            bid = self._responder_bid_nt()
        elif self._opener_bids_three_nt_after_change_of_major():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0529')
        elif self._opener_bids_three_nt_and_hand_has_six_card_major():
            bid = self.suit_bid(4, self.longest_suit, '0205')
        elif self._opener_rebids_second_suit_at_three_level():
            bid = self.suit_bid(4, self.bid_two.denomination, '0524')
        elif self._can_support_openers_second_suit_and_twelve_points():
            bid = self.next_level_bid(suit, '0525')
        elif self._opener_jumped_and_can_support():
            bid = self.nt_bid(4, '0526')
        elif self._opener_bid_minor_at_level_three_twelve_points():
            bid = self.nt_bid(3, '0527')
        elif self._opener_rebids_first_suit_two_card_support():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0528')
        elif self._has_support_for_openers_new_suit_at_level_four():
            bid = self.next_level_bid(self.opener_bid_three.denomination, '0465')
        elif self.hcp >= 16 and self.nt_level <= 4:
            bid = self.nt_bid(4, '0079')
        elif self._opener_strong_and_balanced_and_fifteen_points():
            bid = self.nt_bid(6, '0202')
        elif self._two_card_support_for_openers_six_card_suit_twelve_points():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0251')
        elif self._opener_support_six_card_suit() and not Bid(self.bid_history[-2]).is_game:
            bid = self.next_level_bid(self.longest_suit, '0343')
        elif self._has_support_for_openers_six_card_suit():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0541')
        elif self._opener_at_level_three_nine_points_and_stoppers():
            bid = self.nt_bid(3, '0286')
        elif self._opener_repeats_second_suit():
            bid = self._opener_has_rebid_second_suit()
        elif self.openers_last_bid.denomination == self.longest_suit and self.openers_last_bid.is_game:
            bid = Pass('0935')
        elif self._support_after_opener_shows_six_four():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0473')
        elif self._opener_has_bid_two_nt_and_five_four():
            bid = self.nt_bid(3, '0540')
        elif self._five_five_majors_after_3nt():
            bid = self.suit_bid(4, self.heart_suit, '0771')
        elif self._opener_has_bid_same_suit_three_times_and_not_at_game():
            bid = self.bid_to_game(self.opener_bid_one.denomination, '0000')
        elif self._opener_is_strong_and_has_bid_two_nt():
            bid = self.nt_bid(3, '0809')
        elif (self.opener_bid_three.level == 4 and self.opener_bid_three.denomination.is_minor and
              self.suit_length(self.opener_bid_three.denomination) >= 3 and self.hcp >= 11):
            bid = self.next_level_bid(self.opener_bid_three.denomination, '0835')
        else:
            bid = Pass('0533')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_bid_blackwood(self):
        """Return bid after opener has bid Blackwood."""
        if self.openers_last_bid.name == '4NT':
            bid = Blackwood(self.cards, self.board).ace_count
        elif self.openers_last_bid.name == '5NT':
            bid = Blackwood(self.cards, self.board).king_count
        else:
            bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_bid_nt(self):
        """Return bid after responder has bid NT."""
        if self.previous_bid.name == '4NT':
            bid = self._after_my_4nt()
        elif self.previous_bid.name == '4NT':
            bid = Blackwood(self.cards, self.board).select_contract()
        elif self.previous_bid.name == '5NT':
            bid = Blackwood(self.cards, self.board).select_contract()
        else:
            bid = self.nt_bid(1, '0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def suit_preference(self):
        """Return suit preference."""
        suit_one_holding = self.suit_length(self.opener_bid_one.denomination)
        suit_two_holding = self.suit_length(self.opener_bid_two.denomination)
        if suit_one_holding >= suit_two_holding:
            suit = self.opener_bid_one.denomination
        else:
            suit = self.opener_bid_two.denomination
        return suit

    def _after_my_4nt(self):
        """Return bid after partner has responded to my 4NT bid."""
        if Blackwood(self.cards, self.board).has_four_aces():
            bid = self.nt_bid(5, '0534')
        elif (self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                self.opener_bid_one.denomination != self.responder_bid_one.denomination and
                self.suit_length(self.opener_bid_one.denomination) >= 2):
            bid = self.suit_bid(6, self.opener_bid_one.denomination, '0512')
        else:
            bid = self.next_level_bid(self.suit_preference(), '0498')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _two_club_opening(self):
        if self._suit_support_after__two_club_opening_opening():
            bid = self.next_level_bid(self.longest_suit, '0530')
        elif self._opener_changes_suit_after__two_club_opening_opening():
            suit = self.suit_preference()
            if self.suit_length(suit) <= 2 and self.nt_level <= 3:
                bid = self.nt_bid(3, '0531')
            else:
                bid = self.next_level_bid(suit, '0532')
        elif self.opener_bid_three.is_nt and self.opener_bid_three.level >= 4:
            bid = self._opener_bid_blackwood()
        elif self.shape[1] >= 5 and self.next_level(self.second_suit) <= 5:
            bid = self.next_level_bid(self.second_suit, '0865')
        else:
            bid = Pass('0886')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_has_rebid_second_suit(self):
        """Return bid if opener has rebid second suit."""
        if self.hcp >= 15:
            bid = self.nt_bid(4, '0000')
        elif (self.partner_bid_one.denomination.is_suit and
                self.partner_bid_one.denomination != self.partner_bid_two.denomination and
                self.partner_last_bid.denomination == self.partner_bid_two.denomination and
                self.suit_length(self.partner_bid_one.denomination) > self.suit_length(self.partner_bid_two.denomination)):
            bid = self.next_level_bid(self.partner_bid_one.denomination, '0815')
        elif self.opener_bid_three.is_game:
            bid = Pass('0361')
        else:
            if (self.shape[0] >= 6 and
                    self.suit_points(self.longest_suit) >= 8 and
                    self.next_level(self.longest_suit) <= 4 and
                    self.longest_suit not in self.opponents_suits):
                suit = self.longest_suit
            elif self.opener_bid_two.denomination == self.responder_bid_two.denomination:
                suit = self.opener_bid_two.denomination
            elif self.suit_length(self.opener_bid_one.denomination) >= 2:
                suit = self.opener_bid_one.denomination
            elif self.suit_length(self.opener_bid_two.denomination) >= 2:
                suit = self.opener_bid_two.denomination
            else:
                suit = self.opener_bid_one.denomination
            bid = self.next_level_bid(suit, '0852')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    # Various boolean functions

    def _opener_bids_three_nt_after_change_of_major(self):
        """Return True if opener bids 3NT after change of suit."""
        result = (self.opener_bid_three.name == '3NT' and
                  self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  self.opener_bid_one.is_suit_call and
                  self.opener_bid_two.is_suit_call and
                  self.opener_bid_one.denomination.is_major and
                  self.suit_length(self.opener_bid_one.denomination) >= 3)
        return result

    def _opener_bids_three_nt_and_hand_has_six_card_major(self):
        """Return True if opener bids 3NT and hand has 6 card major."""
        result = (self.opener_bid_three.name == '3NT' and
                  self.shape[0] >= 6 and
                  self.longest_suit.is_major and
                  self.longest_suit not in self.opponents_suits and
                  self.next_level(self.longest_suit) <= 4)
        return result

    def _opener_rebids_second_suit_at_three_level(self):
        """Return True if opener rebids second suit at three level."""
        result = (self.opener_bid_three.denomination == self.bid_two.denomination and
                  self.bid_one.denomination != self.bid_two.denomination and
                  self.opener_bid_three.is_suit_call and
                  self.opener_bid_three.level == 3 and
                  self.next_level(self.bid_two.denomination) <= 4 and
                  self.hcp >= 9)
        return result

    def _can_support_openers_second_suit_and_twelve_points(self):
        """Return True if can support openers second suit with opening hand."""
        result = (self.openers_last_bid.level == 3 and
                  (self.openers_last_bid.denomination == self.longest_suit or
                   self.openers_last_bid.denomination == self.second_suit) and
                  self.hcp >= 12)
        return result

    def _opener_jumped_and_can_support(self):
        """Return True if opener jumps and can support."""
        result = (self.is_jump(self.bid_one, self.opener_bid_two) and
                  self.bid_one.denomination == self.opener_bid_three.denomination and
                  self.hcp >= 16 and
                  self.nt_level <= 4)
        return result

    def _opener_bid_minor_at_level_three_twelve_points(self):
        """Return True if opener bids minor at level 3."""
        result = (self.opener_bid_three.level == 3 and
                  self.opener_bid_three.denomination.is_minor and
                  self.hcp >= 12 and
                  self.is_balanced and
                  self.nt_level <= 3)
        return result

    def _opener_rebids_first_suit_two_card_support(self):
        """Return True if opener rebids opening suit and two card support."""
        result = (self.opener_bid_one.denomination == self.opener_bid_three.denomination and
                  self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  not self.responder_bid_two.is_nt and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  self.opener_bid_three.level <= 4 and
                  not self.opener_bid_three.is_game and
                  self.hcp >= 8)
        return result

    def _suit_support_after__two_club_opening_opening(self):
        """Return True if after 2C can support."""
        result = (self.opener_bid_one.name == '2C' and
                  self.hcp >= 8 and
                  (self.opener_bid_two.denomination == self.longest_suit or
                   self.opener_bid_three.denomination == self.longest_suit) and
                  self.shape[0] >= 6)
        return result

    def _opener_changes_suit_after__two_club_opening_opening(self):
        """Return True if opener changes suit after 2C opening."""
        result = (self.opener_bid_one.name == '2C' and
                  self.opener_bid_two.denomination != self.opener_bid_three.denomination and
                  not self.openers_last_bid.is_game)
        return result

    def _opener_strong_and_balanced_and_fifteen_points(self):
        """Return True if opener is strong and balanced."""
        result = (self.opener_bid_two.name == '2NT' and
                  self.opener_bid_three.name == '3NT' and
                  self.hcp >= 15)
        return result

    def _two_card_support_for_openers_six_card_suit_twelve_points(self):
        """Return True if two card support for opener's six card suit."""
        result = (self.opener_bid_one.denomination.is_major and
                  self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                  self.opener_bid_two.denomination == self.openers_last_bid.denomination and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  self.hcp >= 12 and
                  self.next_level(self.opener_bid_one.denomination) <= 4)
        return result

    def _opener_at_level_three_nine_points_and_stoppers(self):
        """Return True if nine points and stoppers."""
        result = (self.openers_last_bid.level == 3 and
                  not(self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                      self.opener_bid_one.denomination == self.opener_bid_three.denomination) and
                  self.hcp >= 11 and
                  self.stoppers_in_unbid_suits and
                  self.nt_level <= 3)
        return result

    def _opener_repeats_second_suit(self):
        """Return True if opener repeats second_suit."""
        result = (self.opener_bid_two.is_suit_call and
                  self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  self.opener_bid_two.denomination == self.opener_bid_three.denomination
                  and self.nt_level <= 4)
        return result

    def _opener_support_six_card_suit(self):
        """Return True if opener support six card suit."""
        result = (self.opener_bid_three.denomination == self.longest_suit and
                  self.shape[0] >= 6 and
                  self.hcp >= 8 and
                  self.next_level(self.longest_suit) <= 6)
        return result

    def _has_support_for_openers_new_suit_at_level_four(self):
        """Return True if opener shows new suit at 4 level and support."""
        result = (self.opener_bid_three.level == 4 and
                  self.opener_bid_three.denomination != self.opener_bid_one.denomination and
                  self.opener_bid_three.denomination != self.opener_bid_two.denomination and
                  self.suit_length(self.opener_bid_three.denomination) >= 3 and
                  not self.opener_bid_three.is_game)
        return result

    def _support_after_opener_shows_six_four(self):
        """Return True if support for opener who shows six four."""
        result = (self.hcp >= 9 and
                  self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                  self.opener_bid_one.denomination != self.opener_bid_three.denomination and
                  not self.opener_bid_three.is_nt and
                  # self.responder_bid_two.is_nt and
                  not Bid(self.bid_history[-6]).is_pass and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  not (self.partner_last_bid.denomination == self.opener_bid_one.denomination and
                       self.partner_last_bid.is_game))
        return result

    def _opener_has_bid_two_nt_and_five_four(self):
        """Return True if opener hand bid 2NT and hand is 5/4."""
        result = (self.opener_bid_three.name == '2NT' and
                  self.five_four and
                  self.hcp >= 10 and
                  self.nt_level <= 3)
        return result

    def _has_support_for_openers_six_card_suit(self):
        """Return True if opener has 6 card suit and support."""
        result = (self.opener_bid_one.denomination == self.opener_bid_three.denomination and
                  self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  self.hcp >= 12 and
                  self.opener_bid_three.level <= 6 and
                  self.next_level(self.opener_bid_one.denomination) <= 5 and
                  not self.opener_bid_three.is_game)
        return result

    def _five_five_majors_after_3nt(self):
        """Return True if _five_five_majors_after_3nt."""
        result = (self.partner_last_bid.name == '3NT' and
                  self.spades >= 5 and self.hearts >= 5 and
                  self.next_level(self.heart_suit) <= 4 and
                  self.heart_suit not in self.opponents_suits)
        return result

    def _opener_has_bid_same_suit_three_times_and_not_at_game(self):
        """Return True if opener has bid suit 3 times and not at game."""
        result = (self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                  self.opener_bid_one.denomination == self.opener_bid_three.denomination and
                  self.suit_length(self.opener_bid_one.denomination) >= 3 and
                  not self.bidding_above_game and
                  self.hcp >= 12)
        return result

    def _opener_is_strong_and_has_bid_two_nt(self):
        """Return True if opener is strong and has bid 2NT."""
        result = (self.opener_bid_three.name == '2NT' and
                  self.hcp >= 8 and
                  self.opener_bid_one.denomination != self.opener_bid_two.denomination)
        return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result
    #
    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result
