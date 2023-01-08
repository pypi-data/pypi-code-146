""" Bid for Game
    Player class
"""
import time
from termcolor import cprint

from bridgeobjects import ROLES
from .acol_bidding import AcolBid

MODULE_COLOUR = 'blue'

class Player(object):
    """Define BfG Player class."""
    NUMBER_OF_PLAYERS = 4

    def __init__(self, parent=None, hand=None, index=None):
        self.board = parent
        self.hand = hand
        self.index = index
        self.role = -1

    def __repr__(self):
        """Return a string representation of player."""
        return 'player: {}'.format(self.hand)

    def make_bid(self, update_bid_history=True):
        """Make a bid and return bid object."""
        active_bid_history = self._active_bid_history(self.board.bid_history)
        self.role = self._get_role(active_bid_history)
        self.board.active_bid_history = active_bid_history

        bid = AcolBid(self.hand, self.board, self.role).bid
        # cprint(f"{self.board.bid_history} {bid}", MODULE_COLOUR)

        if update_bid_history:
            self.board.bid_history.append(bid.name)
        hc_points = self.hand.high_card_points
        if bid.use_shortage_points:
            distribution_points = 0
            hand_description = '{}+{} = {}'.format(hc_points, distribution_points, hc_points+distribution_points)
        else:
            hand_description = str(hc_points)
        hand_description = '%s ' % hand_description
        bid.hand_points = hand_description
        # print(colored(f'{bid}, {self.board.bid_history}', MODULE_COLOUR))
        return bid

    def _get_role(self, bid_history):
        """Return role based on bid history."""
        role_id = self._get_role_id(bid_history)
        if role_id == 0:
            role = ROLES['Opener']
        elif role_id == 2:
            role = ROLES['Responder']
        else:
            role = self._assign_overcaller_advancer(bid_history, role_id)
        return role

    def _get_role_id(self, bid_history):
        """Return the role_id based on the length of the bid_history."""
        role_id = len(bid_history)-100
        for bid in bid_history:
            if bid != 'P':
                break
            else:
                role_id -= 1
        role_id %= self.NUMBER_OF_PLAYERS
        return role_id

    def _assign_overcaller_advancer(self, bid_history, role_id):
        """Return the role_id if Overcaller or Advancer."""
        first_overcaller = 1
        for bid in bid_history[1::2]:
            if bid != 'P':
                break
            else:
                first_overcaller += 2
        first_overcaller %= self.NUMBER_OF_PLAYERS
        if first_overcaller == role_id:
            role = ROLES['Overcaller']
        else:
            role = ROLES['Advancer']
        return role

    @staticmethod
    def _active_bid_history(bid_history):
        """Return the bid history without leading PASSES."""
        temp_history = []
        started = False
        for bid in bid_history:
            if bid != 'P' or started:
                temp_history.append(bid)
                started = True
        return temp_history
