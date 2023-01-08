""" Bid for Game
    File objects

    PEP8
"""
from bridgeobjects import Hand


class Files(object):
    """Define BfG Files class."""
    def test_hands_from_file(self, test_hand_filename, include_all=False):
        """Generate Hand objects from a test hand file."""
        try:
            with open(test_hand_filename, 'r') as f_test_hands:
                hand_strings = f_test_hands.readlines()
                test_hands = self._get_hands_from_file(hand_strings, include_all)
        except FileNotFoundError:
            print('')
            print(test_hand_filename + ' not found')
            test_hands = []
        return test_hands

    def _get_hands_from_file(self, hand_strings, include_all):
        """Return a list of hands from a test file line."""
        test_hands = []
        for hand_string in hand_strings:
            hand_list = self._list_from_file_line(hand_string)
            header = hand_list[0].split('~')
            description = header[0]
            if len(header) > 1:
                header[1] = header[1].split(',')
                if header[1] == ['']:
                    header[1] = []
                del hand_list[0]
                if description[0] != '#' or include_all:
                    hand = Hand(hand_list)
                    hand.description = header
                    test_hands.append(hand)
        return test_hands

    @staticmethod
    def _list_from_file_line(hand_string):
        """Return a list from a test file line."""
        hand_string = hand_string.replace('\r', '')
        hand_string = hand_string.replace('\n', '')
        hand_list = hand_string.split(':')
        return hand_list
