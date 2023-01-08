import random
import math
import logging
from itertools import combinations
import time
from pprint import pprint

from bridgeobjects import (Card, Suit, SUIT_NAMES, RANKS, HONOUR_POINTS,
                           SHAPES, SHAPE_PROBABILITIES, SEATS)
from .board import Board
from .hand import Hand as Hand
# from bridgeobjects import Hand
from .player import Player

logger = logging.getLogger(__name__)


class DealerEngine(object):
    """The dealer object for the bridgeobjects module."""
    DEFAULT_POINTS_RANGE = [12, 14]
    #: the maximum number of points allowed in a hand
    MAX_POINTS = 26
    POINTS_WEIGHTING = {0: 3639, 1: 7884, 2: 13561, 3: 24624, 4: 38454,
                        5: 51862, 6: 65541, 7: 80281, 8: 88922, 9: 93562,
                        10: 94051, 11: 89447, 12: 80269, 13: 69143, 14: 56933,
                        15: 44237, 16: 33109, 17: 23617, 18: 16051, 19: 10362,
                        20: 6435, 21: 3779, 22: 2100, 23: 1119, 24: 559,
                        25: 264, 26: 117, 27: 49, 28: 19, 29: 7,
                        30: 2, 31: 1}

    pack = Board.full_pack()

    def __init__(self, dealer=None):
        if not dealer:
            dealer = random.choice(SEATS)
        self.dealer = dealer

    def get_hand_from_points_and_shape(self, points_range, shape_list=None, partners_hand=None):
        """Return a hand given the shape and points."""
        if not shape_list:
            shape_list = [shape for shape in SHAPES]
        partition = None
        shape = None

        while not partition:
            points = self.get_points_from_range(points_range)
            shape = self.select_random_shape_from_list(shape_list)
            partition = self._get_candidate_partitions(shape,  points, partners_hand)
        hand = self._complete_hand(partition, shape, partners_hand)
        return hand

    def create_board_from_hands(self, given_hands, dealer='N'):
        """ Populate the remaining hands and return a board given a list of hands."""
        pack = self._remaining_cards(given_hands)
        missing_hands = [0, 1, 2, 3]
        for hand in given_hands:
            if hand in missing_hands:
                missing_hands.remove(hand)
            else:
                raise ValueError(f'Invalid hand index: {hand}')
        for index in missing_hands:
            if len(pack) < 13:
                raise ValueError(f'Invalid pack size: {len(pack)}')
            hand, pack = self._create_random_hand(pack)
            given_hands[index] = hand
        board = Board()
        board.hands = given_hands
        board.dealer = dealer
        hands = [hand for (index, hand) in sorted(board.hands_by_index.items())]
        for index, hand in enumerate(hands):
            board.players[index].hand = hand
            board.hands[SEATS[index]] = hand
        return board

    @staticmethod
    def _create_random_hand(pack):
        """Return hand and remaining pack after a hand is created."""
        cards = []
# TODO: pack can be empty!!!
        while len(cards) < 13:
            card = random.choice(pack)
            pack.remove(card)
            cards.append(card)
        hand = Hand(cards)
        return hand, pack

    @staticmethod
    def _remaining_cards(given_hands):
        """Return a list of the cards remaining after dealing the given hands."""
        pack = Board.full_pack()
        for index, hand in given_hands.items():
            if hand:
                for card in hand.cards:
                    if card in pack:
                        pack.remove(card)
                    # else:
                    #     assert False, 'Missing card in pack %s' % str(card)
        return pack

    def get_points_from_range(self, points_range=None):
        """
            Return a random high card points value for the hand,
            based on distribution probabilities, as an integer.
            N.B. Highest point count catered for is MAX_POINTS.
        """
        if not points_range:
            points_range = [0, self.MAX_POINTS]
        else:
            if len(points_range) == 1:
                points_range = [points_range[0], points_range[0]]
            if points_range[0] > self.MAX_POINTS:
                points_range[0] = self.MAX_POINTS
            if points_range[1] > self.MAX_POINTS:
                points_range[1] = self.MAX_POINTS
        probability_list = []
        # weighting / 100 gives a satisfactory precision
        for value in range(points_range[0], points_range[1]+1):
            weighting = self.POINTS_WEIGHTING[value]
            probability_list.extend([value]*int(round(weighting/100)))
        points = random.choice(probability_list)
        return points

    @staticmethod
    def rotate_hands(board, offset):
        """Return the board with the hands rotated by the given offset."""
        hands = [hand for hand in board.hands]
        for index in range(4):
            target = (offset+index) % 4
            board.hands[target] = hands[index]
        return board

    @classmethod
    def _candidate_shapes_for_points(cls, points):
        candidate_shapes = cls._select_shapes_for_points(points)
        if not candidate_shapes:
