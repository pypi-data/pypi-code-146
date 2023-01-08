""" Bid for Game Hand module."""
import os
import json
import inspect
from .bridge_tools import Bid, Pass
from bridgeobjects import Hand, Card, Call, Suit, NoTrumps, SUIT_NAMES, CALLS, SUITS


class Hand(Hand):
    """A sub class of bridgeobjects Hand, to enable bidding."""
    MODULE_TRACE = 'batch_tests/data//module_trace.txt'
    OVERCALLER_POSITION = {'none': 0, 'second_seat': 1, 'fourth_seat': 2}

    spade_suit, heart_suit, diamond_suit, club_suit = SUITS['S'], SUITS['H'], SUITS['D'], SUITS['C']

    def __init__(self, hand_cards=None, board=None, *args, **kwargs):
        super().__init__(hand_cards, *args, **kwargs)
        self.board = board
        self.suits = [SUITS[name] for name in 'CDHS']
        self.no_trumps = NoTrumps()
        if board:
            self.bid_history = board.active_bid_history
            if len(self.bid_history) % 2 == 0:
                self.overcaller = False
            else:
                self.overcaller = True
        else:
            self.bid_history = []
            self.overcaller = False
        self._losers = None
        self.overcaller_in_second_seat = False
        self.overcaller_in_fourth_seat = False

        # Initialise specific bids
        pass_bid = Pass()
        self.opener_bid_one = pass_bid
        self.opener_bid_two = pass_bid
        self.opener_bid_three = pass_bid
        self.responder_bid_one = pass_bid
        self.responder_bid_two = pass_bid
        self.responder_bid_three = pass_bid
        self.overcaller_bid_one = pass_bid
        self.overcaller_bid_two = pass_bid
        self.overcallers_last_bid = pass_bid
        self.advancer_bid_one = pass_bid
        self.advancer_bid_two = pass_bid
        self.previous_bid = pass_bid
        self.last_bid = pass_bid
        self.right_hand_bid = pass_bid
        self.my_last_bid = pass_bid
        self.partner_bid_one = pass_bid
        self.partner_bid_two = pass_bid
        self.partner_last_bid = pass_bid
        self.bid_one = pass_bid
        self.bid_two = pass_bid
        self.bid_three = pass_bid
        self.unplayed_cards = [card for card in self.cards]

        self.responders_support = False
        self.overcaller_has_jumped = False
        self.bid_after_stayman = False

        self.assign_bids()
        self._update_longest_suit()
        self.trace_module, self.last_hand = self._get_trace_module()

    def to_json(self):
        """Return object as json string property."""
        json_str = json.dumps({
            'cards': [card.name for card in self.cards],
            'unplayed_cards': [card.name for card in self.unplayed_cards],
        })
        return json_str

    def from_json(self, json_str):
        """Populate the attributes from the json string."""
        hand_dict = json.loads(json_str)
        self.cards = [Card(name) for name in hand_dict['cards']]
        self.unplayed_cards = [Card(name) for name in hand_dict['unplayed_cards']]

    def _update_longest_suit(self):
        """Change the longest suit if partner has bid it."""
        if 4 <= self.shape[1] == self.shape[0]:
            if 1 < len(self.bid_history) <= 4:
                partners_suit = Bid(self.bid_history[-2]).denomination
                if self.longest_suit == partners_suit and self.second_suit not in self. opponents_suits:
                    self._longest_suit, self._second_suit = self.second_suit, self.longest_suit

    @property
    def longest_suit(self):
        """Return the longest_suit."""
        return self._longest_suit

    @property
    def second_suit(self):
        """Return the second suit."""
        return self._second_suit

    @property
    def nt_level(self):
        """Return the level of no trumps"""
        return self.next_nt_bid().level

    @property
    def losers(self):
        """Return the number of losers in the Hand."""
        if not self._losers:
            self._losers = self._get_losers()
        return self._losers

    def _get_losers(self):
        """Calculate and return the number of losers in the Hand."""
        losers = 0
        losers_by_suit = {
            'S': [0, 0],
            'H': [0, 0],
            'D': [0, 0],
            'C': [0, 0],
        }
        for suit in SUIT_NAMES:
            cards = [card for card in self.cards_by_suit[suit]]
            honour_count = 0
            for card in cards:
                if card.value >= 12:
                    honour_count += 1
                elif card.value == 11:
                    if self.suit_points(suit) > 2:
                        honour_count += 1
            count = min(3, len(cards))
            losers += count - honour_count
        return losers

    def assign_bids(self):
        """Assign bids based on bid_history."""
        bids = len(self.bid_history)

        if bids >= 1:
            self.opener_bid_one = Bid(self.bid_history[0])
            self.last_bid = Bid(self.bid_history[-1])
            if bids == 1:
                return

        if bids >= 2:
            self._assign_overcaller_seat()
            self.overcaller_bid_one = Bid(self.bid_history[1])
            # noinspection PyTypeChecker
            self.overcaller_has_jumped = self.is_jump(self.opener_bid_one,
                                                      self.overcaller_bid_one)
            self.right_hand_bid = Bid(self.bid_history[-1])
            self.partner_last_bid = Bid(self.bid_history[-2])
            self.partner_bid_one = Bid(self.bid_history[-2])
            if bids == 2:
                return

        if bids >= 3:
            self.responder_bid_one = Bid(self.bid_history[2])
            self.responders_support = (self.opener_bid_one.denomination ==
                                       self.responder_bid_one.denomination)
            if bids == 3:
                return

        if bids >= 4:
            self.advancer_bid_one = Bid(self.bid_history[3])
            self.bid_one = Bid(self.bid_history[-4])
            self.previous_bid = Bid(self.bid_history[-4])
            if self.overcaller_in_fourth_seat:
                self.overcaller_bid_one = Bid(self.bid_history[3])
                # noinspection PyTypeChecker
                self.overcaller_has_jumped = self.is_jump(self.responder_bid_one,
                                                          self.overcaller_bid_one)
            self.my_last_bid = Bid(self.bid_history[-4])
            if bids == 4:
                return

        if bids >= 5:
            self.opener_bid_two = Bid(self.bid_history[4])
            self.bid_after_stayman = self._bid_after_stayman()
            if bids == 5:
                return

        if bids >= 6:
            self.partner_bid_one = Bid(self.bid_history[-6])
            self.partner_bid_two = Bid(self.bid_history[-2])
            if self.overcaller_in_fourth_seat:
                self.overcaller_bid_one = Bid(self.bid_history[3])
                self.advancer_bid_one = Bid(self.bid_history[5])
            if bids == 6:
                return

        if bids >= 7:
            self.responder_bid_two = Bid(self.bid_history[6])
            self.overcaller_bid_two = Bid(self.bid_history[5])
            if bids == 7:
                return

        if bids >= 8:
            self.bid_one = Bid(self.bid_history[-8])
            self.bid_two = Bid(self.bid_history[-4])
            self.overcallers_last_bid = Bid(self.bid_history[-1])
            if self.overcaller_in_fourth_seat:
                self.overcaller_bid_two = Bid(self.bid_history[7])
            else:
                self.advancer_bid_two = Bid(self.bid_history[7])
            if bids == 8:
                return

        if bids >= 9:
            self.opener_bid_three = Bid(self.bid_history[8], '')
            if bids == 9:
                return

        if bids >= 10:
            self.partner_bid_one = Bid(self.bid_history[-10])
            self.partner_bid_two = Bid(self.bid_history[-6])

        if bids >= 11:
            self.responder_bid_three = Bid(self.bid_history[10])
            # self.overcaller_bid_two = Bid(self.bid_history[5])

        if bids >= 12:
            self.bid_one = Bid(self.bid_history[-12])
            self.bid_two = Bid(self.bid_history[-8])
            self.bid_three = Bid(self.bid_history[-4])

    def _assign_overcaller_seat(self):
        """Assign seat to overcaller."""
        if len(self.bid_history) >= 2:
            if Bid(self.bid_history[1]).name != Pass().name:
                self.overcaller_in_second_seat = True
            elif (len(self.bid_history) >= 4 and
                    not Bid(self.bid_history[3]).is_pass):
                self.overcaller_in_fourth_seat = True

    def _get_trace_module(self):
        """Return the name of the module to trace."""
        if os.path.isfile(self.MODULE_TRACE):
            with open(self.MODULE_TRACE, 'r') as f_trace_file:
                text = f_trace_file.read()
                text = text.split('\n')
                text.extend(['', ''])
                return text[0], text[1]
        else:
            return None, None

    def _set_trace_hand(self):
        """Write the current hand to the trace file."""
        if os.path.isfile(self.MODULE_TRACE):
            with open(self.MODULE_TRACE, 'w') as f_trace_file:
                f_trace_file.write('\n'.join([self.trace_module, self.__str__()]))

    def is_insufficient_bid(self, test_bid):
        """Return True if the bid is insufficient."""
        last_bid = None
        for last_bid in self.bid_history[::-1]:
            if Bid(last_bid).is_value_call:
                break
        last_bid_index = CALLS.index(last_bid)
        test_bid_index = CALLS.index(test_bid.name)
        if test_bid_index <= last_bid_index:
            result = True
        else:
            result = False
        return result

    @property
    def singleton_honour(self):
        """Return True if hand has singleton K or Q."""
        return self._singleton_honour()

    def _singleton_honour(self):
        """Return True if hand has singleton K or Q."""
        if self.shape[3] == 1:
            for suit_name in SUIT_NAMES:
                suit = Suit(suit_name)
                if self.suit_length(suit) == 1:
                    for card in self.cards:
                        if card.suit == suit:
                            if card.rank in 'KQ':
                                return True
        return False

    @property
    def opponents_have_bid(self):
        """Return True if the opponents have made a bid."""
        return self._opponents_have_bid()

    def _opponents_have_bid(self):
        """Return True if the opponents have made a bid."""
        for bid in self.bid_history[1::2]:
            if Bid(bid).is_value_call:
                return True
        return False

    @property
    def competitive_auction(self):
        """Return True if the last bid is not Pass or Double."""
        return self._competitive_auction()

    def _competitive_auction(self):
        """Return True if the last bid is not Pass or Double."""
        value = False
        if len(self.bid_history) >= 1:
            value = Bid(self.bid_history[-1]).is_value_call
        if len(self.bid_history) >= 3:
            value = value or Bid(self.bid_history[-3]).is_value_call
        if len(self.bid_history) >= 5:
            value = value or Bid(self.bid_history[-5]).is_value_call
        return value

    @staticmethod
    def _is_value_call_or_double(bid):
        """Return True if is value call or double."""
        call = Bid(bid)
        value = call.is_value_call or call.is_double
        return value

    @property
    def opponents_have_doubled(self):
        """Return True if opponents have doubled with no further bid from them."""
        return self._opponents_have_doubled()

    def _opponents_have_doubled(self):
        """Return True if opponents have doubled with no further bid from them."""
        value = False
        if len(self.bid_history) >= 1:
            if Bid(self.bid_history[-1]).is_double:
                value = True
            elif len(self.bid_history) >= 3:
                if(Bid(self.bid_history[-3]).is_double and
                        Bid(self.bid_history[-1]).is_pass):
                    value = True
        return value

    @property
    def partner_has_passed(self):
        """Return True of partner passed on first round."""
        return self._partner_has_passed()

    def _partner_has_passed(self):
        """Return True of partner passed on first round."""
        value = False
        if len(self.bid_history) >= 5:
            if Bid(self.bid_history[-5]).is_pass:
                value = True
        return value

    def _bid_after_stayman(self):
        """Return True if responder has bid Clubs after NT opening."""
        result = False
        if (self.opener_bid_one.is_nt and
                self.responder_bid_one.denomination == self.club_suit):
            result = True
        return result

