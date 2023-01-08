""" Bid for Game
    Responder's Bid class
"""
import inspect
from .bridge_tools import Bid, Pass, Double, HandSuit
from .hand import Hand
from bridgeobjects import Suit


class RespondersBid(Hand):
    """Responder's bid class."""

    def __init__(self, hand_cards, board):
        super(RespondersBid, self).__init__(hand_cards, board)
        self.trace = 0

    def suggested_bid(self):
        """Direct control to relevant method and return a Bid object."""
        if self.overcaller_bid_one.level >= 4:
            bid = Pass('0036')
        elif self.opener_bid_one.is_nt:
            bid = self._respond_to_nt()
        elif self.opener_bid_one.level == 1:
            bid = self._respond_to_one_suit()
        elif self.opener_bid_one.name == '2C':
            bid = self._respond_to_two_clubs()
        elif self.opener_bid_one.level == 2:
            bid = self._respond_to_weak_two()
        elif self.opener_bid_one.level == 3:
            bid = self._respond_to_weak_three()
        else:
            bid = Pass('0037')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_nt(self):
        """Return responses to 1NT or 2NT."""
        if self.opener_bid_one.level == 1:
            bid = self._respond_to_one_nt()
        elif self.opener_bid_one.level == 2:
            bid = self._respond_to_two_nt()
        else:
            bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_one_nt(self):
        """Respond to 1NT."""
        if self.overcaller_bid_one.is_value_call:
            bid = self._one_nt_with_overcall()
        elif self.hcp <= 10:
            bid = self._weak_take_out()
        else:
            bid = self._one_nt_test_invite()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _one_nt_with_overcall(self):
        """Return bid after 1NT and overcall."""
        if self._six_card_major_thirteen_points():
            bid = self.suit_bid(4, self.longest_suit, '0185')
        elif self._can_bid_after_one_nt_with_overcall():
            bid = self._trial_bid_suit_after_one_nt_with_overcall()
        elif self._is_semi_balanced_eleven_plus():
            bid = self._try_nt_after_one_nt_with_overcall()
        elif self._is_balanced_game_going() and self.five_card_major:
            bid = self.suit_bid(3, self.longest_suit, '0590')
        elif self._is_balanced_game_going():
            bid = self.nt_bid(3, '0196')
        elif self._is_game_going():
            bid = self.next_level_bid(self.longest_suit, '0128')
        elif self.shape[0] >= 6 and self.hcp >= 10 and self.longest_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.longest_suit, '0791')
        else:
            bid = Pass('0038')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _try_nt_after_one_nt_with_overcall(self):
        """Try a NT after 1NT and overcall."""
        if self.hcp >= 13:
            level = 3
        else:
            level = 2
        if level >= self.nt_level:
            bid = self.nt_bid(level, '0041')
        else:
            bid = Pass('0042')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_take_out(self):
        """Return bid for weak-takeout."""
        if self.shape[0] >= 5:
            bid = self._weak_take_out_bid()
        else:
            bid = Pass('0043')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_take_out_bid(self):
        """Return bid for weak-takeout."""
        suit = self.long_suit(5)
        if self.overcaller_bid_one.is_double:
            bid = self.suit_bid(2, suit, '0044')
        elif (self.shape[0] >= 6 and self.shape[1] >= 5 and self.hcp >= 10
              and self.longest_suit.is_major):
            bid = self.suit_bid(4, self.longest_suit, '0649')
        elif suit != self.club_suit:
            bid = self.suit_bid(2, suit, '0045')
        else:
            bid = Pass('0046')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _one_nt_test_invite(self):
        """Bid with four card major."""
        if 11 <= self.hcp <= 12:
            bid = self._one_nt_test_invite_weak()
        elif self.hcp >= 13:
            bid = self._respond_to_one_nt_strong()
        else:
            bid = Pass('0047')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _one_nt_test_invite_weak(self):
        if self.shape[0] >= 6:
            bid = self._respond_to_one_nt_strong()
        elif self.four_card_major:
            bid = self._one_nt_weak_stayman()
        elif self.nt_level <= 2:
            bid = self.nt_bid(2, '0048')
        else:
            bid = Pass('0049')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _one_nt_weak_stayman(self):
        if self.overcall_made:
            bid = self._one_nt_weak_overcall()
        else:
            bid = self.club_bid(2, '0050')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _one_nt_weak_overcall(self):
        """Return bid after overcall."""
        if self.overcaller_bid_one.is_double and self.hcp >= 10:
            bid = Pass('0051')
        elif self.stoppers_in_bid_suits and self.nt_level <= 2:
            bid = self.nt_bid(2, '0052')
        else:
            bid = Pass('0053')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_one_nt_strong(self):
        """Bid after 1NT strong."""
        if self._four_card_major_after_one_nt():
            bid = self._four_card_major_after_one_nt()
        elif self.shape[0] >= 6:
            bid = self.suit_bid(3, self.longest_suit, '0309')
        else:
            bid = self._strong_nt()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _four_card_major_after_one_nt(self):
        """Bid after 1NT, four card major."""
        if self.spades >= 6:
            bid = self.spade_bid(4, '0054')
        elif self.hearts >= 6:
            bid = self.heart_bid(4, '0055')
        elif self.spades >= 5:
            bid = self.spade_bid(3, '0056')
        elif self.hearts >= 5:
            bid = self.heart_bid(3, '0057')
        elif (not self.overcall_made and
              self.hcp <= 18 and
              self.four_card_major):
            bid = self.club_bid(2, '0058')  # Stayman
        else:
            bid = None
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_nt(self):
        """Bid after 1NT, no four card major."""
        if self.hcp <= 18:
            bid = self.nt_bid(3, '0059')
        elif 19 <= self.hcp <= 20:
            bid = self.nt_bid(4, '0060')
        elif 21 <= self.hcp <= 22:
            bid = self.nt_bid(6, '0061')
        elif 23 <= self.hcp <= 24:
            bid = self.nt_bid(5, '0062')
        else:  # elif self.hcp >= 25:
            bid = self.nt_bid(7, '0063')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_two_nt(self):
        """Responses to 2NT."""
        if self.hcp <= 3:
            bid = Pass('0064')
        elif (self.spades >= 5 and
              self.hearts >= 5 and
              self.shape[0] == self.shape[1] and
              self.bid_history[-1] == 'P'):
            bid = self.next_level_bid(self.spade_suit, '0682')
        elif (self.spades >= 4 and
              self.hearts >= 4 and
              self.shape[1] <= 4 and
              self.bid_history[-1] == 'P' and
              self.next_level(self.club_suit) <= 3):
            bid = self.club_bid(3, '0872')
        elif self.spades >= 6 and self.next_level(self.spade_suit) <= 4:
            bid = self.spade_bid(4, '0068')
        elif self.hearts >= 6 and self.next_level(self.heart_suit) <= 4:
            bid = self.heart_bid(4, '0068')
        elif self.spades >= 5 and self.next_level(self.spade_suit) <= 3:
            bid = self.spade_bid(3, '0068')
        elif self.hearts >= 5 and self.next_level(self.heart_suit) <= 3:
            bid = self.heart_bid(3, '0068')
        elif ((self.spades >= 4 or self.hearts >= 4) and
              self.next_level(self.club_suit) <= 3):
            bid = self.club_bid(3, '0069')
        elif 11 <= self.hcp <= 12 and self.nt_level <= 4:
            bid = self.nt_bid(4, '0070')
        elif 13 <= self.hcp <= 14 and self.nt_level <= 6:
            bid = self.nt_bid(6, '0071')
        elif 15 <= self.hcp <= 16 and self.nt_level <= 5:
            bid = self.nt_bid(5, '0072')
        elif self.hcp >= 17 and self.nt_level <= 7:
            bid = self.nt_bid(7, '0073')
        elif self.nt_level <= 3:  #  self.hcp >= 4:
            bid = self.nt_bid(3, '0074')
        else:
            bid = Double('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_one_suit(self):
        """Respond to one of suit."""
        if self.opener_bid_one.denomination.is_minor:
            bid = self._minor_opening_check_major()
        else:
            bid = self._minor_opening_check_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _minor_opening_check_major(self):
        """Respond after one of minor with four card major."""
        if self.four_card_major:
            bid = self._respond_to_one_suit_no_support()
            if bid.is_pass:
                bid = self._minor_opening_check_support()
        else:
            bid = self._respond_to_minor()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _minor_opening_check_support(self):
        """Respond after one of minor, check support."""
        if self.suit_length(self.opener_bid_one.denomination) >= 4:
            bid = self._respond_to_one_suit_with_support()
        else:
            bid = self._respond_to_one_suit_no_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_minor(self):
        """Return bid after opener has bid minor suit."""
        hand_value_points = self.support_points(self.opener_bid_one.denomination)
        if hand_value_points <= 9:
            minor_level = 2
        elif hand_value_points <= 10:
            minor_level = 3
        elif hand_value_points <= 13:
            minor_level = 4
        else:
            minor_level = 5
        if hand_value_points <= 4:
            bid = Pass('0075')
        elif (self.hcp >= 16 and
              self.second_suit == self.opener_bid_one.denomination and
              self.longest_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.longest_suit, '0781', raise_level=1)
        elif self._is_five_four_game_going():
            bid = self.next_level_bid(self.second_suit, '0076', raise_level=1)
        elif self._is_balanced_with_no_long_minor():
            bid = self._nt_response_to_minor()
        elif self._has_six_card_unbid_suit():
            if self.hcp >= 16:
                raise_level = 1
            else:
                raise_level = 0
            bid = self.next_level_bid(self.longest_suit, '0077', raise_level)
        elif self._is_semi_balanced_some_support():
            bid = self.nt_bid(2, '0078')
        elif self.opener_bid_one.denomination == self.club_suit and minor_level > 0:
            bid = self._respond_to_clubs(minor_level)
        elif self.opener_bid_one.denomination == self.diamond_suit and minor_level > 0:
            bid = self._response_to_diamonds(minor_level)
        else:
            bid = self._respond_to_one_suit_no_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _nt_response_to_minor(self):
        """Bid NT in response to minor opening."""
        if self.hcp >= 16 and self.longest_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.longest_suit, '0000', raise_level=1)
        elif self.hcp >= 13 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0079')
        elif self.hcp >= 10 and self.nt_level <= 2:
            bid = self.nt_bid(2, '0080')
        elif self.hcp >= 6 and self.nt_level <= 1:
            bid = self.nt_bid(1, '0081')
        else:
            bid = Pass('0082')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_clubs(self, level):
        """Respond after club opening."""
        club_level = self.next_level(self.club_suit)
        hand_value_points = self.support_points(self.opener_bid_one.denomination)
        if level > 3 and self.hcp >= 13 and self.nt_level <= 3 and self.shape[1] <= 4:
            bid = self.nt_bid(3, '0083')
        elif self._has_five_card_club_support_and_ten_points():
            if self.hcp >= 15:
                level = 5
            elif self.hcp >= 12:
                level = 4
            else:
                level = 3
            bid = self.suit_bid(level, self.club_suit, '0249')
        elif self._has_five_card_suit_and_ten_points():
            bid = self.next_level_bid(self.longest_suit, '0084')
        elif (self.clubs >= 4 and
              hand_value_points >= 5 and
              club_level <= level):
            bid = self.club_bid(level, '0085', True)
        elif self.diamonds >= 5:
            bid = self._respond_to_clubs_with_diamonds()
        elif self.clubs >= 4:
            bid = self._respond_to_one_suit_with_support()
        else:
            bid = self._respond_to_one_suit_no_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_clubs_with_diamonds(self):
        """Respond after club opening with diamonds."""
        if self.diamond_suit in self.opponents_suits:
            bid = Pass('0522')
        elif self.hcp + self.shape[0] >= 16:
            bid = self.next_level_bid(self.diamond_suit, '0086')
        elif self._can_rebid_diamonds_at_next_level():
            bid = self.next_level_bid(self.diamond_suit, '0087')
        else:
            bid = Pass('0088')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _response_to_diamonds(self, level):
        """Respond after diamond opening."""
        club_level = self.next_level(self.club_suit)
        diamond_level = self.next_level(self.diamond_suit)
        hand_value_points = self.support_points(self.opener_bid_one.denomination)
        if 6 <= self.hcp <= 9 and self.is_balanced and self.stoppers_in_bid_suits and self.nt_level == 1:
            bid = self.nt_bid(1, '0312')
        elif self.is_balanced and 10 <= hand_value_points <= 12:
            bid = self.diamond_bid(3, '0764', True)
        elif self.diamonds >= 4 and 10 <= hand_value_points <= 14:
            level = max(level, diamond_level)
            bid = self.diamond_bid(level, '0089', True)
        elif self.clubs >= 5 and hand_value_points >= 9 and club_level <= 2:
            level = 2
            if self.hcp >= 16:
                level = 3
            bid = self.club_bid(level, '0090', True)
        elif self.diamonds >= 4:
            bid = self._respond_to_one_suit_with_support()
        else:
            bid = self._respond_to_one_suit_no_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_one_suit_with_support(self):
        """Respond with support for opener."""
        suit = self.opener_bid_one.denomination
        level = self.next_level(suit)
        hand_value_points = (self.hcp
                             + self.support_shape_points(suit)
                             + self.suit_length(suit) - 4)
        if hand_value_points < 6:
            bid = Pass('0091', True)
        elif (6 <= hand_value_points <= 9 and
              level <= self.opener_bid_one.level + 1):
            bid = self.suit_bid(level, suit, '0092', True)
        elif (10 <= hand_value_points <= 11 and
              level <= self.opener_bid_one.level + 2):
            bid = self.suit_bid(level + 1, suit, '0093', True)
        elif 12 <= hand_value_points <= 15 and level <= self.opener_bid_one.level + 3:
            if self.suit_length(suit) >= 5 and self.hcp >= 11:
                level += (self.suit_length(suit) - 4)
            if 10 <= self.hcp <= 11:
                level -= 1
            level = min(2, level)
            bid = self.suit_bid(level + 2, suit, '0094', True)
        elif suit.is_major and hand_value_points >= 18:
            bid = self.nt_bid(4, '0095', True)  # Blackwood
        elif self.hcp >= 16 and suit.is_minor:
            bid = self.suit_bid(6, suit, '0339')
        elif self.hcp >= 16 and self.shape[1] >= 4 and self.longest_suit not in self.opponents_suits:
            if suit == self.longest_suit and self.second_suit not in self.opponents_suits:
                suit = self.second_suit
            else:
                suit = self.longest_suit
            bid = self.next_level_bid(suit, '0479', raise_level=1)
        elif hand_value_points >= 13:
            bid = self.bid_to_game(suit, '0096')
        else:
            bid = Pass('0097', True)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_one_suit_no_support(self):
        """Respond to opening suit bid with no support."""
        own_suit = self._suit_for_response_no_support()
        response_level = self._level_for_response(own_suit)
        if own_suit == self.no_trumps:
            bid = self._no_support_bid_nt()
        elif self.hcp >= 16:
            bid = self._no_support_strong(own_suit, response_level)
        elif 9 <= self.hcp <= 15:
            bid = self._no_support_intermediate(response_level, own_suit, '0098')
        elif 6 <= self.hcp <= 8:
            bid = self._no_support_weak(response_level, own_suit)
        elif self.hcp == 5 and response_level == 1 and self.shape[0] >= 5:
            bid = self.suit_bid(1, own_suit, '0099')
        else:  # elif self.hcp <= 5:
            bid = Pass('0100')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_bid_nt(self):
        """Respond to opening suit bid with no support, nt."""
        if self.hcp >= 8:
            stoppers = self.four_in_bid_suits()
        else:
            stoppers = self.stoppers_in_bid_suits
        poor_stoppers = self.poor_stoppers_in_bid_suits
        hold_opponents_suit = False
        if (self.overcaller_bid_one.is_suit_call and
                self.suit_length(self.overcaller_bid_one.denomination) >= 5):
            hold_opponents_suit = True
        if self.hcp <= 9 and hold_opponents_suit:
            bid = Pass('0101')
        elif stoppers or (self.shape[0] == 4 and poor_stoppers):
            bid = self._bid_nt_stoppers()
        else:
            bid = Pass('0102')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _bid_nt_stoppers(self):
        """Return NT bid with stoppers."""
        if self.nt_level <= 3 and self.hcp >= 13:
            bid = self.nt_bid(3, '0103')
        elif self.nt_level <= 2 and self.hcp >= 10:
            bid = self.nt_bid(2, '0104')
        elif self.nt_level == 1 and self.hcp >= 6:
            bid = self.nt_bid(1, '0105')
        else:
            bid = Pass('0106')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_strong(self, own_suit, response_level):
        """Respond to opening suit bid with no support, strong."""
        level = self._get_level__no_support_strong(own_suit, response_level)
        bid = self.suit_bid(level, own_suit, '0107')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_intermediate(self, response_level, own_suit, comment=''):
        """Return bid with no support for opener's suit, intermediate."""
        trial_bid = self._no_support_intermediate_trial_bid(response_level, own_suit, comment)
        if (self.opener_bid_one.name == '1S' and
                trial_bid.name == '2H' and self.hearts < 5):
            bid = self._no_support_intermediate_after_spade()
        elif self._has_five_card_major_and_game_going():
            bid = self.next_level_bid(self.five_card_major_suit, '0098')
        elif self._is_balanced_and_strong():
            bid = self.nt_bid(3, '0136')
        elif self._is_game_going_support_for_partners_minor(response_level):
            bid = Double('0408')
        elif (self._has_four_card_major_and_game_going(response_level) and
              self.longest_suit == self.opener_bid_one.denomination):
            suit = self.next_four_card_suit()
            bid = self.next_level_bid(suit, '0108')
        elif self._has_overcall_but_no_support(own_suit):
            if self.hcp >= 14:
                level = 3
            else:
                level = 2
            bid = self.nt_bid(level, '0109')
        else:
            bid = self._no_support_intermediate_not_spade(own_suit, trial_bid)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_intermediate_trial_bid(self, level, own_suit, comment):
        """Return trial bid with no support, intermediate."""
        if level == 1 and not comment:
            comment = '0110'
        elif own_suit == self.opener_bid_one.denomination:
            comment = '0093'
        else:
            comment = '0111'
        bid = self.suit_bid(level, own_suit, comment)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_intermediate_after_spade(self):
        """Return bid with no support for opener's spade."""
        if self._has_good_diamonds():
            bid = self.diamond_bid(2, '0112')
        elif self._has_good_clubs():
            bid = self.club_bid(2, '0113')
        else:
            hcp = self.hcp
            level = self.quantitative_raise(hcp, 0, [0, 10, 13], 3)
            if level >= self.nt_level:
                bid = self.nt_bid(level, '0114')
            else:
                bid = Pass('0115')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_intermediate_not_spade(self, own_suit, trial_bid):
        """Return bid with no support for opener's suit, intermediate."""
        if own_suit == self.spade_suit and self.hcp >= 10:
            bid = trial_bid
            bid.comment = '0116'
        elif own_suit.is_minor and self.is_balanced and self.hcp == 9:
            bid = self._no_support_intermediate_minor_balanced()
        elif self._is_semi_balanced_no_support(own_suit) and self.hcp <= 12:
            bid = self._no_support_intermediate_minor_balanced_overcall()
        elif self._four_four_one_stoppers():
            bid = self._singleton_in_openers_suit(trial_bid)
        elif self._has_singleton_in_openers_suit_and_stoppers(own_suit):
            bid = self.nt_bid(2, '0117')
        elif self._has_no_support_and_no_long_suit(own_suit, trial_bid):
            if self.hcp >= 13:
                level = 3
                comment = '0161'
            else:
                comment = '0118'
                level = 2
            bid = self.nt_bid(level, comment)
        elif self._forced_to_jump_bid(own_suit, trial_bid):
            bid = Pass('0119')
        else:
            bid = trial_bid
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _singleton_in_openers_suit(self, trial_bid):
        """Return bid if holding a singleton in openers suit."""
        if self.nt_level == 2:
            if self.overcaller_bid_one.is_nt:
                if self.hcp >= 10:
                    bid = self.nt_bid(2, '0120')
                else:
                    bid = Pass('0121')
            else:
                bid = self.nt_bid(2, '0122')
        else:
            bid = trial_bid
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_intermediate_minor_balanced(self):
        """Return bid with no support balanced but minor suit."""
        if self.nt_level == 1 and self.stoppers_in_bid_suits:
            if self.shape[1] == 4 and self.next_level(self.longest_suit) == 1:
                bid = self.next_level_bid(self.longest_suit, '0123')
            else:
                bid = self.nt_bid(1, '0124')
        else:
            bid = Pass('0125')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_intermediate_minor_balanced_overcall(self):
        """Return bid with no support balanced, overcall, minor suit."""
        if (self.overcaller_bid_one.name == '1NT' and
                self.hcp >= 10):
            bid = Double('0126')
        else:
            if self.hcp >= 13:
                level = 3
            elif self.hcp >= 10:
                level = 2
            else:
                level = self.nt_level
            if level >= self.nt_level:
                bid = self.nt_bid(level, '0127')
            else:
                bid = Pass('0128')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_weak(self, response_level, own_suit):
        """Respond to opening suit bid with no support, weak."""
        if response_level == 1:
            bid = self._no_support_weak_level_one(response_level, own_suit)
        else:
            bid = self._no_support_weak_over_level_one(own_suit)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_weak_level_one(self, level, own_suit):
        """Respond to bid with no support at level one, weak."""
        if self.next_level(own_suit) == 1:
            bid = self.suit_bid(level, own_suit, '0129')
        else:
            suit = self.second_suit
            level = self.next_level(suit)
            bid = self.suit_bid(level, suit, '0130')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_weak_over_level_one(self, own_suit):
        """Respond to bid with no support above level one, weak."""
        major = self.four_card_major_suit
        if major and self.next_level(major) == 1:
            bid = self.next_level_bid(major, '0131')
        elif (not self.overcaller_bid_one.is_pass and
              not self.overcaller_bid_one.is_double):
            bid = self._no_support_weak_over_level_one_overcall()
        elif own_suit.is_minor:
            bid = self._no_support_weak_over_level_one_minor()
        else:
            bid = self.nt_bid(1, '0132')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_weak_over_level_one_overcall(self):
        """Respond to bid with no support above level one, overcall."""
        stopper = False
        if not self.overcaller_bid_one.is_nt:
            stopper = self.has_stopper(self.overcaller_bid_one.denomination)
        if stopper and self.nt_level <= 1:
            bid = self.nt_bid(1, '0133')
        elif (self.shape[0] >= 7 and
              self.hcp >= 8 and
              self.longest_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.longest_suit, '0134')
        else:
            bid = Pass('0135')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_weak_over_level_one_minor(self):
        """Respond to bid with no support above level one, minor."""
        if (self.hearts >= 4 and
                self.next_level(self.heart_suit) == 1):
            bid = self.heart_bid(1, '0136')
        elif (self.spades >= 4 and
              self.next_level(self.spade_suit) == 1):
            bid = self.spade_bid(1, '0137')
        elif self.shape[0] >= 8 and self.hcp >= 8 and self.next_level(self.longest_suit) <= 2:
            bid = self.next_level_bid(self.longest_suit, '0783')
        else:
            bid = self.nt_bid(1, '0138')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_two_clubs(self):
        """Rebid after 2C opening."""
        suit = self._get_suit_after_two_clubs_opening()
        quality = HandSuit(suit, self).suit_quality()
        suit_length = self.suit_length(self.longest_suit)
        if ((self.hcp > 7 or
             (self.hcp == 7 and
              quality >= 2)) and suit_length >= 5):
            bid = self._suit_response_after_two_clubs(suit)
        elif self.is_balanced and self.hcp > 7:
            bid = self.nt_bid(2, '0139')
        elif (self.diamond_suit not in self.opponents_suits and
              self.next_level(self.diamond_suit) <= 2):
            bid = self.diamond_bid(2, '0140')
        else:
            bid = Pass('0254')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _suit_response_after_two_clubs(self, own_suit):
        """Make suit response after 2C."""
        if own_suit == self.spade_suit:
            bid = self.spade_bid(2, '0141')
        elif own_suit == self.heart_suit:
            bid = self.heart_bid(2, '0142')
        elif own_suit == self.diamond_suit:
            bid = self.diamond_bid(3, '0143')
        else:  # elif own_suit == self.club_suit:
            bid = self.club_bid(3, '0144')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_weak_two(self):
        """Respond to weak two."""
        openers_suit = self.opener_bid_one.denomination
        hand_value_points = (self.hcp +
                             self.support_shape_points(openers_suit))
        if self.hcp <= 10:
            bid = self._respond_to_weak_two_weak()
        elif self.overcaller_bid_one.is_double:
            bid = Pass('0145')
        elif self._support_after_suit_overcall_game_going():
            level = self.next_level(openers_suit)
            bid = self.suit_bid(level, openers_suit, '0146', True)
        elif hand_value_points >= 16:
            bid = self._respond_to_weak_two_strong()
        elif self._has_singleton_in_openers_suit_and_own_six_card_suit():
            bid = self.next_level_bid(self.longest_suit, '0147')
        else:
            bid = Pass('0148')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_weak_two_weak(self):
        """Respond to weak two if weak."""
        openers_suit = self.opener_bid_one.denomination
        level = self.next_level(openers_suit)
        if self.suit_length(openers_suit) >= 4 and level <= 4:
            bid = self.suit_bid(4, openers_suit, '0149')
        elif self.suit_length(openers_suit) >= 3 and level <= 3:
            bid = self.suit_bid(3, openers_suit, '0150')
        else:
            bid = Pass('0151')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_weak_two_strong(self):
        """Respond to weak two if strong."""
        if self._has_two_card_support_for_major():
            bid = self.suit_bid(4, self.opener_bid_one.denomination, '0152', True)
        elif self.hcp >= 16 and self._shape[0] >=8 and self.longest_suit.is_major:
            bid = self.bid_to_game(self.longest_suit, '0427')
        elif self._has_own_suit():
            bid = self.next_level_bid(self.longest_suit, '0153')
        elif self.hcp >= 23 and self.suit_length(self.opener_bid_one.denomination) >= 2 and self.is_balanced:
            bid = self.nt_bid(3, '0905')
        elif self.hcp >= 23 and self.suit_length(self.opener_bid_one.denomination) >= 2:
            bid = self.suit_bid(6, self.opener_bid_one.denomination, '0622')
        elif (self.hcp >=15 and
                self.shape[1] >= 5 and
                self.longest_suit.is_major and
                self.second_suit.is_major and
                self.longest_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.longest_suit, '0921')
        else:
            if self.nt_level <= 3:
                bid = self.nt_bid(3, '0154')
            else:
                bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_weak_three(self):
        """Respond to weak three."""
        if self.hcp >= 15:
            bid = self._respond_to_weak_three_strong()
        elif (self.hcp <= 9 and
              self.suit_length(self.opener_bid_one.denomination) >= 2):
            bid = self.suit_bid(4, self.opener_bid_one.denomination, '0155')
        else:
            bid = Pass('0156')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_to_weak_three_strong(self):
        """Respond to weak three, strong."""
        if self._two_card_support_for_major_fifteen_points():
            bid = self.suit_bid(4, self.opener_bid_one.denomination, '0157')
        elif self.is_balanced and self.nt_level <= 3:
            bid = self.nt_bid(3, '0158')
        elif (self.opener_bid_one.denomination.is_major and
              self.suit_length(self.opener_bid_one.denomination) >= 1):
            bid = self.suit_bid(4, self.opener_bid_one.denomination, '0159')
        elif self._can_bid_six_card_suit_at_level_three():
            bid = self.next_level_bid(self.longest_suit, '0832')
        elif self.nt_level <= 3:
            bid = self.nt_bid(3, '0160')
        else:
            bid = Pass('0161')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    # Various utility functions

    def _get_suit_after_two_clubs_opening(self):
        """Determine best suit after 2C opening."""
        if self.five_five:
            if self.longest_suit < self.second_suit:
                suit = self.second_suit
            else:
                suit = self.longest_suit
        else:
            suit = self.longest_suit
        return suit

    def _get_one_nt_jump_level(self):
        """Return jump level for response after 1NT with overcall."""
        if self.hcp >= 12:
            jump_level = 1
        else:
            jump_level = 0
        return jump_level

    def _level_for_response(self, own_suit):
        """Return level for no support bid."""
        level = self.next_level(own_suit)
        if self._has_overcall_ten_points_shortage(own_suit):
            level += 1
        elif self._has_support_nine_points_shortage(own_suit):
            level += 1
        return level

    def _get_level__no_support_strong(self, own_suit, level):
        """Return level for strong bid with no support."""
        if self.longest_suit.is_major and self.shape[0] >= 6:
            level += 2
        else:
            level += 1
        jump_level = self.next_level(own_suit) + 1
        level = min(level, jump_level)
        return level

    def _suit_for_response_no_support(self):
        """Return suit for responder when no support for opener."""
        if self.five_five_or_better:
            next_suit = self._higher_five_card_suit()
        else:
            next_suit = self._cheapest_four_card_suit(self.opener_bid_one.denomination)
        suit = self.longest_suit
        if suit in self.opponents_suits:
            suit = self.second_suit
        if self.suit_length(suit) == 4:
            for bid in self.bid_history[::-1]:
                if Bid(bid).is_value_call:
                    suit = self._cheapest_four_card_suit(Bid(bid).denomination)
                    break
        if self.suit_length(suit) < 4:
            suit = self.no_trumps
        elif suit == self.overcaller_bid_one.denomination:
            suit = self.no_trumps
        elif (self.hcp >= 16 and
              self.longest_suit == self.opener_bid_one.denomination and
              self.shape[1] == 4 and
              next_suit and
              next_suit not in self.opponents_suits):
            suit = next_suit
        return suit

    def _cheapest_four_card_suit(self, bid_suit):
        """Return cheapest 4 card suit after given suit."""
        loop = 0
        rank = bid_suit.rank
        while True:
            rank = (rank + 1) % 4
            if self.suit_length(self.suits[rank]) >= 4:
                break
            loop += 1
            if loop > 4:
                rank = 4
                break
        suit_name = ['C', 'D', 'H', 'S', None][rank]
        suit = Suit(suit_name)
        return suit

    def _higher_five_card_suit(self):
        """Return highest five card suit."""
        for rank in list(range(4))[::-1]:
            if self.suit_length(self.suits[rank]) >= 5:
                suit_name = ['C', 'D', 'H', 'S'][rank]
                suit = Suit(suit_name)
                return suit

    def _get_best_major(self):
        """Return the best major suit."""
        if self.spades >= 6:
            suit = self.spade_suit
        elif self.hearts >= 6:
            suit = self.heart_suit
        elif self.spades == 5:
            suit = self.spade_suit
        elif self.hearts == 5:
            suit = self.heart_suit
        elif self.hearts == 4:
            suit = self.heart_suit
        else:
            suit = self.spade_suit
        return suit

    def _one_nt_max_level(self):
        """Return maximum level for response after 1NT with overcall."""
        if (self.hcp >= 12 or
                (self.hcp == 11 and self.shape[0] >= 6)):
            max_level = 3
        elif self.hcp >= 8:
            max_level = 2
        elif self.hcp >= 6 and self.shape[0] >= 6:
            max_level = 2
        else:
            max_level = 1
        return max_level

    def _trial_bid_suit_after_one_nt_with_overcall(self):
        """Try a suit after 1NT and overcall."""
        jump_level = self._get_one_nt_jump_level()
        trial_bid = self.next_level_bid(self.longest_suit, '0039', jump_level)
        return trial_bid

    # Various boolean functions

    def _six_card_major_thirteen_points(self):
        """Return True if hand has a six+ card_major with 13 points."""
        result = (self.shape[0] >= 6 and
                  self.longest_suit not in self.opponents_suits and
                  self.longest_suit.is_major and
                  self.hcp >= 13)
        return result

    def _can_bid_after_one_nt_with_overcall(self):
        """Return True if suit bid can be made after 1NT with overcall."""
        max_level = self._one_nt_max_level()
        trial_bid = self._trial_bid_suit_after_one_nt_with_overcall()
        result = (self.shape[0] >= 5 and
                  trial_bid.denomination not in self.opponents_suits and
                  trial_bid.level <= max_level)
        return result

    def _is_semi_balanced_eleven_plus(self):
        """Return True if semi balanced and 11+ points and stoppers."""
        result = False
        if self.is_semi_balanced and self.hcp >= 11:
            if self.stoppers_in_bid_suits:
                result = True
            elif (self.suit_length(self.overcaller_bid_one.denomination) >= 2 and
                  self.suit_points(self.overcaller_bid_one.denomination) >= 2):
                result = True
        return result

    def _is_balanced_game_going(self):
        """Return True if balanced with 13+ points."""
        result = (self.hcp >= 13 and
                  self.is_balanced and
                  # self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _is_game_going(self):
        """Return True with 13+ points."""
        result = (self.hcp >= 13 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _is_five_four_game_going(self):
        """Return True with 5/4 and 14+ points."""
        result = (self.hcp >= 14 and
                  self.five_four and
                  self.second_suit not in self.opponents_suits)
        return result

    def _is_balanced_with_no_long_minor(self):
        """Return True if balanced with only 4 card minors."""
        result = (self.is_balanced and
                  self.clubs < 5 and self.diamonds < 5 and
                  self.stoppers_in_bid_suits)
        return result

    def _has_six_card_unbid_suit(self):
        """Return True with 6+ card unbid suit."""
        result = (self.shape[0] >= 6 and
                  self.hcp >= 9 and
                  self.opener_bid_one.denomination != self.longest_suit
                  and self.longest_suit not in self.opponents_suits)
        return result

    def _is_semi_balanced_some_support(self):
        """Return True if semi balanced with 3+cards in partners suit."""
        result = (self.is_semi_balanced and
                  self.suit_length(self.opener_bid_one.denomination) >= 3 and
                  self.stoppers_in_bid_suits and
                  11 <= self.hcp <= 12 and
                  self.longest_suit == self.opener_bid_one.denomination and
                  self.nt_level <= 2 and
                  self.shape[3] >= 2)
        return result

    def _has_five_card_club_support_and_ten_points(self):
        """Return True with 5+ support for clubs and 10+ points."""
        result = (self.longest_suit == self.club_suit and
                  self.shape[0] >= 5 and
                  self.hcp >= 10 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _has_five_card_suit_and_ten_points(self):
        """Return True with 5 card suits and 10+ points."""
        result = (self.shape[0] >= 5 and
                  10 <= self.hcp <= 15 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _is_balanced_fewer_than_eight_points(self):
        """Return True if balanced and fewer than 8 points."""
        result = (6 <= self.hcp <= 8 and
                  self.is_balanced and
                  self.stoppers_in_bid_suits and
                  self.nt_level == 1)
        return result

    def _has_overcall_ten_points_shortage(self, own_suit):
        """Return True if overcall and 10 points and doubleton."""
        result = (self.overcall_made and self.hcp >= 10 and
                  self.shape[3] <= 2 and
                  self.shape[self.opener_bid_one.denomination.rank] >= 2 and
                  own_suit == self.opener_bid_one.denomination)
        return result

    def _has_support_nine_points_shortage(self, own_suit):
        """Return True if 5 card support and 9 points and singleton."""
        result = (own_suit == self.opener_bid_one.denomination and
                  self.suit_length(own_suit) >= 5 and
                  self.shape[3] <= 1 and
                  self.hcp >= 9)
        return result

    def _has_five_card_major_and_game_going(self):
        """Return True with 5 card major and 13+ points."""
        result = (self.five_card_major_suit and
                  self.hcp >= 13 and
                  self.five_card_major_suit not in self.opponents_suits)
        return result

    def _is_balanced_and_strong(self):
        """Return True if balanced and 15+ points."""
        result = (self.hcp >= 15 and
                  self.shape[0] == 4 and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3 and
                  (not self.four_card_major_or_better or
                   self.overcall_made))
        return result

    def _has_four_card_major_and_game_going(self, response_level):
        """Return True with 4 card major and 13+ points."""
        result = (self.four_card_major_suit and
                  response_level >= 2 and
                  self.hcp >= 13 and
                  self.four_card_major_suit not in self.opponents_suits and
                  (self.opener_bid_one.denomination != self.spade_suit or
                   self.four_card_major_suit != self.heart_suit)  # and
                  # self.suit_length(self.opener_bid_one.denomination) >= 4
                  )
        return result

    def _has_overcall_but_no_support(self, suit):
        """Return True if no support with overcall."""
        result = (self.nt_level == 2 and
                  self.suit_length(suit) <= 4 and
                  suit != self.opener_bid_one.denomination and
                  self.overcaller_bid_one.is_suit_call
                  and self.stoppers_in_bid_suits)
        return result

    def _has_good_diamonds(self):
        """Return True with good diamonds."""
        diamond_level = self.next_level(self.diamond_suit)
        result = (diamond_level <= 2 and (self.diamonds >= 5 or
                                          (self.diamonds == 4 and
                                           self.hcp >= 10)))
        return result

    def _has_good_clubs(self):
        """Return True with good clubs."""
        club_level = self.next_level(self.club_suit)
        result = (club_level <= 2 and (self.clubs >= 5 or
                                       (self.clubs == 4 and
                                        self.hcp >= 10)))
        return result

    def _is_semi_balanced_no_support(self, own_suit):
        """Return True if semi balanced and overcall."""
        result = (self.stoppers_in_bid_suits and
                  self.is_semi_balanced and
                  own_suit.is_minor and
                  self.overcall_made and
                  (own_suit != self.opener_bid_one.denomination or
                   self.hcp >= 10))
        return result

    def _four_four_one_stoppers(self):
        """Return True if 4441 and singleton in opener's suit."""
        result = (self.stoppers_in_bid_suits and
                  self.shape[0] == 4 and
                  self.suit_length(self.opener_bid_one.denomination) == 1)
        return result

    def _has_singleton_in_openers_suit_and_stoppers(self, own_suit):
        """Return True if singleton in opener's suit and stopper, level 2."""
        result = (self.stoppers_in_bid_suits and
                  self.overcall_made and
                  self.suit_length(self.opener_bid_one.denomination) == 1
                  and own_suit != self.longest_suit and
                  self.hcp >= 10 and self.nt_level == 2)
        return result

    def _has_no_support_and_no_long_suit(self, own_suit, trial_bid):
        """Return True with no support and no long suit."""
        result = (trial_bid.level >= 2 and
                  self.suit_length(own_suit) < 5 and
                  self.is_jump(self.opener_bid_one, trial_bid) and
                  own_suit != self.opener_bid_one.denomination and
                  self.is_balanced and
                  self.hcp >= 10 and self.nt_level <= 2 and
                  (self.stoppers_in_bid_suits or
                   (self.is_balanced and self.shape[3] >= 3)))
        return result

    def _forced_to_jump_bid(self, own_suit, trial_bid):
        """Return True if forced to jump."""
        result = (trial_bid.level >= 2 and
                  self.suit_length(own_suit) < 5 and
                  self.is_jump(self.opener_bid_one, trial_bid) and
                  self.hcp <= 10)
        return result

    def _support_after_suit_overcall_game_going(self):
        """Return True with support after overcall."""
        hand_value_points = (self.hcp +
                             self.support_shape_points(self.opener_bid_one.denomination))
        result = (12 <= hand_value_points <= 15 and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  self.overcaller_bid_one.is_value_call)
        return result

    def _has_singleton_in_openers_suit_and_own_six_card_suit(self):
        """Return True if singleton in opener's suit and a 6+card suit."""
        result = (self.shape[0] >= 6 and
                  self.hcp >= 12 and
                  self.suit_length(self.opener_bid_one.denomination) <= 1 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _has_two_card_support_for_major(self):
        """Return True if openers suit is major and two card support."""
        result = (self.opener_bid_one.denomination.is_major and
                  self.suit_length(self.opener_bid_one.denomination) >= 2)
        return result

    def _has_own_suit(self):
        if self.shape[0] >= 6:
            suit_quality = HandSuit(self.longest_suit, self).suit_quality()
            has_own_suit = True
        else:
            suit_quality = 0
            has_own_suit = False
        result = (has_own_suit and suit_quality >= 2 and
                  self.suit_length(self.opener_bid_one.denomination) <= 1 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _two_card_support_for_major_fifteen_points(self):
        """Return True with support for opener's major."""
        result = (self.opener_bid_one.denomination.is_major and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  self.hcp >= 15 and
                  self.next_level(self.opener_bid_one.denomination) <= 4)
        return result

    def _is_game_going_support_for_partners_minor(self, response_level):
        """Return True if game going and support for openers minor."""
        result = (self._has_four_card_major_and_game_going(response_level) and
                  self.next_four_card_suit() == self.opener_bid_one.denomination and
                  self.opener_bid_one.denomination.is_minor)
        return result

    def _can_rebid_diamonds_at_next_level(self):
        """Return True if can bid diamonds at the next level."""
        hand_value_points = self.support_points(self.opener_bid_one.denomination)
        level = self.next_level(self.diamond_suit)
        result = ((hand_value_points >= 5 and level <= 1) or
                  (hand_value_points >= 9 and
                   self.suit_points(self.diamond_suit) >= 5 and
                   level <= 2))
        return result

    def _can_bid_six_card_suit_at_level_three(self):
        """Return True if Can bid six card suit at 3 level."""
        result = (self.shape[0] >= 6 and
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