# @TODO Generate Error here
            print('No candidate shapes found')
            return []
        else:
            return candidate_shapes

    @classmethod
    def _complete_hand(cls, honour_list, shape, partners_hand):
        """Return a complete hand given the shape and honours."""
        shape_found = False
        loop_two = 0
        shuffled_shape = []
        while not shape_found:
            unsorted_shape = [length for length in shape]
            honour_shape = [0, 0, 0, 0]
            for card in honour_list:
                honour_shape[card.suit.rank]+=1
            shuffled_shape = []
            # Need to create the list 'shuffled_shape' in random order, but the
            # but the number of cards in each suit has to be >= the number of
            # honours in that suit.
            for index in range(4):
                suit_found = False
                loop = 0
                while not suit_found:
                    shape_found = False
                    suit_length = random.choice(unsorted_shape)
                    if suit_length >= honour_shape[index]:
                        shuffled_shape.append(suit_length-honour_shape[index])
                        unsorted_shape.remove(suit_length)
                        suit_found = True
                        shape_found = True
                    loop += 1
                    if loop > 10:
                        suit_found = True
                    if len(shuffled_shape) < 4:
                        shape_found = False
            loop_two+=1
        if loop_two >= 100:
            logger.info('_complete_hand', str(shape), str(honour_list))
        hand_list = [card for card in honour_list]
        pack_pips = cls._pack_pips(partners_hand)
        for suit, remainder in enumerate(shuffled_shape):
            for _ in range(remainder):
                if pack_pips[suit]:
                    card = random.choice(pack_pips[suit])
                    pack_pips[suit].remove(card)
                    hand_list.append(card)
        hand = Hand(hand_list)
        # print('_complete_hand', hand, hand.shape, hand.hcp)
        return hand

    @classmethod
    def select_random_shape_from_list(cls, shapes):
        """Return a hand shape from the list shapes based on probabilities."""
        total_shapes = []
        for shape in shapes:
            weighting = SHAPE_PROBABILITIES[''.join(map(str, shape))]
            total_shapes.extend([shape]*weighting)
        return random.choice(total_shapes)

    @staticmethod
    def _select_shapes_for_points(points):
        """Return candidate shapes that can support the points given."""
        candidate_shapes = [shape for shape in SHAPES]
        found = False
        for shape in SHAPES:
            if points > Hand().maximum_points_for_shape(shape):
                candidate_shapes.remove(shape)
        return candidate_shapes

    @classmethod
    def _pack_pips(cls, partners_hand):
        """ Return a list with all pips in the pack."""
        if partners_hand:
            partners_cards = partners_hand.cards
        else:
            partners_cards = []
        pack_pips = [[], [], [], []]
        two = RANKS.index("2")
        ten = RANKS.index("T")
        for suit_index, suit in enumerate(SUIT_NAMES):
            for rank in RANKS[two:ten+1]:
                card = Card(rank+suit)
                if card in cls.pack and card not in partners_cards:
                    pack_pips[suit_index].append(card)
        return pack_pips

    @staticmethod
    def get_partitions(points, partners_hand=None):
        """
            Return a list of partitions that match the points count.

            A partition is a list containing the number of aces, kings etc.
            that can make up the number of points.

            e.g. with 4 points the possible partitions are:
            [[0, 0, 0, 4], [0, 0, 1, 2], [0, 0, 2, 0],
             [0, 1, 0, 1], [1, 0, 0, 0]]
            i.e. 4 jacks, 1 queen and 2 jacks, etc..
        """
        if partners_hand:
            used_honours = [partners_hand.aces,
                            partners_hand.kings,
                            partners_hand.queens,
                            partners_hand.jacks]
        else:
            used_honours = [0, 0, 0, 0]
        partitions = []
        # get the maximum number of aces that can occur in 'points'.
        max_aces = int(points/HONOUR_POINTS['A'])
        # loop through aces from 0 up to the maximum number.
        for aces in range(max_aces+1):
            # get the number of points not covered by the aces.
            ace_remainder = points - HONOUR_POINTS['A']*aces
            # repeat for kings etc.
            max_kings = int(ace_remainder/HONOUR_POINTS['K'])
            for kings in range(max_kings+1):
                king_remainder = ace_remainder - HONOUR_POINTS['K']*kings
                max_queens = int(king_remainder/HONOUR_POINTS['Q'])
                for queens in range(max_queens+1):
                    queen_remainder = king_remainder - HONOUR_POINTS['Q']*queens
                    jacks = int(queen_remainder/HONOUR_POINTS['J'])
                    # only use valid partitions.
                    if (aces <= 4-used_honours[0] and
                            kings <= 4-used_honours[1] and
                            queens <= 4-used_honours[2] and
                            jacks <= 4-used_honours[3]):
                        partitions.append([aces, kings, queens, jacks])
        return partitions

    def _get_candidate_partitions(self, shape, points, partners_hand):
        """Return a list of partitions that meet the points criterion."""
        # now = time.time()
        honour_cards = self._available_honours(partners_hand)
        candidate_partitions = []
        honour_list = ['A', 'K', 'Q', 'J']
        partition_shape = [cards for cards in shape]
        candidates = []
        partitions = self.get_partitions(points, partners_hand)
        loop = 0
        while not candidates:
            if not partners_hand:
                selected_partitions = [random.choice(partitions)]
            else:
                selected_partitions = [partition for partition in partitions]
            for partition in selected_partitions:
                ace_list = []
                king_list = []
                queen_list = []
                jack_list = []
                for index, honour_count in enumerate(partition):
                    candidate_cards = [card for card in honour_cards
                                            if card.rank == honour_list[index]]
                    for combination in list(combinations(candidate_cards, honour_count)):
                        candidate_honours = list(combination)
                        if index == 0:
                            ace_list.append(candidate_honours)
                        elif index == 1:
                            king_list.append(candidate_honours)
                        elif index == 2:
                            queen_list.append(candidate_honours)
                        elif index == 3:
                            jack_list.append(candidate_honours)
                    for jacks in jack_list:
                        for queens in queen_list:
                            for kings in king_list:
                                for aces in ace_list:
                                    candidate = []
                                    candidate.extend(aces)
                                    candidate.extend(kings)
                                    candidate.extend(queens)
                                    candidate.extend(jacks)
                                    if (self._candidate_shape_match(shape, candidate) and
                                            self._partion_points(candidate) == points):
                                        candidates.append(candidate)
            loop += 1
            if loop > 10:
                return None
        return random.choice(candidates)

    def _available_honours(self, partners_hand):
        """Return a list of honours available after partner's hand has been dealt."""
        if partners_hand:
            partners_cards = partners_hand.cards
        else:
            partners_cards = []
        honour_cards = []
        for card in self.pack:
            if card.high_card_points:
                if card not in partners_cards:
                    honour_cards.append(card)
        return honour_cards

    @staticmethod
    def _candidate_shape(cards):
        """Return a shape list based on cards."""
        candidate_shape = [0, 0, 0, 0]
        for card in cards:
            candidate_shape[card.suit.rank] += 1
        candidate_shape = sorted(candidate_shape, reverse=True)
        return candidate_shape

    def _candidate_shape_match(self, shape, cards):
        """Return a shape list based on cards."""
        shape_ok = True
        for index, cards in enumerate(self._candidate_shape(cards)):
            if cards > shape[index]:
                shape_ok = False
                break
        return shape_ok

    @staticmethod
    def _partion_points(partition):
        """Return the points represented by a partition."""
        points = 0
        for card in partition:
            points += card.high_card_points
        return points

    @classmethod
    def get_points_probability(cls, points, partners_hand=None):
        """
        Return the probability of a hand having the requisite number of points.

        Find the partitions that correspond to a give points count,
        calculate the probability for each partition and sum.

        The probability of being dealt the given number of points is then
        the number of ways the points can be dealt divided by the
        total number of possible deals.
        """
        probability = 0
        partitions = cls.get_partitions(points, partners_hand)
        for partition in partitions:
            probability += cls._partition_probability(partition, partners_hand)
        return probability

    @classmethod
    def _partition_probability(cls, honours, partners_hand):
        """
        Return the probability of a hand holding the honours in
        the list ([aces, kings, queens, Jacks]).
        """
        combinations = 1
        if partners_hand:
            available_honours = [4-partners_hand.aces,
                                 4-partners_hand.kings,
                                 4-partners_hand.queens,
                                 4-partners_hand.jacks]
        else:
            available_honours = [4, 4, 4, 4]
        for index, honour in enumerate(honours):
            available = available_honours[index]
            combinations = combinations * cls._honour_combinations(honour, available)
        return combinations*cls._pip_combinations(13-sum(honours), partners_hand)

    @classmethod
    def _honour_combinations(cls, cards, available):
        """
        Return the number of ways the quantity of an honour(e.g. Aces)
        can be obtained from 4.
        """
        fact = math.factorial
        if cards == available:
            combs = 1
        elif cards == 0:
            combs = 1
        else:
            combs = (fact(available) / fact(cards) / fact(available -cards))
        return combs

    @classmethod
    def _pip_combinations(cls, pip_cards, partners_hand):
        """
        Return the number of ways that the pip cards can be
        allocated once the honours have been used to make up a point count.

        To calculate the number of possible ways in which a hand of 13 cards
        can be dealt from a pack if 52 use the binomial coefficient:
            n! / k!(n-k)!
        in this case use n=number of cards in the pack and k=number of pip cards.
        """

        if partners_hand:
            pack = 39.0
            partners_honours = (partners_hand.aces +
                                partners_hand.kings +
                                partners_hand.queens +
                                partners_hand.jacks)
            pips = 36 - (13 - partners_honours)
        else:
            pack, pips = 52.0, 36
        fact = math.factorial
        pos_deals = fact(pack)/fact(13)/fact(pack-13)
        return float(fact(pips)/fact(pips-pip_cards))/fact(pip_cards) / pos_deals
