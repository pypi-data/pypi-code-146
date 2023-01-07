from time import sleep

from random import randint
from copy import copy, deepcopy

import socket
import pickle

from threading import Thread


##############################
# Bridge Server
##############################

class Players():
    '''
    info
    '''

    def __init__(self, host='', port=5000):
        self.player_sockets = [False, False, False, False]
        self.player_messages = [None, None, None, None]

        t = Thread(target=self.connection_handler, args=(host, port))
        t.setDaemon(True) # this line makes sure the thread exits when the server is stopped (with ctrl-c)
        t.start()

    def connection_handler(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)

        while True:

            print('Awaiting new connection')
            sock, addr = server_socket.accept()
            print('Connection request from %r. Awaiting player number...' % (addr, ))
            player = int(sock.recv(512))
            print('Player number is %i.  ' % player)
            if self.player_sockets[player]:
                print("There was already a client connected for player %s. That client will be disconnected." % BridgeServer.PLAYERS[player])
                self.player_sockets[player].close()
                self.player_sockets[player] = False

            self.player_sockets[player] = sock
            self.player_sockets[player].settimeout(5)
            print("Player %s connected from %r" % (BridgeServer.PLAYERS[player], addr))

            if self.player_messages[player] is not None:
                self.send(player, self.player_messages[player])


    def send(self, playernr, message):
        self.player_messages[playernr] = message
        if self.player_sockets[playernr] is not False:
            try:
                self.player_sockets[playernr].send(message)
            except socket.error as e:
                print("error in communication with client of player %i " % playernr)
                print("socket error: %s" % e)
                print("removing socket")
                self.player_sockets[playernr].close()
                self.player_sockets[playernr] = False

    def recv(self, playernr):
        while True:
            if self.player_sockets[playernr] is not False:
                try:
                    data = self.player_sockets[playernr].recv(2048)
                    return data
                except socket.timeout:
                    pass
                except socket.error as e:
                    print("error in communication with client of player %i " % playernr)
                    print("socket error: %s" % e)
                    print("removing socket")
                    self.player_sockets[playernr].close()
                    self.player_sockets[playernr] = False
            sleep(1)

class BridgeServer():

    PLAYERS = ['north', 'east', 'south', 'west']
    PLAYERNAMES = ['koen', 'jelle', 'frans', 'pieter']

    CARDS = [ 'SA', 'SH', 'SV', 'SB', 'S10', 'S9', 'S8', 'S7', 'S6', 'S5', 'S4', 'S3', 'S2',
              'HA', 'HH', 'HV', 'HB', 'H10', 'H9', 'H8', 'H7', 'H6', 'H5', 'H4', 'H3', 'H2',
              'RA', 'RH', 'RV', 'RB', 'R10', 'R9', 'R8', 'R7', 'R6', 'R5', 'R4', 'R3', 'R2',
              'KA', 'KH', 'KV', 'KB', 'K10', 'K9', 'K8', 'K7', 'K6', 'K5', 'K4', 'K3', 'K2' ]

    BIDS = [ '0',
             '1K', '1R', '1H', '1S', '1SA',
             '2K', '2R', '2H', '2S', '2SA',
             '3K', '3R', '3H', '3S', '3SA',
             '4K', '4R', '4H', '4S', '4SA',
             '5K', '5R', '5H', '5S', '5SA',
             '6K', '6R', '6H', '6S', '6SA',
             '7K', '7R', '7H', '7S', '7SA' ]


    def __init__(self, host='', port=5000):
        self.players = Players(host=host, port=port)
        print('Game started')
        self.start()

    def _init_gamestate(self):
        self._gamestate = {
            "HIGHEST_BID" : '0',
            "HIGHEST_BIDDER" : -1,
            "CONTRACT" : '',
            "DOUBLET" : False,
            "REDOUBLET" : False,
            "DUMMY" : -1,
            "SCORE" : [0, 0],
            "TABLE" : ['', '', '', ''],
            "ROUNDS" : [],
            "BIDS" : [],
            "HANDS" : ['', '', '', ''],
            "SHOW_DUMMY" : False,
            "SHOW_BIDS" : False,
            "SHOW_ROUNDS" : False,
            "SHOW_ALL" : False,
            "PLAYERS" : self.PLAYERS,
            }

    def start(self):
        start_bidder = 0
        while True:
            valid_contract = False
            while not valid_contract:
                self._init_gamestate()
                FULLHANDS = self.deal()
                self._gamestate['HANDS'] = deepcopy(FULLHANDS)
                valid_contract = self.bid(start_bidder)
            self.play((self._gamestate['DUMMY']-1) % 4)
            self._gamestate['HANDS'] = FULLHANDS
            self._gamestate['TABLE'] = ['', '', '', '']
            self.query(start_bidder, 'end of round, press enter to deal again', show_all=True)
            start_bidder = (start_bidder + 1) % 4

