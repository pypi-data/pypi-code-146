""" Bid for Game
    Acol OverCallersBid module
"""

import inspect
from .bridge_tools import Bid, Pass, Double
from .hand import Hand

import time


class OverCallersBid(Hand):
    """BfG OverCallersBid class."""
    def __init__(self, hand_cards, board):
        now = time.time()
        super(OverCallersBid, self).__init__(hand_cards, board)
        self.trace = 0

    def suggested_bid(self):
        """Direct control to relevant method and return a Bid object"""
        now = time.time()
        suit = self.longest_suit
        if self._has_eight_points_and_eight_card_major():
            bid = self.bid_to_game(self.longest_suit, '0539')
        elif self._has_eight_points_and_eight_card_minor():
            bid = self.next_level_bid(suit, '0325')
        elif self._can_bid_seven_card_suit_over_openers_weak_two():
            bid = self.next_level_bid(self.longest_suit, '0252')
        elif len(self.bid_history) >= 5 and self.opener_bid_one.is_suit_call:
            bid = Pass('0540')
        elif self.opener_bid_one.name == '2C' or self.opener_bid_one.name == '2NT':
            bid = Pass('0541')
        elif self.hcp >= 15:
            bid = self._strong_bid()
        elif self.shape[0] >= 5 and self.hcp >= 9:
            bid = self._suit_overcall()
        elif self._can_make_weak_balanced_overcall():
            bid = self._weak_balanced_overcall()
        elif self._can_bid_six_card_suit_at_two_level():
            bid = self.next_level_bid(self.longest_suit, '0270')
        elif self._can_double_in_pass_out_seat():
            bid = Double('0501')
        else:
            bid = Pass('0542')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_bid(self):
        """Overcall with strong hand."""
        if self._very_strong_semi_balanced_with_stoppers():
            bid = self.nt_bid(3, '0543')
        elif self.hcp >= 19 and self.nt_level <= 2:
            bid = Double('0544')
        elif self._is_strong_and_semi_balanced_with_stoppers_over_weak_two():
            bid = self.nt_bid(2, '0545')
        elif self._is_strong_and_semi_balanced_with_stoppers_over_one_level():
            bid = self.nt_bid(self.nt_level, '0546')
        elif self._is_strong_shortage_in_bid_suits_and_minimum_in_unbid_suits():
            bid = Double('0547')
        elif self._is_strong_and_minimum_in_unbid_suits():
            bid = Double('0548')
        elif self._has_fifteen_points_and_minimum_in_openers_suit():
            bid = Double('0549')
        elif self._is_strong_and_opener_bid_one_nt():
            bid = Double('0550')
        elif self.is_balanced:
            bid = self._strong_bid_balanced()
        elif self.hcp >= 16 and self.shape == [4, 4, 4, 1] and self.nt_level <= 2:
            bid = self._strong_bid_4441()
        else:
            bid = self._suit_overcall()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_bid_4441(self):
        """Overcall with strong 4441 hand."""
        if self._two_or_fewer_in_openers_suit():
            bid = Double('0551')
        else:
            bid = self.next_nt_bid('0552')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_bid_balanced(self):
        """Overcall with strong balanced hand."""
        if 20 <= self.hcp <= 22 and self.stoppers_in_bid_suits and self.nt_level <= 2:
            bid = self.nt_bid(2, '0553')
        elif self._has_eighteen_points_and_stoppers_in_bid_suits():
            bid = Double('0554')
        elif self.hcp >= 15 and self.stoppers_in_bid_suits and self.nt_level == 1:
            bid = self.nt_bid(1, '0555')
        elif self._has_sixteen_points_and_shortage_or_opener_bid_one_nt():
            bid = Double('0556')
        else:
            bid = self._suit_overcall()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _suit_overcall(self):
        """Overcall with suit."""
        if self._has_five_card_biddable_suit():
            bid = self._overcall_with_suit()
        else:
            bid = Pass('0557')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_with_suit(self):
        """Return a bid in chosen suit."""
        if self.opener_bid_one.level == 1:
            bid = self._overcalls_at_one_level()
        elif self.opener_bid_one.level == 2:
            bid = self._overcall_after_weak_two()
        elif self.opener_bid_one.level == 3:
            bid = self._overcall_after_weak_three()
        else:
            bid = Pass('0558')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcalls_at_one_level(self):
        """Return  overcall bid after one level opening."""
        suit = self._select_suit()
        if self.hcp >= 16 and self.six_card_suit:
            raise_level = 1
            if self.responder_bid_one.is_value_call:
                raise_level = 0
            bid = self.next_level_bid(suit, '0559', raise_level)
        elif self._can_double():
            bid = Double('0560')
        elif self._has_twelve_points_and_void_in_bid_suits():
            bid = Double('0000')
        elif self.next_level(self._select_suit()) <= 1:
            bid = self._overcall_suit_at_one_level()
        elif self.next_level(self._select_suit()) <= 2:
            bid = self._overcall_suit_at_two_level()
        elif (self.hcp >= 15 and self.longest_suit not in self.opponents_suits and
              (self.next_level(self.longest_suit) <= 2 or
               self.last_bid.name != '2NT')):
            bid = self.next_level_bid(self.longest_suit, '0830')
        else:
            bid = Pass('0562')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_suit_at_one_level(self):
        """Overcall a suit at the 1 level."""
        suit = self._select_suit()
        if self.hcp > 20 and self.is_balanced:
            bid = self._strong_balanced_overcall()
        elif self._has_nine_points_and_some_shape(suit):
            bid = self.suit_bid(1, suit, '0563')
        elif self._can_bid_good_suit_at_one_level(suit):
            bid = self.suit_bid(1, suit, '0564')
        else:
            bid = Pass('0591')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_suit_at_two_level(self):
        """Overcall a suit at the 2 level."""
        suit = self._select_suit()
        suit_points = self.suit_points(suit)
        hand_points = self.hcp + self.distribution_points
        if self._has_strong_seven_card_suit():
            bid = self.suit_bid(3, suit, '0909')
        elif suit_points >= 9 and self.hcp >= 16:
            bid = Double('0565')
        elif self.shape == [5, 4, 4, 0] and self.hcp >= 11 and self.opener_bid_one.name != '1NT':
            bid = Double('0283')
        elif hand_points >= 12 and self.suit_points(self.longest_suit) >= 3:
            bid = self.suit_bid(2, suit, '0566')
        elif hand_points >= 12 and self.five_five_or_better:
            bid = self.suit_bid(2, suit, '0567')
        elif hand_points >= 12 and self.shape[0] >= 6:
            bid = self.suit_bid(2, suit, '0568')
        elif hand_points >= 12 and self.hcp + suit_points >= 17:
            bid = self.suit_bid(2, suit, '0569')
        else:
            bid = self._strong_balanced_overcall()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_after_weak_two(self):
        """Return overcall bids after weak two opening."""
        suit = self._select_suit()
        if self.shape[0]+self.suit_points(suit) >= 9:
            bid = self._overcall_suit_after_weak_two()
        elif self._has_twelve_points_shortage_and_minimum_in_unbid_suits():
            bid = Double('0572')
        else:
            bid = Pass('0570')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_suit_after_weak_two(self):
        """Return overcall suit after weak two opening."""
        suit = self._select_suit()
        if self._can_bid_suit_at_level_two(suit):
            bid = self.suit_bid(2, suit, '0571')
        elif self.hcp >= 16:
            bid = Double('0573')
        elif self.next_level(suit) == 3 and self.hcp >= 12:
            bid = self.suit_bid(3, suit, '0574')
        # elif self._has_thirteen_points_and_can_bid_six_card_suit_at_level_three(suit):
        #     bid = self.next_level_bid(suit, '0575')
        elif self._has_six_card_suit_can_overcall_weak_two():
            bid = self.next_level_bid(self.longest_suit, '0672')
        else:
            bid = Pass('0576')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_after_weak_three(self):
        """Overcall after weak three."""
        if (self.shape == [5, 4, 4, 0] and
                self.suit_length(self.opener_bid_one.denomination) == 0):
            bid = Double('0915')
        elif (self.hcp >= 19 and
                self.suit_length(self.opener_bid_one.denomination) <= 2 and
                self.four_card_major):
            bid = Double('0518')
        elif self._can_rebid_over_weak_three():
            bid = self._overcall_suit_after_weak_three()
        else:
            bid = Pass('0577')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_suit_after_weak_three(self):
        """Return overcall suit after weak three opening."""
        suit = self._select_suit()
        if self._can_bid_nt_with_minor_suit(suit):
            bid = self.nt_bid(3, '0578')
        elif self._has_strong_hand(suit) and self.opponents_at_game:
            bid = Double('0579')
        elif self._has_strong_hand(suit) and self.next_level(suit) <= 4:
            bid = self.next_level_bid(suit, '0580')
        elif self.next_level(suit) <= 3:
            bid = self.suit_bid(3, suit, '0581')
        elif self._can_bid_suit_at_level_four(suit):
            bid = Double('0582')
        else:
            bid = Pass('0583')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_balanced_overcall(self):
        """Overcall with a weak balanced hand."""
        if self._opponents_not_in_fit_at_level_one():
            bid = Double('0584')
        elif self._fffo_and_opener_bids_suit():
            bid = Double('0350')
        elif self._can_double_weak_two():
            bid = Double('0850')
        else:
            bid = Pass('0586')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_balanced_overcall(self):
        """Overcall with a strong balanced hand."""
        if self.is_balanced:
            bid = self._strong_balanced_overcall_make_bid()
        else:
            bid = Pass('0587')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_balanced_overcall_make_bid(self):
        """Overcall with a strong balanced hand."""
        if self._fewer_than_seventeen_points_can_bid_one_nt():
            bid = self.nt_bid(1, '0588')
        elif self._eighteen_plus_points_stoppers_minimum_in_unbid_suits():
            bid = Double('0589')
        elif self.hcp >= 15 and self.shape[0] >= 5:
            bid = self.next_level_bid(self.longest_suit, comment='0590')
        else:
            bid = Pass('0303')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    # Various utility functions

    def _has_strong_hand(self, suit):
        """Return True if hand is strong with good suit."""
        suit_points = self.suit_points(suit)
        return (self.hcp >= 16 and
                self.shape[0] >= 5 and
                suit_points >= 6)

    def _has_minimum_hand(self, suit):
        """Return True if hand is minimum with good suit."""
        suit_points = self.suit_points(suit)
        return ((self.hcp >= 14 and
                 self.shape[0] >= 5 and
                 suit_points >= 6) or
                (self.hcp >= 12 and
                 self.shape[0] >= 6 and
                 suit_points >= 5) or
                (self.hcp >= 11 and
                 self.shape[0] >= 7 and
                 suit_points >= 4))

    def _select_suit(self):
        """Return selected overcall suit."""
        if 5 <= self.shape[0] == self.shape[1]:
            long_suit = self.higher_ranking_suit(self.longest_suit,
                                                 self.second_suit)
        elif self.shape[0] >= 5:
            long_suit = self.longest_suit
        else:
            long_suit = self.longest_suit
        chosen_suit = long_suit
        if long_suit in self.opponents_suits:
            chosen_suit = self._second_five_card_suit(long_suit)
        return chosen_suit

    def _second_five_card_suit(self, long_suit):
        """Select 5 card suit if long suit is opponent's suit."""
        if self.spades >= 5 and long_suit != self.spade_suit:
            suit = self.spade_suit
        elif self.hearts >= 5 and long_suit != self.heart_suit:
            suit = self.heart_suit
        elif self.diamonds >= 5 and long_suit != self.diamond_suit:
            suit = self.diamond_suit
        elif self.clubs >= 5 and long_suit != self.club_suit:
            suit = self.club_suit
        else:
            suit = self.no_trumps
        return suit

    def _minimum_in_unbid_suits(self):
        """
            Return True if hand has the minimum required number of
            cards in each unbid suit.
        """
        value = True
        if not self.overcaller_in_fourth_seat:
            minimum = 3
        elif self.responder_bid_one.is_pass:
            minimum = 3
        else:
            minimum = 4
        bid_suits = [Bid(bid).denomination for bid in self.bid_history[::2]]
        for suit in self.suits:
            if suit not in bid_suits:
                if self.suit_length(suit) <= minimum - 1:
                    value = False
                    break
        # if self.opener_bid_one.denomination.name == 'S':
        #     if self.opener_bid_one.level == 1 and self.suit_length(self.heart_suit) < 4:
        #         value = False
        return value

    def _two_or_fewer_in_openers_suit(self):
        """Return True if hand holds two or fewer in opener's suit."""
        return self._fewer_in_openers_suit(2)

    def _three_or_fewer_in_openers_suit(self):
        """Return True if hand holds three or fewer in opener's suit."""
        return self._fewer_in_openers_suit(3)

    def _fewer_in_openers_suit(self, limit):
        """Return True if hand holds fewer than limit in opener's suit."""
        value = False
        if self.opener_bid_one.is_suit_call:
            if self.suit_length(self.opener_bid_one.denomination) <= limit:
                value = True
        if self.responder_bid_one.is_suit_call:
            value = False
            if self.suit_length(self.responder_bid_one.denomination) <= limit:
                value = True
        return value

    def _three_minimum(self):
        """Return True if hand is void or 3+ cards in each suit."""
        value = True
        for suit_holding in self.shape:
            if 1 <= suit_holding <= 2:
                value = False
                break
        return value

    def _void_in_bid_suits(self):
        """Return True if hand is void in bid suit."""
        value = False
        bid_suits = []
        for bid in self.bid_history[::2]:
            suit = Bid(bid).denomination
            if suit.is_suit:
                bid_suits.append(suit)
        for suit in bid_suits:
            if self.suit_length(suit) == 0:
                value = value and True
            else:
                value = False
        return value

    # Various boolean functions

    def _has_eight_points_and_eight_card_major(self):
        """Return True if pre-emptive 8 card suit."""
        result = (self.shape[0] >= 8 and
                  self.hcp >= 8 and
                  self.longest_suit not in self.opponents_suits and
                  self.next_level(self.longest_suit) <= self.longest_suit.game_level and
                  self.longest_suit.is_major)
        return result

    def _has_eight_points_and_eight_card_minor(self):
        """Return True if zzz."""
        result = (self.shape[0] >= 8 and
                  self.hcp >= 8 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _can_bid_seven_card_suit_over_openers_weak_two(self):
        """Return True if can bid 7 card suit over weak two opening."""
        result = (self.opener_bid_one.level == 2 and
                  self.shape[0] >= 7 and
                  self.hcp >= 12 and
                  self.longest_suit not in self.opponents_suits and
                  self.next_level(self.longest_suit) <= 2)
        return result

    def _can_make_weak_balanced_overcall(self):
        """Return True if can make weak balanced overcall."""
        result = (self.hcp >= 12 and
                  ((self.suit_length(self.opener_bid_one.denomination) <= 2 or
                    self.opener_bid_one.is_nt) or
                   (self.shape == [4, 3, 3, 3] and len(self.bid_history) >= 2)))
        return result

    def _can_bid_six_card_suit_at_two_level(self):
        """Return True if can bid a six card suit at the two level."""
        result = (self.shape[0] >= 6 and
                  self.hcp >= 8 and
                  self.longest_suit.is_major and
                  self.longest_suit not in self.opponents_suits and
                  self.opener_bid_one.level == 1 and
                  self.next_level(self.longest_suit) <= 2)
        return result

    def _very_strong_semi_balanced_with_stoppers(self):
        """Return True if very strong and semi_balanced."""
        result = (self.hcp >= 22 and
                  self.is_semi_balanced and
                  self.has_stopper(self.opener_bid_one.denomination) and
                  self.nt_level <= 3)
        return result

    def _is_strong_and_semi_balanced_with_stoppers_over_weak_two(self):
        """Return True if strong and semi-balanced over weak two."""
        result = (self.hcp >= 16 and
                  self.is_semi_balanced and
                  self.opener_bid_one.level == 2 and
                  self.has_stopper(self.opener_bid_one.denomination) and
                  self.nt_level <= 2)
        return result

    def _is_strong_and_semi_balanced_with_stoppers_over_one_level(self):
        """Return True if zzz."""
        result = (16 <= self.hcp <= 17 and
                  self.is_balanced and
                  self.opener_bid_one.is_suit_call and
                  self.has_stopper(self.opener_bid_one.denomination) and
                  self.nt_level <= 1)
        return result

    def _is_strong_shortage_in_bid_suits_and_minimum_in_unbid_suits(self):
        """Return True if strong and has minimum in unbid suits."""
        result = (self.hcp >= 16 and
                  self._two_or_fewer_in_openers_suit() and
                  self._minimum_in_unbid_suits() and
                  self.responder_bid_one.is_pass and
                  not self.previous_bid.is_game)
        return result

    def _is_strong_and_minimum_in_unbid_suits(self):
        """Return True if strong and minimum in unbid suits."""
        result = (self.hcp >= 16 and self._two_or_fewer_in_openers_suit() and
                  self._minimum_in_unbid_suits() and
                  not self.previous_bid.is_game)
        return result

    def _has_fifteen_points_and_minimum_in_openers_suit(self):
        """Return True if 15 points and fewer than 2 in openers suit."""
        result = (self.hcp >= 15 and
                  self._two_or_fewer_in_openers_suit() and
                  self._minimum_in_unbid_suits() and
                  not self.previous_bid.is_game and
                  self.next_level(self.longest_suit) > 1 and
                  not (self.shape[0] >= 5 and
                       self.suit_points(self.longest_suit) >= 4))
        return result

    def _is_strong_and_opener_bid_one_nt(self):
        """Return True if 16 points and opener has bid 1NT."""
        result = (self.hcp >= 16 and
                  self.opener_bid_one.name == '1NT' and
                  not self.responder_bid_one.is_value_call)
        return result

    def _has_eighteen_points_and_stoppers_in_bid_suits(self):
        """Return True if 18/19 points and stoppers in bid suits."""
        result = (18 <= self.hcp <= 19 and
                  self.stoppers_in_bid_suits and
                  self.longest_suit not in self.opponents_suits and
                  self.nt_level <= 2)
        return result

    def _has_sixteen_points_and_shortage_or_opener_bid_one_nt(self):
        """Return True if zzz."""
        result = (self.hcp >= 16 and
                  (self._three_or_fewer_in_openers_suit() or
                   self.opener_bid_one.is_nt))
        return result

    def _has_five_card_biddable_suit(self):
        """Return True if has 5 card biddable suit."""
        chosen_suit = self._select_suit()
        result = (chosen_suit.is_suit and
                  self.suit_length(chosen_suit) >= 5 and
                  chosen_suit not in self.opponents_suits)
        return result

    def _has_twelve_points_and_void_in_bid_suits(self):
        """Return True if 23 points and void in bid suits and minimum in bid suits."""
        result = (self.hcp >= 12 and
                  self._void_in_bid_suits() and
                  self._three_minimum() and
                  not self.five_five and
                  not self.shape[0] >= 6 and
                  self.nt_level <= 3)
        return result

    def _has_nine_points_and_some_shape(self, suit):
        """Return True if 9/10 points and shapely."""
        hand_points = self.hcp + self.distribution_points
        result = (9 <= hand_points <= 10 and
                  self.suit_points(suit) >= 6 and
                  self.next_level(suit) == 1 or
                  self.five_five or
                  (self.shape[0] >= 6 and
                   self.shape[0]+self.suit_points(suit) >= 9))
        return result

    def _can_bid_good_suit_at_one_level(self, suit):
        """Return True if can bid a strong suit at one level."""
        hand_points = self.hcp + self.distribution_points
        result = (hand_points >= 11 and
                  self.next_level(suit) == 1 and
                  (self.suit_points(suit) >= 1 or
                   (self.suit_points(suit) >= 1 and self.has_sequence(suit))))
        return result

    def _has_strong_seven_card_suit(self):
        """Return True if has strong 7 card suit."""
        result = (self.hcp + self.distribution_points >= 13 and
                  self.shape[0] >= 7 and
                  self.suit_points(self.longest_suit) == 10)
        return result

    def _can_bid_suit_at_level_two(self, suit):
        """Return True if 12 points or seven card suit and level <= 2."""
        result = (self.next_level(suit) <= 2 and
                  (self.shape[0] >= 7 or
                   (self.shape[0] >= 6 and self.hcp >= 11) or
                   (self.shape[0] == 5 and self.hcp >= 12)))
        return result

    def _has_twelve_points_shortage_and_minimum_in_unbid_suits(self):
        """Return True if 12 points shortage and minimum in unbid suits."""
        result = (self.hcp >= 12 and
                  self.suit_length(self.opener_bid_one.denomination) <= 2 and
                  # self._minimum_in_unbid_suits() and
                  (self.shape == [4, 4, 3, 2] or
                   self.shape == [5, 4, 3, 1]))
        return result

    # def _has_thirteen_points_and_can_bid_six_card_suit_at_level_three(self, suit):
    #     """Return True if 13 points and can bid 6 card suit at 3 level."""
    #     result = (self.hcp >= 13 and
    #               self.shape[0] >= 6 and
    #               self.next_level(suit) <= 3)
    #     return result

    def _can_rebid_over_weak_three(self):
        """Return True if hand suitable for overcalling a weak 3."""
        suit = self._select_suit()
        result = self._has_strong_hand(suit) or self._has_minimum_hand(suit)
        return result

    def _can_bid_nt_with_minor_suit(self, suit):
        """Return True if suit is minor can bid NT."""
        result = (suit.is_minor and
                  self.suit_points(suit) >= 9 and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _can_bid_suit_at_level_four(self, suit):
        """Return True if can bid suit ay level 4."""
        result = (self.suit_length(self.opener_bid_one.denomination) <= 2 and
                  self._minimum_in_unbid_suits() and
                  self.next_level(suit) <= 4)
        return result

    def _opponents_not_in_fit_at_level_one(self):
        """Return True if opponents bid different suits at level 1."""
        result = (self.opener_bid_one.level <= 1 and
                  self._minimum_in_unbid_suits() and
                  self.responder_bid_one.level <= 1 and
                  self.opener_bid_one.is_suit_call and
                  not self.responder_bid_one.is_nt and
                  not self.opponents_at_game)
        return result

    def _fffo_and_opener_bids_suit(self):
        """Return True if strong or 4441."""
        result = (self.four_four_four_one and
                  self.opener_bid_one.is_suit_call and
                  not self.opponents_at_game)
        return result

    def _fewer_than_seventeen_points_can_bid_one_nt(self):
        """Return True if fewer then 17 points stopper and nt_level 1."""
        result = (15 <= self.hcp <= 17 and
                  self.stoppers_in_bid_suits and
                  self.nt_level == 1)
        return result

    def _eighteen_plus_points_stoppers_minimum_in_unbid_suits(self):
        """Return True if 18+ points, stoppers and minimum in bid suits."""
        result = (self.hcp >= 18 and
                  self.stoppers_in_bid_suits and
                  self._minimum_in_unbid_suits())
        return result

    def _can_double_in_pass_out_seat(self):
        """Return True if can double in the pass out seat."""
        result = (len(self.bid_history) == 3 and
                  self.hcp >= 11 and
                  self.four_four_four_one and
                  self.suit_length(self.opener_bid_one.denomination) == 1)
        return result

    def _has_six_card_suit_can_overcall_weak_two(self):
        """Return True if can overcall weak two."""
        result = (self.hcp >= 10 and
                  # self.suit_points(self.opener_bid_one.denomination) >= 7 and
                  self.shape[0] >= 6 and
                  self.suit_points(self.longest_suit) >= 3 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _can_double(self):
        """Return True if double is allowed."""
        can_double = False
        if len(self.bid_history) == 1:
            can_double = True
        elif (len(self.bid_history) == 3 and
                self.responder_bid_one.is_value_call and
                self.opener_bid_one.denomination == self.responder_bid_one.denomination):
            can_double = True

        result = ((self.hcp >= 16 or (self.hcp >= 15 and self.shape[0] >= 7)) and can_double)
        return result

    def _can_double_weak_two(self):
        """Return True if can double a weak two."""
        result = (self.hcp >= 12 and
                  self.shape[2] >= 3 and
                  self.suit_length(self.opener_bid_one.denomination) <= 2 and
                  self.opener_bid_one.level ==2 and
                  self.opener_bid_one.denomination.name != 'S')
        return result

    # def xxx(self):
    #     """Return True if zzz."""
    #     result = False
    #     return result

    # def xxx(self):
    #     """Return True if zzz."""
    #     result = False
    #     return result