# TODO: sort out use of shortage points
    def suit_bid(self, level, suit, comment='0000', use_shortage_points=False):
        """Return a bid in the suit at the given level."""
        return Bid(self._call_name(level, suit.name), comment, use_shortage_points)

    def heart_bid(self, level, comment='0000', use_shortage_points=False):
        """Return a bid in Hearts at the given level."""
        return Bid(self._call_name(level, 'H'), comment, use_shortage_points)

    def spade_bid(self, level, comment='0000', use_shortage_points=False):
        """Return a bid in Spades at the given level."""
        return Bid(self._call_name(level, 'S'), comment, use_shortage_points)

    def club_bid(self, level, comment='0000', use_shortage_points=False):
        """Return a bid in Clubs at the given level."""
        return Bid(self._call_name(level, 'C'), comment, use_shortage_points)

    def diamond_bid(self, level, comment='0000', use_shortage_points=False):
        """Return a bid in Diamonds at the given level."""
        return Bid(self._call_name(level, 'D'), comment, use_shortage_points)

    def nt_bid(self, level, comment='0000', use_shortage_points=False):
        """Return a bid in NT at the given level."""
        return Bid(self._call_name(level, 'NT'), comment, use_shortage_points)

    def barrier_is_broken(self, first_bid, second_bid):
        """Return True if second_bid breaks the barrier relative to bid_one."""
        broken = False
        level_one = first_bid.level
        barrier = Bid(self._call_name(level_one+1, first_bid.denomination.name))
        # noinspection PyTypeChecker
        if self._higher_bid(barrier, second_bid):
            broken = True
        return broken

    def cheapest_long_suit(self):
        """Return the longest suit or cheapest of equal length suits to bid."""
        if self.shape[0] > self.shape[1] and self.longest_suit not in self.opponents_suits:
            return self.longest_suit
        else:
            max_length = self.shape[1]
            last_bid_denomination = self._last_denomination_called()
            extended_suit_list = self._get_extended_suit_list()

            # find the starting index in the extended suit list
            index = extended_suit_list.index(last_bid_denomination)

            # find the level of NT in the middle of the extended suit list
            nt_level = self.nt_level
            while index < len(extended_suit_list) - 1 and index < 8:
                index += 1
                if index >= 4:
                    # if we're in the second half, increment the level by 1.
                    # I.e. we have past NT and onto the next level
                    level =  nt_level + 1
                else:
                    level = nt_level

                # test the next suit
                suit = extended_suit_list[index]
                if (self.suit_length(suit) == max_length and
                        self.next_level(suit) == level and
                        suit not in self.opponents_suits):
                    return suit
            else:
                return None

    def _last_denomination_called(self):
        """Return the denomination of the last value call."""
        for bid in self.bid_history[::-1]:
            call = Bid(bid)
            if call.is_suit_call:
                return call.denomination
        else:
            assert False, 'Last denomination called with no value call in history'

    @staticmethod
    def _get_extended_suit_list():
        """Return an extended list of sorted of suits, e.g. [C, D, H, S, C, D, H, S]."""
        extended_suit_list = [Suit(name) for name in SUIT_NAMES]
        extended_suit_list.sort(key=lambda x: x.rank)

        # get a double suit list, e.g. [C, D, H, S, C, D, H, S]
        extended_suit_list.extend(extended_suit_list)
        return extended_suit_list

    @staticmethod
    def _higher_bid(first_bid, second_bid):
        """Return True if first_bid is the lower."""
        higher = False
        level_one = first_bid.level
        level_two = second_bid.level
        if level_two > level_one:
            higher = True
        else:
            if level_one == level_two:
                if first_bid.denomination < second_bid.denomination:
                    higher = True
        return higher

    @staticmethod
    def is_jump(first_bid, second_bid):
        """Return True if second bid is a jump over first."""
        # e.g.  first_bid = Bid('1S')
        #       second_bid = Bid('2NT')
        result = False
        if second_bid.is_value_call and first_bid.is_value_call:
            jump_level = second_bid.level - first_bid.level
            if jump_level > 1:
                result = True
            elif jump_level == 1:
                if second_bid.is_suit_call and first_bid.is_suit_call:
                    if second_bid.denomination > first_bid.denomination:
                        result = True
                elif second_bid.is_nt:
                    result = True
            else:
                result = False
        return result

    def jump_bid_made(self, test_bid):
        """Test bid against bid-history and return True
           if test_bid is a jump over last relevant bid.
        """
        second_bid = None
        for bid in self.bid_history[::-1]:
            if bid != 'P' and bid != 'D' and bid != 'R':
                second_bid = Bid(bid)
                break
        jump_level = test_bid.level - second_bid.level
        if jump_level > 1:
            result = True
        elif jump_level == 1 and second_bid.denomination < test_bid.denomination:
            result = True
        else:
            result = False
        return result

    def levels_to_bid(self, bid_one, bid_two):
        """
        Return the number of 'steps' between bid_one and bid_two.

        e.g.

        1C to 3H is 3 steps: (1C, 2C 3C, 3H) but
        1S to 3H is 2 steps: (1S, 2S, 3H).
        """
        steps = 0
        while bid_one < bid_two:
            bid_one = self.suit_bid(bid_one.level+1, bid_one.denomination)
            steps += 1
        return steps

    @property
    def overcall_made(self):
        """Return 1 if an overcall has been made by 2nd and not by 4th seat.
        Return 2 if overcall has been made in 4th seat.
        """
        return self._overcall_made()

    def _overcall_made(self):
        """Return 1 if an overcall has been made by 2nd and not by 4th seat.
        Return 2 if overcall has been made in 4th seat.
        """
        bid_history = self.bid_history
        result = self.OVERCALLER_POSITION['none']
        for bid in bid_history[1::2]:
            if not Bid(bid).is_pass:
                result = self.OVERCALLER_POSITION['second_seat']
                if Bid(bid_history[-1]).is_value_call and len(bid_history) > 2:
                    result = self.OVERCALLER_POSITION['fourth_seat']
                break
        return result

    @property
    def opponents_at_game(self):
        """Return True if opponents at game level."""
        return self._opponents_at_game()

    def _opponents_at_game(self):
        """Return True if opponents at game level."""
        result = False
        if len(self.bid_history) >= 3:
            if (Bid(self.bid_history[-3]).is_game or
                    Bid(self.bid_history[-1]).is_game):
                result = True
        elif len(self.bid_history) >= 1:
            if Bid(self.bid_history[-1]).is_game:
                result = True
        return result

    @property
    def bidding_above_game(self):
        """Return True if the bidding is at or above game level."""
        return self._bidding_above_game()

    def _bidding_above_game(self):
        """Return True if the bidding is at or above game level."""
        result = False
        for bid in self.bid_history[::1]:
            if Bid(bid).is_game:
                result = True
                break
        return result

    @property
    def partner_doubled_game(self):
        """Return True if partner has doubled at or above game level."""
        return self._partner_doubled_game()

    def _partner_doubled_game(self):
        """Return True if partner has doubled at or above game level."""
        result = False
        if 'D' in self.bid_history:
            index = self.bid_history.index('D')
            bids = [Bid(bid) for bid in self.bid_history[index::-1]]
            for bid in bids:
                if bid.is_value_call:
                    result = bid.is_game
                    break
        return result

    def double_level(self):
        """Return the level at which the DOUBLE was made."""
        level = 0
        index = self.bid_history.index('D')
        bids = [Bid(bid) for bid in self.bid_history[index::-1]]
        for bid in bids:
            if bid.is_value_call:
                level = bid.level
                break
        return level

    @property
    def opponents_suits(self):
        """Return a list of all opponent's bid suits."""
        return self._opponents_suits()

    def _opponents_suits(self):
        """Return a list of all opponent's bid suits."""
        opponents_suits = []
        if self.overcaller:
            start = 0
        else:
            start = 1
        for bid in self.bid_history[start::2]:
            call = Bid(bid)
            if call.is_suit_call:
                opponents_suits.append(Suit(call.denomination.name))
        return opponents_suits

    def partner_bids_at_lowest_level(self):
        """Return True if partner has not jumped."""
        value = False
        double_index = None
        for index, bid in enumerate(self.bid_history):
            if Bid(bid).is_double:
                double_index = index
                break
        partners_bid = Bid(self.bid_history[double_index+2])
        for bid in list(reversed(self.bid_history))[double_index+1::2]:
            if Bid(bid).is_value_call:
                # noinspection PyTypeChecker
                value = self.is_jump(Bid(bid), partners_bid)
        return value

    def openers_agreed_suit(self):
        """Return a suit agreed by opener."""
        suit = None
        if len(self.bid_history) >= 5:
            opponents_bid_one = Bid(self.bid_history[0], '')
            opponents_bid_two = Bid(self.bid_history[2], '')
            opponents_bid_three = Bid(self.bid_history[4], '')
            if ((opponents_bid_one.denomination == opponents_bid_two.denomination) or
                    (opponents_bid_two.denomination == opponents_bid_three.denomination)):
                suit = opponents_bid_two.denomination
            if opponents_bid_one.is_double and opponents_bid_two.is_suit_call:
                suit = opponents_bid_two.denomination
        return suit

    def cheaper_suit(self, suit_one, suit_two):
        """Return the cheaper of two suits based on bid history."""
        suits = [suit_one, suit_two]
        suit = self.cheapest_suit(suits)
        return suit

    def next_four_card_suit(self):
        """Return the cheapest four card suit."""
        suits = []
        for suit in self.suits_by_length:
            if self.suit_length(suit) == 4:
                suits.append(suit)
        suit = self.cheapest_suit(suits)
        return suit

    def cheapest_suit(self, suits):
        """Return the cheapest suit based on bid history."""
        suit_names = [(suit.name, suit.rank) for suit in suits]
        sorted_suits = sorted(suit_names, key=lambda tup: tup[1])
        suits = [Suit(suit[0]) for suit in sorted_suits]
        last_rank = self._last_bid_rank()
        if not suits:
            return None
        for suit in suits:
            if suit.rank > last_rank:
                break
        else:
            suit = suits[0]
        return suit

    def _last_bid_rank(self):
        """Return the rank of the last value bid."""
        bid = None
        for bid in self.bid_history[::-1]:
            if Call(bid).is_value_call:
                break
        last_rank = Call(bid).denomination.rank
        if last_rank == 4:
            last_rank = -1
        return last_rank

    @staticmethod
    def game_level(suit):
        """Return the level of game in the suit."""
        if suit.is_major:
            level = 4
        elif suit.is_minor:
            level = 5
        else:
            level = 3
        return level

    def bid_to_game(self, denomination, comment='0000', use_distribution_points=False):
        """Return game level bid in given denomination"""
        if denomination.is_nt:
            bid = Bid('3NT', comment, use_distribution_points)
        elif denomination.is_major:
            bid = Bid(self._call_name(4,  denomination.name), comment, use_distribution_points)
        elif denomination.is_minor:
            bid = Bid(self._call_name(5,  denomination.name), comment, use_distribution_points)
        else:
            bid = None
        return bid

    @property
    def stoppers_in_bid_suits(self):
        """Return True if hand contains stoppers in all opponent's bid suits."""
        return self._stoppers_in_bid_suits()

    @property
    def poor_stoppers_in_bid_suits(self):
        """Return True if hand contains stoppers (including ten) in all opponent's bid suits."""
        return self._stoppers_in_bid_suits(lowest_card='T')

    def _stoppers_in_bid_suits(self, lowest_card='J'):
        """Return True if hand contains stoppers in all opponent's bid suits."""
        result = True
        for suit in self.opponents_suits:
            if not self.suit_stopper(suit, lowest_card):
                result = False
                break
            if not result:
                break
        return result

    def suit_stopper(self, suit, lowest_card='J'):
        """Return True if the hand contains a stopper in 'suit'."""
        suit_holding = self.suit_holding
        result = False
        if not suit.is_suit:
            return False
        if suit_holding[suit] >= 5:
            result = True
        else:
            poor_stopper = False
            ace_stopper = Card('A', suit.name) in self.cards
            king_stopper = (Card('K', suit.name) in self.cards and suit_holding[suit] >= 2)
            queen_stopper = (Card('Q', suit.name) in self.cards and suit_holding[suit] >= 3)
            jack_stopper = (Card('J', suit.name) in self.cards and suit_holding[suit] >= 4)
            if lowest_card == 'T':
                poor_stopper = (Card('T', suit.name) in self.cards and suit_holding[suit] >= 4)
            if ace_stopper or king_stopper or queen_stopper or jack_stopper or poor_stopper:
                result = True
        return result

    @property
    def unbid_suit(self):
        """Return the unbid _suit (if any) or None."""
        return self._unbid_suit()

    def _unbid_suit(self):
        """Return the unbid _suit (if any) or None."""
        suits = [suit for suit in self.suits]
        for bid in self.bid_history:
            bid_suit = Bid(bid).denomination
            if bid_suit in suits:
                suits.remove(bid_suit)
        if len(suits) == 1:
            return suits[0]
        else:
            return None

    def stoppers_in_unbid_suits(self):
        """Return True if hand contains stoppers in all opponent's unbid suits."""
        result = True
        bid_suits = []
        for bid in self.bid_history:
            bid_suit = Bid(bid).denomination
            if bid_suit.is_suit:
                bid_suits.append(bid_suit)
        for suit in self.suits:
            if suit not in bid_suits:
                if not self.suit_stopper(suit):
                    result = False
                    break
            if not result:
                break
        return result

    def stoppers_in_other_suits(self, suit):
        """Return True if hand has stoppers in all suits except suit."""
        stoppers = True
        for test_suit in self.suits:
            if test_suit != suit:
                if not self.suit_stopper(test_suit):
                    stoppers = False
                    break
        return stoppers

    def four_in_bid_suits(self, lowest_card='J'):
        """Return True if hand contains stoppers or 4 cards in all
            opponent's bid suits.
        """
        result = True
        for suit in self.opponents_suits:
            if (not self.suit_stopper(suit, lowest_card) and
                    self.suit_holding[suit] <= 3):
                result = False
                break
            if not result:
                break
        return result

    def five_in_opponents_suits(self):
        """Return True if hand has five cards in opponents suits."""
        result = False
        for suit in self.opponents_suits:
            if self.suit_holding[suit] >= 5:
                result = True
        return result

    def three_suits_bid_and_stopper(self):
        """Returns True if three suits bid and
                hand has an stopper in the unbid suit"""
        result = False
        suits_bid = [False, False, False, False]
        for bid_name in self.bid_history[::2]:
            bid = Bid(bid_name)
            if bid.is_suit_call:
                suits_bid[bid.denomination.rank] = True
                suits_bid[bid.denomination.rank] = True
        if suits_bid.count(True) == 3:
            for index, suit_bid in enumerate(suits_bid):
                if not suit_bid:
                    suit = self.suits[index]
                    if self.suit_stopper(suit):
                        result = True
                    elif self.suit_points(suit) >= 1 and self.suit_holding[suit] >= 3:
                        result = True
                    break
        return result

    def can_bid_suit(self, suit):
        """Return False if suit is in opponents bids."""
        result = True
        for bid in self.bid_history[::-1][::2]:
            if Bid(bid).is_suit_call:
                if suit == Bid(bid).denomination:
                    result = False
                    break
        return result

    def has_stopper(self, suit):
        """Return self.suit_stopper."""
        return self.suit_stopper(suit)

    def next_level(self, suit, raise_level=0):
        """Return the next next level for a suit bid."""
        level = self.next_level_bid(suit, '000', raise_level).level
        return level

    def current_bid_level(self):
        """Return the level of the latest quantitative bid."""
        bid = self._get_last_bid()
        return bid.level

    def next_level_bid(self, suit, comment='0000', raise_level=0):
        """Return the lowest possible bid in suit."""
        last_bid = self._get_last_bid()
        if last_bid is None:
            level = 1
        else:
            level = last_bid.level
            level += raise_level
            if last_bid.is_nt:
                level += 1
            elif suit.is_suit:
                if last_bid.denomination >= suit:
                    level += 1
            if level > 7:
                level = 7
        new_bid = Bid(self._call_name(level, suit.name), comment)
        return new_bid

    def _get_last_bid(self):
        """Return last quantitative bid from history."""
        last_bid = None
        for bid_level in self.bid_history[::-1]:
            if bid_level != 'P' and bid_level != 'D' and bid_level != 'R':
                last_bid = Bid(bid_level, '0000')
                break
                break
        return last_bid

    def next_nt_bid(self, comment='0000', raise_level=0):
        """Return the lowest possible bid in no trumps."""
        denomination = self.no_trumps
        bid = self.next_level_bid(denomination, comment, raise_level)
        return bid

    def responder_weak_bid(self):
        """Responder has shown preference at  the lowest level."""
        overcallers_last_bid = Call(self.bid_history[-3])
        if (overcallers_last_bid.is_pass and
                self.partner_bid_one.is_pass and
                (self.partner_last_bid.denomination == self.opener_bid_one.denomination or
                 self.partner_last_bid.denomination == self.opener_bid_two.denomination) and
                not self.is_jump(self.opener_bid_two, self.partner_last_bid)):
            return True
        else:
            return False

    def advancer_preference(self, call_id='0000'):
        """Respond after a 3 level bid make suit preference."""
        if self.overcaller_bid_one.is_double:
            suit_one = self.overcaller_bid_two.denomination
            suit_two = self.overcaller_bid_three.denomination
        else:
            suit_one = self.overcaller_bid_one.denomination
            suit_two = self.overcaller_bid_two.denomination
        if suit_one.is_major and self.suit_length(suit_one) >= 3:
            suit = suit_one
        elif self.suit_holding[suit_one] + 1 >= self.suit_holding[suit_two]:
            suit = suit_one
        else:
            suit = suit_two
        raise_level = 0
        if self.hcp >= 8 and self.next_level(suit) <= 3:
            raise_level = 1
        bid = self.next_level_bid(suit, call_id, raise_level=raise_level)
        self.tracer(__name__, inspect.currentframe(), bid, self.trace)
        return bid

    def unbid_four_card_major(self):
        """Return an unbid four card major or None."""
        suit = None
        bid_suits = [Bid(bid).denomination for bid in self.bid_history if Bid(bid).is_suit_call]
        if (self.hearts >= 4 and
                self.heart_suit not in bid_suits):
            suit = self.heart_suit
        elif (self.spades >= 4 and
                self.spade_suit not in bid_suits):
            suit = self.spade_suit
        return suit

    @staticmethod
    def quantitative_raise(points, base_level,
                           point_list, maximum_level=5):
        """
            Return a bid based on a quantitative raise.
            max raise is the number of elements in pointlist 1, 2,3 or 4
            scan the (reversed) points list until the points in
            the hand exceeds the level
            This shows whether it is a 3,2 or 1 raise etc.

            e.g.
            level = self.quantitative_raise(points, 1, [6, 10, 13, 16], 5)
            if points = 11 this raises level = 1+2 = 3.
        """
        maximum_raise = len(point_list)
        point_list = list(reversed(point_list))
        raise_level = 0
        for index, item in enumerate(point_list):
            if points >= item:
                raise_level = base_level + maximum_raise - index
                break
        if raise_level > maximum_level:
            raise_level = maximum_level
        return raise_level

    def hand_value_points(self, bid_suit):
        """Return the hand value points for the given suit."""
        hand_value_points = (self.hcp + self.support_shape_points(bid_suit))
        return hand_value_points

    def support_points(self, bidders_suit):
        """
        Calculate the sum of high card points and distribution points
        based on support_shape_points.
        """
        return self.high_card_points + self.support_shape_points(bidders_suit)

    def support_shape_points(self, bidders_suit):
        """
        Calculate the distribution points based on
        3 for a void, 2 for a singleton and 1 for a doubleton.
        """
        points = 0
        if bidders_suit.is_suit:
            if self._suit_support(bidders_suit):
                for index in range(4):
                    if self.shape[index] < 3:
                        points += 3 - self.shape[index]
        return points

    def _suit_support(self, bid_suit):
        """Return True if the hand contains at least 3 of bid_suit."""
        match = False
        if self.suit_holding[bid_suit] >= 3:
            match = True
        return match

    @property
    def ordered_holding(self):
        """Returns suits and holdings in decreasing order of holding
            e.g. [[5, 1], [4, 0], [3, 2], [1, 3]].
        """
        holding = ([[self._spades, self.spade_suit],
                    [self._hearts, self.heart_suit],
                    [self._diamonds, self.diamond_suit],
                    [self._clubs, self.club_suit]])
        holding.sort(reverse=True)
        return holding

    def long_suit(self, minimum_holding):
        """Return the first suit with minimum_holding number of cards."""
        suit = None
        if self.spades >= minimum_holding:
            suit = self.spade_suit
        elif self.hearts >= minimum_holding:
            suit = self.heart_suit
        elif self.diamonds >= minimum_holding:
            suit = self.diamond_suit
        elif self.clubs >= minimum_holding:
            suit = self.club_suit
        return suit

    @property
    def suit_shape(self):
        """Return a list of suits in decreasing order by holding."""
        shape = []
        for suit in self.ordered_holding:
            shape.append(suit[1])
        return shape

    @staticmethod
    def higher_ranking_suit(suit_one, suit_two):
        """Return the higher ranking of two suits."""
        if suit_one > suit_two:
            suit = suit_one
        else:
            suit = suit_two
        return suit

    def has_sequence(self, suit):
        """Return True if hand contains a three card sequence starting with
            an honour."""
        result = False
        sequences = ['AKQ', 'KQJ', 'QJT', 'JT9', 'T98']
        cards = [card for card in self.cards if card.suit == suit]
        if len(cards) >= 3:
            for index, card in enumerate(cards[2:]):
                triple = cards[index].rank + cards[index+1].rank + card.rank
                if triple in sequences:
                    result = True
                    break
                break
        return result

    def suit_length(self, suit):
        """Return the length of a suit or a dummy value."""
        if suit.is_suit:
            return self.suit_holding[suit]
        else:
            return -999

    @staticmethod
    def _call_name(level, suit):
        """Return a call name form level and suit."""
        call_name = ''.join([str(level), suit])
        return call_name

    def tracer(self, module, get_frame, trace_value='', display=False, trace_message=''):
        """Print function trace information."""
        if self.trace_module:
            source_file = module.replace('bfg_components.source.', '')
            if self.trace_module == source_file:
                display = True
        else:
            source_file = ''
        display_all = 0
        suppress_all = 0
        if isinstance(trace_value, Bid):
            call_id = trace_value.call_id
            name = trace_value.name
        else:
            call_id = ''
            name = ''
        if (display or display_all) and not suppress_all:
            hand = self.__str__()
            if hand != self.last_hand:
                if self.last_hand:
                    print('')
                print(hand)
                self._set_trace_hand()
                self.last_hand = hand

            output = "{:03d}, call id={}, {}, {:.<40}, {}{}"
            line_number = get_frame.f_lineno
            function = get_frame.f_code.co_name
            if trace_message:
                trace_message = ''.join([', ', trace_message])
            print(output.format(line_number, call_id, source_file, function, name,  trace_message))

    def get_attributes_from_hand(self, hand):
        """Set the attributes of this object from a hand instance."""
        for key, item in hand.__dict__.items():
            self.__dict__[key] = item