# QUERY

    def query(self, player, message, show_dummy=False, show_all=False):

        self._gamestate['SHOW_DUMMY'] = show_dummy
        self._gamestate['SHOW_ALL'] = show_all

        self._gamestate['message'] = 'no input'
        for i in range(4):
            if i != player:
                self.players.send(i, pickle.dumps(self._gamestate))

        self._gamestate['message'] = message
        self.players.send(player, pickle.dumps(self._gamestate))
        data = self.players.recv(player)

        return data.decode()

# DEAL

    def deal(self):

        DECK = copy(BridgeServer.CARDS)

        HAND0 = []
        HAND1 = []
        HAND2 = []
        HAND3 = []

        for i in range(13):
            HAND0.append(DECK.pop(randint(0,len(DECK)-1)))
            HAND1.append(DECK.pop(randint(0,len(DECK)-1)))
            HAND2.append(DECK.pop(randint(0,len(DECK)-1)))
            HAND3.append(DECK.pop(randint(0,len(DECK)-1)))

        HAND0 = self.sorthand(HAND0)
        HAND1 = self.sorthand(HAND1)
        HAND2 = self.sorthand(HAND2)
        HAND3 = self.sorthand(HAND3)

        return [HAND0, HAND1, HAND2, HAND3]

    def sorthand(self, hand):

        idx = []
        sortedhand = []

        for i in range(13):
            idx.append(BridgeServer.CARDS.index(hand[i]))

        idx.sort()

        for i in range(13):
            sortedhand.append(BridgeServer.CARDS[idx[i]])

        return sortedhand

