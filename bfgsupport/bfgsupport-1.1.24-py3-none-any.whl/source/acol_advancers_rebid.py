""" Bid for Game
    Acol AdvancersRebid module
"""

import inspect
from .bridge_tools import Bid, Pass
from .hand import Hand


class AdvancersRebid(Hand):
    """BfG AdvancersRebid class."""
    def __init__(self, hand_cards, board):
        super(AdvancersRebid, self).__init__(hand_cards, board)
        if len(self.bid_history) >= 6:
            self.overcaller_bid_one = Bid(self.bid_history[-6], '')
            self.overcaller_bid_two = Bid(self.bid_history[-2], '')
        else:
            self.overcaller_bid_one = Bid(self.bid_history[-2], '')
            self.overcaller_bid_two = None
        self.bid_one = Bid(self.bid_history[-4], '')
        self.overcaller_repeats_suit = (self.overcaller_bid_one.denomination ==
                                        self.overcaller_bid_two.denomination)
        self.trace = 0

    def suggested_bid(self):
        """Direct control to relevant method and return a Bid object."""
        if self.overcaller_bid_one.is_double:
            bid = self._overcaller_has_doubled()
        else:
            bid = self._overcaller_has_not_doubled()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcaller_has_doubled(self):
        """Return bid after overcaller has doubled."""
        if self._has_four_card_support_for_overcallers_second_suit():
            bid = self._double_and_support_second_suit()
        elif self._has_eight_points_and_no_support_for_second_suit():
            bid = self._eight_points_and_no_support_for_second_suit()
        elif self.overcaller_bid_one.is_double and self.overcaller_bid_two.is_double:
            bid = self._two_doubles()
        elif self._three_card_support_for_overcallers_second_suit():
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0142')
        elif self._has_eight_points_and_overcaller_passed_suit():
            bid = self.next_level_bid(self.longest_suit, '0647')
        else:
            bid = self._overcaller_has_not_doubled()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _eight_points_and_no_support_for_second_suit(self):
        """Return a bid with 8 points and no support for overcallers second suit."""
        if self._can_bid_at_this_level():
            bid = self._overcaller_has_doubled_suit_bid()
        elif self._has_three_cards_in_overcallers_major():
            bid = self.bid_to_game(self.overcaller_bid_two.denomination, '0025')
        elif self.stoppers_in_bid_suits:
            bid = self.next_nt_bid('0778')
        else:
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0025')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcaller_has_doubled_suit_bid(self):
        """Return bid after overcaller has doubled and shown suit."""
        if self._has_three_cards_in_overcallers_minor_at_level_four():
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0779')
        elif self._can_bid_second_suit_if_five_four():
            bid = self.next_level_bid(self.second_suit, '0780')
        elif self.suit_length(self.overcaller_bid_two.denomination) >= 3:
            if self.hcp >= 10:
                raise_level = 1
            else:
                raise_level = 1
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0782', raise_level)
        elif self.longest_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.longest_suit, '0783')
        else:
            bid = Pass('0784')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcaller_has_not_doubled(self):
        """Direct control to relevant method and return a Bid object."""
        if self.overcaller_bid_two.level >= 3:
            bid = self._respond_to_three_level()
        elif self.overcaller_bid_one.name in ['1NT', '2NT'] and self.bid_one.name == '2C':
            bid = self._stayman()
        elif self.overcaller_bid_two.name in ['1NT', '2NT']:
            bid = self._respond_to_nt()
        elif self.partner_bid_two.denomination == self.longest_suit and self.shape[0] >= 7:
            bid = self.next_level_bid(self.longest_suit, '0790')
        elif self._overcaller_has_bid_two_suits():
            bid = self._show_preference()
        elif self._can_bid_five_card_suit_after_overcaller_repeats_suit():
            bid = self._overcaller_repeats_suit()
        elif self._has_two_card_support_for_overcallers_six_card_suit():
            bid = self.next_level_bid(self.overcaller_bid_one.denomination, '0785')
        elif self._has_ten_points_and_four_card_support_for_overcaller():
            raise_level = self._support_raise_level(self.overcaller_bid_one.denomination)
            bid = self.next_level_bid(self.overcaller_bid_one.denomination, '0786', raise_level)
        elif self._can_rebid_seven_card_suit():
            bid = self.next_level_bid(self.longest_suit, '0787')
        else:
            bid = Pass('0788')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcaller_repeats_suit(self):
        """Return Bid after overcaller has repeated suit with strong hand."""
        if self.suit_length(self.overcaller_bid_one.denomination) >= 2:
            bid = self.next_level_bid(self.overcaller_bid_one.denomination, '0789')
        elif self.longest_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.longest_suit, '0790')
        elif self.hcp >= 12 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0791')
        elif self.nt_level <= 2:
            bid = self.nt_bid(2, '0792')
        else:
            bid = Pass('0793')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _two_doubles(self):
        """Bid after overcaller has doubled twice."""
        opponents_suit = self.openers_agreed_suit()
        if not self.openers_agreed_suit():
            bid = self._respond_to_three_level()
        elif self.suit_length(opponents_suit) >= 4:
            bid = Pass('0794')
        else:
            bid = self._respond_to_three_level()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _double_and_support_second_suit(self):
        """Bid after overcaller has doubled."""
        suit = self.overcaller_bid_two.denomination
        level = self.next_level(self.overcaller_bid_two.denomination)
        if self.hcp >= 10 and level < 4:
            level = min(4, level + 1)
            bid = self.suit_bid(level, suit, '0795')
        elif self.hcp >= 6 and level <= 3:
            level = min(3, level)
            bid = self.suit_bid(level, suit, '0796')
        elif self.hcp >= 8 and level <= 3:
            level = min(4, level)
            bid = self.suit_bid(level, suit, '0797')
        elif self._has_four_card_support_for_overcallers_second_suit_at_level_three():
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0798')
        elif self._overcaller_shows_support_after_double():
            bid = self.next_level_bid(suit, '0300')
        else:
            bid = Pass('0799')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_three_level(self):
        """Respond after a 3 level bid."""
        if (self.shape[0] >= 7 and self.longest_suit.is_major and self.next_level(self.longest_suit) <= 4 and
                self.longest_suit not in self.opponents_suits):
            bid = self.bid_to_game(self.longest_suit, '0575')
        elif self.overcaller_bid_two.is_game:
            bid = Pass('0800')
        elif self._can_bid_nt_after_overcaller_minor():
            bid = self._respond_to_three_level_minor()
        elif self._can_support_overcaller_second_suit_at_level_three():
            bid = self._respond_to_three_level_two_card_support()
        elif self._can_support_overcaller_second_suit_at_level_four():
            bid = self._respond_to_three_level_with_four_card_support()
        elif self._has_ten_points_and_can_support_overcaller_at_four_level():
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0801')
        elif self._can_support_overcaller_after_nt_and_major_bids():
            bid = self.bid_to_game(self.overcaller_bid_two.denomination, '0802')
        elif self._overcaller_has_jumped_after_double():
            bid = self.nt_bid(3, '0803')
        elif self.overcaller_bid_one.is_double and self.overcaller_bid_two.is_suit_call:
            bid = self._double_and_suit()
        elif self.overcaller_bid_two.is_double:
            bid = self._three_level_doubled()
        elif self._has_six_points_and_overcaller_bids_two_suits():
            bid = self.advancer_preference('0889')
        elif self._can_bid_six_card_major_over_overcallers_minor():
            bid = self.next_level_bid(self.longest_suit, '0322')
        elif self._has_five_four_after_overcaller_bids_minor():
            bid = self._respond_to_three_level_five_four()
        else:
            bid = Pass('0805')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _three_level_doubled(self):
        """Return bid after level 3 bid doubled."""
        if self.longest_suit in self.opponents_suits:
            bid = self._holding_opponents_suits()
        else:
            bid = self.next_level_bid(self.longest_suit, '0806')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _holding_opponents_suits(self):
        """Return bid after level 3 bid doubled holding opponents suits."""
        if self.shape[1] <= 3:
            bid = self.next_nt_bid('0807')
        elif self.second_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.second_suit, '0808')
        else:
            bid = Pass('0809')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _double_and_suit(self):
        """Return bid after overcaller has doubled and shown own suit."""
        if self.hcp <= 6 and self.shape[0] <= 6:
            bid = Pass('0810')
        elif self.suit_length(self.overcaller_bid_two.denomination) >= 3:
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0811')
        elif self.five_four_or_better and self.second_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.second_suit, '0812')
        elif self._is_unbalanced_and_can_show_suit():
            suit = self.longest_suit
            if suit in self.opponents_suits:
                suit = self.second_suit
            bid = self.next_level_bid(suit, '0813')
        elif self.hcp >= 16:
            bid = self.next_level_bid(self.second_suit, '0814')
        else:
            bid = self.next_nt_bid('0815')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_three_level_minor(self):
        """Respond after a 3 level bid with minor suit."""
        if self.overcaller_bid_two.denomination != self.bid_one.denomination:
            holding_one = self.suit_length(self.overcaller_bid_one.denomination)
            holding_two = self.suit_length(self.overcaller_bid_two.denomination)
            if holding_two - holding_one > 1:
                bid = Pass('0816')
            else:
                bid = self.next_level_bid(self.overcaller_bid_one.denomination, '0817')
        else:
            bid = Pass('0818')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_three_level_two_card_support(self):
        """Respond after a 3 level bid with 2 card support."""
        if self.next_level(self.overcaller_bid_two) <= self.overcaller_bid_two.game_level:
            bid = self.bid_to_game(self.overcaller_bid_two, '0819')
        else:
            bid = Pass('0820')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_three_level_with_four_card_support(self):
        """Respond after a 3 level bid with 4 card support."""
        if self._is_strong_and_four_card_support_for_overcallers_suit():
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0821')
        elif self._is_strong_and_no_support_for_overcaller_after_one_nt():
            bid = Pass('0822')
        elif self._has_nine_points_and_overcaller_strong():
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0823')
        elif self._has_support_for_overcallers_major():
            bid = self.next_level_bid(self.overcaller_bid_two.denomination, '0171')
        else:
            bid = Pass('0824')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_three_level_five_four(self):
        """Respond after a 3 level bid with 5/4 hand"""
        if self.bid_one.denomination == self.second_suit or not self.opener_bid_two.is_pass:
            suit = self.longest_suit
        else:
            suit = self.second_suit
        if self._has_thirteen_points_and_overcaller_support():
            bid = Pass('0825')
        elif self._has_two_card_support_for_overcallers_and_second_suit_minor():
            bid = self.next_level_bid(self.overcaller_bid_one.denomination, '0120')
        elif self._can_bid_selected_suit_at_level_four(suit):
            bid = self.next_level_bid(suit, '0826')
        else:
            bid = Pass('0827')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _stayman(self):
        """Return bid after overcaller responds to Stayman."""
        if self.overcaller_bid_two.is_major:
            if self.hcp <= 8:
                level = 3
            else:
                level = 4
            if (self.suit_length(self.overcaller_bid_two.denomination) >= 4 and
                    self.next_level(self.overcaller_bid_two.denomination) <= level):
                bid = self.suit_bid(level, self.overcaller_bid_two.denomination, '0828')
            else:
                level = 2
                if self.hcp > 10:
                    level = 3
                if level >= self.nt_level:
                    bid = self.nt_bid(level, '0829')
                else:
                    bid = Pass('0830')
        else:
            if self.nt_level <= 3:
                if self.hcp >= 10:
                    bid = self.nt_bid(3, '0238')
                else:
                    bid = self.next_nt_bid('0000')
            else:
                bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_nt(self):
        """Bid after overcaller has bid NT."""
        if self.is_semi_balanced or self.shape == [4, 4, 4, 1]:
            bid = self._respond_to_nt_semi_balanced()
        elif self.overcaller_bid_one.is_double and self.overcaller_bid_two.name == '2NT':
            bid = self._suit_after_nt()
        elif self.five_four_or_better and self.second_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.second_suit, '0831')
        else:
            bid = Pass('0832')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _suit_after_nt(self):
        """Return bid after DOUBLE, then NT with distributional hand."""
        suit = self.second_suit
        if suit not in self.opponents_suits:
            bid = self.next_level_bid(suit, '0833')
        else:
            bid = Pass('0834')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_nt_semi_balanced(self):
        """Bid after overcaller has bid NT and hand is semi-balanced."""
        if self.overcaller_bid_two.name == '1NT' or self.opener_bid_one.name == '1NT':
            bid = self._respond_to_nt_semi_balanced_after_one_nt()
        else:
            bid = self._respond_to_nt_semi_balanced_after_two_nt()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_nt_semi_balanced_after_one_nt(self):
        """Bid after overcaller has bid 1NT and hand is semi-balanced."""
        if 8 <= self.hcp <= 9 and self.nt_level <= 2:
            bid = self.nt_bid(2, '0835')
        elif self.hcp >= 10 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0836')
        else:
            bid = Pass('0837')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_nt_semi_balanced_after_two_nt(self):
        """Bid after overcaller has bid 2NT and hand is semi-balanced."""
        if (self.hcp >= 6 and self.nt_level <= 3 and not self.bid_one.is_pass):
            bid = self.nt_bid(3, '0838')
        elif self._has_five_points_and_five_card_major():
            bid = self.next_level_bid(self.longest_suit, '0849')
        else:
            bid = Pass('0839')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _show_preference(self):
        """Show preference after overcaller has bid two suits."""
        suit_one = self.overcaller_bid_one.denomination
        suit_two = self.overcaller_bid_two.denomination
        if self.suit_length(suit_one) >= self.suit_length(suit_two):
            suit = suit_one
        else:
            suit = suit_two
        level = self.next_level(suit)
        if self.suit_length(suit_one) >= 5 and self.shape[0]+self.shape[1] >= 10:
            bid = self.bid_to_game(suit_one, '0670')
        elif (self.hcp >= 4 and level <= 2) or self.hcp >= 10:
            bid = self.next_level_bid(suit, '0840')
        else:
            bid = Pass('0841')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    # Various utility functions

    def _support_raise_level(self, suit):
        """Return the level to support overcaller."""
        if suit.is_major:
            game_level = 4
        else:
            game_level = 5
        if self.hcp <= 10:
            raise_level = 0
        elif self.hcp <= 12:
            raise_level = 1
        else:
            raise_level = 2
        while self.next_level(suit, raise_level) > 4:
            raise_level -= 1
        while self.next_level(suit, raise_level) > game_level:
            raise_level -= 1
        return raise_level

    def _overcaller_minimum_rebid(self):
        """Return True if overcaller has made minimum bid."""
        if (self.overcaller_repeats_suit and
                self.overcaller_bid_two.level - self.overcaller_bid_one.level == 1):
            overcaller_minimum = True
        else:
            overcaller_minimum = False
        return overcaller_minimum

    # Various boolean functions

    def _has_four_card_support_for_overcallers_second_suit(self):
        """Return True if 4 card support for overcallers second bid."""
        result = (self.overcaller_bid_one.is_double and
                  self.overcaller_bid_two.is_suit_call and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 4 and
                  self.overcaller_bid_two.denomination.is_major)
        return result

    def _has_eight_points_and_no_support_for_second_suit(self):
        """Return True if 8 points and little support for overcallers second suit."""
        result = (self.overcaller_bid_one.is_double and
                  self.overcaller_bid_two.is_suit_call and
                  self.overcaller_bid_two.denomination != self.longest_suit and
                  self.hcp >= 8 and
                  not self.overcaller_bid_two.is_game)
        return result

    def _has_eight_points_and_overcaller_passed_suit(self):
        """Return True if 8 points and little support for overcallers second suit."""
        result = (self.overcaller_bid_one.is_double and
                  self.overcaller_bid_two.is_pass and
                  self.next_level(self.longest_suit) <= 2 and
                  self.shape[0] >= 5 and
                  self.hcp >= 8 and
                  not self.overcaller_bid_two.is_game and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _three_card_support_for_overcallers_second_suit(self):
        """Return True if can support overcallers second suit if major."""
        result = (self.overcaller_bid_one.is_double and
                  self.overcaller_bid_two.is_suit_call and
                  self.overcaller_bid_two.is_major and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 3 and
                  self.hcp >= 7)
        return result

    def _can_bid_at_this_level(self):
        """Return True if can bid at this level."""
        result = (self.next_level(self.longest_suit) <= 2 or
                  not self.is_semi_balanced or
                  self.nt_level > 3)
        return result

    def _has_three_cards_in_overcallers_major(self):
        """Return True if 3 card support for overcallers major."""
        result = (self.suit_length(self.overcaller_bid_two.denomination) >= 3 and
                  self.overcaller_bid_two.denomination.is_major)
        return result

    def _has_three_cards_in_overcallers_minor_at_level_four(self):
        """Return True if 3 card support for overcallers minor at 4 level."""
        result = (self.overcaller_bid_two.is_minor and
                  self.overcaller_bid_two.level == 4 and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 3)
        return result

    def _can_bid_second_suit_if_five_four(self):
        """Return True if can bid a 5/4 suit."""
        result = (self.five_four and
                  self.second_suit not in self.opponents_suits)
        return result

    def _overcaller_has_bid_two_suits(self):
        """Return True if overcaller has bid two suits."""
        result = (not self.overcaller_repeats_suit and
                  (self.overcaller_bid_one.is_suit_call and
                   self.overcaller_bid_two.is_suit_call))
        return result

    def _can_bid_five_card_suit_after_overcaller_repeats_suit(self):
        """Return True if own 5 card suit after overcaller_repeats suit."""
        result = (self.overcaller_repeats_suit and
                  self.hcp >= 12 and
                  self.shape[0] >= 5)
        return result

    def _has_two_card_support_for_overcallers_six_card_suit(self):
        """Return True if 2 card support for overcallers 6 card suit."""
        result = (self.overcaller_repeats_suit and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 2 and
                  self.hcp >= 9 and
                  self.suit_length(self.opener_bid_one.denomination) <= 2)
        return result

    def _has_ten_points_and_four_card_support_for_overcaller(self):
        """Return True if 10 points and 4 card support for overcaller."""
        result = (self.hcp >= 10 and
                  self.suit_length(self.overcaller_bid_one.denomination) >= 4 and
                  self.overcaller_bid_one.is_suit_call and
                  not self.bidding_above_game and
                  self.next_level_bid(self.overcaller_bid_one.denomination).level <= 4)
        return result

    def _can_rebid_seven_card_suit(self):
        """Return True if can repeat 7 card suit."""
        result = (self.hcp >= 7 and self.shape[0] >= 7 and
                  self.next_level(self.longest_suit) <= 3 and
                  self.longest_suit not in self.opponents_suits and
                  (self.overcaller_bid_two.is_value_call or
                   self.bid_one.is_value_call) and
                  self.bid_one.denomination != self.overcaller_bid_one.denomination)
        return result

    def _has_four_card_support_for_overcallers_second_suit_at_level_three(self):
        """Return True if 4 card support for overcallers second suit."""
        result = (((self.hcp >= 5 and self.opener_bid_one.name == '1NT') or
                   self.hcp >= 9) and
                  self.next_level(self.overcaller_bid_two.denomination) <= 3 and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 4)
        return result

    def _overcaller_shows_support_after_double(self):
        """Return True if overcaller support after he has doubled."""
        result = (self.overcaller_bid_one.is_double and
                  self.overcaller_bid_two.denomination == self.bid_one.denomination and
                  self.overcaller_bid_two.level == 3 and
                  self.hcp >= 8 and
                  self.suit_length(self.bid_one.denomination) >= 5 and
                  self.next_level(self.bid_one.denomination) <= 4)
        return result

    def _can_bid_nt_after_overcaller_minor(self):
        """Return True if can bid NT over overcaller minor."""
        stoppers = (self.stoppers_in_bid_suits or
                    self.overcaller_bid_one.is_nt or self.overcaller_bid_two.is_nt)
        result = (self.hcp >= 7 and
                  self.overcaller_bid_two.denomination.is_minor and
                  not self._overcaller_minimum_rebid() and
                  stoppers and
                  self.nt_level == 3)
        return result

    def _can_support_overcaller_second_suit_at_level_three(self):
        """Return True if can support overcaller with 2 cards at level 3."""
        result = (self.hcp >= 7 and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 2 and
                  self.next_level(self.overcaller_bid_two.denomination) <= 3)
        return result

    def _can_support_overcaller_second_suit_at_level_four(self):
        """Return True if able to support overcallers second suit at the 4 level."""
        result = (self.suit_length(self.overcaller_bid_two.denomination) >= 4 and
                  self.hcp >= 6 and
                  self.next_level(self.overcaller_bid_two.denomination) <= 4)
        return result

    def _has_ten_points_and_can_support_overcaller_at_four_level(self):
        """Return True if can support overcaller repeated suit at level 4."""
        result = (self.overcaller_repeats_suit and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 3 and
                  self.hcp >= 10 and
                  self.next_level(self.overcaller_bid_two.denomination) <= 4 and
                  not self.opener_bid_one.is_nt and
                  not self.opener_bid_two.is_value_call)
        return result

    def _can_support_overcaller_after_nt_and_major_bids(self):
        """Return True if overcaller has bid suit after nt."""
        result = (self.overcaller_bid_one.is_nt and
                  self.overcaller_bid_two.is_suit_call and
                  self.overcaller_bid_two.denomination.is_major and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 3 and
                  self.next_level(self.overcaller_bid_two.denomination) <= 4)
        return result

    def _overcaller_has_jumped_after_double(self):
        """Return True if overcaller has jumped after a double."""
        result = (self.overcaller_bid_two.is_double and
                  self.stoppers_in_bid_suits and
                  self.hcp >= 10 and
                  not self._overcaller_minimum_rebid() and
                  self.nt_level <= 3)
        return result

    def _has_six_points_and_overcaller_bids_two_suits(self):
        """Return True if 8 points and overcaller changes suits."""
        result = (self.overcaller_bid_one.level == 1 and
                  not self.overcaller_repeats_suit and
                  self.overcaller_bid_one.is_suit_call and
                  self.overcaller_bid_two.is_suit_call and
                  self.hcp >= 6)
        return result

    def _can_bid_six_card_major_over_overcallers_minor(self):
        """Return True if can bid six card major over overcaller's minor."""
        result = (self.overcaller_bid_two.denomination.is_minor and
                  self.hcp >= 10 and
                  self.shape[0] >= 6 and
                  self.longest_suit.is_major and
                  self.next_level(self.longest_suit) <= 3 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _has_five_four_after_overcaller_bids_minor(self):
        """Return True if 5/4 and overcaller rebids minor."""
        result = (self.overcaller_bid_two.denomination.is_minor and
                  self.hcp >= 6 and
                  self.five_four and
                  not (self.overcaller_repeats_suit and
                       self.overcaller_bid_one.denomination == self.bid_one.denomination))
        return result

    def _is_unbalanced_and_can_show_suit(self):
        """Return True if unbalanced and can show a suit."""
        result = (not self.is_balanced and
                  (self.longest_suit not in self.opponents_suits or
                   self.second_suit not in self.opponents_suits))
        return result

    def _is_strong_and_four_card_support_for_overcallers_suit(self):
        """Return True if strong and 4 card support overcallers suit."""
        result = (((self.hcp >= 10 and self.overcaller_bid_two.denomination.is_major) or
                   self.hcp >= 12) and
                  self.suit_length(self.overcaller_bid_two.denomination) >= 4 and
                  self.overcaller_repeats_suit)
        return result

    def _is_strong_and_no_support_for_overcaller_after_one_nt(self):
        """Return True if strong and no support for overcaller."""
        result = (self.hcp <= 11 and
                  not self.overcaller_bid_one.is_nt and
                  self.suit_points(self.overcaller_bid_two.denomination) <= 2)
        return result

    def _has_nine_points_and_overcaller_strong(self):
        """Return True if overcaller strong and 9 points."""
        result = (self.hcp >= 9 and
                  not self.overcaller_repeats_suit and
                  (self.overcaller_bid_one.level >= 2 or
                   self.overcaller_bid_one.is_nt))
        return result

    def _has_support_for_overcallers_major(self):
        """Return True if support of overcallers major."""
        result = (self.hcp+self.support_points(self.overcaller_bid_two.denomination) >= 10 and
                  self.overcaller_bid_two.denomination.is_major)
        return result

    def _has_thirteen_points_and_overcaller_support(self):
        """Return True if 13 points and overcaller supports suit."""
        result = (self.overcaller_bid_two.denomination == self.bid_one.denomination and
                  self.hcp <= 13 and
                  self.next_level(self.bid_one.denomination) >= 4)
        return result

    def _has_two_card_support_for_overcallers_and_second_suit_minor(self):
        """Return True if overcaller strong and repeats suit."""
        result = (self.is_jump(self.opener_bid_one, self.overcaller_bid_one) and
                  self.overcaller_repeats_suit and
                  self.suit_length(self.overcaller_bid_one.denomination) >= 2 and
                  self.second_suit.is_minor)
        return result

    def _can_bid_selected_suit_at_level_four(self, suit):
        """Return True if can bid suit at level 4."""
        result = ((self.next_level(suit) <= 4 or self.hcp >= 8) and
                  self.second_suit.is_minor and
                  not self.bid_one.is_pass and
                  suit not in self.opponents_suits)
        return result

    def _has_five_points_and_five_card_major(self):
        """Return True if 5 points a nd 5 card major."""
        result = (self.hcp >= 5 and self.shape[0] >= 5 and
                  self.longest_suit.is_major and
                  self.next_level(self.longest_suit) <= 3 and
                  self.longest_suit not in self.opponents_suits)
        return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result
