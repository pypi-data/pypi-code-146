"""
    Bid for Game
    Acol opening bid module
"""
import inspect
from .bridge_tools import Pass, HandSuit
from .hand import Hand


class OpeningBid(Hand):
    """BfG OpeningBid class."""
    def __init__(self, hand_cards, board):
        super(OpeningBid, self).__init__(hand_cards, board)
        self.trace = 0

    def suggested_bid(self):
        """Directs control to relevant method and return a Bid."""
        if self.hcp >= 23:
            bid = self.club_bid(2, '0005')
        elif self.is_balanced or (self.is_semi_balanced and 20 <= self.hcp <= 22):
            bid = self._balanced_openings()
        elif self._can_open_normally():
            bid = self._unbalanced_openings()
        elif self.shape[0] >= 6:
            bid = self._weak_opening_bid()
        else:
            bid = Pass('0025')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _can_open_normally(self):
        """Return True if hand suitable for opening bid."""
        if self.hcp >= 12:
            value = True
        elif (self.hcp == 11 and  (self.shape[0] >= 6 or self.five_five) or
              (self.five_four and self.suit_points(self.longest_suit) + self.suit_points(self.second_suit) >= 11)):
            value = True
        else:
            value = False
        return value

    def _balanced_openings(self):
        """Return bid for balanced hands."""
        if 12 <= self.hcp <= 14:
            bid = self._weak_balanced_bid()
        elif 14 <= self.hcp < 20:
            bid = self._unbalanced_openings()
        elif 20 <= self.hcp <= 22:
            bid = self.nt_bid(2, '0001')
        else:
            bid = Pass('0003')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_balanced_bid(self):
        """Return bid for weak (12-14) balanced hands."""
        if self._five_card_major_with_seven_suit_points():
            bid = self._unbalanced_openings()
        else:
            bid = self.nt_bid(1, '0004')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _unbalanced_openings(self):
        """ return bid for unbalanced hands."""
        # points checked before entry to here
        if self.shape[0] >= 8 and self.hcp <= 14:
            bid = self._weak_eight_card_suits_bid()
        elif self.shape[0] >= 5:
            bid = self._bid_with_five_card_suit()
        elif self.shape == [4, 4, 4, 1]:
            bid = self._four_four_four_one_bid()
        else:
            bid = self._four_card_suits()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_eight_card_suits_bid(self):
        """Return bid for 8+ card suits and fewer than 15 points."""
        suit = self.longest_suit
        if suit.is_major:
            game_level = 4
        else:
            game_level = 5
        level = self.shape[0] - 4
        level = min(level, game_level)
        if self.longest_suit.is_minor and self.shape[1] >= 4:
            bid = self.suit_bid(1, self.longest_suit, '0253')
        else:
            bid = self.suit_bid(level, suit, '0006')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _four_card_suits(self):
        """Return bid with two four card suits."""
        if self.spades == 4:
            bid = self._four_spades()
        elif self.hearts == 4:
            bid = self.heart_bid(1, '0007')
        elif self.diamonds == 4:
            bid = self._four_diamonds()
        else:
            bid = self.club_bid(1, '0008')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _four_spades(self):
        """Return bid if hand has 4 spades."""
        if self.hearts == 4:
            bid = self.heart_bid(1, '0009')
        elif self.diamonds == 4:
            bid = self.spade_bid(1, '0010')
        elif self.clubs == 4:
            bid = self.club_bid(1, '0011')
        else:
            bid = self.spade_bid(1, '0012')  # 4,3,3,3
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _four_diamonds(self):
        """Return bid if hand has 4 diamonds (and possibly 4 clubs)."""
        if self.clubs == 4:
            bid = self.club_bid(1, '0013')
        else:
            bid = self.diamond_bid(1, '0014')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _bid_with_five_card_suit(self):
        """Return bid with two five card suits."""
        if (self.longest_suit.is_minor and
                self.is_semi_balanced and
                self.hcp >= 20):
            bid = self.suit_bid(2, self.club_suit, '0015')
        elif not self.equal_long_suits:
            bid = self.suit_bid(1, self.longest_suit, '0016')
            if self.hcp <= 11 and self.shape[0] == 5 and self.shape[1] == 4:
                bid.call_id = '0681'
            elif self.hcp <= 11:
                bid.call_id = '0680'
        else:
            bid = self._five_five_hands_bid()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_five_hands_bid(self):
        """Return bid for five/five hands."""
        if self.spades >= 5 and self.clubs >= 5:
            bid = self.club_bid(1, '0017')
        elif self.spades >= 5:
            bid = self.spade_bid(1, '0018')
        elif self.hearts >= 5:
            bid = self.heart_bid(1, '0019')
        elif self.diamonds >= 5:
            bid = self.diamond_bid(1, '0020')
        else:
            assert False, 'Bid not defined'
        if self.hcp <= 11:
            bid.call_id = '0569'
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _four_four_four_one_bid(self):
        """Return bid for 4441 hands."""
        if self.clubs == 1:
            bid = self.heart_bid(1, '0021')
        elif self.diamonds == 1:
            bid = self.club_bid(1, '0022')
        elif self.hearts == 1:
            bid = self.diamond_bid(1, '0023')
        elif self.spades == 1:
            bid = self.heart_bid(1, '0024')
        else:
            assert False, 'Bid not defined'
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_opening_bid(self):
        """Return bid for weak opening hands."""
        if self.six_six:
            return self._weak_six_six_bid()
        else:
            bid = self._select_weak_bid()
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _select_weak_bid(self):
        """Return weak bids."""
        if self.hcp >= 6 and self.shape[0] == 6:
            bid = self._weak_two_bid()
        elif self.shape[0] >= 7:
            bid = self._weak_three_bid()
        else:
            bid = Pass('0026')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_two_bid(self):
        """Return weak two bid."""
        suit = self.longest_suit
        suit_quality = HandSuit(suit, self).suit_quality()
        if suit != self.club_suit and suit_quality >= 0:
            bid = self.suit_bid(2, suit, '0027')
        else:
            bid = Pass('0028')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_three_bid(self):
        """Return weak three bid."""
        suit = self.longest_suit
        suit_quality = HandSuit(suit, self).suit_quality()
        if self.hcp <= 9 and suit_quality >= 0.5:
            bid = self.suit_bid(3, suit, '0029')
        else:
            bid = Pass('0030')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _weak_six_six_bid(self):
        """Return bid for  weak hand with two six card suits."""
        if self.hcp < 6:
            bid = Pass('0031')
        elif self.spades == 6 and self.has_stopper(self.spade_suit):
            bid = self.spade_bid(2, '0032')
        elif self.hearts == 6 and self.has_stopper(self.heart_suit):
            bid = self.heart_bid(2, '0033')
        elif (self.diamonds == 6 and
              self.has_stopper(self.diamond_suit)):
            bid = self.diamond_bid(2, '0034')
        else:
            bid = Pass('0035')
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def _five_card_major_with_seven_suit_points(self):
        """Returns True if hand has 5 card major with 7 points in that suit."""
        result = False
        for suit in (self.spade_suit, self.heart_suit):
            if (self.cards_in_suit(suit) == 5 and
                    self.suit_points(suit) >= 7):
                result = True
        return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result

    # def xxx(self):
    #     """Return True if xxx."""
    #     result = False
    #     return result
