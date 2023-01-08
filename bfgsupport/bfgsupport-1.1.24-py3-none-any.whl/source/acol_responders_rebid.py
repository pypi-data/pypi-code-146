""" Bid for Game
    Responder's Rebid class
"""

import inspect
from .bridge_tools import Bid, Pass, HandSuit
from .blackwood import Blackwood
from .hand import Hand
from bridgeobjects import Denomination


class RespondersRebid(Hand):
    """Responder's Rebid class."""
    def __init__(self, hand_cards, board):
        super(RespondersRebid, self).__init__(hand_cards, board)
        self.overcaller_bid_one = Bid(self.bid_history[1])
        self.overcallers_rebid = Bid(self.bid_history[5])
        self.barrier_broken = self.barrier_is_broken(self.opener_bid_one,
                                                     self.opener_bid_two)
        self.trace = 0

    def suggested_bid(self):
        """Direct control to relevant method and return a Bid object."""
        if self._weak_two_opening():
            bid = self._after_weak_opening()
        elif self._has_six_card_suit_and_opener_passed():
            bid = self.next_level_bid(self.longest_suit, '0310')
        elif self.opener_bid_two.is_pass:
            bid = self._opener_has_passed()
        elif self.opener_bid_two.name == '4NT':
            bid = self._response_to_blackwood()
        elif self.bid_one.name == '4NT':
            bid = self._after_responders_blackwood()
        elif self._opener_at_game_but_can_show_preference():
            suit_to_bid = self._suit_preference()
            if suit_to_bid == self.opener_bid_one.denomination:
                bid = self.next_level_bid(suit_to_bid, '0896')
            else:
                bid = Pass('0897')
        elif self._game_has_been_bid_by_opposition():
            bid = Pass('0311')
        elif self._has_fifteen_points_and_opener_has_rebid_three_nt():
            if self.opener_bid_one.name == '2C':
                bid = self.nt_bid(7, '0083')
            else:
                bid = self.nt_bid(6, '0520')
        elif self._has_fourteen_with_openers_twenty_three_in_nt():
            bid = self.nt_bid(7, '0158')
        elif self._has_twelve_with_openers_nineteen_in_nt():
            bid = self.nt_bid(6, '0312')
        elif self._has_six_card_suit_with_openers_nineteen_in_nt():
            bid = self.next_level_bid(self.longest_suit, '0313')
        elif self.opener_bid_two.name == '3NT' and self.hcp >= 19:
            bid = self.nt_bid(6, '0314')
        elif self.opener_bid_one.name == '2C' and self.hcp >= 9:
            bid = self.nt_bid(4, '0053')
        elif self._thirteen_points_support_and_opener_in_game_in_major():
            bid = self.nt_bid(4, '0261')
        elif (self.opener_bid_one.name == '2NT' and
                self.five_five_or_better):
            suit = self.second_suit
            bid = self.next_level_bid(suit, '0683')
        elif self.opener_bid_two.is_game:
            bid = Pass('0315')
        elif self.opener_bid_one.is_nt:
            bid = self._after_nt_opening()
        else:
            bid = self._after_suit_opening()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_weak_opening(self):
        """Rebid after a weak opening."""
        if self._opener_has_passed_can_compete():
            bid = self._weak_opening_and_competitive_auction()
        elif self._has_sixteen_and_six_card_suit():
            bid = self.next_level_bid(self.longest_suit, '0316')
        elif self._has_sixteen_and_three_card_support():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0317')
        elif (self.hcp >= 15 and self.shape[0] >= 5 and self.opener_bid_two.denomination == self.longest_suit):
            bid = self.bid_to_game(self.longest_suit, '0924')
        else:
            bid = Pass('0318')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_opening_and_competitive_auction(self):
        """Rebid after a weak opening and competitive auction."""
        if self._has_seventeen_and_three_card_support_can_bid_game():
            bid = self.suit_bid(4, self.opener_bid_one.denomination, '0320')
        elif self._can_rebid_openers_suit():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0319')
        else:
            bid = Pass('0321')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_nt_opening(self):
        """Rebid after NT opening."""
        if self._opener_has_responded_to_stayman():
            bid = self._after_stayman()
        elif self._opener_has_bid_major_at_three_level_thirteen_points():
            bid = self._strong_after_nt_opening()
        elif self._has_six_card_suit_ten_points_and_opener_support():
            bid = self.bid_to_game(self.bid_one.denomination, '0900')
        elif self._support_for_openers_major_after_nt_opening():
            bid = self.bid_to_game(self.opener_bid_two.denomination, '0800')
        else:
            bid = Pass('0322')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _strong_after_nt_opening(self):
        """Return bid after 1NT opening with opening hand."""
        if self.suit_length(self.opener_bid_two.denomination) >= 3:
            bid = self.next_level_bid(self.opener_bid_two.denomination, '0323')
        elif self.nt_level <= 3:
            bid = self.nt_bid(3, '0324')
        else:
            bid = Pass('0325')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman(self):
        """Return bid after Stayman."""
        if self.opener_bid_one.name == '2NT':
            bid = self._after_stayman_two_nt_opening()
        elif self.opener_bid_two.name == '2NT':
            bid = self._after_stayman_two_nt_rebid()
        elif (self.opener_bid_two.denomination.is_major and
              self.suit_length(self.opener_bid_two.denomination) >= 4):
            bid = self._after_stayman_four_card_major()
        elif self.hcp >= 12 and not self.is_semi_balanced:
            bid = self._after_stayman_other_major()
        else:
            bid = self._after_stayman_no_four_card_major()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_other_major(self):
        """Return bid after Stayman with distribution."""
        if self._opener_bids_hearts_but_fewer_than_four_hearts():
            bid = self.suit_bid(3, self.spade_suit, '0326')
        else:
            bid = self.nt_bid(3, '0327')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_four_card_major(self):
        """Return bid after Stayman with 4 card major."""
        if self.opener_bid_one.name == "1NT":
            if self.suit_length(self.opener_bid_two.denomination) >= 5:
                bid = self.bid_to_game(self.opener_bid_two.denomination, '0814')
            else:
                bid = self._after_stayman_level_two_four_card_major()
        else:
            bid = self._after_stayman_level_three_four_card_major()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_level_two_four_card_major(self):
        """Return bid after Stayman with 4 card major at two level."""
        if 11 <= self.hand_value_points(self.opener_bid_two.denomination) <= 12:
            level = 3
        else:
            level = 4
        bid = self.suit_bid(level, self.opener_bid_two.denomination, '0328', True)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_level_three_four_card_major(self):
        """Return bid after Stayman with 4 card major at three level."""
        if self.suit_length(self.opener_bid_two.denomination) >= 4:
            bid = self.suit_bid(4, self.opener_bid_two.denomination, '0329')
        else:
            bid = self.nt_bid(3, '0330')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_no_four_card_major(self):
        """Return bid after Stayman with no 4 card major."""
        if 11 <= self.hcp <= 12:
            level = 2
        else:
            level = 3

        if level >= self.nt_level:
            bid = self.nt_bid(level, '0331')
        else:
            bid = Pass('0332')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_two_nt_opening(self):
        """Return bid after 2NT opening Stayman."""
        # import pdb; pdb.set_trace()
        suit = self.opener_bid_two.denomination
        if self._has_four_cards_in_openers_major_fewer_than_ten_points():
            bid = self.bid_to_game(suit, '0918')
        elif self.hcp >= 12:
            bid = Bid('6NT', '0917')
        elif self.hcp >= 4:
            bid = Bid('3NT', '0919')
        else:
            bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_stayman_two_nt_rebid(self):
        """Return bid after 2NT rebid Stayman."""
        selected_suit = self._get_suit_if_five_five()
        if self.hcp >= 13 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0333')
        elif self._overcall_made_has_five_five(selected_suit):
            bid = self.next_level_bid(selected_suit, '0334')
        elif self.hcp >= 11 and self.is_balanced and self.nt_level <= 3:
            bid = self.nt_bid(3, '0521')
        elif self.hcp >= 12 and self.shape[1] >= 5 and self.longest_suit.is_major and self.second_suit.is_major:
            bid = self.heart_bid(4, '0910')
        else:
            bid = Pass('0336')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _response_to_blackwood(self):
        """Bid after 4NT."""
        bid = Blackwood(self.cards, self.board).count_aces()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_responders_blackwood(self):
        """Select contract after responder initiates Blackwood."""
        aces = self.aces
        opener_bid_two_name = self.opener_bid_two.name
        if (self.suit_length(self.opener_bid_one.denomination) >= 4 and
                self.shape[3] <= 2):
            slam_suit = self.opener_bid_one.denomination
        elif self.is_balanced:
            slam_suit = self.no_trumps
        else:
            slam_suit = self._suit_preference()
        if opener_bid_two_name == '5C':
            if aces == 0:
                aces = 4
        elif opener_bid_two_name == '5D':
            aces += 1
        elif opener_bid_two_name == '5H':
            aces += 2
        elif opener_bid_two_name == '5S':
            aces += 3
        if self.nt_level >= 6:
            bid = Pass('000')
        elif aces == 4:
            bid = self.nt_bid(5, '0337')
        elif aces == 3:
            bid = self.suit_bid(6, slam_suit, '0338')
        else:
            if slam_suit == self.no_trumps:
                bid = Pass('0339')
            else:
                if opener_bid_two_name == self.suit_bid(5, slam_suit).name:
                    bid = Pass('0340')
                else:
                    bid = self.next_level_bid(slam_suit, '0341')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_suit_opening(self):
        """Select process after suit opening."""
        if self.opener_bid_one.name == '2C':
            bid = self._opener_bid_two_clubs()
        elif (self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                self.opener_bid_two.is_suit_call):
            bid = self._opener_has_repeated_suit()
        elif (self.opener_bid_two.denomination == self.bid_one.denomination and
                self.opener_bid_two.is_suit_call):
            bid = self._opener_has_supported_responder()
        else:
            bid = self._after_suit_opening_no_match()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_bid_two_clubs(self):
        """Return bid after opener has bid 2C."""
        if self.opener_bid_two.name == '2NT':
            bid = self._opener_bid_two_nt_after_two_clubs()
        elif self.hcp <= 9:
            bid = self._fewer_that_ten_points_after_two_club_opening()
        else:
            bid = self.nt_bid(4, '0345')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_bid_two_nt_after_two_clubs(self):
        """Return bid if opener has bid 2NT after 2C."""
        if self.hcp <= 2:
            bid = Pass('0342')
        elif self.shape[1] >= 5:
            bid = self.next_level_bid(self.second_suit, '0854')
        elif self.shape[0] >= 5:
            bid = self.next_level_bid(self.longest_suit, '0002')
        elif self.is_semi_balanced and self.nt_level <= 3 and self.four_card_major_or_better and self.next_level(self.club_suit) <= 3:
            bid = self.club_bid(3, '0904')
        elif self.is_semi_balanced and self.nt_level <= 3:
            bid = self.nt_bid(3, '0343')
        else:
            bid = self.next_level_bid(self.longest_suit, '0344')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _fewer_that_ten_points_after_two_club_opening(self):
        """Return bid if fewer than 10 points after 2C opening."""
        if self.suit_length(self.opener_bid_two.denomination) >= 3:
            if self.opener_bid_two.denomination.is_major:
                bid = self.bid_to_game(self.opener_bid_two.denomination, '0000')
            else:
                bid = self.next_level_bid(self.opener_bid_two.denomination, '0049')
        elif self.is_semi_balanced and self.nt_level <= 3:
            bid = self.nt_bid(3, '0346')
        elif (self.longest_suit not in self.opponents_suits and
                (self.next_level(self.longest_suit) <= 3 or
                    self.shape[0] >= 7)):
            bid = self.next_level_bid(self.longest_suit, '0347')
        else:
            bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _after_suit_opening_no_match(self):
        """Bid after suit opening no match opener/responder."""
        if self.bid_one.is_nt:
            if self.opener_bid_two.is_nt:
                bid = self._opener_nt_after_nt_response()
            else:
                bid = self._opener_changed_suit_after_nt()
        else:
            if self.opener_bid_two.is_nt:
                bid = self._opener_nt_after_suit_response()
            elif self._opener_has_has_doubled_and_five_card_suit():
                bid = self.next_level_bid(self.longest_suit, '0349')
            else:
                bid = self._three_suits_bid()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_has_repeated_suit(self):
        """Respond after partner has repeated suit."""
        if self._has_bid_two_nt_and_opener_bids_minor():
            bid = Pass('0351')
        elif self._responder_jumped_support_fewer_than_five_points():
            bid = Pass('0352')
        elif self._opener_has_jumped_or_level_is_three():
            bid = self._opener_has_jumped_or_bid_at_level_three()
        elif not self.my_last_bid.is_pass:
            bid = self._no_jump_bid()
        else:
            bid = Pass('0184')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_has_jumped_or_bid_at_level_three(self):
        """Return a bid if opener has jumped or bid at the three level."""
        if self.opener_bid_one.denomination == self.bid_one.denomination:
            if (self.hand_value_points(self.opener_bid_one.denomination) >= 8 and
                    self.bid_one.denomination.is_major and
                    not self.overcall_made):
                bid = self.next_level_bid(self.opener_bid_one.denomination, '0353', )
            else:
                bid = Pass('0354')
        elif (self.bid_one.level == 2 and
                self.suit_length(self.opener_bid_one.denomination) <= 2):
            bid = self._no_jump_bid()
        else:
            bid = self._opener_jumped()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_jump_bid(self):
        """Respond after opener has bid with no jump."""
        if self.opener_bid_one.level > 1:
            bid = Pass('0355')
        elif self._has_fewer_than_nine_points_and_passed_or_one_nt():
            bid = Pass('0356')
        elif self.suit_length(self.opener_bid_one.denomination) >= 3:
            bid = self._no_jump_bid_support_for_opener()
        elif self._has_six_card_suit_and_can_bid():
            bid = self._responder_long_suit()
        elif self._is_weak_and_shortage_in_openers_suit():
            bid = Pass('0358')
        elif self._opener_repeats_major_at_level_three_balanced():
            bid = self.next_nt_bid('0473')
        elif self._opener_bids_major_at_level_three_can_support():
            bid = self.suit_bid(4, self.opener_bid_two.denomination, '0357')
        elif self._has_five_four_and_opener_at_three_level():
            bid = self.next_level_bid(self.second_suit, '0359')
        elif self.five_four_or_better:
            bid = self._no_jump_bid_no_support_five_four()
        elif self.stoppers_in_bid_suits:
            bid = self._no_jump_bid_no_support_balanced()
        elif self._intermediate_balanced_cannot_rebid_suit():
            bid = self.nt_bid(3, '0511')
        elif self.longest_suit not in self.opponents_suits and self.shape[0] >= 5:
            bid = self.next_level_bid(self.longest_suit, '0360')
        elif self.opener_bid_one.denomination == self.opener_bid_two.denomination:
            bid = Pass('0769')
        else:
            bid = self.next_nt_bid('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_jump_bid_support_for_opener(self):
        """Bid with no jump and 3+ card support for partner."""
        level = self.opener_bid_two.level
        next_level = self.next_level(self.opener_bid_one.denomination)
        level_allowed = next_level <= level + 1

        if self.hcp >= 13:
            nt_level = 3
        else:
            nt_level = 2

        if self.hand_value_points(self.opener_bid_one.denomination) <= 9:
            bid = Pass('0361')
        elif self._is_weak_openers_suit_is_minor():
            bid = self.next_nt_bid('0262')
        elif self._intermediate_has_four_card_major_and_opener_in_minor():
            bid = self.next_level_bid(self.second_suit, '0902')
        elif self._strong_has_six_card_major_and_opener_in_minor():
            bid = self.bid_to_game(self.longest_suit, '0348')
        elif self._weak_has_six_card_major_and_opener_in_minor():
            bid = self.next_level_bid(self.longest_suit, '0204', raise_level=1)
        elif self.suit_length(self.partner_bid_one.denomination) >= 5:
            bid = self.bid_to_game(self.partner_bid_one.denomination, '0782')
        elif self._weak_has_stoppers_and_opener_in_minor(nt_level):
            bid = self.nt_bid(nt_level, '0881')
        elif (self.hand_value_points(self.opener_bid_one.denomination) <= 12 and
                level_allowed):
            bid = self.suit_bid(level + 1, self.opener_bid_one.denomination, '0362')
        else:
            bid = self._no_jump_bid_support_for_opener_strong()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_jump_bid_support_for_opener_strong(self):
        """Bid with no jump, string hand and 3+ card support for partner."""
        level = self.opener_bid_two.level
        if level >= 3:
            raise_level = level + 1
        else:
            raise_level = level + 2
        if self._intermediate_has_seven_car_major():
            bid = self.suit_bid(4, self.longest_suit, '0266')
        elif self._opener_in_minor_and_stoppers():
            bid = self.nt_bid(3, '0363')
        elif self.next_level(self.opener_bid_one.denomination) <= raise_level:
            bid = self.suit_bid(raise_level, self.opener_bid_one.denomination, '0364')
        else:
            bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_jump_bid_no_support_five_four(self):
        """Bid with no support for partner but 5/4 hand."""
        if self.hcp <= 14:
            raise_level = 0
        else:
            raise_level = 1
        if (self.longest_suit.is_major and
                self.second_suit.is_major and
                self.five_four_or_better and
                self.second_suit not in self.opponents_suits and
                self.next_level(self.second_suit) <= 2):
            bid = self.next_level_bid(self.second_suit, '0797', raise_level=raise_level)
        elif self.hcp <= 10:
            bid = Pass('0365')
        elif self._opener_in_minor_distributional_with_stoppers():
            bid = self.nt_bid(3, '0366')
        elif self.second_suit in self.opponents_suits and self.hcp <= 12:
            bid = self.next_nt_bid('0367')
        elif self.second_suit in self.opponents_suits and self.hcp >= 13:
            bid = self.nt_bid(3, '0897')
        elif self.hcp <= 10 and self.next_level(self.second_suit) > 2:
            bid = self.next_nt_bid('0368')
        elif self.second_suit.is_minor and self.next_level(self.second_suit) == 4:
            bid = self.next_nt_bid('0595')
        else:
            bid = self.next_level_bid(self.second_suit, '0369', 0)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _no_jump_bid_no_support_balanced(self):
        """Bid with no support for partner but balanced hand."""
        if self.hcp <= 9 and self.shape[0] <= 7:
            bid = Pass('0370')
        elif self.shape[0] >= 8 and self.hcp >= 8:
            bid = self.next_level_bid(self.longest_suit, '0793')
        elif self.hcp <= 12 and self.nt_level <= 2:
            bid = self.nt_bid(2, '0371')
        elif self.hcp <= 19 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0372')
        elif self.hcp <= 20 and self.nt_level <= 4:
            bid = self.nt_bid(4, '0373')
        else:
            bid = Pass('0000')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_has_supported_responder(self):
        """Bid after opener has supported responder's suit."""
        if self.is_jump(self.bid_one, self.opener_bid_two):
            bid = self._opener_has_supported_responder_jump()
        else:
            bid = self._opener_has_supported_responder_no_jump()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_has_supported_responder_no_jump(self):
        """Bid after opener has supported suit."""
        suit_to_bid = self.bid_one.denomination
        if (self.bid_one.denomination.is_minor and
                self.suit_length(self.opener_bid_one.denomination) >= 3):
            suit_to_bid = self.opener_bid_one.denomination
        level = self.next_level(suit_to_bid)

        if self.hcp >= 20:
            bid = self.nt_bid(4, '0194')
        elif suit_to_bid.is_minor and self._can_bid_four_card_major():
            suit_to_bid = self.second_suit
            bid = self.next_level_bid(suit_to_bid, '0375')
        elif self.hcp >= 19:
            bid = self.suit_bid(6, suit_to_bid, '0113')
        elif (self.hcp >= 16 and
                self.suit_length(self.opener_bid_one.denomination) >= 4 and
                self.nt_level <= 4):
            bid = self.nt_bid(4, '0497')
        elif self.hcp >= 18:
            bid = self.bid_to_game(suit_to_bid, '0901')
        elif (self.hcp + self.distribution_points >= 13 and level <= 4 and
                self.hcp >= 13):
            bid = self.bid_to_game(suit_to_bid, '0876')
        elif (self.hcp + self.distribution_points >= 13 and level <= 4 and
                self.hcp >= 11):
            bid = self.suit_bid(4, suit_to_bid, '0376')
        elif self.hcp >= 9 and level <= 3:
            bid = self.suit_bid(3, suit_to_bid, '0377')
        elif self._opener_has_jumped_no_support():
            bid = self.bid_to_game(self.bid_one.denomination, '0378')
        else:
            bid = Pass('0379')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_has_supported_responder_jump(self):
        """Bid after opener has supported suit and jumped."""
        if self.longest_suit.is_minor and self._can_support_openers_major():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0500')
        elif (self.hcp >= 9 or
                (self.hcp >= 8 and self.suit_length(self.bid_one.denomination) >= 5)):
            bid = self.next_level_bid(self.bid_one.denomination, '0380')
        else:
            bid = Pass('0381')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_long_suit(self):
        """Bid with own long suit."""
        own_suit = self.longest_suit
        if self.hcp <= 9 and own_suit not in self.opponents_suits:
            bid = self.next_level_bid(own_suit, '0382', 0)
        elif self.hcp <= 12:
            bid = self._responder_long_suit_weak()
        else:
            bid = self._responder_long_suit_strong()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_long_suit_strong(self):
        """Bid with own long suit in strong hand."""
        if self.longest_suit in self.opponents_suits:
            bid = Pass('0383')
        elif self._own_suit_is_minor_stoppers_in_other_suits_level_three():
            bid = self.nt_bid(3, '0384')
        elif self._opponents_bid_own_suit_stoppers():
            bid = self.nt_bid(3, '0385')
        elif self._is_strong_can_show_second_suit():
            bid = self.next_level_bid(self.second_suit, '0531')
        elif self.hcp >= 20 and self.shape[0] >= 7:
            bid = self.nt_bid(4, '0932')
        elif self._has_thirteen_points_competitive():
            if self.next_level(self.longest_suit) <= 2:
                level = 2
            else:
                level = 1
            bid = self.next_level_bid(self.longest_suit, '0386', level)
        elif self.hcp >= 13 and self.shape[0] >= 6 and self.longest_suit.is_major and self.next_level(self.longest_suit) <= 3:
            bid = self.suit_bid(3, self.longest_suit, '0911')
        elif self.hcp >= 13 and self.shape[1] >= 4 and self.second_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.second_suit, '0000')
        else:
            bid = Pass('0137')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _responder_long_suit_weak(self):
        """Bid with own long suit in weak hand."""
        own_suit = self.longest_suit
        if self._own_suit_is_minor_stoppers_in_other_suits_level_two():
            bid = self.nt_bid(2, '0387')
        elif self._opener_has_shown_six_card_suit():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0535')
        elif own_suit not in self.opponents_suits:
            if (self.overcall_made or
                    (self.hcp <= 12 and self.next_level(own_suit) >= 3)):
                raise_level = 0
            else:
                raise_level = 1
            bid = self.next_level_bid(own_suit, '0388', raise_level)
        else:
            bid = Pass('0389')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_jumped(self):
        """Bid after opener has jumped."""
        if self.hcp >= 20 and self.suit_length(self.opener_bid_one.denomination) >= 2:
            bid = self.nt_bid(4, '0294')
        elif self._is_strong_unbalanced_and_two_card_support_for_opener():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0390')
        elif self.five_five and self.overcallers_rebid.is_pass:
            bid = self._opener_jumped_five_five()
        elif self.shape[0] == 6:
            bid = self._opener_jumped_six_card_suit()
        elif self.suit_length(self.opener_bid_one.denomination) >= 2:
            bid = self._opener_jumped_two_card_support()
        else:
            bid = self._opener_jumped_no_support()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_jumped_five_five(self):
        """Bid after opener has jumped with 5/5 hand."""
        if (self.second_suit in self.opponents_suits or
                self.bid_one.is_pass):
            bid = Pass('0391')
        else:
            suit = self._get_suit_with_five_five_after_opener_jumped()
            bid = self.next_level_bid(suit, '0392')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_jumped_six_card_suit(self):
        """Bid after opener has jumped with 6 card suit."""
        if self.longest_suit.is_minor and self.nt_level <= 3:
            bid = self.nt_bid(3, '0393')
        elif self.longest_suit not in self.opponents_suits:
            bid = self.next_level_bid(self.longest_suit, '0394')
        else:
            bid = Pass('0395')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_jumped_two_card_support(self):
        """Bid after opener has jumped with 2+ card support."""
        if self.hand_value_points(self.opener_bid_one.denomination) >= 8:
            bid = self._opener_jumped_support_strong()
        else:
            bid = Pass('0396')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_jumped_support_strong(self):
        """Bid after opener has jumped with 2+ card support, good hand."""
        if self._balanced_and_opener_bid_minor():
            bid = self.nt_bid(3, '0397')
        elif self._opener_has_jumped_and_can_support_non_competitive():
            bid = self.bid_to_game(self.opener_bid_one.denomination, '0398', True)
        elif self.support_points(self.opener_bid_one.denomination) >= 15:
            bid = self.bid_to_game(self.opener_bid_one.denomination, '0623', True)
        elif self._opener_has_jumped_and_can_support_competitive():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0696')
        elif (self.opener_bid_one.denomination == self.opener_bid_two.denomination and
              self.opener_bid_one.denomination.is_major and
              self.opener_bid_two.level == 3 and
              self.suit_length(self.opener_bid_one.denomination) >= 2 and
              self.hcp >= 11):
            bid = self.bid_to_game(self.opener_bid_one.denomination, '0811', True)
        elif self._can_bid_second_suit_at_level_three():
            bid = self.next_level_bid(self.second_suit, '0819')
        else:
            bid = Pass('0399')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_jumped_no_support(self):
        """Bid after opener has jumped with no support."""
        if self.hcp <= 7 or self.bid_one.is_nt:
            bid = Pass('0400')
        else:
            bid = self._opener_jumped_no_support_intermediate_strong()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_jumped_no_support_intermediate_strong(self):
        """Bid after opener has jumped with no support good hand."""
        if self.shape[0] >= 7 and self.longest_suit not in self.opponents_suits:
            bid = self.bid_to_game(self.longest_suit, '0401')
        elif self.hcp >= 16 and self.shape[0] >= 5:
            bid = self.next_level_bid(self.bid_one.denomination, '0402')
        elif self._has_thirteen_points_and_opener_has_jumped():
            bid = self.nt_bid(4, '0086')
        elif self._has_twelve_points_and_opener_has_jumped():
            bid = self.nt_bid(3, '0403')
        else:
            bid = Pass('0404')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_changed_suit_after_nt(self):
        """Return bid after opener has changed suit after responder NT."""
        suit_to_bid = self._select_suit()
        barrier_is_broken = self.barrier_is_broken(self.opener_bid_one,
                                                   self.opener_bid_two)
        if self._weak_but_barrier_broken(suit_to_bid):
            if (self.hcp+self.distribution_points >= 9 and
                    self.suit_length(self.opener_bid_one.denomination) >= 3):
                raise_level = 1
            else:
                raise_level = 0
            bid = self.next_level_bid(suit_to_bid, '0405', raise_level=raise_level)
        elif barrier_is_broken and self.hcp >= 9:
            bid = self._opener_changed_suit_after_nt_intermediate()
        elif not self.overcall_made:
            if self.shape[0] >= 6:
                bid = self.next_level_bid(self.longest_suit, '0612')
            elif self.hcp >= 6 and self.next_level(suit_to_bid) <= 2:
                bid = self.next_level_bid(suit_to_bid, '0409')
            else:
                bid = Pass('0859')
        elif self._both_openers_suits_are_minors():
            bid = self.nt_bid(3, '0410')
        else:
            bid = self._opener_changed_suit_after_nt_overcall_major()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_changed_suit_after_nt_intermediate(self):
        """Return bid after opener has reversed after responder NT, 9+ points."""
        suit_to_bid = self._select_suit()
        if suit_to_bid in self.opponents_suits:
            suit_to_bid = self.opener_bid_one.denomination
        if self._no_support_own_suit_is_minor_with_stops():
            bid = self.nt_bid(3, '0613')
        elif suit_to_bid.is_no_trumps:
            bid = self.nt_bid(3, '0406')
        elif self._is_balanced_own_suit_is_minor_with_stops():
            bid = self.next_nt_bid('0914')
        elif self.next_level(suit_to_bid) <= 4:
            bid = self.suit_bid(4, suit_to_bid, '0407')
        else:
            bid = Pass('0408')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_changed_suit_after_nt_overcall_major(self):
        """Return bid after opener two suits  one major and overcall."""
        trial_bid = self._opener_changed_suit_after_nt_overcall_major_trial()
        level = trial_bid.level
        own_suit = self.longest_suit
        borrowed_bid = own_suit in self.opponents_suits
        if level < 3 or self.hcp >= 10 or self.suit_length(trial_bid.denomination) >= 5:
            bid = trial_bid
        elif borrowed_bid and self.hcp >= 9:
            bid = trial_bid
        else:
            bid = Pass('0411')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_changed_suit_after_nt_overcall_major_trial(self):
        """Return bid after opener two suits one major and overcall."""
        suit_to_bid = self._suit_for_trial_after_opener_changes_suit()
        if self.hcp >= 12 and suit_to_bid.is_major:
            jump = 1
        else:
            jump = 0
        bid = self.next_level_bid(suit_to_bid, '0412', jump)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_nt_after_nt_response(self):
        """Return bid if opener has bid NT after a NT response."""
        if self.opener_bid_two.name == '3NT':
            bid = Pass('0413')
        elif self.hcp >= 8:
            bid = self.nt_bid(3, '0414')
        elif (self.shape[0] >= 6 and
                self.longest_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.longest_suit, '0609')
        else:
            bid = Pass('0415')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _three_suits_bid(self):
        """Return bid after opener shows third suit."""
        suit_to_bid = self._select_suit()
        barrier_is_broken = self.barrier_is_broken(self.opener_bid_one,
                                                   self.opener_bid_two)
        suit_support_points = self._suit_support_points(suit_to_bid)

        if barrier_is_broken and self.hcp <= 15:
            bid = self._opener_broken_barrier_weak()
        elif self._has_fourteen_points_and_suit_is_minor(suit_to_bid):
            bid = self.nt_bid(3, '0416')
        elif self._has__strong_seven_card_suit_and_fourteen_points():
            bid = self.bid_to_game(self.longest_suit, '0899')
        elif self._has_ten_points_and_can_support_opener(suit_to_bid,
                                                         suit_support_points):
            bid = self._three_suits_bid_support_opener()
        elif suit_to_bid.is_no_trumps:
            bid = self._three_suits_and_nt_selected()
        elif self._has_eleven_points_and_three_suits_bid():
            if self.hcp >= 13:
                level = 3
            else:
                level = 2
            bid = self.nt_bid(level, '0420')
        elif (self.hcp >= 10 and
              suit_to_bid not in self.opponents_suits):
            bid = self._three_suits_bid_medium_hand()
        else:
            bid = self._three_suits_bid_weak()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _three_suits_bid_support_opener(self):
        """Return bid after opener shows third suit and hand supports opener."""
        suit_to_bid = self._select_suit()
        if suit_to_bid.is_minor:
            unbid_suit = self._unbid_suit()
        else:
            unbid_suit = None
        suit_support_points = self._suit_support_points(suit_to_bid)
        if self._can_support_minor_but_is_semi_balanced(suit_to_bid, suit_support_points):
            bid = self.nt_bid(2, '0178')
        elif self.hcp >= 16 and self.nt_level <= 3 and self.stoppers_in_unbid_suits():
            bid = self.nt_bid(3, '0567')
        elif self.hcp >= 16 and self.barrier_broken:
            bid = self.next_level_bid(suit_to_bid, '0642')
        elif self._has_six_card_suit_and_opening_points():
            bid = self.suit_bid(3, self.longest_suit, '0931')
        elif 10 <= self.hcp <= 13 and not self.is_semi_balanced and suit_to_bid.is_minor:
            bid = self.suit_bid(4, suit_to_bid, '0804', True)
        elif unbid_suit and self.hcp >= 12 and (self.suit_length(unbid_suit) + self.suit_points(unbid_suit)) >= 4:
            bid = self.nt_bid(3, '0922')
        elif suit_support_points >= 13 and self.next_level(suit_to_bid) <= suit_to_bid.game_level:
            bid = self.bid_to_game(suit_to_bid, '0417', True)
        elif self._is_balanced_intermediate_stoppers(suit_to_bid):
            bid = self.nt_bid(2, '0801')
        elif self.suit_length(suit_to_bid) >= 4 and self.hcp >= 10:
            bid = self.next_level_bid(suit_to_bid, '0418', 1)
        elif self._is_balanced_support_for_openers_second_suit(suit_to_bid):
            bid = self.nt_bid(2, '0206')
        elif self._suit_to_support_is_minor_and_stoppers(suit_to_bid):
            if self.hcp <= 9:
                level = 1
            elif self.hcp <= 13:
                level = 2
            else:
                level = 3
            bid = self.nt_bid(level, '0391')
        elif suit_support_points >= 11:
            bid = self.next_level_bid(suit_to_bid, '0874', raise_level=1)
        elif self._has_three_card_support_for_openers_major():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0285')
        elif self.hcp == 10 and self.is_balanced and self.nt_level <= 2:
            bid = self.nt_bid(2, '0265')
        elif self.hcp == 10:
            bid = self.next_level_bid(suit_to_bid, '0419')
        elif suit_support_points >= 10:
            if self.six_four:
                raise_level = 1
            else:
                raise_level = 0
            bid = self.next_level_bid(suit_to_bid, '0423', raise_level=raise_level)
        else:
            assert False, 'bid not assigned'
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _three_suits_bid_medium_hand(self):
        """Return bid after opener shows third suit, medium hand."""
        suit_to_bid = self._select_suit()
        level = self.next_level_bid(suit_to_bid).level
        if (self.hcp >= 16 and
                self.shape[0] >= 7 and
                self.nt_level <= 4):
            bid = self.nt_bid(4, '0910')
        elif self._is_strong_has_stoppers():
            bid = self.nt_bid(4, '0000')
        elif (self.shape[0] >= 7 and
                self.longest_suit.is_major and
                self.opener_bid_two.level >= 2 and
                self.next_level(suit_to_bid) <= 4):
            bid = self.suit_bid(4, suit_to_bid, '0330')
        elif (self._is_distributional_and_barrier_not_broken(suit_to_bid) and
                self.shape[0] >= 8):
            bid = self.bid_to_game(self.longest_suit, '0735')
        elif self._is_distributional_and_barrier_not_broken(suit_to_bid):
            level += 1
            bid = self.suit_bid(level, suit_to_bid, '0422')
        else:
            bid = self.suit_bid(level, suit_to_bid, '0421', True)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _three_suits_bid_weak(self):
        """Return bid after opener shows third suit, weak hand."""
        suit_to_bid = self._select_suit()
        if self.shape[0] >= 7:
            suit_to_bid = self.longest_suit
        elif self.shape[0] >= 6 and self.hcp == 5:
            suit_to_bid = self.longest_suit

        if self._has_biddable_five_card_major(suit_to_bid):
            bid = self.next_level_bid(self.longest_suit, '0424')
        elif self._opener_has_doubled_can_bid_suit(suit_to_bid):
            bid = self.next_level_bid(suit_to_bid, '0629')
        elif self.three_suits_bid_and_stopper() and self.suit_length(self.unbid_suit) >= 5:
            bid = self.next_nt_bid('0927')
        elif self._is_weak_can_bid_suit(suit_to_bid):
            bid = self.next_level_bid(suit_to_bid, '0425')
        elif self._is_weak_can_show_preference(suit_to_bid):
            bid = self._show_preference(suit_to_bid)
        elif self.partner_last_bid.is_double and self.last_bid.is_pass and not self.opponents_at_game and self.cheapest_long_suit():
            bid = self.next_level_bid(self.cheapest_long_suit(), '0820')
        else:
            bid = Pass('0426')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _show_preference(self, selected_suit):
        """Return bid when weak and no support for opener."""
        if selected_suit in self.opponents_suits:
            suit_preference = self._select_suit_support_opener()
            if suit_preference == self.opener_bid_two.denomination:
                bid = Pass('0427')
            else:
                bid = self.next_level_bid(suit_preference, '0428')
        else:
            bid = self.next_level_bid(selected_suit, '0429')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _three_suits_and_nt_selected(self):
        """Return bid after three suits shown and NT is selected."""
        barrier_is_broken = self.barrier_is_broken(self.opener_bid_one, self.opener_bid_two)
        level = self._three_suits_and_nt_selected_get_level(barrier_is_broken)
        if level >= self.nt_level:
            bid = self.nt_bid(level, '0430')
        else:
            bid = Pass('0431')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_broken_barrier_weak(self):
        """Return bid after opener breaks barrier with weak hand."""
        suit_to_bid = self._select_suit()
        best_major = self._best_major_fit()
        suit_preference = self._suit_preference()

        if self.hcp >= 15 and self.suit_length(self.opener_bid_one.denomination) >= 4:
            bid = self.nt_bid(4, '0895')
        elif best_major and self.hcp >= 11 and self.next_level(best_major) <= 4:
            bid = self.suit_bid(4, best_major, '0245')
        elif self._has_eleven_points_and_opening_bid_is_major():
            bid = self.suit_bid(4, self.opener_bid_one.denomination, '0432')
        elif self.hcp >= 12 and self.three_suits_bid_and_stopper() and self.nt_level == 3:
            bid = self.nt_bid(3, '0617')
        elif self._has_eleven_points_five_four_no_support_for_opening_bid():
            bid = self._progress_suit()
        elif self._has_eleven_points_five_card_suit_no_support_for_opening_bid():
            bid = self.next_level_bid(self.longest_suit, '0433')
        elif suit_to_bid.is_minor and 10 <= self.hcp <= 13 and self.is_balanced:
            bid = self.next_nt_bid('0551')
        elif (suit_to_bid.is_minor and 10 <= self.hcp <= 13 and
                suit_to_bid not in self.opponents_suits):
            level = max(4, self.next_level(suit_to_bid))
            bid = self.suit_bid(level, suit_to_bid, '0434')
        elif self._can_bid_suit_at_next_level(suit_to_bid):
            bid = self.bid_to_game(suit_to_bid, '0435')
        elif suit_to_bid.is_minor and self.stoppers_in_bid_suits and self.nt_level <= 3 and self.overcall_made:
            bid = self.nt_bid(3, '0933')
        elif self._nine_points_bid_up_to_level_four(suit_to_bid):
            bid = self.suit_bid(4, suit_to_bid, '0436')
        elif self._has_three_card_support_for_openers_major():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0395')
        elif (self.shape[0] >= 6 and
                HandSuit(self.longest_suit, self).honours >= 3 and
                self.longest_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.longest_suit, '0686')
        elif self._eight_points_and_stoppers():
            bid = self.nt_bid(3, '0437')
        elif Bid(self.bid_history[-1]).is_value_call and self.hcp <= 9:
            bid = Pass('0438')
        elif self._opener_bid_new_suit_level_three_and_semi_balanced(suit_preference):
            bid = self.nt_bid(3, '0441')
        elif self._no_support_but_nt_possible(suit_preference):
            bid = self.nt_bid(3, '0615')
        elif self._seven_points_or_level_two_or_some_support():
            bid = self.next_level_bid(suit_preference, '0440')
        else:
            bid = Pass('0439')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _progress_suit(self):
        """Agreed suit, push on."""
        if self._fourteen_points_and_support_for_second_suit() or self.overcall_made:
            bid = self.next_level_bid(self.second_suit, '0313', raise_level=1)
        else:
            bid = self.next_level_bid(self.second_suit, '0102')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_nt_after_suit_response(self):
        """Respond after opener has bid NT after a suit response."""
        opener_jumped = self.is_jump(self.opener_bid_one, self.opener_bid_two)
        if self.opener_bid_two.name == '3NT':
            bid = Pass('0441')
        elif self.hcp >= 10 or (opener_jumped and self.hcp >= 7):
            bid = self._opener_nt_after_suit_response_strong()
        elif self._opener_has_rebid_one_nt_and_nt_level_is_two():
            bid = self.nt_bid(2, '0442')
        elif self._opener_has_rebid_one_nt_and_six_card_major():
            bid = self.bid_to_game(self.longest_suit, '0510')
        elif self._opener_has_rebid_one_nt_and_five_card_suit():
            bid = self.next_level_bid(self.longest_suit, '0443')
        elif self._opener_rebid_two_nt_and_five_four_and_shortage():
            bid = self.next_level_bid(self.second_suit, '0444')
        elif self._has_six_card_suit_and_level_three():
            bid = self.next_level_bid(self.longest_suit, '0445')
        elif self._cannot_support_openers_first_suit():
            bid = self.next_level_bid(self.second_suit, '0534')
        elif (self.suit_length(self.opener_bid_one.denomination) >= 6 and
                self._has_shortage()):
            bid = self.bid_to_game(self.opener_bid_one.denomination, '0589')
        elif self.nt_level >= 3 and self._has_shortage():
            bid = self.next_level_bid(self.longest_suit, '0446')
        elif self._opponents_doubled_openers_nt():
            bid = self.next_level_bid(self.longest_suit, '0447')
        # elif self.opener_bid_two.is_nt and self.nt_level < 3:
            # bid = self.nt_bid(3, '0000')
        elif self.opener_bid_two.is_nt and self.shape[0] >= 8:
            bid = self.suit_bid(4, self.longest_suit, '0561')
        else:
            bid = Pass('0448')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_nt_after_suit_response_strong(self):
        """Respond, opener has bid NT after a suit response strong."""
        nt_level = self._get_nt_level_after_strong_nt()
        if self._has_seven_card_suit_and_fourteen_points():
            bid = self.nt_bid(4, '0122')
        elif self.five_five:
            bid = self._opener_nt_after_suit_response_strong_five_five()
        elif self.spades >= 6 and self.spade_suit not in self.opponents_suits:
            bid = self.bid_to_game(Denomination('S'), '0449')
        elif self.hearts >= 6 and self.heart_suit not in self.opponents_suits:
            bid = self.bid_to_game(Denomination('H'), '0450')
        elif self._has_five_four_and_no_support():
            if self.hcp >= 11 and self.nt_level == 2:
                raise_level = 1
            else:
                raise_level = 0
            bid = self.next_level_bid(self.second_suit, '0076', raise_level)
        elif self._has_five_four_and_can_show_second_suit():
            bid = self.next_level_bid(self.second_suit, '0625', 1)
        elif self._can_bid_spades():
            bid = self.spade_bid(3, '0451')
        elif self.hearts >= 5 and self.nt_level <= 3:
            bid = self.nt_bid(3, '0452')
        elif self._has_three_card_support_for_openers_major():
            bid = self.suit_bid(3, self.opener_bid_one.denomination, '0453')
        elif nt_level == 6 and self.stoppers_in_bid_suits:
            bid = self.nt_bid(nt_level, '0614')
        elif self.hcp >= 22:
            bid = self.nt_bid(7, '0000')
        elif self.hcp >= 17:
            bid = self.nt_bid(6, '0754')
        elif self._nt_can_support_minor():
            bid = self.nt_bid(3, '0855')
        elif self._has_five_four_and_fewer_than_ten_points():
            bid = self.next_level_bid(self.second_suit, '0241')
        elif self.nt_level <= 3 and self.stoppers_in_bid_suits:
            bid = self.nt_bid(nt_level, '0454')
        else:
            bid = Pass('0455')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_nt_after_suit_response_strong_five_five(self):
        """Respond, opener has bid NT after a suit response strong 5/5."""
        suit_to_bid = self._select_best_five_five()
        if suit_to_bid.is_major and self.hcp >= 10:
            raise_level = 1
        else:
            raise_level = 0
        bid = self.next_level_bid(suit_to_bid, '0456', raise_level=raise_level)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _opener_has_passed(self):
        """Rebid after opener has passed."""
        if self._has_four_card_support_at_level_three():
            bid = self.next_level_bid(self.opener_bid_one.denomination, '0457')
        elif self._has_six_card_suit_after_nt_opening():
            bid = self.next_level_bid(self.longest_suit, '0458')
        elif self.five_five_or_better:
            bid = self._bid_second_suit()
        elif self._has_strong_six_card_suit_at_level_two():
            bid = self.next_level_bid(self.longest_suit, '0459')
        elif self._is_balanced_thirteen_points():
            bid = self.nt_bid(3, '0460')
        elif (self.hcp >= 11 and self.five_four_or_better and
                self.second_suit not in self.opponents_suits):
            bid = self.next_level_bid(self.second_suit, '0374')
        elif self.hcp >= 11 and self.stoppers_in_bid_suits and self.nt_level <= 2:
            bid = self.next_nt_bid('0860')
        else:
            bid = Pass('0461')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _bid_second_suit(self):
        """Bid second suit after opener has passed."""
        if self._can_bid_second_suit_at_level_three():
            bid = self.next_level_bid(self.second_suit, '0463')
        else:
            bid = Pass('0464')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    # Various utility functions

    def _three_suits_and_nt_selected_get_level(self, barrier_is_broken):
        """Return level after NT is selected."""
        if self.hcp >= 13 or (barrier_is_broken and self.hcp >= 7):
            level = 3
        elif self.hcp >= 10:
            level = 2
        else:
            level = 1
        return level

    def _best_major_fit(self):
        """Return the best major fit (if any)."""
        best_major = None
        suit_one = self.opener_bid_one.denomination
        suit_two = self.opener_bid_two.denomination
        if (suit_one.is_major and
                suit_two.is_major and
                suit_one != suit_two):
            holding_one = self.suit_length(suit_one)
            holding_two = self.suit_length(suit_two)
            if holding_one <= 2 and holding_two <= 3:
                best_major = None
            elif holding_two+1 > holding_one:
                best_major = suit_two
            else:
                best_major = suit_one
        return best_major

    def _get_nt_level_after_strong_nt(self):
        """Return the appropriate NT level if opener bids nt after suit """
        nt_level = 3
        if self.opener_bid_two.name == '2NT':
            if self.hcp >= 15 and self.bid_one.level == 1:
                nt_level = 6
            # elif self.hcp >= 13 and self.bid_one.level == 1:
            #     nt_level = 4
        return nt_level

    # Suit selection functions

    def _select_suit(self):
        """ Return responder's selected suit following change
            of suit by opener.
        """
        if ((self.shape[0] >= 7 or self.hcp >= 11) and
                self.longest_suit.is_major and
                self.suit_length(self.opener_bid_one.denomination) <= 2 and
                self.suit_length(self.opener_bid_two.denomination) <= 3):
            selected_suit = self._select_suit_no_support()
        else:
            selected_suit = self._select_suit_support_opener()
        return selected_suit

    def _select_suit_no_support(self):
        """Return suit with no support for opener."""
        if self.shape[1] >= 5 and self.shape[3] <= 1:
            selected_suit = self.second_suit
        else:
            selected_suit = self.longest_suit
        if selected_suit in self.opponents_suits:
            if selected_suit == self.longest_suit:
                selected_suit = self.second_suit
            else:
                selected_suit = self.longest_suit
        return selected_suit

    def _select_suit_support_opener(self):
        """Return suit support for opener."""
        if (self.suit_length(self.opener_bid_one.denomination) >= 3 or
                self.suit_length(self.opener_bid_two.denomination) >= 4):
            bid_no_trumps = False
        elif self.barrier_is_broken(self.opener_bid_one, self.opener_bid_two) or self.hcp >= 10:
            bid_no_trumps = self._suitability_for_nt()
        else:
            bid_no_trumps = False
        if bid_no_trumps:
            selected_suit = self.no_trumps
        else:
            selected_suit = self._suit_preference()
        return selected_suit

    def _suit_preference(self):
        """Return suit preference for a bid."""
        suit_one = self.opener_bid_one.denomination
        suit_two = self.opener_bid_two.denomination
        if suit_one.is_suit:
            holding_one = self.suit_length(suit_one)
        else:
            holding_one = 0
        if suit_two.is_suit:
            holding_two = self.suit_length(suit_two)
        else:
            holding_two = 0
        if holding_one + 1 == holding_two:
            if (suit_one.is_minor and
                    suit_two.is_major and
                    (not self.is_jump(self.opener_bid_one, self.opener_bid_two) or
                     self.opener_bid_two.level == 3 or
                     (self.opener_bid_one.is_minor and self.opener_bid_two.is_major) and
                     self.suit_length(self.opener_bid_two.denomination) >= 4)):
                selected_suit = suit_two
            else:
                selected_suit = suit_one
        elif holding_one >= holding_two:
            if (suit_one.is_minor and
                    suit_two.is_major and
                    holding_two >= 4):
                selected_suit = suit_two
            elif (suit_one.is_minor and
                    suit_two.is_major and
                    self.opener_bid_two.level == 3 and
                    holding_two >= 3):
                selected_suit = suit_two
            else:
                selected_suit = suit_one
        else:
            selected_suit = suit_two
        if not suit_one.is_suit:
            selected_suit = suit_two
        if not suit_two.is_suit:
            selected_suit = suit_one
        return selected_suit

    def _suits_not_bid_by_opener(self):
        """Return a list of suits not bid by opener."""
        suit_list = []
        for suit in self.suits:
            if (suit != self.opener_bid_one.denomination and
                    suit != self.opener_bid_two.denomination):
                suit_list.append(suit)
        return suit_list

    def _get_suit_if_five_five(self):
        """Return selected suit."""
        first_suit = self.longest_suit
        second_suit = self.second_suit
        if first_suit.is_major:
            suit = first_suit
        else:
            suit = second_suit
        return suit

    def _get_suit_with_five_five_after_opener_jumped(self):
        """Return the suit to bid with 5/5."""
        if self.bid_one.denomination == self.longest_suit:
            suit = self.second_suit
        else:
            suit = self.longest_suit

        if suit in self.opponents_suits:
            if suit == self.longest_suit:
                suit = self.second_suit
            else:
                suit = self.longest_suit
        return suit

    def _suit_for_trial_after_opener_changes_suit(self):
        """Return a suit for trial bid after opener changed suit."""
        suit_to_bid = self._suit_preference()
        if (self.five_card_major_or_better and
                self.hcp >= 10 or
                (self.hcp >= 8 and self.shape[0] >= 6)):
            if (self.hearts >= 5 and
                    self.heart_suit not in self.opponents_suits):
                suit_to_bid = self.heart_suit
            elif (self.spades >= 5 and
                    self.spade_suit not in self.opponents_suits):
                suit_to_bid = self.spade_suit
        return suit_to_bid

    def _select_best_five_five(self):
        """Return the best suit for a 5/5 or better hand."""
        suits = []
        for suit in self.suits:
            if self.suit_length(suit) >= 5 and suit not in self.opponents_suits:
                suits.append(suit)
        suit = suits[0]
        return suit

    def _unbid_suit(self):
        """Return the 4th (unbid) suit (if any)"""
        suits = [self.spade_suit, self.heart_suit, self.diamond_suit, self.club_suit]
        calls = [self.opener_bid_one, self.responder_bid_one, self.opener_bid_two]
        for call in calls:
            if call.is_suit_call:
                suits.remove(call.denomination)
            else:
                return None
        if len(suits) == 1:
            unbid_suit = suits[0]
        else:
            unbid_suit = None
        return unbid_suit

    # Various boolean functions

    def _suit_support_points(self, suit_to_bid):
        """Return suit_support_points: a measure of support strength."""
        if suit_to_bid.is_suit:
            suit_support_points = self.hand_value_points(suit_to_bid)
            suit_holding = self.suit_length(suit_to_bid)
            if suit_holding >= 4:
                suit_support_points += suit_holding - 4  # add 1 for any length over 4
        else:
            suit_support_points = 0
        return suit_support_points

    def _suitability_for_nt(self):
        """ Return True if  a strong 5 card suit or a 4 card suit with stoppers."""
        suitability = False
        if self.nt_level > 3:
            suitability = False
        else:
            for suit in self._suits_not_bid_by_opener():
                quality = HandSuit(suit, self).suit_quality()
                if (self.suit_length(suit) >= 5 or
                        (self.suit_length(suit) == 4 and
                         quality >= 1.5) or
                        self.has_stopper(suit) or
                        self.barrier_is_broken(self.opener_bid_one, self.opener_bid_two)):
                    suitability = True
                else:
                    suitability = False
                    break
        return suitability

    def _weak_two_opening(self):
        """Return True if opener has bid weak two."""
        result = (self.opener_bid_one.level >= 2 and
                  self.opener_bid_one.is_suit_call and
                  self.opener_bid_one.name != '2C')
        return result

    def _has_six_card_suit_and_opener_passed(self):
        """Return True if opener has passed and responder has 6 card suit."""
        result = (self.opener_bid_two.is_pass and
                  self.shape[0] >= 6 and
                  self.hcp >= 10 and
                  self.next_level(self.longest_suit) <= 2 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _game_has_been_bid_by_opposition(self):
        """Return True if game has been bid."""
        result = (self.overcaller_bid_one.is_game or
                  self.advancer_bid_one.is_game or
                  self.overcallers_rebid.is_game)
        return result

    def _opener_at_game_but_can_show_preference(self):
        """Return True if Opener at game level and can rebid own suit."""
        result = (self.opener_bid_two.is_game and
                  self.opener_bid_two.is_suit_call and
                  self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  self.longest_suit.rank < self.opener_bid_two.denomination.rank)
        return result

    def _has_fifteen_points_and_opener_has_rebid_three_nt(self):
        """Return True if opener has rebid 3NT and hand hs 15+ points."""
        result = (self.opener_bid_one.is_suit_call and
                  self.opener_bid_two.name == '3NT' and
                  self.bid_one.level != 3 and
                  self.hcp >= 15)
        return result

    def _has_fourteen_with_openers_twenty_three_in_nt(self):
        """Return True if opener has 23+ points, rebid 3NT and hand has 14+."""
        result = (self.opener_bid_one.name == '2C' and
                  self.opener_bid_two.name == '3NT' and
                  self.hcp >= 14)
        return result

    def _has_twelve_with_openers_nineteen_in_nt(self):
        """Return True if opener rebids 3NT after suit and 12+."""
        result = (self.opener_bid_one.is_suit_call and
                  self.opener_bid_two.name == '3NT' and
                  self.bid_one.level == 1 and
                  self.hcp >= 12)
        return result

    def _has_six_card_suit_with_openers_nineteen_in_nt(self):
        """Return True if opener rebids 3NT after suit and 6 card suit."""
        result = (self.opener_bid_two.name == '3NT' and
                  self.my_last_bid.level <= 2 and
                  self.shape[0] >= 6 and
                  self.longest_suit not in self.opponents_suits and
                  self.longest_suit.is_major)
        return result

    def _thirteen_points_support_and_opener_in_game_in_major(self):
        """Return True if opener at game in major, 14+ points with support."""
        result = (self.opener_bid_two.level == 4 and
                  not self.opener_bid_one.name == '1NT' and
                  self.opener_bid_two.denomination.is_major and
                  self.hcp >= 13 and
                  (self.suit_length(self.opener_bid_two.denomination) >= 3 or
                   self.suit_points(self.opener_bid_two.denomination) >= 4))
        return result

    def _opener_has_passed_can_compete(self):
        """Return True if opener has passed and can compete."""
        if self.overcaller_bid_one.denomination.is_suit:
            holding_in_overcallers_suit = self.suit_length(self.overcaller_bid_one.denomination)
        else:
            holding_in_overcallers_suit = 0
        result = (self.opener_bid_two.is_pass and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  self.overcall_made and
                  (holding_in_overcallers_suit <= 2 or
                   self.overcaller_bid_one.is_double))
        return result

    def _has_sixteen_and_six_card_suit(self):
        """Return True with 16+ points and a six card suit."""
        result = (self.shape[0] >= 6 and
                  self.hcp >= 16 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _has_sixteen_and_three_card_support(self):
        """Return True with 16+ points and a 3 card support."""
        result = (self.hcp >= 16 and
                  self.suit_length(self.opener_bid_one.denomination) >= 3 and
                  not self.bidding_above_game)
        return result

    def _has_seventeen_and_three_card_support_can_bid_game(self):
        """Return True with 17+ points, 3 card support and can bid game."""
        result = (self.hcp >= 17 and
                  self.opener_bid_one.is_major and
                  self.suit_length(self.opener_bid_one.denomination) >= 3 and
                  self.next_level(self.opener_bid_one.denomination) <= 4)
        return result

    def _can_rebid_openers_suit(self):
        """Return True if possible to rebid openers suit."""
        trial_bid = self.next_level_bid(self.opener_bid_one.denomination, '0319')
        result = (trial_bid.level <= 3 or
                  (trial_bid.level <= 4 and not self.overcall_made) or
                  (trial_bid.level <= 4 and self.hcp >= 12))
        return result

    def _opener_has_responded_to_stayman(self):
        """Return True if responder's previous bid was Stayman."""
        result = ((self.opener_bid_one.name == '1NT' and
                   self.bid_one.name == '2C') or
                  (self.opener_bid_one.name == '2NT' and
                   self.bid_one.name == '3C'))
        return result

    def _opener_has_bid_major_at_three_level_thirteen_points(self):
        """Return True if opener has bid a major at 3 level and 13+ points."""
        result = (self.opener_bid_two.level == 3 and
                  self.opener_bid_two.denomination.is_major and
                  self.hcp >= 13)
        return result

    def _has_six_card_suit_ten_points_and_opener_support(self):
        """Return True six card suit, 10 points and opener's support."""
        result = (self.hcp >= 10 and
                  self.shape[0] >= 6 and
                  self.opener_bid_two.denomination == self.bid_one.denomination)
        return result

    def _opener_bids_hearts_but_fewer_than_four_hearts(self):
        """Return True if opener has bid hearts, not spades (stayman)."""
        result = (self.suit_length(self.opener_bid_two.denomination) <= 4 and
                  self.opener_bid_two.denomination == self.heart_suit and
                  self.spade_suit not in self.opponents_suits)
        return result

    def _has_four_cards_in_openers_major_fewer_than_ten_points(self):
        """Return True with fewer than 10 points and suit is 4+ card major."""
        result = (self.opener_bid_two.denomination.is_major and
                  self.suit_length(self.opener_bid_two.denomination) >= 4 and
                  self.hcp <= 10)
        return result

    def _overcall_made_has_five_five(self, suit):
        """Return True if overcall and 5/5."""
        result = (self.overcall_made and
                  self.five_five and
                  suit not in self.opponents_suits)
        return result

    def _opener_has_has_doubled_and_five_card_suit(self):
        """Return True if opener's rebid is double and 5 card suit."""
        result = (self.opener_bid_two.is_double and
                  self.suit_length(self.opener_bid_one.denomination) <= 1 and
                  self.shape[0] >= 5 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _has_bid_two_nt_and_opener_bids_minor(self):
        """Return True if bid 2NT and opener bids minor."""
        result = (self.bid_one.name == '2NT' and
                  self.opener_bid_two.denomination.is_minor and
                  (self.opener_bid_two.level < 2 or
                   self.hcp <= 11))
        return result

    def _responder_jumped_support_fewer_than_five_points(self):
        """Return True if responder has jumped, opener support fewer than 5 pts."""
        result = ((self.is_jump(self.opener_bid_one, self.bid_one) and
                   self.bid_one.denomination == self.opener_bid_one.denomination) or
                  self.hcp <= 5)
        return result

    def _opener_has_jumped_or_level_is_three(self):
        """Return True if opener has jumped."""
        opener_jumped = self.is_jump(self.opener_bid_one, self.opener_bid_two) and not self.overcall_made
        responder_has_jumped = self.is_jump(self.opener_bid_one, self.bid_one)
        result = ((opener_jumped and
                   not self.overcall_made and
                   not responder_has_jumped) or
                  self.opener_bid_two.level >= 3)
        return result

    def _has_fewer_than_nine_points_and_passed_or_one_nt(self):
        """Return True if weak and no suit."""
        result = (self.hcp <= 9 and
                  (self.bid_one.name == '1NT' or
                   self.bid_one.is_pass))
        return result

    def _has_six_card_suit_and_can_bid(self):
        """Return True if six card suit and can bid"""
        result = (self.shape[0] >= 6 and
                  (self.next_level(self.longest_suit) <= 2 or
                   self.hcp >= 10))
        return result

    def _opener_bids_major_at_level_three_can_support(self):
        """Return True if opener bids major at level 3 and can support."""
        result = (self.opener_bid_two.level == 3 and
                  self.suit_length(self.opener_bid_two.denomination) >= 2 and
                  self.opener_bid_two.denomination.is_major)
        return result

    def _is_weak_and_shortage_in_openers_suit(self):
        """Return True with singleton or void in opener's repeated suit."""
        result = (self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                  not self.is_jump(self.my_last_bid, self.opener_bid_two) and
                  self.suit_length(self.opener_bid_one.denomination) <= 1 and
                  self.hcp <= 12 and
                  self.nt_level >= 3)
        return result

    def _has_five_four_and_opener_at_three_level(self):
        """Return True if opener at level 3 and hand has 5/4."""
        result = (self.opener_bid_two.level == 3 and
                  self.five_four and
                  self.next_level(self.second_suit) <= 3 and
                  self.second_suit not in self.opponents_suits)
        return result

    def _is_weak_openers_suit_is_minor(self):
        """Return True if weak and opener's suit is a minor."""
        result = (self.opener_bid_one.denomination.is_minor and
                  10 <= self.hcp <= 12 and
                  self.is_balanced and
                  self.stoppers_in_bid_suits)
        return result

    def _intermediate_has_four_card_major_and_opener_in_minor(self):
        """Return True if weak and opener in minor and 4 card major."""
        result = (self.opener_bid_one.denomination.is_minor and
                  10 <= self.hcp <= 12 and
                  self.shape[1] >= 4 and
                  self.second_suit.is_major and
                  self.second_suit not in self.opponents_suits)
        return result

    def _strong_has_six_card_major_and_opener_in_minor(self):
        """Return True if opener in minor and 6 card major."""
        result = (self.opener_bid_one.denomination.is_minor and
                  self.hcp >= 15 and
                  self.shape[0] >= 6 and
                  self.longest_suit.is_major and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _weak_has_six_card_major_and_opener_in_minor(self):
        """Return True if opener in minor and 6 card major."""
        result = (self.opener_bid_one.denomination.is_minor and
                  self.hcp >= 10 and
                  self.shape[0] >= 6 and
                  self.longest_suit.is_major and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _weak_has_stoppers_and_opener_in_minor(self, nt_level):
        """Return True if opener in minor and stoppers."""
        result = (self.opener_bid_one.denomination.is_minor and
                  self.hcp >= 10 and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= nt_level)
        return result

    def _intermediate_has_seven_car_major(self):
        """Return True with 7  card major and fewer than 17 points."""
        result = (self.shape[0] >= 7 and
                  self.longest_suit.is_major and
                  self.hcp <= 16)
        return result

    def _opener_in_minor_and_stoppers(self):
        """Return True if opener has bid minor and hand has stoppers."""
        result = (self.opener_bid_one.denomination.is_minor and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _opener_in_minor_distributional_with_stoppers(self):
        """Return True if opener in minor, distributional with stoppers."""
        result = (self.hcp >= 13 and
                  self.opener_bid_one.denomination.is_minor and
                  self.stoppers_in_bid_suits and
                  self.shape[1] <= 4 and
                  self.nt_level <= 3)
        return result

    def _can_bid_four_card_major(self):
        """Return True if suit_to_bid is a minor and has 4 card major."""
        result = (self.five_four and
                  self.second_suit.is_major and
                  self.second_suit not in self. opponents_suits)
        return result

    def _opener_has_jumped_no_support(self):
        """Return True if opener_has_jumped and no support."""
        result = (self.is_jump(self.opener_bid_one, self.bid_one) and
                  self.opener_bid_one.denomination != self.bid_one.denomination and
                  not self.overcaller_bid_one.is_value_call)
        return result

    def _own_suit_is_minor_stoppers_in_other_suits_level_three(self):
        """Return True if own suit is minor but stoppers in other suits."""
        result = (self.longest_suit.is_minor and
                  self.stoppers_in_other_suits(self.opener_bid_one.denomination) and
                  self.nt_level <= 3)
        return result

    def _opponents_bid_own_suit_stoppers(self):
        """Return True if opponents_bid own suit and stoppers."""
        result = (self.longest_suit in self.opponents_suits and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _has_thirteen_points_competitive(self):
        """Return True if 13+ points and competitive."""
        result = (self.hcp >= 13 and
                  not self.overcall_made and
                  self.next_level(self.longest_suit) <= 4)
        return result

    def _own_suit_is_minor_stoppers_in_other_suits_level_two(self):
        """Return True if own suit is minor and stoppers."""
        result = (self.longest_suit.is_minor and
                  self.nt_level <= 2 and
                  self.stoppers_in_other_suits(self.opener_bid_one.denomination))
        return result

    def _balanced_and_opener_bid_minor(self):
        """Return True if balanced and opener bid minor"""
        result = (self.opener_bid_one.denomination.is_minor and
                  self.stoppers_in_bid_suits and
                  self.is_balanced and
                  self.nt_level <= 3)
        return result

    def _opener_has_jumped_and_can_support_non_competitive(self):
        """Return True if opener has jumped and 2 card support card suit."""
        result = (self.hand_value_points(self.opener_bid_one.denomination) >= 9 and
                  not self.competitive_auction and
                  (self.is_jump(self.opener_bid_one, self.opener_bid_two) and
                   not self.overcaller_bid_one.is_value_call))
        return result

    def _opener_has_jumped_and_can_support_competitive(self):
        """Return True if opener has jumped and 3 card support card suit."""
        result = (self.hcp >= 12 and
                  self.hand_value_points(self.opener_bid_one.denomination) >= 10 and
                  self.competitive_auction and
                  (self.is_jump(self.opener_bid_one, self.opener_bid_two) and
                   self.overcaller_bid_one.is_value_call))
        return result

    def _has_thirteen_points_and_opener_has_jumped(self):
        """Return True if hcp >= 13 and opener has jumped."""
        result = (self.hcp >= 13 and
                  self.is_jump(self.bid_one, self.opener_bid_two) and
                  self.nt_level <= 4)
        return result

    def _has_twelve_points_and_opener_has_jumped(self):
        """Return True if hcp >= 12 and opener has jumped."""
        result = ((self.hcp >= 12 or
                  self.is_jump(self.bid_one, self.opener_bid_two)) and
                  self.nt_level <= 3 and
                  self.stoppers_in_bid_suits)
        return result

    def _weak_but_barrier_broken(self, suit):
        """Return True if weak and barrier broken."""
        barrier_is_broken = self.barrier_is_broken(self.opener_bid_one,
                                                   self.opener_bid_two)
        result = (barrier_is_broken and
                  6 <= self.hcp <= 8 and
                  self.next_level(suit) <= 3 and
                  suit not in self.opponents_suits)
        return result

    def _no_support_own_suit_is_minor_with_stops(self):
        """Return True if _suit is minor and stops."""
        suit_to_bid = self._select_suit()
        result = (self.nt_level <= 3 and
                  ((suit_to_bid.is_minor and
                    self.stoppers_in_bid_suits and
                    self.suit_length(self.opener_bid_two.denomination) <= 3) or
                   suit_to_bid in self.opponents_suits))
        return result

    def _is_balanced_own_suit_is_minor_with_stops(self):
        """Return True if own suit is minor, balanced and stops.
        :rtype: boolean
        """
        suit_to_bid = self._select_suit()
        result = (self.is_balanced and
                  suit_to_bid.is_minor and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _both_openers_suits_are_minors(self):
        """Return True if both opener's suits are minor."""
        result = (self.opener_bid_one.denomination.is_minor and
                  self.opener_bid_two.denomination.is_minor and
                  self.stoppers_in_bid_suits and
                  self.hcp >= 13)
        return result

    def _can_support_opener(self, suit_to_bid):
        """Return True if suit is one of opener's suits."""
        result = (suit_to_bid == self.opener_bid_one.denomination or
                  suit_to_bid == self.opener_bid_two.denomination)
        return result

    def _has_fourteen_points_and_suit_is_minor(self, suit_to_bid):
        """Return True if suit is minor and 14+ points."""
        result = (self.hcp >= 14 and
                  self.three_suits_bid_and_stopper() and
                  suit_to_bid.is_minor and
                  self.nt_level <= 3)
        return result

    def _has__strong_seven_card_suit_and_fourteen_points(self):
        """Return True with a strong 7 card suit and 14 points."""
        result = (self.shape[0] >= 7 and
                  self. hcp >= 14 and
                  self.suit_points(self.longest_suit) >= 8)
        return result

    def _has_ten_points_and_can_support_opener(self, suit_to_bid, suit_support_points):
        """Return True with 10+points and can support opener."""
        result = (self._can_support_opener(suit_to_bid) and
                  (suit_support_points >= 10 or
                   self.suit_length(suit_to_bid) >= 4 and
                   self.hcp >= 10))
        return result

    def _has_eleven_points_and_three_suits_bid(self):
        """Return True with 11+ points and three suits bid."""
        result = (self.hcp >= 11 and
                  self.three_suits_bid_and_stopper() and
                  self.is_semi_balanced and
                  self.nt_level <= 2)
        return result

    def _can_support_minor_but_is_semi_balanced(self, suit_to_bid, suit_support_points):
        """Return True if can support minor and semi_balanced."""
        result = (suit_support_points >= 13 and
                  suit_to_bid.is_minor and
                  self.is_semi_balanced and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 2 and
                  self.shape[3] >= 2)
        return result

    def _is_balanced_support_for_openers_second_suit(self, suit_to_bid):
        """Return True if suit is opener's second and is balanced."""
        result = (suit_to_bid == self.opener_bid_two.denomination and
                  self.suit_length(suit_to_bid) <= 3 and
                  self.is_balanced and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 2)
        return result

    def _has_three_card_support_for_openers_major(self):
        """Return True if 3 card support for opener's major."""
        result = (self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  self.opener_bid_one.denomination.is_major and
                  self.suit_length(self.opener_bid_one.denomination) >= 3
                  and self.next_level(self.opener_bid_one.denomination) <= 3)
        return result

    def _is_strong_has_stoppers(self):
        """Return True if very strong with stoppers."""
        result = (self.is_jump(self.bid_one, self.opener_bid_two) and
                  self.hcp >= 16 and
                  self.stoppers_in_unbid_suits and
                  self.nt_level <= 4)
        return result

    def _is_distributional_and_barrier_not_broken(self, suit_to_bid):
        """Return True if distributional and barrier not broken."""
        trial_bid = self.next_level_bid(suit_to_bid)
        barrier_is_broken = self.barrier_is_broken(self.opener_bid_one, self.opener_bid_two)
        result = (not trial_bid.is_game and
                  self.five_five_or_better or
                  (self.suit_length(suit_to_bid) < 7 and
                   self.shape[0] >= 6 and not barrier_is_broken) or
                  (self.shape[0] >= 6 and
                   self.hcp >= 10) and
                  trial_bid.level <= 2)
        return result

    def _has_biddable_five_card_major(self, suit_to_bid):
        """Return True with biddable major."""
        result = (5 <= self.hcp <= 9 and
                  suit_to_bid.is_minor and
                  self.longest_suit.is_major and
                  self.suit_points(self.longest_suit) >= 5 and
                  not self.competitive_auction and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _opener_has_doubled_can_bid_suit(self, suit_to_bid):
        """Return True if weak hand passes suit test."""
        result = (self.opener_bid_two.is_double and
                  Bid(self.bid_history[-1]).is_pass and
                  (self.next_level_bid(suit_to_bid).level <= 2 or
                   self.hcp >= 8) and
                  (self.hcp >= 6 or self.suit_length(suit_to_bid) >= 4) and
                  suit_to_bid not in self.opponents_suits)
        return result

    def _is_weak_can_bid_suit(self, suit_to_bid):
        """Return True if weak hand passes suit test."""
        result = ((self.next_level_bid(suit_to_bid).level <= 2 or
                   self.hcp >= 8) and
                  (self.hcp >= 6 or self.suit_length(suit_to_bid) >= 4) and
                  suit_to_bid not in self.opponents_suits)
        return result

    def _is_weak_can_show_preference(self, suit_to_bid):
        """Return True if hand can make suit preference."""
        result = (Bid(self.bid_history[-1]).is_pass and
                  self.next_level(suit_to_bid) <= 2 and
                  self.opener_bid_two.denomination != suit_to_bid)
        return result

    def _has_eleven_points_and_opening_bid_is_major(self):
        """Return True if opening bid is major and 11+ points."""
        result = (self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  self.opener_bid_one.denomination.is_major and
                  self.hcp >= 11 and
                  self.suit_length(self.opener_bid_one.denomination) >= 3 and
                  self.next_level(self.opener_bid_one.denomination) <= 4)
        return result

    def _has_eleven_points_five_four_no_support_for_opening_bid(self):
        """Return True with 11 +points, no support for opening bid and 5/4."""
        result = (self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  self.five_four_or_better and
                  self.suit_length(self.opener_bid_one.denomination) <= 3 and
                  self.hcp >= 11 and
                  self.second_suit not in self.opponents_suits)
        return result

    def _has_eleven_points_five_card_suit_no_support_for_opening_bid(self):
        """Return True with 11 +points, no support for opening bid and semi_balanced."""
        result = (self.opener_bid_one.denomination != self.opener_bid_two.denomination and
                  self.is_semi_balanced and
                  self.shape[0] >= 5 and
                  self.suit_length(self.opener_bid_one.denomination) <= 3 and
                  self.hcp >= 11 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _can_bid_suit_at_next_level(self, suit_to_bid):
        """Return True with 12 points or 9 points and major"""
        result = ((self.hcp >= 12 or
                  (self.hcp >= 9 and suit_to_bid.is_major)) and
                  suit_to_bid not in self.opponents_suits)
        return result

    def _nine_points_bid_up_to_level_four(self, suit_to_bid):
        """Return True points greater."""
        result = (self.hcp >= 9 and
                  suit_to_bid.is_suit and
                  suit_to_bid not in self.opponents_suits and
                  self.next_level(suit_to_bid) <= 4)
        return result

    def _eight_points_and_stoppers(self):
        """Return True if 8+ points and stoppers."""
        result = (self.hcp >= 9 and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _seven_points_or_level_two_or_some_support(self):
        """Return True if some possibility to bid."""
        result = ((self.hcp >= 7 or
                  self.opener_bid_two.level <= 2 or
                  self.suit_length(self.opener_bid_one.denomination) >= 2))
        return result

    def _fourteen_points_and_support_for_second_suit(self):
        """Return True if 14+ points and support for second suit."""
        trial_bid = self.next_level_bid(self.second_suit, raise_level=1)
        result = (self.opener_bid_two.denomination == self.second_suit and
                  self.hcp <= 14 and
                  (not trial_bid.is_game or
                   self.is_jump(self.opener_bid_one, self.opener_bid_two)))
        return result

    def _opener_has_rebid_one_nt_and_nt_level_is_two(self):
        """Return True if opener bid 1NT with 9+ points."""
        result = (self.opener_bid_two.name == '1NT' and
                  self.shape[0] <= 5 and
                  self.hcp == 9 and
                  self.nt_level <= 2)
        return result

    def _opener_has_rebid_one_nt_and_six_card_major(self):
        """Return True if opener bid 1NT with 9+ points and six card major."""
        result = (self.opener_bid_two.name == '1NT' and
                  self.hcp == 9 and
                  self.shape[0] >= 6 and
                  self.longest_suit.is_major and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _opener_has_rebid_one_nt_and_five_card_suit(self):
        """Return True if opener bid 1NT with 9+ points."""
        result = (self.opener_bid_two.name == '1NT' and
                  self.hcp == 9 and
                  self.shape[0] >= 5 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _opener_rebid_two_nt_and_five_four_and_shortage(self):
        """Return True if opener rebids 2NT and 5/4."""
        result = (self.opener_bid_two.name == '2NT' and
                  self.hcp >= 6 and
                  not self._has_bid_four_card_major_at_one_level() and
                  self.five_four_or_better and
                  self.suit_length(self.opener_bid_one.denomination) <= 1 and
                  self.second_suit not in self.opponents_suits)
        return result

    def _has_bid_four_card_major_at_one_level(self):
        """Return True if a weak hand has bid 4 card major at one level."""
        result = (self.hcp <= 6 and
                  self.bid_one.is_major and
                  self.bid_one.denomination != self.longest_suit)
        return result

    def _has_six_card_suit_and_level_three(self):
        """Return True if siz card suit and next level <= 3."""
        result = (4 <= self.hcp <= 7 and
                  self.shape[0] >= 6 and
                  self.longest_suit not in self.opponents_suits and
                  self.second_suit not in self.opponents_suits and
                  self.next_level(self.longest_suit) <= 3)
        return result

    def _has_shortage(self):
        """Return True if has shortage and level <= 3."""
        result = (self.hcp >= 5 and
                  self.shape[3] <= 1 and
                  self.shape[0] >= 5 and
                  self.next_level(self.longest_suit) <= 3 and
                  self.longest_suit not in self.opponents_suits and
                  not self._has_bid_four_card_major_at_one_level())
        return result

    def _opponents_doubled_openers_nt(self):
        """Return True if opponents have doubled openers NT bid."""
        result = (self.hcp >= 5 and
                  self.opponents_have_doubled and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _has_seven_card_suit_and_fourteen_points(self):
        """Return True if 7 card suit and 14+ points."""
        result = (self.opener_bid_two.name == '2NT' and
                  self.shape[0] >= 7 and
                  self.hcp >= 14)
        return result

    def _has_five_four_and_no_support(self):
        """Return True if 5/4 and no support."""
        result = (self.five_four_or_better and
                  self.hcp >= 14 and
                  self.suit_length(self.opener_bid_one.denomination) <= 2 and
                  self.second_suit not in self.opponents_suits)
        return result

    def _has_five_four_and_fewer_than_ten_points(self):
        """Return True if 5/4 and fewer than 10 points."""
        result = (self.hcp <= 9 and
                  self.five_four_or_better and
                  not self.bid_one.is_pass and
                  self.second_suit not in self.opponents_suits)
        return result

    def _can_bid_spades(self):
        """Return True if 5+ spades and level <= 3."""
        result = (self.spades >= 5 and
                  self.my_last_bid.denomination != self.spade_suit and
                  self.next_level(self.spade_suit) <= 3 and
                  self.spade_suit not in self.opponents_suits)
        return result

    def _has_four_card_support_at_level_three(self):
        """Return True if has 4 card support at level 3."""
        result = (self.opener_bid_one.is_suit_call and
                  self.suit_length(self.opener_bid_one.denomination) >= 4 and
                  self.hand_value_points(self.opener_bid_one.denomination) >= 10 and
                  self.next_level(self.opener_bid_one.denomination) <= 3)
        return result

    def _has_six_card_suit_after_nt_opening(self):
        """Return True if opening bid is nt and has 6 card suit."""
        result = (self.opener_bid_one.is_nt and
                  self.shape[0] >= 6 and
                  not self.overcaller_bid_one.is_double and
                  self.longest_suit not in self.opponents_suits and
                  self.next_level(self.longest_suit) <= 3 and
                  self.hcp >= 6)
        return result

    def _has_strong_six_card_suit_at_level_two(self):
        """Return True if strong 6 card suit at level 2."""
        result = (self.shape[0] >= 6 and
                  self.suit_points(self.longest_suit) >= 7 and
                  self.next_level(self.longest_suit) <= 2 and
                  self.longest_suit not in self.opponents_suits)
        return result

    def _is_balanced_thirteen_points(self):
        """Return True if is balanced with 13+ points."""
        result = (self.hcp >= 13 and
                  # self.is_balanced and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _can_bid_second_suit_at_level_three(self):
        """Return True if can bid second suit at level 3."""
        result = (((self.hcp >= 7 and
                  (self.suit_length(self.second_suit) >= 6 or
                   self.next_level_bid(self.second_suit).level <= 2) or
                  self.hcp >= 12) or

                  (self.shape[1] >= 4 and
                   self.hcp >= 6 and
                   self.next_level(self.second_suit) <= 3)) and

                  self.second_suit not in self.opponents_suits)
        return result

    def _is_strong_unbalanced_and_two_card_support_for_opener(self):
        """Return True if strong_unbalanced and 2 card support for opener."""
        result = (self.hcp >= 16 and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  not self.is_balanced)
        return result

    def _suit_to_support_is_minor_and_stoppers(self, suit_to_bid):
        """Return True if suit is minor and stoppers."""
        if self.hcp <= 9:
            level = 1
        elif self.hcp <= 13:
            level = 2
        else:
            level = 3
        result = (suit_to_bid.is_minor and
                  # self.is_balanced and
                  self.stoppers_in_unbid_suits() and
                  self.nt_level <= level)
        return result

    def _opener_bid_new_suit_level_three_and_semi_balanced(self, suit_preference):
        """Return True if opener has bid new suit at level 3 and semi balanced."""
        result = (suit_preference.is_minor and
                  suit_preference == self.opener_bid_two.denomination and
                  self.hcp >= 6 and
                  self.opener_bid_two.level == 3 and
                  self.stoppers_in_bid_suits and
                  self.is_semi_balanced and
                  self.nt_level <= 3)
        return result

    def _opener_repeats_major_at_level_three_balanced(self):
        """Return True if opener repeats major at 3 level and balanced."""
        result = (self.is_balanced and
                  self.opener_bid_one.is_major and
                  self.opener_bid_two.level == 3 and
                  self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                  self.suit_length(self.opener_bid_two.denomination) <= 3 and
                  self.stoppers_in_bid_suits and
                  self.nt_level <= 3)
        return result

    def _can_support_openers_major(self):
        """Return True if can support opener's major."""
        result = (self.opener_bid_one.is_major and
                  self.suit_length(self.opener_bid_one.denomination) >= 3 and
                  not self.opener_bid_two.is_game)
        return result

    def _intermediate_balanced_cannot_rebid_suit(self):
        """Return True if intermediate and balanced."""
        result = (self.hcp >= 15 and
                  self.is_balanced and
                  (self.longest_suit.is_minor or
                   self.shape[0] == 4) and
                  self.nt_level <= 3)
        return result

    def _opener_has_shown_six_card_suit(self):
        """Return True if opener has shown a six card suit."""
        result = (self.opener_bid_one.denomination == self.opener_bid_two.denomination and
                  self.opener_bid_two.level == 3 and
                  self.suit_length(self.opener_bid_one.denomination) >= 2 and
                  self.longest_suit.is_minor)
        return result

    def _is_strong_can_show_second_suit(self):
        """Return True if strong and can show second suit."""
        result = (self.hcp >= 16 and
                  self.shape[1] >= 4 and
                  self.next_level(self.second_suit) <= 4 and
                  self.second_suit not in self. opponents_suits)
        return result

    def _cannot_support_openers_first_suit(self):
        """Return True if can support opener's first suit."""
        result = (self.shape[1] >= 5 and
                  self.suit_length(self.opener_bid_one.denomination) <= 4 and
                  self.second_suit not in self.opponents_suits)
        return result

    def _no_support_but_nt_possible(self, suit_preference):
        """Return True if no support but nt possible."""
        support_points = (self.support_points(self.opener_bid_one.denomination) +
                          self.support_points(self.opener_bid_two.denomination))
        result = (self.hcp >= 7 and
                  self.suit_length(suit_preference) <= 1 and
                  self.nt_level <= 3 and
                  support_points >= 4 and
                  self.stoppers_in_bid_suits)
        return result

    def _has_five_four_and_can_show_second_suit(self):
        """Return True if has 5/4 and can show second suit."""
        result = (self.five_four and
                  10 <= self.hcp <= 15 and
                  self.next_level(self.second_suit) <= 2 and
                  self.second_suit not in self.opponents_suits)
        return result

    def _support_for_openers_major_after_nt_opening(self):
        """Return True if support for opener's major."""
        result = (self.opener_bid_two.is_suit_call and
                  self.hcp >= 12 and 
                  self.suit_length(self.opener_bid_two.denomination) >= 3 and 
                  self.opener_bid_two.denomination.is_major)
        return result

    def _is_balanced_intermediate_stoppers(self, suit_to_bid):
        """Return True if balanced with 10 to 12 points and stoppers."""
        result = (self.is_balanced and 
                  10 <= self.hcp <= 12 and 
                  self.stoppers_in_unbid_suits() and 
                  suit_to_bid.is_minor and self.nt_level <= 2)
        return result

    def _nt_can_support_minor(self):
        """Return True if longest suit  is openers opening minor."""
        result = (self.opener_bid_two.name == '2NT' and
                  self.opener_bid_one.is_minor and
                  self.is_semi_balanced and
                  self.nt_level <= 3 and
                  self.longest_suit == self.opener_bid_one.denomination)
        return result
    
    def _has_six_card_suit_and_opening_points(self):
        """Return True if long suit and opening values."""
        result = (self.hcp >= 12 and 
                  self.shape[0] >= 6 and 
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
