""" Bid for Game
    Board class
"""

from datetime import datetime
import json
from termcolor import cprint

from .player import Player
from .hand import Hand
from bridgeobjects import (Board as bfg_Board, RANKS, SEATS, SUITS,
                            parse_pbn, Contract,
                            Auction, Trick)


MODULE_COLOUR = 'blue'

DEFAULT_SUIT_ORDER = ['S', 'H', 'C', 'D']


class Board(bfg_Board):
    """Define BfG Board class."""
    def __init__(self, *args, **kwargs):
        super(Board, self).__init__(*args, **kwargs)
        self.auction = Auction()
        self.description = ''
        self.bid_history = []
        self.warning = None
        self.active_bid_history = []
        self._stage = None
        self.players = {}
        for index in range(4):
            self.players[index] = Player(self, None, index)
            self.players[SEATS[index]] = Player(self, None, index)
        # self.check_bids = []
        self._dealer = None
        self.leader = None
        self.current_player = None
        self.current_trick = Trick()
        # self.reset = False
        # self._dict = {}
        self.unplayed_cards = {seat:[] for seat in SEATS}
        self.hands = {seat:Hand() for seat in SEATS}
        self.hand_cards = {seat: [card.name for card in self.hands[seat].cards] for seat in SEATS}
        self.unplayed_card_names = []
        self.current_player = ''
        self.NS_tricks = 0
        self.EW_tricks = 0
        self.score = 0
        self.suit_order = self._get_suit_order()
        # self.timestamp = 0
        # self.test_board = False

    def __repr__(self):
        """Return a string representation of the deal."""
        return f"Board: North's hand {self.hands[0]}"

    def __str__(self):
        """Return a string representation of the deal."""
        return f"Board: North's hand {self.hands[0]}"

    def to_json(self):
        """Return object as json string."""
        self.update_state()

        # Objects
        hands = {}
        for key, hand in self.hands.items():
            hands[key] = hand.to_json()
        tricks = []
        for trick in self.tricks:
            tricks.append(trick.to_json())
        current_trick = self.current_trick.to_json()

        # Strings
        json_str = json.dumps({
            'auction': self._auction.to_json(),
            'bid_history': self.bid_history,
            'warning': self.warning,
            'contract': self.contract.to_json(),
            'current_player': self.current_player,
            'current_trick': current_trick,
            'declarer': self.declarer,
            'declarer_index': self.declarer_index,
            'declarers_tricks': self.declarers_tricks,
            'dealer': self.dealer,
            'dealer_index': self.dealer_index,
            'description': self.description,
            'east': self.east,
            'EW_tricks': self.EW_tricks,
            'hands': hands,
            'identifier': self.identifier,
            'north': self.north,
            'NS_tricks': self.NS_tricks,
            'south': self.south,
            'stage': self._stage,
            # 'reset': self.reset,
            'tricks': tricks,
            'vulnerable': self.vulnerable,
            'west': self.west,

            # Board state
            'max_suit_length': self.max_suit_length,
            'hand_suit_length': self.hand_suit_length,
            # 'self.current_player': self.current_player,
            'score': self.score,
            'suit_order': self.suit_order,
            # 'timestamp': self.timestamp,
            # 'test_board': self.test_board,
        })
        return json_str

    def from_json(self, json_str):
        """Populate attributes from json string."""
        board_dict = dict(json.loads(json_str))

        self._auction = Auction().from_json(board_dict['auction'])
        self.bid_history = self._update_attribute(board_dict, 'bid_history', [])
        self.warning = self._update_attribute(board_dict, 'warning')
        self._contract = Contract().from_json(board_dict['contract'])
        self.current_player = self._update_attribute(board_dict, 'current_player')
        self.declarer = self._update_attribute(board_dict, 'declarer')
        self.declarer_index = self._update_attribute(board_dict, 'declarer_index')
        self.declarers_tricks = int(self._update_attribute(board_dict, 'declarers_tricks', 0))
        self.dealer = self._update_attribute(board_dict, 'dealer', '')
        self.dealer_index = self._update_attribute(board_dict, 'dealer_index')
        self.description = self._update_attribute(board_dict, 'description')
        self.east = self._update_attribute(board_dict, 'east')
        self.EW_tricks = int(self._update_attribute(board_dict, 'EW_tricks', 0))
        self.hands = self._get_hands_from_json(board_dict)
        if board_dict['identifier'] == '':
            board_dict['identifier'] = 0
        self.identifier = int(self._update_attribute(board_dict, 'identifier', 0))
        self.north = self._update_attribute(board_dict, 'north')
        self.NS_tricks = int(self._update_attribute(board_dict, 'NS_tricks', 0))
        self.south = self._update_attribute(board_dict, 'south')
        self._stage = self._update_attribute(board_dict, 'stage')
        self.tricks = self._get_tricks_from_json(board_dict)
        self.current_trick = self._get_current_trick_from_json(board_dict)
        self.vulnerable = self._update_attribute(board_dict, 'vulnerable')
        self.west = self._update_attribute(board_dict, 'west')
        return self

    def _get_hands_from_json(self, board_dict):
        hands_json = self._update_attribute(board_dict, 'hands', {})
        hands = {}
        for key, raw_hand in hands_json.items():
            hand = Hand()
            hand.from_json(raw_hand)
            if key.isnumeric():
                key = int(key)
            self.players[key].hand = hand
            hands[key] = hand
        return hands

    def _get_tricks_from_json(self, board_dict):
        tricks_json = self._update_attribute(board_dict, 'tricks', [])
        tricks = []
        for raw_trick in tricks_json:
            trick = Trick()
            trick.from_json(raw_trick)
            tricks.append(trick)
        return tricks

    def _get_current_trick_from_json(self, board_dict):
        current_trick_json = self._update_attribute(board_dict, 'current_trick', '')
        trick = Trick()
        if current_trick_json:
            return trick.from_json(board_dict['current_trick'])
        else:
            return trick

    @staticmethod
    def _update_attribute(board_dict, key, default=None):
        if key in board_dict:
            return board_dict[key]
        return default

    @property
    def dealer(self):
        return self._dealer

    @dealer.setter
    def dealer(self, value):
        assert value in SEATS, f'Invalid dealer: {value}'
        self._dealer = value
        self.dealer_index = SEATS.index(value)

    @property
    def auction(self):
        """Return auction property."""
        return self._auction

    @auction.setter
    def auction(self, value):
        """Set auction property."""
        self._auction = value
        if value:
            self._contract = self.get_contract()

    @property
    def stage(self):
        """Assign stage property."""
        return self._stage

    @stage.setter
    def stage(self, value):
        """Set stage property."""
        self._stage = value

    def deal_from_pbn(self, pbn_string):
        """Create a deal from pbn_string."""
        pass

    def set_description(self, description):
        """Set the Board description."""
        self.description = description


    def get_auction(self, test=False):
        """Generate the auction."""
        if test:
            player_index = 0
        else:
            player_index = self.dealer_index
        auction_calls = []

        bid_history, self.bid_history = self.bid_history, []
        while not self.three_final_passes(auction_calls):
            player = self.players[player_index]
            bid = player.make_bid()
            auction_calls.append(bid)
            player_index += 1
            player_index %= 4
        auction = Auction()
        auction.calls = auction_calls
        auction.first_caller = self.dealer
        self.bid_history = bid_history
        return auction

    @staticmethod
    def three_final_passes(calls):
        """Return True if there have been three consecutive passes."""
        three_passes = False
        if len(calls) >= 4:
            if calls[-1].is_pass and calls[-2].is_pass and calls[-3].is_pass:
                three_passes = True
        return three_passes

    @staticmethod
    def _default_hands():
        hands = []
        dummy_hand = ['AS', 'KS', 'QS', 'JS', 'TS', '9S', '8S',
                      '7S', '6S', '5S', '4S', '3S', '2S']
        hands.append(Hand(dummy_hand))
        dummy_hand = [hand.replace('S', 'H') for hand in dummy_hand]
        hands.append(Hand(dummy_hand))
        dummy_hand = [hand.replace('H', 'D') for hand in dummy_hand]
        hands.append(Hand(dummy_hand))
        dummy_hand = [hand.replace('D', 'C') for hand in dummy_hand]
        hands.append(Hand(dummy_hand))
        return hands

    def parse_pbn_board(self, pbn_board, delimiter=":"):
        """Return a list of hands from a pbn deal string."""
        # example deal
        #   ['[Board "Board 1"]', '[Dealer "N"]',
        #    '[Deal "N:JT84.A987.8.T982 AKQ.KQ54.KQ2.A76 7652.JT3.T9.KQJ5 93.62.AJ76543.43"]']
        # hands = [None, None, None, None]
        # # Assign hands to board in correct position
        # self._dealer = deal[0]
        # hand_index = self._get_pbn_dealer_index(deal)
        # raw_hands = deal[2:].split(delimiter)
        # for card_list in raw_hands:
        #     hand = Hand(card_list)
        #     hands[hand_index] = hand
        #     hand_index = (hand_index + 1) % 4
        events = parse_pbn(pbn_board)
        board = events[0].boards[0]
        self.description = board.description
        self.dealer = board.dealer
        self.hands = {}
        for key, hand in board.hands.items():
            self.hands[key] = Hand(hand.cards)
        for index in range(4):
            self.players[index].hand = self.hands[index]
        return board.hands

    def _get_pbn_dealer_index(self, deal):
        """
            Return the first hand index to ensure that the first hand
            assigned to the board's hands list is that of the board dealer.
        """
        # first_hand is the position index of the first hand given in the deal
        first_hand = SEATS.index(deal[0])

        # dealer_index is the position index of the dealer
        dealer_index = SEATS.index(self.dealer)

        # rotate the hand index to ensure that the
        # first hand created is the dealer's
        hand_index = (first_hand - dealer_index) % 4
        return hand_index

    def create_pbn_list(self):
        """Return a board as a list of strings in pbn format."""
        deal_list = ['[Event "bfg generated deal"]',
                     '[Date "{}"]'.format(datetime.now().strftime('%Y.%m.%d')),
                     '[Board "{}"]'.format(self.description),
                     '[Dealer "{}"]'.format(self.dealer),
                     '[Deal "{}:{}"]'.format(self.dealer, self._get_deal_pbn(' ')),
                     '']
        return deal_list

    def _get_deal_pbn(self, delimiter=' '):
        """Return a board's hands as a string in pbn format."""
        hands_list = []
        for _, hand in self.hands.items():
            hand_list = []
            for _ in range(4):
                hand_list.append(['']*13)
            for card in hand.cards:
                suit = 3 - card.suit.rank
                rank = 13 - RANKS.index(card.rank)
                hand_list[suit][rank] = card.name[0]
            for index in range(4):
                hand_list[index] = ''.join(hand_list[index])
            hands_list.append('.'.join(hand_list))
        return delimiter.join(hands_list)

    @staticmethod
    def rotate_board_hands(board, increment=1):
        """Return the hands rotated through increment clockwise."""
        rotated_hands = {}
        hands = board.hands
        for index in range(4):
            rotated_index = (index + increment) % 4
            if index in hands:
                rotated_hands[rotated_index] = hands[index]
                board.players[rotated_index].hand = hands[index]
            if SEATS[index] in hands:
                rotated_hands[SEATS[rotated_index] ] = hands[SEATS[index]]
        board.hands = rotated_hands
        return board

    def get_contract(self):
        """Return a contract from the auction."""
        contract = Contract()
        if not self._auction:
            return contract

        if not (self._three_final_passes(self._auction.calls) and
                not self._passed_out(self._auction.calls)):
            return contract

        dealer_index = SEATS.index(self.dealer)
        auction_calls = [call for call in self._auction.calls]
        auction_calls.reverse()
        modifier = ''
        for call in auction_calls:
            if call.name == 'R':
                modifier = 'R'
            if not modifier and call.name == 'D':
                modifier = 'D'
            if call.is_value_call:
                break
        denomination = call.denomination
        declarer_partition = self._auction.calls.index(call)

        for index, check_call in enumerate(self._auction.calls):
            if (check_call.denomination == denomination and
                    (declarer_partition - index) % 2 == 0):
                break
        declarer_index = (dealer_index + index) % 4
        declarer = SEATS[declarer_index]
        contract = Contract(f'{call.name}{modifier}', declarer)
        return contract

    @staticmethod
    def _passed_out(calls):
        """Return True if the board has been passed out."""
        if len(calls) != 4:
            return False
        for call in calls:
            if not call.is_pass:
                return False
        return True

    @staticmethod
    def _three_final_passes(calls):
        """Return True if there have been three consecutive passes."""
        three_passes = False
        if len(calls) >= 4:
            if calls[-1].is_pass and calls[-2].is_pass and calls[-3].is_pass:
                three_passes = True
        return three_passes

    def get_attributes_from_board(self, board):
        """Set the attributes of this object from a board instance."""
        for key, item in board.__dict__.items():
            self.__dict__[key] = item

        unplayed_cards = {}
        for seat, hand in board.hands.items():
            if not isinstance(hand, Hand):
                newhand = Hand()
                newhand.get_attributes_from_hand(hand)
                hand = newhand
            unplayed_cards[seat] = [card for card in hand.unplayed_cards]
        for key, raw_hand in board.hands.items():
            hand = Hand(raw_hand.cards)
            board.hands[key] = hand
        for seat, hand_cards in unplayed_cards.items():
            board.hands[seat].unplayed_cards = [card for card in hand_cards]

        for index in range(4):
            self.players[index].hand = board.hands[index]

        self.auction = Auction()
        for key, item in board.auction.__dict__.items():
            self.auction.__dict__[key] = item

        self.contract = Contract()
        for key, item in board.contract.__dict__.items():
            self.contract.__dict__[key] = item

        self.tricks = []
        for raw_trick in board.tricks:
            trick = Trick()
            for key, item in raw_trick.__dict__.items():
                trick.__dict__[key] = item
            self.tricks.append(trick)

    def update_state(self):
        """Return a context with the current state of the board."""
        # These variables (dicts) are all natural ('N' etc. based on SEATS)
        (hand_suit_length, max_suit_length, unplayed_cards) = self._hand_shape_details()
        score = 0
        if self.NS_tricks + self.EW_tricks == 13:
            score = self._get_score()

        self.hand_cards = {seat: [card.name for card in self.hands[seat].cards] for seat in SEATS}
        self.unplayed_card_names = unplayed_cards
        self.max_suit_length = max_suit_length
        self.hand_suit_length = hand_suit_length
        self.current_player = self.current_player
        self.NS_tricks = self.NS_tricks
        self.EW_tricks = self.EW_tricks
        self.score = score
        context = {
            'hand_cards': { seat: [card.name for card in self.hands[seat].cards] for seat in SEATS},
            'unplayed_card_names': unplayed_cards,
            'max_suit_length': max_suit_length,
            'hand_suit_length': hand_suit_length,
            'current_player': self.current_player,
            'NS_tricks': self.NS_tricks,
            'EW_tricks': self.EW_tricks,
            # 'board_status': self.status,
            # 'play_status': self.play_status,
            # 'play_master': self.play_master,
            'score': score,
        }
        return context

    def _hand_shape_details(self):
        """Return hand shape details used to calculate E/W display in card play."""
        # unplayed_cards: dict keyed on seat of the unplayed cards in that hand
        unplayed_cards = {}

        # hand_suit_length: dict keyed on seat of list of suit lengths (in suit_order) by hand
        hand_suit_length = {}

        # max_suit_length: dict keyed on seat with max suit length for that seat
        max_suit_length = {}
        for seat in SEATS:
            # print(board.hands)
            hand = self.hands[seat]
            # Get the shape depending on unplayed_cards
            hand_for_shape = Hand(hand.unplayed_cards)
            hand_for_shape.cards = [card for card in hand.unplayed_cards]
            unplayed = Hand.sort_card_list(hand_for_shape.cards, self.suit_order)
            unplayed_cards[seat] = [card.name for card in unplayed]
            suit_length = []
            for suit_name in self.suit_order:
                suit = SUITS[suit_name]
                suit_length.append(hand_for_shape.suit_length(suit))
            hand_suit_length[seat] = suit_length
            max_suit_length[seat] = hand_for_shape.shape[0]
        return (hand_suit_length, max_suit_length, unplayed_cards)

    def _get_suit_order(self):
        """Return a list of suit order."""
        if self._three_passes():
            bid_history = self.bid_history[:-3]
            while bid_history and bid_history[-1] in ['D', 'R']:
                bid_history = self.bid_history[:-1]
            contract = bid_history[-1]
            suit = contract[-1]
            if suit in DEFAULT_SUIT_ORDER:
                if suit == 'S':
                    return DEFAULT_SUIT_ORDER
                if suit == 'H':
                    return ['H', 'S', 'D', 'C']
                if suit == 'D':
                    return ['D', 'S', 'H', 'C']
                if suit == 'C':
                    return ['C', 'H', 'S', 'D']
            else:
                return DEFAULT_SUIT_ORDER
        else:
            return DEFAULT_SUIT_ORDER

    def _three_passes(self):
        """Return True if there are 3 passes."""
        if len(self.bid_history) >= 4:
            if (self.bid_history[-1] == 'P' and
                    self.bid_history[-2] == 'P' and
                    self.bid_history[-3] == 'P'):
                return True
        return False

    def _get_score(self):
        """Return the score for the board."""
        vulnerable = False
        if self.contract.declarer in 'NS':
            declarers_tricks = self.NS_tricks
            if self.vulnerable in ['NS', 'Both', 'All']:
                vulnerable = True
        else:
            declarers_tricks = self.EW_tricks
            if self.vulnerable in ['EW', 'Both', 'All']:
                vulnerable = True
        return self.contract.score(declarers_tricks, vulnerable)