# BID

    def bid(self, start_bidder):
        bids = []
        bids += [''] * (start_bidder % 4)
        while True:
            for i in range(4):
                player = (i + start_bidder) % 4
                bids.append(self.pickbid(player))
                if bids[-4:] == ['PASS', 'PASS', 'PASS', 'PASS']:
                    self.query(start_bidder, 'no valid bids, press enter to deal again', show_all=True)
                    return False
                elif len(bids) > 3 + (start_bidder % 4) and bids[-3:] == ['PASS', 'PASS', 'PASS']:
                    self._gamestate['BIDS'] = bids
                    self._gamestate['CONTRACT'] = self._gamestate['HIGHEST_BID']
                    #self._gamestate['DUMMY'] = (self._gamestate['HIGHEST_BIDDER'] + 2) % 4
                    if (self._gamestate['HIGHEST_BIDDER'] % 2) == 0:
                        for j in range(0,len(bids),2):
                            if bids[j] != '' and bids[j] != 'PASS' and bids[j][-1] == self._gamestate['CONTRACT'][-1]:
                                self._gamestate['DUMMY'] = ((j+2) % 4)
                                break
                    else:
                        for j in range(1,len(bids),2):
                            if bids[j] != '' and bids[j] != 'PASS' and bids[j][-1] == self._gamestate['CONTRACT'][-1]:
                                self._gamestate['DUMMY'] = ((j+2) % 4)
                                break
                    return True


    def pickbid(self, player):
        bid_valid = False
        message = 'Player %s bid: ' % BridgeServer.PLAYERS[player]
        self._gamestate['TABLE'][player] = 'X'
        while not bid_valid:
            bid = self.query(player, message)
            bid = bid.upper()
            if bid == 'PASS':
                bid_valid = True
            elif BridgeServer.BIDS.count(bid) > 0:
                if BridgeServer.BIDS.index(bid) > BridgeServer.BIDS.index(self._gamestate['HIGHEST_BID']):
                    self._gamestate['HIGHEST_BID'] = bid
                    self._gamestate['HIGHEST_BIDDER'] = player
                    self._gamestate['DOUBLET'] = False
                    self._gamestate['REDOUBLET'] = False
                    bid_valid = True
                else:
                    message = 'bid lower than highest bid, try again: '
            elif bid == 'D':
                if not self._gamestate['DOUBLET'] and self._gamestate['HIGHEST_BID'] != '0':
                    self._gamestate['DOUBLET'] = True
                    bid_valid = True
                elif self._gamestate['DOUBLET']:
                    message = 'alreadry playing DOUBLET, try again: '
                elif self._gamestate['HIGHEST_BID'] == '0':
                    message = 'cannot bid DOUBLET when there is no other bid, try again: '
            elif bid == 'R':
                if self._gamestate['DOUBLET'] and not self._gamestate['REDOUBLET']:
                    self._gamestate['REDOUBLET'] = True
                    bid_valid = True
                elif not self._gamestate['DOUBLET']:
                    message = 'cannot play REDOUBLET when there is no DOUBLET, try again: '
                elif self._gamestate['REDOUBLET']:
                    message = 'already playing REDOUBLET, try again: '
            else:
                message = 'bid not recognised, try again: '
        self._gamestate['TABLE'][player] = bid
        return bid

# PLAY

    def play(self, start_player):
        self._gamestate['SHOW_DUMMY'] = False
        for i in range(13):
            self._gamestate['TABLE'] = ['', '', '', '']
            self._gamestate['FIRST_CARD'] = ''
            for j in range(4):
                player = (j + start_player) % 4
                picked_card = self.pickcard(player)
                if j < 1:
                    self._gamestate['SHOW_DUMMY'] = True
                    self._gamestate['FIRST_CARD'] = picked_card
            self._gamestate['ROUNDS'].append(self._gamestate['TABLE'])
            winning_player = self.pickwin()
            self._gamestate['SCORE'][winning_player % 2] += 1
            start_player = winning_player

    def pickcard(self, player):
        message = 'Player %s pick card: ' % BridgeServer.PLAYERS[player]
        self._gamestate['TABLE'][player] = 'X'
        while True:
            picked_card = self.query(player, message, show_dummy=self._gamestate['SHOW_DUMMY'])
            picked_card = picked_card.upper()
            if self._gamestate['HANDS'][player].count(picked_card) > 0:
                self._gamestate['HANDS'][player].pop(self._gamestate['HANDS'][player].index(picked_card))
                self._gamestate['TABLE'][player] = picked_card
                return picked_card
            else:
                message = 'card does not exist, try again: '

    def pickwin(self):
        idx = [ BridgeServer.CARDS.index(self._gamestate['TABLE'][0]),
                BridgeServer.CARDS.index(self._gamestate['TABLE'][1]),
                BridgeServer.CARDS.index(self._gamestate['TABLE'][2]),
                BridgeServer.CARDS.index(self._gamestate['TABLE'][3]) ]
        for i in range(4):
            if self._gamestate['TABLE'][i][0] != self._gamestate['FIRST_CARD'][0]:
                idx[i] += 100
            if self._gamestate['TABLE'][i][0] == self._gamestate['CONTRACT'][1:]:
                idx[i] -= 200
        m = min(idx)
        wp = idx.index(m)
        self.query(wp, 'Player %s won, hit enter to continue' % BridgeServer.PLAYERS[wp], show_dummy=True)
        return wp


