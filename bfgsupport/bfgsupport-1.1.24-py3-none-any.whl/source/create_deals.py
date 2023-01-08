# #! /usr/bin/env python
# import logging
# import sys
# sys.path.append('/home/jeff/bfg')
#
# from bridge_tools import Bid
# from deal import Deal
# from pbn import PBN
# from dealer import Dealer
# from bridgeobjects import Suit, Clubs, Card, Hand
# from datetime import datetime
# import time
# from pprint import pprint
#
# #log_path = 'generate.log'
# #logging.basicConfig(filename=log_path, level=logging.INFO)
# #with open(log_path, 'w') as log_file:
#     #pass
# logger = logging.getLogger(__name__)
#
# class Generator(object):
#     """Deal Generator class."""
#     DEAL_FILE_PATH = '/home/jeff/Dropbox/Bridge/test_deals/created_deals_{}.pbn'
#
#     def __init__(self, user):
#         #file_number = input("Deal file number: ")
#         #number_of_tests = 50
#         file_number = "1"
#         number_of_tests = 50
#
#         with open(self.DEAL_FILE_PATH.format(file_number), 'w') as deal_file:
#             deal_file.write("")
#         with open(self.DEAL_FILE_PATH.format(file_number), 'a') as deal_file:
#             deal_list = self.create_deals(deal_file, number_of_tests)
#             board_list = self.event_from_deals(deal_list)
#             deal_file.write('\n'.join(board_list))
#
#     def create_deals(self, deal_file, number_of_tests):
#         item = 1
#         test_deals = []
#         sorted_pack = self.sorted_pack()
#         while item <= number_of_tests:
#             dealer = Dealer('S') # need a new Deal() and Dealer() for every board
#             deal = Deal()
#             #partners_hand = Hand('A8654.KQ5.T.QJT6')
#             #board = dealer.deal_balanced_board([12, 14])
#             #board = dealer.deal_single_suited_board([5, 19])
#             #board = dealer.deal_two_suited_board([10, 19])
#             #board = dealer.deal_opening_one_board()
#             dealer = Dealer('N')
#             #board = dealer.deal_limit_bids_responder_board()
#             #board = dealer.deal_positive_one_nt_board()
#             board = dealer.deal_defence_to_one_nt_board()
#
#             #hand = board.hands[0]
#             #print(hand, hand.shape, hand.hcp)
#             #hand = board.hands[2]
#             #print(hand, hand.shape, hand.hcp)
#
#             deal.dealer = board.dealer
#             for index, player in enumerate(deal.players):
#                 hand = board.hands[index]
#                 hand = Hand(self.sort_hand(hand, sorted_pack))
#                 player.hand = hand
#                 deal.hands[index] = hand
#             deal_list = deal.create_pbn_list()
#             deal_string = '\n'.join(deal_list)
#             logger.info(deal_string)
#             item += 1
#             #print('item', item)
#             test_deals.append(deal)
#         return test_deals
#
#     def event_from_deals(self, deal_list):
#         """Return a list of boards from a list of deals."""
#         board_list = []
#         board_list.append("% PBN 2.1")
#         board_list.append("% EXPORT1")
#         board_list.append("% Content-type: text/pbn; charset=ISO-8859-1")
#         board_list.append("% Creator: Bid for Game")
#         board_list.append("")
#         board_list.extend(PBN().get_file_rows(deal_list))
#         return board_list
#
#     def sort_hand(self, hand, sorted_pack):
#         hand_list = []
#         for card in sorted_pack:
#             if card in hand.cards:
#                 hand_list.append(card)
#         return hand_list
#
#     def sorted_pack(self,):
#         """Return a pack in sorted order."""
#         pack = []
#         ranks = list(reversed(Card.RANKS[1:]))
#         for suit in ['S', 'H', 'D', 'C']:
#             pack.extend([Card(rank, suit) for rank in ranks])
#         return pack
#
#     def save_deal(self, item, deal, deal_file, save=False):
#         if save:
#             deal.bid_history = []
#             deal.set_description('{0:04d}'.format(item))
#             deal_out = deal.create_pbn_list()
#             deal_file.write('\n'.join(deal_out))
#             sys.stdout.write('#')
#             sys.stdout.flush()
#         return 1
#
# class User(object):
#     pass
#
# if __name__ == '__main__':
#     deal_generator = Generator(User())
