""" Bid for Game
    Acol OpenersReBid module
"""

import inspect
from .bridge_tools import Bid, Pass, Double
from .hand import Hand
from .blackwood import Blackwood


class OpenersReBid(Hand):
    """BfG OpenersReBid class."""
    def __init__(self, hand_cards, board):
        super(OpenersReBid, self).__init__(hand_cards, board)
        self.trace = 0

    def suggested_bid(self):
        """Direct control to relevant method and return a Bid object."""
        if (self.responder_bid_one.name == '3NT' and
                self.shape[0] <= 5 and
                self.hcp <= 17):
            bid = Pass('0162')
        elif self.bid_one.is_nt:
            bid = self._rebid_after_nt_opening()
        elif self.responder_bid_one.is_pass:
            bid = self._responder_has_passed()
        elif self.bid_one.name == '2NT' and self.responder_bid_one.name == '4NT':
            if self.hcp == 22:
                bid = self.nt_bid(6, '0000')
            else:
                bid = Pass('0333')
        elif self.responder_bid_one.name == '4NT':
            bid = Blackwood(self.cards, self.board).count_aces()
        elif self.bid_one.name == '2C':
            bid = self._rebid_after_two_club_opening()
        elif (self.bid_one.level == 2 and
              self.bid_one.is_suit_call):
            bid = self._rebid_after_weak_two()
        elif (self.overcall_made and
              self.responder_bid_one.level == 3):
            bid = self._responder_at_three_overcall()
        elif self.responder_bid_one.is_double:
            bid = self._responder_has_doubled()
        else:
            bid = self._rebid_after_suit_opening()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_has_passed(self):
        """Bid after responder has passed."""
        if (self.overcall_made and
                self.bid_one.level == 1):
            bid = self._responder_pass_overcall()
        elif self.bid_history[-3:] == ['P', 'P', 'P']:
            bid = Pass('0942')
        else:
            bid = Pass('0163')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_after_nt_opening(self):
        """Rebid after NT opening."""
        if self.bid_one.name == '1NT':
            bid = self._rebid_after_one_nt_opening()
        elif self.bid_one.name == '2NT':
            bid = self._rebid_after_two_nt_opening()
        elif self.bid_one.name == '3NT':
            bid = Pass('0000')
        else:
            assert False, 'Bid not defined'
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_after_one_nt_opening(self):
        """Rebid after 1NT opening."""
        if self.responder_bid_one.is_game:
            bid = Pass('0164')
        elif self.responder_bid_one.name == 'NT':
            bid = self._after_two_nt_response()
        elif self.responder_bid_one.name == '2NT':
            bid = self._after_two_nt_response()
        elif self.overcaller_bid_one.is_double:
            bid = self._one_nt_is_doubled()
        elif self.responder_bid_one.name == '2C':
            bid = self._after_stayman_two_clubs()
        elif self.responder_bid_one.level == 2:
            bid = self._after_one_nt_at_level_two()
        elif self.responder_bid_one.level == 3:
            bid = self._after_one_nt_at_level_three()
        else:
            bid = Pass('0588')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_one_nt_at_level_two(self):
        """Rebid after 1NT opening, responder at level 2."""
        if self._three_card_support_for_responder_overcall_made():
            bid = self.next_level_bid(self.responder_bid_one.denomination, '0166')
        elif self._four_card_support_for_responder_overcall_made():
            bid = self.next_level_bid(self.responder_bid_one.denomination, '0167')
        else:
            bid = Pass('0168')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_one_nt_at_level_three(self):
        """Rebid after 1NT opening, responder at level 3."""
        if (self.responder_bid_one.name == '3H' or
                self.responder_bid_one.name == '3S'):
            bid = self._after_three_of_major_response()
        elif (self.five_card_major and
              self.longest_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.longest_suit, '0169')
        elif self.nt_level <= 3 and self.stoppers_in_bid_suits:
            bid = self.nt_bid(3, '0170')
        elif self.longest_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.longest_suit, '0807')
        else:
            bid = Pass('0172')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _one_nt_is_doubled(self):
        """Rebid after 1NT has been doubled."""
        if Bid(self.bid_history[-1]).is_value_call:
            bid = Pass('0172')
        elif self.responder_bid_one.is_value_call:
            bid = Pass('0579')
        else:
            bid = Pass('0585')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_two_clubs(self):
        """Rebid after Stayman 2C."""
        if self.overcaller_bid_one.is_double:
            bid = Pass('0172')
        elif self.nt_level >= 3:
            bid = Pass('0574')
        elif (self.hearts >= 4 and
              self.next_level(self.heart_suit) <= 2):
            bid = self.heart_bid(2, '0173')
        elif (self.spades >= 4 and
              self.next_level(self.spade_suit) <= 2):
            bid = self.spade_bid(2, '0174')
        elif self.next_level(self.diamond_suit) <= 2:
            bid = self.diamond_bid(2, '0175')
        elif self.opener_bid_one.name != '1NT' or self.stoppers_in_bid_suits:
            bid = self.nt_bid(2, '0176')
        else:
            bid = Pass('0130')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_three_clubs(self):
        """Rebid after Stayman."""
        if self.overcaller_bid_one.is_double:
            bid = Pass('0854')
        elif (self.overcall_made and
                self.nt_level >= 3):
            bid = Pass('0855')
        elif (self.hearts >= 4 and
              self.next_level(self.heart_suit) <= 3):
            bid = self.heart_bid(3, '0856')
        elif (self.spades >= 4 and
              self.next_level(self.spade_suit) <= 3):
            bid = self.spade_bid(3, '0857')
        elif self.next_level(self.diamond_suit) <= 3:
            bid = self.diamond_bid(3, '0858')
        else:
            bid = self.nt_bid(3, '0859')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_after_two_nt_opening(self):
        """Rebid after 2NT opening."""
        if self.responder_bid_one.name == '3NT':
            bid = Pass('0177')
        elif self.bid_one.name == '2NT' and self.responder_bid_one.name == '4NT':
            if self.hcp == 22:
                bid = self.nt_bid(6, '0707')
            else:
                bid = Pass('0333')
        elif self.responder_bid_one.name == '3C':
            bid = self._after_stayman_three_clubs()
        elif (self.suit_length(self.responder_bid_one.denomination) >= 3 and
                not self.bidding_above_game):
            bid = self.bid_to_game(self.responder_bid_one.denomination, '0875')
        elif (self.responder_bid_one.is_suit_call and
                self.nt_level <= 3):
            bid = self.nt_bid(3, '0876')
        elif self.responder_bid_one.name == '4NT' and self.hcp <= 22:
            bid = Pass('0333')
        else:
            bid = Pass('0178')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_pass_overcall(self):
        """Rebid after an overcall and responder has passed."""
        first_suit, second_suit = self._get_best_suits()
        level = self.next_level(first_suit)
        if self.hcp >= 19:
            bid = self._respond_with_power(first_suit, second_suit)
        elif self._is_strong_with_five_five(second_suit):
            bid = self.next_level_bid(second_suit, '0179')
        elif self._strong_with_second_suit(level):
            bid = self.next_level_bid(second_suit, '0180')
        elif self._six_card_suit_weak():
            bid = self.next_level_bid(first_suit, '0181')
        elif self._is_strong_with_five_four(second_suit):
            bid = self.next_level_bid(second_suit, '0695')
        elif self._repeatable_five_card_suit():
            if self.hcp >= 18 and self.shape[0] >= 6 and self.overcaller_in_second_seat:
                raise_level = 1
            else:
                raise_level = 0
            bid = self.next_level_bid(first_suit, '0182', raise_level=raise_level)
        elif self._strong_and_balanced():
            bid = self.next_nt_bid('0183')
        elif self.hcp >= 16 and self.shape[0] >= 6:
            suit = self._select_suit_if_six_four()
            bid = self.next_level_bid(suit, '0184')
        else:
            bid = self._responder_pass_overcall_weak()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_pass_overcall_weak(self):
        """Rebid after an overcall and responder has passed weakish hand."""
        first_suit = self.longest_suit
        if self._weak_five_four():
            bid = self._weak_five_four_bid()
        elif self._weak_six_cards():
            bid = self.next_level_bid(first_suit, '0185')
        elif self.five_five and self.nt_level <= 3:
            bid = self._five_five_rebid()
        elif self._can_rebid_five_card_suit_at_two_level():
            bid = self.next_level_bid(self.longest_suit, '0186')
        elif self._can_rebid_seven_card_suit_at_three_level():
            bid = self.next_level_bid(self.longest_suit, '0878')
        else:
            bid = Pass('0187')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_five_four_bid(self):
        """Return bid if weak but biddable 5/4."""
        barrier_will_be_broken = self.barrier_is_broken(self.bid_one,
                                                        self.next_level_bid(self.second_suit))
        will_be_jump_bid = self.is_jump(self.bid_one,
                                        self.next_level_bid(self.longest_suit))
        if will_be_jump_bid:
            bid = Pass('0188')
        elif barrier_will_be_broken:
            bid = self.next_level_bid(self.longest_suit, '0189')
        else:
            bid = self.next_level_bid(self.second_suit, '0190')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_five_rebid(self):
        """Bid with 5/5 hand"""
        suit = self._other_five_card_suit()
        if self._overcaller_doubled_and_advancer_bid():
            bid = Pass('0191')
        elif self.next_level(suit) > 3:
            bid = Pass('0192')
        elif suit == self.bid_one.denomination and self.hcp <= 13:
            bid = Pass('0906')
        elif suit not in self.opponents_suits and self.hcp >= 12:
            bid = self.next_level_bid(suit, '0193')
        elif self.bid_one.denomination not in self.opponents_suits and self.hcp >= 12:
            bid = self.next_level_bid(self.bid_one.denomination, '0194')
        else:
            bid = Pass('0195')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _respond_with_power(self, first_suit, second_suit):
        """Rebid after an overcall and responder has passed 19+ points."""
        if self.six_four:
            bid = self._powerful_six_four_bid(first_suit, second_suit)
        elif self.five_four_or_better:
            if second_suit not in self.opponents_suits:
                suit = second_suit
            else:
                suit = first_suit
            bid = self._powerful_five_four_bid(suit)
        elif self.stoppers_in_bid_suits and self.nt_level <= 3:
            bid = self.next_nt_bid('0196')
        else:
            bid = Double('0197')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _powerful_six_four_bid(self, first_suit, second_suit):
        """Bid powerful hand with 6/4."""
        first_suit_points = self.suit_points(first_suit)
        second_suit_points = self.suit_points(second_suit)
        if first_suit_points > second_suit_points+1:
            suit = first_suit
        else:
            suit = second_suit
        if suit in self.opponents_suits:
            if suit == first_suit:
                suit = second_suit
            else:
                suit = first_suit
        if (self.next_level(suit) <= 2 and
                (suit == self.opener_bid_one.denomination or
                 suit.rank < self.opener_bid_one.denomination.rank)):
            raise_level = 1
        else:
            raise_level = 0
        bid = self.next_level_bid(suit, '0198', raise_level)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _powerful_five_four_bid(self, second_suit):
        """Bid powerful hand with 5/4."""
        suit = second_suit
        raise_level = 0
        trial_bid = self.next_level_bid(suit, '0199', raise_level)
        level = trial_bid.level
        if ((trial_bid.level <= 3 and
             self.responder_bid_one.is_value_call and
             not self.overcall_made) or
                self.hcp >= 22):
            level = 3
        next_level = self.next_level(suit)
        level = max(next_level, level)
        bid = self.suit_bid(level, suit, '0200')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_after_two_club_opening(self):
        """Bid after a two club opening."""
        if self.is_balanced:
            bid = self._balanced_after_two_clubs()
        else:
            bid = self._rebid_no_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _balanced_after_two_clubs(self):
        """Bid with a balanced hand after two club opening."""
        if self.responder_bid_one.name == '2NT':
            bid = self.nt_bid(3, '0600')
        else:
            bid = self._balanced_two_clubs_responder_with_values()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _balanced_two_clubs_responder_with_values(self):
        """Bid with a balanced hand after two club opening with support."""
        if self.hcp >= 28:
            bid = self.nt_bid(4, '0202')
        elif self.responder_bid_one.is_major and self.suit_length(self.responder_bid_one.denomination):
            bid = self.next_level_bid(self.responder_bid_one.denomination, '0941')
        elif ((self.hcp >= 25 or self.responder_bid_one.level == 3) and
              self.nt_level <= 3):
            bid = self.nt_bid(3, '0203')
        elif self.nt_level <= 2:
            bid = self.nt_bid(2, '0204')
        else:
            bid = self.next_level_bid(self.responder_bid_one.denomination, '0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_after_weak_two(self):
        """Rebid after a weak two opening."""
        if self.responder_bid_one.denomination == self.bid_one.denomination:
            bid = Pass('0205')
        else:
            bid = self._rebid_after_suit_opening()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_two_nt_response(self):
        """Rebid after 2NT response from responder."""
        if self.five_card_major and self.longest_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.longest_suit, '0687')
        elif self.nt_level <= 3:
            bid = self._after_two_nt_response_bid_nt()
        else:
            bid = Pass('0206')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_two_nt_response_bid_nt(self):
        """Rebid after 2NT response from responder, bid NT."""
        if (self.hcp == 13 and (self.shape[0] == 5 or
                                self.tens_and_nines >= 4)):
            bid = self.nt_bid(3, '0207')
        elif self.hcp == 14:
            bid = self.nt_bid(3, '0208')
        else:
            bid = Pass('0209')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_three_of_major_response(self):
        """Rebid after 3 major response."""
        suit = self.responder_bid_one.denomination
        level = self.next_level(suit)
        if self.responder_bid_one.name == '3H' and self.hearts >= 3 and level <= 4:
            bid = self.heart_bid(4, '0210')
        elif self._can_rebid_spades(level):
            bid = self.spade_bid(4, '0211')
        elif self.nt_level <= 3:
            bid = self.nt_bid(3, '0212')
        else:
            bid = Pass('0213')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_after_suit_opening(self):
        """Rebid after suit opening."""
        if self.responder_bid_one.is_nt:
            bid = self._rebid_after_nt_response()
        elif self._responder_shows_support_or_can_support_responder():
            bid = self._after_suit_opening_support()
        elif self._can_support_responders_major():
            if self.hcp <= 12:
                raise_level = 0
            else:
                raise_level = 1
            bid = self.next_level_bid(self.responder_bid_one.denomination, '0214', raise_level)
        else:
            bid = self._rebid_no_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_suit_opening_support(self):
        """Rebid after suit opening with support."""
        if self.responder_bid_one.is_minor and self.is_balanced:
            bid = self._rebid_no_support()
        else:
            bid = self._rebid_with_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_after_nt_response(self):
        """Rebid after NT response."""
        if self._responder_has_bid_nt_game_over_minor():
            bid = Pass('0215')
        elif self._is_shapely_intermediate_hand():
            bid = self._rebid_no_support()
        else:
            bid = self._support_nt()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _support_nt(self):
        """Support NT bid from partner."""
        if self.responder_bid_one.name == '1NT':
            bid = self._support_one_nt()
        elif self.responder_bid_one.name == '2NT':
            bid = self._support_two_nt()
        elif self.responder_bid_one.name == '3NT':
            bid = Pass('0216')
        else:
            bid = Pass('999')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _support_one_nt(self):
        """Respond to 1NT bid from partner."""
        old_level = self.responder_bid_one.level
        level = self.quantitative_raise(self.hcp, old_level, [16, 19], 3)
        if self.hcp >= 16 and self.nt_level <= level:
            bid = self.nt_bid(level, '0217')
        elif self.shape[0] >= 5 and (self.last_bid.is_pass or self.shape[0] >= 6):
            bid = self._rebid_no_support()
        elif self.hcp >= 13 and self.overcall_made:
            bid = self._rebid_no_support()
        else:
            bid = Pass('0218')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _support_two_nt(self):
        """Support 2NT bid from partner."""
        if self.hcp >= 15 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0219')
        else:
            bid = Pass('0220')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_with_support(self):
        """Rebid after suit decided."""
        if self.bid_one.is_suit_call:
            change_suit = (self.responder_bid_one.denomination != self.bid_one.denomination and
                           self.responder_bid_one.denomination.is_suit and
                           self.bid_one.denomination.is_suit)
        else:
            change_suit = None
        if change_suit:
            bid = self._opener_can_support_responder()
        else:
            bid = self._rebid_support_no_suit_changes()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_support_no_suit_changes(self):
        """Rebid responder supports opener."""
        if self.responder_bid_one.level == 4:
            if (self.hcp >= 19 or
                (self.hcp >= 17 and
                 self.bid_one.denomination.is_major)):
                if self.nt_level <= 4:
                    bid = self.nt_bid(4, '0317')
                else:
                    bid = self.next_level_bid(self.responder_bid_one.denomination, '0000')
            elif self.hcp >= 16:
                bid = self.next_level_bid(self.responder_bid_one.denomination, '0925')
            else:
                bid = Pass('0221')
        elif self.responder_bid_one.level >= 3:
            bid = self._support_at_level_three()
        elif self.responder_bid_one.level >= 2:
            bid = self._support_at_level_two()
        else:
            bid = Pass('0222')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _support_at_level_three(self):
        """Rebid with support and no suit changes at level 3."""
        next_level = self.next_level(self.responder_bid_one.denomination)
        if (self.responder_bid_one.denomination.is_major and self.hcp >= 14 and
                next_level <= 4):
            bid = self.bid_to_game(self.responder_bid_one.denomination, '0223')
        elif (self.responder_bid_one.denomination.is_minor and self.hcp >= 16 and
              next_level <= 5):
            bid = self.bid_to_game(self.responder_bid_one.denomination, '0224')
        else:
            bid = Pass('0225')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _support_at_level_two(self):
        """Rebid with support and no suit changes at level 2."""
        agreed_suit = self.my_last_bid.denomination
        next_level = self.next_level(agreed_suit)
        game_bid = self.bid_to_game(agreed_suit)
        if self.hcp >= 19 and next_level <= game_bid.level:
            bid = self.bid_to_game(agreed_suit, '0226')
        elif self._has_six_card_minor_and_eighteen_points():
            bid = self.nt_bid(3, '0227')
        elif self.hcp >= 16 and next_level <= 4:
            bid = self.next_level_bid(agreed_suit, '0228')
        elif self.overcall_made and self.hcp >= 15 and next_level <= 3:
            bid = self.next_level_bid(agreed_suit, '0229')
        elif self.shape[0] >= 7:
            bid = self.next_level_bid(agreed_suit, '0230')
        elif self.hcp >= 14 and self.shape[0] >= 5 and not self.right_hand_bid.is_pass:
            bid = self.next_level_bid(agreed_suit, '0756')
        elif self.shape[0] >= 6 and self.shape[1] >= 5:
            bid = self.next_level_bid(self.longest_suit, '0792')
        else:
            bid = Pass('0231')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_can_support_responder(self):
        """Return bid when opener supports responder."""
        suit_to_bid = self._get_suit_support_for_responder()
        level = self._get_level_with_support(suit_to_bid)
        next_level = self.next_level_bid(suit_to_bid).level
        level = max(level, next_level)
        responder_has_jumped = (self.is_jump(self.bid_one, self.responder_bid_one))

        if self.hcp >= 16 and responder_has_jumped and self.overcaller_bid_one.is_pass:
            bid = self._opener_can_support_responder_strong(suit_to_bid)
        elif suit_to_bid.is_no_trumps:
            bid = Pass('0234')
        elif self.suit_length(suit_to_bid) <= 3:
            if self.responder_bid_one.level == 2 and self.hcp >= 14:
                bid = self.next_level_bid(suit_to_bid, '0263', raise_level=1)
            else:
                bid = self.next_level_bid(suit_to_bid, '0235')
        elif self._is_unbalanced_with_sixteen_points():
            bid = self._medium_unbalanced_hand()
        elif level >= next_level:
            bid = self.suit_bid(level, suit_to_bid, '0236', use_shortage_points=True)
        else:
            bid = Pass('0237')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _medium_unbalanced_hand(self):
        """Return bid with 16+ points and unbalanced."""
        if self.overcall_made:
            raise_level = 0
        else:
            raise_level = 1
        if self._can_support_nineteen_points():
            bid = self.bid_to_game(self.second_suit, '0199')
        elif self._can_support_seventeen_points_and_void():
            bid = self.bid_to_game(self.responder_bid_one.denomination, '0733')
        elif self._fffo_strong_four_card_support():
            bid = self.bid_to_game(self.responder_bid_one.denomination, '0327')
        elif self._no_biddable_second_suit_and_support_for_partner():
            bid = self.bid_to_game(self.responder_bid_one.denomination, '0689')
        elif self.second_suit == self.responder_bid_one.denomination:
            bid = self.next_level_bid(self.second_suit, '0203', raise_level=raise_level)
        else:
            bid = self.next_level_bid(self.second_suit, '0165', raise_level=raise_level)
            # if bid.level > self.game_level(self.second_suit):
            #     bid = Double('0203')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_can_support_responder_strong(self, suit_to_bid):
        """Return bid when opener supports responder and 16+ points."""
        if self.hcp >= 16 and suit_to_bid.is_major:
            if self.responder_bid_one.level == 3:
                bid = self.nt_bid(4, '0232')
            else:
                bid = self.nt_bid(2, '0264')
        else:
            bid = self.next_level_bid(suit_to_bid, '0233')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_no_support(self):
        """Rebid with no responder support."""
        trial_bid = self._five_four_rebids()
        if self.bid_one.name == '2C':
            bid = trial_bid
        elif self.is_balanced:
            bid = self._no_support_balanced()
        elif self._has_strong_minor_responder_has_jumped():
            bid = self.nt_bid(4, '0239')
        elif self.shape[0] >= 7:
            bid = self._single_suited_rebids()
        elif self.five_five:
            bid = self._no_support_five_five()
        elif self._competitive_auction_weak_with_minor() and trial_bid.level >= 3:
            bid = Pass('0240')
        elif self._competitive_auction_with_support_for_responder():
            bid = self._rebid_partners_major()
        elif self.five_in_opponents_suits():
            bid = Pass('0241')
        elif self.five_four or self.five_five_or_better:
            bid = self._five_four_rebids()
        elif self.shape[0] >= 6:
            bid = self._single_suited_rebids()
        elif self.shape == [4, 4, 4, 1]:
            bid = self._four_four_four_one_bid()
        else:
            bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_five_five(self):
        """Rebid with no responder support and 5/5 hand."""
        suit_to_bid = self._get_suit_no_support_five_five()
        raise_level = 1
        level = min(self.next_level(suit_to_bid, raise_level=raise_level), 3)

        if self._suit_is_major_and_eighteen_points(suit_to_bid):
            if self.responder_bid_one.is_nt:
                bid = self.suit_bid(4, suit_to_bid, '0880')
            else:
                bid = self.suit_bid(level, suit_to_bid, '0201')
        elif self.next_level(suit_to_bid) <= 3 and self.hcp >= 16:
            bid = self.suit_bid(level, suit_to_bid, '0242')
        elif self.five_in_opponents_suits():
            bid = Pass('0243')
        elif (self.responder_bid_one.name != '2NT' and
                (self.next_level(suit_to_bid) <= 2 or
                 self.hcp >= 15 or
                 self.overcaller_bid_one.denomination == self.advancer_bid_one.denomination)):
            bid = self.next_level_bid(suit_to_bid, '0244')
        else:
            bid = Pass('0335')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_partners_major(self):
        """Rebid with no responder support competitive auction and partner major."""
        responders_suit = self.responder_bid_one.denomination
        if (self.hcp >= 14 and
                self.support_shape_points(responders_suit) >= 2):
            bid = self.next_level_bid(responders_suit, '0245', raise_level=1)
        else:
            bid = self.next_level_bid(responders_suit, '0246')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_support_balanced(self):
        """Bid with no support and balanced hand."""
        level = self.next_level(self.bid_one.denomination)
        if self.hcp >= 19:
            bid = self._bid_with_19_points()
        elif self.hcp >= 15 or level > 2:
            bid = self._invitational_bid()
        else:
            bid = self.next_level_bid(self.bid_one.denomination, '0247')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _bid_with_19_points(self):
        """Return bid with a 19 point hand."""
        unbid_major = self.unbid_four_card_major()
        if self._powerful_and_has_four_cards_in_unbid_major(unbid_major):
            bid = self.next_level_bid(unbid_major, '0248', raise_level=1)
        elif self._responder_support_with_jump():
            bid = self.nt_bid(3, '0943')
        elif (self.hcp >= 17 and self.is_jump(self.bid_one,
                                              self.responder_bid_one)):
            bid = self.nt_bid(6, '0015')
        elif self.nt_level <= 3:
            bid = self.nt_bid(3, '0250')
        else:
            bid = Pass('0251')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _invitational_bid(self):
        """Return bid with 15+ points or partner has 10+ points."""
        if self.stoppers_in_bid_suits:
            bid = self._rebid_balanced_hand()
        elif self.shape[1] >= 4 and self.hcp >= 16 and self.second_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.second_suit, '0757')
        elif self.shape[0] < 5:
            bid = self._opener_can_support_responder()
        else:
            bid = self._single_suited_rebids()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_four_rebids(self):
        """Rebid with 5/4 hands."""
        responder_jumped = self.jump_bid_made(self.responder_bid_one)
        suit_to_bid = self._get_suit_with_five_four()
        test_bid = self.next_level_bid(suit_to_bid)
        cannot_show_second_suit = self.barrier_is_broken(self.bid_one, test_bid)
        if self._weak_and_able_to_repeat_suit(cannot_show_second_suit, responder_jumped):
            suit_to_bid = self.bid_one.denomination

        if self.hcp >= 16:
            bid = self._five_four_strong(suit_to_bid)
        else:
            bid = self._five_four_weak(suit_to_bid, cannot_show_second_suit)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_four_strong(self, suit_to_bid):
        """Bid with strong hand."""
        if self.bid_one.name == '2C':
            bid = self._rebid_after_two_clubs()
        elif self.five_five:
            suit_to_bid = self.longest_suit
            if self.hcp >= 16:
                raise_level = 1
            else:
                raise_level = 0
            bid = self.next_level_bid(suit_to_bid, '0252', raise_level)
        else:
            bid = self._five_four_strong_balanced(suit_to_bid)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_four_strong_balanced(self, suit_to_bid):
        """Bid with strong 5/4 hand."""
        test_bid = self.next_level_bid(suit_to_bid, '0253')
        if self._five_four_strong_test_nt(test_bid):
            bid = self.nt_bid(3, '0254')
        elif self._can_repeat_suit_and_seventeen_points(suit_to_bid):
            bid = self._five_four_strong_nt()
        elif self._has_five_four_and_sixteen_points(suit_to_bid):
            second_suit = self._get_second_suit_for_opener()
            bid = self.next_level_bid(second_suit, '0255')
        else:
            raise_level = self._raise_level_with_five_four_strong(suit_to_bid, test_bid)
            if (self.next_level(suit_to_bid, raise_level) > 3 or
                    (self.responder_bid_one.name == '1NT' and self.hcp <= 16)):
                raise_level = 0
            bid = self.next_level_bid(suit_to_bid, '0257', raise_level)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_four_strong_nt(self):
        """Bid with strong 5/4 hand try NT."""
        if self.hcp >= 19 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0258')
        elif self._can_bid_three_nt():
            bid = self.nt_bid(3, '0000')
        elif self._can_bid_two_nt():
            bid = self.nt_bid(2, '0259')
        elif self.nt_level <= 1:
            bid = self.nt_bid(1, '0260')
        else:
            if self.second_suit in self.opponents_suits:
                suit_to_bid = self.longest_suit
            else:
                suit_to_bid = self.second_suit
            bid = self.next_level_bid(suit_to_bid, '0261')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_after_two_clubs(self):
        """Return bid after a 2C opening."""
        if self.is_semi_balanced and self.hcp >= 25 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0523')
        elif self.is_balanced:
            bid = self.next_nt_bid('0262')
        elif self.responder_bid_one.name == '2D' and self.longest_suit == self.diamond_suit:
            bid = Pass('0000')
        elif self.responder_bid_one.name == '2D':
            bid = self.next_level_bid(self.longest_suit, '0848')
        elif self.suit_length(self.responder_bid_one.denomination) >= 3:
            if (self.hcp + self.suit_length(self.responder_bid_one.denomination) >= 26 and
                    self.nt_level <= 4):
                bid = self.nt_bid(4, '0000')
            else:
                bid = self.bid_to_game(self.responder_bid_one.denomination, '0264')
        elif self.longest_suit.is_minor and self.responder_bid_one.denomination.is_minor:
            bid = self.next_nt_bid('0265')
        else:
            bid = self.next_level_bid(self.longest_suit, '0266')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_four_weak(self, suit, cannot_show_second_suit):
        """Bid with weak 5/4 hand."""
        suit_to_bid = self._five_four_weak_suit(suit, cannot_show_second_suit)
        level = self.next_level(suit)
        if self._weak_five_four_with_weak_suit(suit_to_bid):
            bid = Pass('0267')
        elif self._weak_five_four_consider_bid(level):
            bid = self._five_four_weak_bid(suit_to_bid, cannot_show_second_suit)
        elif self._can_bid_at_appropriate_level(suit_to_bid, level):
            bid = self.next_level_bid(suit_to_bid, '0268')
        elif self.bid_history[-1] == 'P':
            bid = self.next_level_bid(self.longest_suit, '0271')
        else:
            bid = Pass('0269')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_four_weak_bid(self, suit_to_bid, cannot_show_second_suit):
        """Return bid if a sound bid is possible."""
        overcall = Bid(self.bid_history[-1])
        trial_bid = self.next_level_bid(suit_to_bid, '0270')
        if trial_bid.level >= 3 or (not overcall.is_value_call):
            bid = self._five_four_weak_invitational(suit_to_bid, cannot_show_second_suit)
        elif self.hcp <= 11:
            bid = Pass('0271')
        elif self.hcp <= 12 and cannot_show_second_suit:
            bid = Pass('0272')
        else:
            bid = self.next_level_bid(suit_to_bid, '0273')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_four_weak_invitational(self, suit_to_bid, cannot_show_second_suit):
        """Return bid with 5/4 hand and next level is 3."""
        responder_jumped = self.is_jump(self.bid_one, self.responder_bid_one)
        if self.bid_one.level == 2:
            bid = Pass('0274')
        elif self.next_level(suit_to_bid) <= 2 and self.shape[0] >= 6:
            if self.shape[0] >= 7 and self.hcp >= 13:
                raise_level = 1
            else:
                raise_level = 0
            bid = self.next_level_bid(suit_to_bid, '0275', raise_level=raise_level)
        elif self._weak_after_one_nt_and_barrier_broken(cannot_show_second_suit):
            bid = Pass('0276')
        elif self._six_four_responder_at_level_two():
            bid = self.next_level_bid(self.second_suit, '0277')
        elif self._weak_overcall_responder_level_one() and cannot_show_second_suit:
            bid = Pass('0278')
        elif self._can_bid_second_suit_after_nt():
            bid = self.next_level_bid(self.second_suit, '0834')
        elif self.hcp <= 12 and cannot_show_second_suit:
            bid = self.next_level_bid(self.bid_one.denomination, '0873')
        elif self._strong_or_can_bid_at_level_two(suit_to_bid):
            bid = self.next_level_bid(suit_to_bid, '0279')
        elif responder_jumped and not self.responder_bid_one.is_nt:
            if self.second_suit not in self.opponents_suits:
                bid = self.next_level_bid(self.second_suit, '0000')
            else:
                bid = self.next_level_bid(self.longest_suit, '0000')
        elif self._strong_five_four_or_better():
            bid = self.next_level_bid(self.second_suit, '0130')
        else:
            bid = Pass('0908')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _single_suited_rebids(self):
        """Return bid with single suited hands."""
        if self.hcp >= 18 or self.shape[0] >= 8:
            bid = self._single_suited_rebids_strong()
        elif self.hcp >= 16:
            bid = self._single_suited_intermediate()
        else:
            bid = self._single_suited_rebids_weak()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _single_suited_rebids_strong(self):
        """Return bid with strong single suited hands."""
        suit = self.longest_suit
        level = self.next_level(suit)
        if suit.is_major:
            bid = self._single_suited_strong_major(suit, level)
        else:
            level = self.next_level(suit)
            level = max(3, level)
            bid = self.suit_bid(level, suit, '0280')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _single_suited_strong_major(self, suit, level):
        """Return bid with strong single major suited hands."""
        level = max(4, level)
        if (self.shape[0] <= 5 and
                self.nt_level <= 3):
            bid = self.nt_bid(3, '0281')
        elif level <= 5:
            bid = self.suit_bid(level, suit, '0282')
        else:
            bid = Pass('0283')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _single_suited_intermediate(self):
        """Return bid with intermediate single suited hands."""
        if self.hcp == 19:
            nt_level = 3
        elif self.hcp >= 17 or self.nt_level == 2:
            nt_level = 2
        else:
            nt_level = 1
        if self._is_strong_with_seven_card_major():
            bid = self.bid_to_game(self.longest_suit, '0903')
        elif self._is_strong_six_four_with_major():
            bid = self.next_level_bid(self.second_suit, '0256')
        elif self.shape[0] <= 5 and self.longest_suit.is_minor and self.nt_level <= nt_level:
            bid = self.nt_bid(nt_level, '0117')
        else:
            if self._weak_with_overcall_or_next_level_three():
                raise_level = 0
            else:
                raise_level = 1
            bid = self.next_level_bid(self.longest_suit, '0284', raise_level)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _single_suited_rebids_weak(self):
        """Return bid with weak single suited hands."""
        if ((self.overcall_made == self.OVERCALLER_POSITION['fourth_seat']) and
                not self.responders_support):
            bid = self._single_suited_weak_competitive()
        else:
            bid = self._single_suited_uncontested()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _single_suited_uncontested(self):
        """Return bid with weak single suited hands in uncontested auction."""
        if self.responder_bid_one.is_game:
            bid = Pass('0285')
        elif self._has_minor_can_support_responders_major():
            bid = self.next_level_bid(self.responder_bid_one.denomination, '0286')
        elif self._has_six_card_major_and_responder_bid_one_nt():
            bid = self.suit_bid(2, self.longest_suit, '0912')
        elif self._has_six_card_major_and_responder_bid_two_nt():
            if ((self.shape[0] >= 7 and self.next_level(self.longest_suit) <= 3) or
                    (self.shape[0] == 6 and self.hcp >= 14 and
                     self.next_level(self.longest_suit) <= 4)):
                level = 4
            else:
                level = self.next_level(self.longest_suit)
            bid = self.suit_bid(level, self.longest_suit, '0287')
        elif self.responder_bid_one.name == '1NT' and self.hcp <= 15 and self.shape[0] <= 5:
            bid = Pass('0521')
        elif self.shape[0] >= 6 and self.longest_suit.is_major and self.hcp >= 12:
            if self.shape[0] >= 7 and self.hcp >= 13 and self.next_level(self.longest_suit) <= 2:
                raise_level = 1
            else:
                raise_level = 0
            bid = self.next_level_bid(self.longest_suit, '0929', raise_level)
        elif self._can_bid_three_nt():
            bid = self.next_nt_bid('0288')
        elif self.responder_bid_one.level >= 3 and self.suit_length(self.responder_bid_one.denomination) >= 3:
            bid = self.next_level_bid(self.responder_bid_one.denomination, '0360')
        elif self.hcp <= 9:
            bid = Pass('0836')
        else:
            bid = self.next_level_bid(self.longest_suit, '0890')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _single_suited_weak_competitive(self):
        """Return bid with weak single suited hands in competitive auction."""
        if self._is_strong_with_solid_seven_card_suit():
            bid = self.next_level_bid(self.longest_suit, '0891')
        elif self._has_five_card_suit_fifteen_points_level_two():
            bid = self.next_level_bid(self.longest_suit, '0033')
        elif self._has_seven_card_suit_and_weak():
            bid = self.next_level_bid(self.longest_suit, '0887')
        elif self.shape[0] >= 6 and self.next_level(self.longest_suit) <= 2:
            bid = self.next_level_bid(self.longest_suit, '0892')
        elif self._has_six_card_suit_responder_at_level_two():
            bid = self.next_level_bid(self.longest_suit, '0893')
        else:
            bid = Pass('0289')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _four_four_four_one_bid(self):
        """Rebid with 4441 hands."""
        singleton_suit = self.suit_shape[3]
        if self.responder_bid_one.denomination == singleton_suit:
            bid = self._fffo_partner_bids_singleton()
        else:
            bid = self._rebid_with_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _fffo_partner_bids_singleton(self):
        """Rebid with 4441 hands after partner bids singleton suit."""
        suit = self._select_suit_for_four_four_four_one()
        if self.responder_bid_one.level == 1:
            level = self.quantitative_raise(self.hcp, 0, [15, 17, 19], 3)
        else:
            level = self.quantitative_raise(self.hcp, 0, [12, 13, 15], 3)
        test_bid = self.next_level_bid(suit, '0290', False)
        if self._has_fifteen_points_and_level_is_one(level):
            bid = self.nt_bid(level, '0291')
        elif self._barrier_would_break_and_fewer_that_sixteen(suit, test_bid):
            bid = Pass('0292')
        else:
            bid = test_bid
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _rebid_balanced_hand(self):
        """Return bid with a balanced hand."""
        bid_level = self._balanced_bid_level()
        if self._strong_can_bid_nt(bid_level):
            comment = ['0067', '0293', '0065', '0066'][bid_level]
            bid = self.nt_bid(bid_level, comment)
        elif self._no_fit_fifteen_points_responder_level_two():
            bid = self.nt_bid(3, '0294')
        elif self.hcp >= 15 and self.is_balanced and self.stoppers_in_unbid_suits() and self.nt_level == 1:
            bid = self.nt_bid(1, '0816')
        else:
            bid = Pass('0295')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_at_three_overcall(self):
        """Return bid after responder jumped to 3 level after an overcall."""
        if self.responder_bid_one.name == '3NT':
            bid = self._responder_at_three_nt_overcall()
        else:
            bid = self._at_three_overcall_suit()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _at_three_overcall_suit(self):
        """Return bid after responder jumped to 3 of a suit after overcall."""
        if self.bid_one.denomination == self.responder_bid_one.denomination:
            bid = self._at_three_overcall_support()
        elif self._is_balanced_or_no_fit_with_responder():
            bid = self.nt_bid(3, '0296')
        else:
            bid = self._at_three_overcall_no_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_at_three_nt_overcall(self):
        """Return bid after responder has jumped to 3NT after an overcall."""
        if self.hcp >= 18 and self.nt_level <= 4:
            bid = self.nt_bid(4, '0297')
        elif self._has_six_card_major_and_can_bid_game():
            bid = self.suit_bid(4, self.longest_suit, '0298')
        else:
            bid = Pass('0299')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _at_three_overcall_support(self):
        """Return bid with 3 level support after an overcall."""
        if self.hcp >= 14:
            bid = self._overcall_support_strong()
        else:
            bid = Pass('0300')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_support_strong(self):
        """Return bid with 3 level support after overcall with strong hand."""
        hvp = self.support_points(self.bid_one.denomination)
        if self.bid_one.denomination.is_minor and hvp >= 18:
            bid = self._at_three_overcall_support_minor()
        elif self._is_balanced_minor_suit_can_bid_nt_game():
            bid = self.nt_bid(3, '0301')
        elif self.next_level(self.bid_one.denomination) <= 4:
            bid = self.suit_bid(4, self.bid_one.denomination, '0302')
        else:
            bid = Pass('0303')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _at_three_overcall_support_minor(self):
        """Return bid with 3 level support after overcall with strong minor."""
        if self._is_balanced_can_bid_nt_game():
            bid = self.nt_bid(3, '0304')
        elif self.next_level(self.bid_one.denomination) <= 5:
            bid = self.suit_bid(5, self.bid_one.denomination, '0305')
        else:


            bid = Pass('0911')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _at_three_overcall_no_support(self):
        """Return bid with no support, responder at 3 after overcall."""
        if self._has_six_card_major_and_can_bid_at_three_level():
            bid = self.suit_bid(3, self.bid_one.denomination, '0306')
        else:
            bid = self._overcall_no_support_minor()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _overcall_no_support_minor(self):
        """Return bid with no support, minor suit, after overcall."""
        responders_suit = self.responder_bid_one.denomination
        next_level = self.next_level(responders_suit)
        level = '4'
        if responders_suit.is_minor and self.hcp >= 15:
            level = '5'
        if (self.five_five and
                self.second_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.second_suit, '0307')
        elif int(level) >= next_level:
            bid = self.suit_bid(level, responders_suit, '0308')
        else:
            bid = Pass('0309')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_has_doubled(self):
        """Return bid after responder has doubled."""
        if (self.suit_length(self.second_suit) >= 4 and
                self.second_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.second_suit, '0000')
        else:
            bid = self.next_level_bid(self.longest_suit, '0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    # Various utility functions

    def _get_second_suit_for_opener(self):
        """Return suit to bid after overcall."""
        if self.shape == [5, 4, 4, 0]:
            if self.second_suit not in self.opponents_suits:
                suit = self.second_suit
            elif self.third_suit not in self.opponents_suits:
                suit = self.third_suit
            else:
                suit = self.longest_suit
        elif self.second_suit in self.opponents_suits:
            suit = self.longest_suit
        else:
            suit = self.second_suit
        return suit

    def _get_level_with_support(self, suit):
        """Return appropriate level with partner support."""
        # use distribution points
        hand_value_points = (self.hcp +
                             self.support_shape_points(suit))
        point_list = [13, 17, 19]
        if suit.is_major:
            game = 4
        else:
            game = 5
        # quantitative_raise with point_list = [13, 16, 19]
        # means single raise if points between 13 and 15
        # jump  with points between 16 and 18 etc.
        level = self.quantitative_raise(hand_value_points,
                                        self.responder_bid_one.level,
                                        point_list, game)
        return level

    def _get_suit_support_for_responder(self):
        """Return suit if opener can support responder."""
        suit_to_bid = self.responder_bid_one.denomination
        if self.responder_bid_one.is_double:
            if self.shape[0] >= 6:
                suit_to_bid = self.longest_suit
            else:
                suit_to_bid = self.second_suit
        return suit_to_bid

    def _get_suit_no_support_five_five(self):
        """Return the suit to bid if no support and hand is 5/5."""
        suit_to_bid = self._other_five_card_suit()
        barrier_is_broken = self.barrier_is_broken(self.bid_one,
                                                   self.next_level_bid(suit_to_bid))

        can_break_barrier = (self.hcp >= 15 or
                             (self.hcp >= 14 and self.responder_bid_one.is_nt))
        if barrier_is_broken and not can_break_barrier:
            suit_to_bid = self.bid_one.denomination
        return suit_to_bid

    def _get_best_suits(self):
        """Return the *ordered* first and second suits."""
        first_suit = self.longest_suit
        second_suit = self.second_suit
        if self.five_five:
            first_suit = self.bid_one.denomination
            second_suit = self._other_five_card_suit()
        return first_suit, second_suit

    def _select_suit_if_six_four(self):
        """Return selected suit with 6/4 shape."""
        suit = self.longest_suit
        if self.shape[1] >= 4:
            if self.second_suit not in self.opponents_suits:
                second_suit = self.second_suit
                suit = self.cheaper_suit(suit, second_suit)
        return suit

    def _other_five_card_suit(self):
        """Return unbid 5 card suit in 5/5 hands."""
        suit_one = self.bid_one.denomination
        if suit_one == self.longest_suit:
            suit = self.second_suit
            if suit in self.opponents_suits:
                suit = self.longest_suit
        else:
            suit = self.longest_suit
            if suit in self.opponents_suits:
                suit = self.second_suit
        return suit

    def _raise_level_with_five_four_strong(self, suit_to_bid, test_bid):
        """Return the raise level with a strong 5/4 hand."""
        if self.hcp >= 19:
            raise_level = 1
        elif self.hcp < 16:
            raise_level = 0
        elif test_bid.level > 3:
            raise_level = 0
        elif suit_to_bid == self.bid_one.denomination:
            raise_level = 0
        elif suit_to_bid.rank > self.bid_one.denomination.rank:
            raise_level = 0
        else:
            raise_level = 1
        return raise_level

    def _five_four_weak_suit(self, suit, cannot_show_second_suit):
        """Return selected suit for weak 5/4 hands."""
        if suit < self.bid_one.denomination or not cannot_show_second_suit:
            suit_to_bid = suit
        elif self.bid_one.denomination == self.club_suit and suit == self.spade_suit:
            suit_to_bid = self.spade_suit
        else:
            suit_to_bid = self.bid_one.denomination
        return suit_to_bid

    def _get_suit_with_five_four(self):
        """Return suit with 5/4 hands."""
        if self.bid_one.denomination == self.longest_suit:
            suit = self.second_suit
            if self.shape[1] == 4 and self.shape[2] == 4:
                suit = self.cheaper_suit(self.ordered_holding[1][1],
                                         self.ordered_holding[2][1])
            if not self.can_bid_suit(suit):
                suit = self.longest_suit
        else:
            suit = self.longest_suit
            if suit in self.opponents_suits:
                suit = self.second_suit
        return suit

    def _cheapest_four_card_suit(self):
        """Return the cheapest 4 card suit."""
        suits = []
        for suit in self.suits:
            if self.suit_length(suit) == 4:
                suits.append(suit)
        cheapest = None
        for suit in suits:
            if cheapest:
                if suit < cheapest:
                    cheapest = suit
            else:
                cheapest = suit
        return cheapest

    def _balanced_bid_level(self):
        """Return bid level for balanced rebids."""
        bid_level = 0
        if self.nt_level == 1:
            if self.hcp >= 19:
                bid_level = 3
            elif self.hcp >= 17:
                bid_level = 2
            else:
                bid_level = 1
        elif self.nt_level == 2:
            if self._has_seventeen_points_and_no_support_from_responder():
                bid_level = 3
            elif self.hcp >= 18 and self.responder_bid_one.level == 2:
                bid_level = 3
            else:
                bid_level = 2
        if bid_level == 0 and self._balanced_jump():
            bid_level = 3
        return bid_level

    def _select_suit_for_four_four_four_one(self):
        """Select suit with 4441 hands after partner bids singleton suit."""
        singleton_suit = self.suit_shape[3]
        rank = singleton_suit.rank
        rank = (rank+1) % 4
        if self.suits[rank] in self.opponents_suits:
            rank = (rank+1) % 4
            if rank == self.bid_one.denomination.rank:
                rank = (rank+1) % 4
        suit = self.suits[rank]
        return suit

    # Various boolean tests

    def _balanced_jump(self):
        """Return True if there has been a jump bid."""
        if self.overcaller_bid_one.is_value_call:
            result = self.is_jump(self.overcaller_bid_one, self.responder_bid_one)
        else:
            result = self.is_jump(self.bid_one, self.responder_bid_one)
        return result

    def _weak_and_able_to_repeat_suit(self, cannot_show_second_suit, responder_jumped):
        """Return True if weak and able to repeat suit"""
        result = (cannot_show_second_suit and
                  self.hcp <= 14 and
                  not responder_jumped and
                  (not self.overcall_made or
                   self.shape[0] >= 6))
        return result

    def _has_strong_minor_responder_has_jumped(self):
        """Return True with strong hand after partner jumps and no major."""
        result = (self.hcp >= 16 and
                  self.is_jump(self.bid_one, self.responder_bid_one) and
                  self.bid_one.denomination.is_minor and
                  self.responder_bid_one.denomination.is_minor and
                  not self.overcaller_bid_one.is_value_call)
        return result

    def _competitive_auction_weak_with_minor(self):
        """Return True if competitive auction, no support and minor."""
        result = ((self.advancer_bid_one.is_value_call or
                   self.overcaller_bid_one.is_nt) and
                  self.bid_one.denomination.is_minor and
                  self.hcp <= 13 and
                  self.shape[0] <= 5)
        return result

    def _competitive_auction_with_support_for_responder(self):
        """Return True if competitive auction and support for partner's major."""
        result = ((self.overcaller_bid_one.is_value_call or
                   self.advancer_bid_one.is_value_call) and
                  self.responder_bid_one.denomination.is_major and
                  self.responder_bid_one.level >= 2 and
                  self.suit_length(self.responder_bid_one.denomination) >= 3)
        return result

    def _responder_has_bid_nt_game_over_minor(self):
        """Return True of responder bid 3NT over a minor."""
        result = (self.responder_bid_one.name == '3NT' and
                  self.bid_one.denomination.is_minor)
        return result

    def _is_shapely_intermediate_hand(self):
        """Return True if two suits and 14+ points."""
        result = (self.shape[0] + self.shape[1] >= 9 and
                  (self.responder_bid_one.name != '1NT' or
                   self.hcp >= 14))
        return result

    def _repeatable_five_card_suit(self):
        """Return True if weak with repeatable five card suit."""
        first_suit = self.longest_suit
        level = self.next_level(first_suit)
        result = (self.hcp >= 16 and
                  self.shape[0] >= 5 and level <= 2 and
                  self.suit_points(first_suit) >= 5)
        return result

    def _weak_five_four(self):
        """Return True if weak but biddable 5/4."""
        second_suit = self.second_suit
        result = (self.hcp >= 12 and
                  self.five_four and
                  second_suit not in self.opponents_suits)
        return result

    def _three_card_support_for_responder_overcall_made(self):
        """Return True with support for responder and overcall made."""
        result = (self.overcall_made and
                  not self.overcaller_bid_one.is_double and
                  self.hcp == 14 and
                  self.suit_length(self.responder_bid_one.denomination) >= 3)
        return result

    def _four_card_support_for_responder_overcall_made(self):
        """Return True with support for responder and overcall made."""
        result = (self.hcp == 13 and
                  self.suit_length(self.responder_bid_one.denomination) >= 4 and
                  self.overcall_made and
                  not self.overcaller_bid_one.is_double)
        return result

    def _strong_with_second_suit(self, level):
        """Return True if strong and has biddable second suit."""
        second_suit = self.second_suit
        result = (self.hcp >= 16 and
                  self.five_four and
                  (self.shape[0] <= 5 or
                   self.suit_points(second_suit) >= 6) and
                  second_suit != self.overcaller_bid_one.denomination and
                  second_suit != self.advancer_bid_one.denomination and
                  self.overcaller_bid_one.denomination == self.advancer_bid_one.denomination and
                  level <= 3)
        return result

    def _is_strong_with_five_five(self, second_suit):
        """"Return True with 16 points and two five card suits."""
        result = (self.hcp >= 16 and
                  self.five_five_or_better and
                  second_suit not in self.opponents_suits)
        return result

    def _is_strong_with_five_four(self, second_suit):
        """"Return True with 16 points and five/four."""
        opening_next_level = self.next_level(self.my_last_bid.denomination)
        result = (self.hcp >= 16 and
                  self.five_four and
                  self.next_level(second_suit) <= opening_next_level and
                  self.next_level(second_suit) <= 3 and
                  second_suit not in self.opponents_suits)
        return result

    def _six_card_suit_weak(self):
        """Return True if weak with six card suit."""
        first_suit = self.longest_suit
        level = self.next_level(first_suit)
        result = (self.shape[0] >= 6 and
                  12 <= self.hcp <= 15 and
                  level <= 3 and
                  (level <= 2 or
                   self.suit_points(first_suit) >= 5) and
                  Bid(self.bid_history[-1]).is_pass)
        return result

    def _strong_and_balanced(self):
        """Return True if strong, balanced and got stoppers."""
        result = (self.hcp >= 17 and
                  self.is_balanced and
                  self.stoppers_in_bid_suits and
                  not self.overcaller_bid_one.is_nt and
                  (self.responder_bid_one.is_value_call or
                   self.nt_level <= 1))
        return result

    def _weak_six_cards(self):
        """Return True if weak with six card suit."""
        result = (self.hcp >= 12 and
                  self.shape[0] >= 6 and
                  self.suit_points(self.longest_suit) >= 5 and
                  self.longest_suit not in self.opponents_suits and
                  self.next_level(self.longest_suit) <= 3)
        return result

    def _can_rebid_five_card_suit_at_two_level(self):
        """Return True if 5 card suit can be rebid."""
        result = (self.shape[0] == 5 and
                  self.hcp >= 12 and
                  self.next_level(self.longest_suit) <= 2 and
                  not self.bid_one.is_nt and
                  not self.overcaller_bid_one.is_nt)
        return result

    def _can_rebid_seven_card_suit_at_three_level(self):
        """Return True if 7 card suit can be rebid."""
        result = (self.shape[0] >= 7 and
                  self.next_level(self.longest_suit) <= 3)
        return result

    def _overcaller_doubled_and_advancer_bid(self):
        """Return True if overcaller has doubled and advancer has bid."""
        result = (self.overcaller_bid_one.is_double and
                  not self.advancer_bid_one.is_pass and
                  self.hcp <= 15)
        return result

    def _can_rebid_spades(self, level):
        """Return True if opener can rebid spades."""
        result = False
        if self.responder_bid_one.name == '3S' and self.spades >= 3:
            result = True
        elif (self.spades >= 2 and
              self.advancer_bid_one.is_value_call and
              self.spade_suit not in self.opponents_suits and
              level <= 4):
            result = True
        if self.next_level(self.spade_suit) > 4:
            return False
        return result

    def _responder_shows_support_or_can_support_responder(self):
        """Return True if responder has shown support."""
        result = (self.responder_bid_one.denomination == self.bid_one.denomination or
                  self.suit_length(self.responder_bid_one.denomination) >= 4 or
                  (self.responder_bid_one.level == 2 and
                   self.responder_bid_one.is_major and
                   self.suit_length(self.responder_bid_one.denomination) >= 3))
        return result

    def _can_support_responders_major(self):
        """Return True can support responder's major."""
        result = (self.responder_bid_one.level >= 2 and
                  self.suit_length(self.responder_bid_one.denomination) >= 3 and
                  self.responder_bid_one.denomination.is_major and
                  self.overcall_made)
        return result

    def _has_six_card_minor_and_eighteen_points(self):
        """Return True with 18 points and six card suit."""
        result = (self.hcp >= 18 and
                  self.responder_bid_one.denomination.is_minor and
                  self.shape[0] >= 6 and
                  self.stoppers_in_bid_suits and
                  self.stoppers_in_unbid_suits and
                  self.nt_level <= 3)
        return result

    def _is_unbalanced_with_sixteen_points(self):
        """Return True if 16+ points and unbalanced."""
        result = (self.hcp >= 16 and
                  not self.is_balanced and
                  self .second_suit not in self.opponents_suits)
        return result

    def _can_support_nineteen_points(self):
        """Return True if 19+ points and support for responder."""
        result = (self.hcp >= 19 and
                  self.responder_bid_one.denomination == self.second_suit and
                  self.game_level(self.second_suit) >= self.next_level(self.second_suit))
        return result

    def _can_support_seventeen_points_and_void(self):
        """Return True if 17+ points and support for responder and a void."""
        result = (self.hcp >= 17 and
                  self.responder_bid_one.denomination == self.second_suit and
                  self.shape[3] == 0 and
                  self.game_level(self.second_suit) >= self.next_level(self.second_suit))
        return result

    def _suit_is_major_and_eighteen_points(self, suit_to_bid):
        """Return True if 18+ points and level <= 3."""
        result = (self.next_level(suit_to_bid) <= 3 and
                  suit_to_bid.is_major and
                  self.hcp >= 18)
        return result

    def _responder_support_with_jump(self):
        """Return True if responder supports and has jumped."""
        result = (self.responder_bid_one.denomination == self.bid_one.denomination and
                  self.is_jump(self.bid_one, self.responder_bid_one) and
                  self.nt_level <= 3)
        return result

    def _can_repeat_suit_and_seventeen_points(self, suit_to_bid):
        """Return True if can repeat opening suit and 17+ points."""
        result = (suit_to_bid == self.bid_one.denomination and
                  self.hcp >= 17 and
                  self.stoppers_in_bid_suits)
        return result

    def _has_five_four_and_sixteen_points(self, suit_to_bid):
        """Return True if 5/4 and 16+ points."""
        result = (suit_to_bid == self.bid_one.denomination and
                  self.hcp >= 16 and
                  self.five_four_or_better)
        return result

    def _five_four_strong_test_nt(self, test_bid):
        """Return True if NT bid is allowed."""
        responder_jumped = self.jump_bid_made(self.responder_bid_one)
        result = (test_bid.level == 3 and
                  self.nt_level <= 3 and
                  self.shape[0] < 6 and
                  self.is_balanced and
                  self.stoppers_in_bid_suits and
                  not responder_jumped)
        return result

    def _weak_five_four_with_weak_suit(self, suit_to_bid):
        """Return True if suit too weak to rebid."""
        value_one = (suit_to_bid == self.bid_one.denomination and
                     self.overcall_made and
                     not self.responder_bid_one.is_value_call and
                     self.suit_points(suit_to_bid) <= 4)
        value_two = (suit_to_bid == self.bid_one.denomination and
                     (self.overcaller_bid_one.is_nt or
                      self.advancer_bid_one.is_nt) and
                     self.suit_points(suit_to_bid) <= 4)
        result = (value_one or value_two and
                  (self.responder_bid_one.is_pass or
                   self.bid_history[-2] != 'P'))
        return result

    def _can_bid_at_appropriate_level(self, suit_to_bid, level):
        """Return True if possible to bid at appropriate level."""
        result = (level <= 2 or
                  ((self.hcp >= 13 or
                   suit_to_bid == self.bid_one.denomination) and
                   self.responder_bid_one.level == 2))
        return result

    def _weak_five_four_consider_bid(self, level):
        """Return True if a sound bid is possible for weak 5/4."""
        result = (level <= 2 or self.shape[0] >= 6 or
                  (self.responder_bid_one.is_nt and level <= 3) or
                  not self.overcall_made or
                  (self.jump_bid_made(self.responder_bid_one) and
                   self.responder_bid_one.denomination != self.bid_one.denomination))
        return result

    def _weak_after_one_nt_and_barrier_broken(self, cannot_show_second_suit):
        """Return True if barrier broken after responder bids 1NT."""
        result = (self.hcp <= 15 and
                  cannot_show_second_suit and
                  self.responder_bid_one.name == '1NT')
        return result

    def _six_four_responder_at_level_two(self):
        """"Return True if 6/4 and responder at level 2."""
        result = (self.six_four and
                  self.responder_bid_one.level == 2 and
                  self.levels_to_bid(self.bid_one,
                                     self.next_level_bid(self.second_suit)) <= 2 and
                  self.second_suit not in self.opponents_suits)
        return result

    def _strong_or_can_bid_at_level_two(self, suit_to_bid):
        """Return True if can bid at level 2 or strong."""
        result = (self.next_level(suit_to_bid) <= 2 or
                  self.hcp >= 16 or
                  (self.overcall_made and
                   self.suit_length(self.overcaller_bid_one.denomination) == 0))
        return result

    def _strong_five_four_or_better(self):
        """Return True if strong and 5/4 or better."""
        result = (self.hcp >= 15 and
                  self.five_four_or_better and
                  self.second_suit not in self.opponents_suits)
        return result

    def _is_strong_with_seven_card_major(self):
        """Return True if strong with seven card major."""
        result = (self.hcp >= 16 and
                  self.shape[0] >= 7 and
                  self.longest_suit.is_major and
                  self.next_level(self.longest_suit) <= self.longest_suit.game_level)
        return result

    def _is_strong_six_four_with_major(self):
        """Return True if strong with six card major."""
        result = (self.hcp >= 16 and
                  self.second_suit.is_major and
                  self.second_suit not in self.opponents_suits and
                  self.shape[1] >= 4)
        return result

    def _weak_with_overcall_or_next_level_three(self):
        """Return True if overcall or next level greater than 2."""
        result = ((self.overcall_made and
                   self.hcp <= 15) or
                  self.next_level(self.longest_suit) > 2)
        return result

    def _has_minor_can_support_responders_major(self):
        """Return True if suit is a minor and can support responder's major."""
        result = (self.longest_suit.is_minor and
                  self.responder_bid_one.denomination.is_major and
                  self.suit_length(self.responder_bid_one.denomination) >= 4)
        return result

    def _has_six_card_major_and_responder_bid_two_nt(self):
        """Return True if six card major after responder bids NT."""
        result = (self.responder_bid_one.name == '2NT' and
                  self.shape[0] >= 6 and
                  self.longest_suit.is_major)
        return result

    def _is_strong_with_solid_seven_card_suit(self):
        """Return True if strong with solid 7 card suit."""
        result = (self.hcp >= 15 and
                  self.shape[0] >= 7 and
                  self.solid_suit_honours(self.longest_suit))
        return result

    def _has_five_card_suit_fifteen_points_level_two(self):
        """Return True if intermediate with 5 card suit."""
        result = (self.hcp >= 15 and
                  self.shape[0] >= 5 and
                  self.next_level(self.longest_suit) <= 2)
        return result

    def _has_seven_card_suit_and_weak(self):
        """Return True if weak with 7 card suit."""
        result = (self.hcp >= 11 and
                  self.shape[0] >= 7 and
                  self.next_level(self.longest_suit) <= 3)
        return result

    def _has_six_card_suit_responder_at_level_two(self):
        """Return True if 6 card suit and responder at level 2."""
        result = (self.shape[0] >= 6 and
                  self.responder_bid_one.level >= 2 and
                  self.next_level(self.longest_suit) <= 3)
        return result

    def _has_fifteen_points_and_level_is_one(self, level):
        """Return True if 15+ points and level is 1."""
        result = self.hcp >= 15 and level >= self.nt_level
        return result

    def _barrier_would_break_and_fewer_that_sixteen(self, suit, test_bid):
        """Return True if barrier broken and fewer than 16 points."""
        cannot_show_second_suit = (self.barrier_is_broken(self.bid_one, test_bid) and
                                   not self.is_jump(self.bid_one, self.responder_bid_one))
        result = ((self.hcp <= 16 and cannot_show_second_suit) or suit in self.opponents_suits)
        return result

    def _strong_can_bid_nt(self, bid_level):
        """Return True if it appropriate to bid NT."""
        result = (0 <= bid_level <= 3 and
                  bid_level >= self.nt_level and
                  (not self._weak_partner() or self.hcp >= 18))
        return result

    def _no_fit_fifteen_points_responder_level_two(self):
        """Return True with 15+points and no fit and responder at level 2."""
        result = (self.responder_bid_one.denomination != self.bid_one.denomination and
                  self.responder_bid_one.level >= 2 and
                  self.hcp >= 15 and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _has_seventeen_points_and_no_support_from_responder(self):
        """Return True with 17+ points and no support."""
        result = (self.hcp >= 17 and
                  self.bid_one.denomination != self.responder_bid_one.denomination and
                  not self.overcall_made)
        return result

    def _is_balanced_or_no_fit_with_responder(self):
        """Return True if balanced or no fit with responder."""
        result = ((self.is_balanced or
                   self.suit_length(self.responder_bid_one.denomination) <= 2) and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _weak_partner(self):
        """Return True if partner has indicated a weak hand."""
        result = (self.responder_bid_one.level == 1 and
                  (self.overcaller_bid_one.level == 2 or
                   self.overcaller_bid_one.is_double or
                   self.advancer_bid_one.is_nt or
                   self.advancer_bid_one.level == 2) or
                  (self._responder_bids_openers_suit_at_lowest_level() and
                   self.hcp < 17))
        return result

    def _responder_bids_openers_suit_at_lowest_level(self):
        """Return True if responder bids opener's suit at lowest level."""
        result = (self.my_last_bid.denomination == self.responder_bid_one.denomination and
                  self.my_last_bid.level+1 == self.responder_bid_one.level)
        return result

    def _has_six_card_major_and_can_bid_game(self):
        """Return True with 6 card major and below game level."""
        result = (self.shape[0] >= 6 and
                  self.longest_suit.is_major and
                  self.next_level(self.longest_suit) <= 4)
        return result

    def _has_six_card_major_and_can_bid_at_three_level(self):
        """Return True with 6 card major and can_bid_at 3 level."""
        result = (self.shape[0] >= 6 and
                  self.longest_suit.is_major and
                  self.next_level(self.bid_one.denomination) <= 3)
        return result

    def _is_balanced_minor_suit_can_bid_nt_game(self):
        """Return True if suit is manor, balanced and can bid 3NT."""
        result = (self.bid_one.denomination.is_minor and
                  self._is_balanced_can_bid_nt_game())
        return result

    def _is_balanced_can_bid_nt_game(self):
        result = (self.is_balanced and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _can_bid_two_nt(self):
        """Return True if can bid 2NT."""
        result = ((self.hcp >= 17 or self.nt_level == 2) and
                  self.nt_level <= 2 and
                  self.stoppers_in_bid_suits)
        return result

    def _powerful_and_has_four_cards_in_unbid_major(self, unbid_major):
        """Return True if powerful hand with 4 card unbid major."""
        result = (unbid_major is not None and
                  unbid_major not in self.opponents_suits and
                  (self.five_four_or_better or
                   self.my_last_bid.is_minor))
        return result

    def _weak_overcall_responder_level_one(self, ):
        """Return True if weak and responder has bid at level 1."""
        result = (self.hcp <= 12 and
                  self.overcall_made and
                  self.responder_bid_one.level == 1)
        return result

    def _fffo_strong_four_card_support(self):
        """Return True if strong and can support partner suit."""
        result = (self.responder_bid_one.level == 2 and
                  self.shape == [4, 4, 4, 1] and
                  self.suit_length(self.responder_bid_one.denomination) >= 4 and
                  self.hcp >= 17)
        return result

    def _can_bid_three_nt(self):
        """Return True if can support NTs."""
        result = (self.responder_bid_one.is_nt and
                  self.shape[0] >= 5 and
                  self.nt_level <= 3 and
                  self.stoppers_in_bid_suits and
                  self.hcp >= 12)
        return result

    def _no_biddable_second_suit_and_support_for_partner(self):
        """Return True if Support for responder and second suit not biddable major."""
        suit = self.responder_bid_one.denomination
        result = (self.responder_bid_one.level >= 2 and
                  self.hcp >= 16 and
                  self.suit_length(suit) >= 4 and
                  self.next_level(suit) <= suit.game_level and
                  not (self.second_suit.is_major and self.shape[1] >= 4))
        return result

    def _can_bid_second_suit_after_nt(self):
        """Return True if can bid second suit after a 2NT response."""
        result = (self.five_four and
                  self.partner_bid_one.name == '2NT' and
                  self.second_suit.rank < self.longest_suit.rank and
                  self.second_suit not in self.opponents_suits)
        return result

    def _has_six_card_major_and_responder_bid_one_nt(self):
        """Return True if xxx."""
        result = (self.hcp >= 15 and
                  self.shape[0] >= 6 and
                  self.longest_suit.is_major and
                  self.responder_bid_one.name == '1NT')
        return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result
