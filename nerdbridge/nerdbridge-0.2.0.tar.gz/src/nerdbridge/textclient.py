import socket
import pickle

##############################
# Bridge Text Client
##############################

class BridgeTextClient():
    '''
    '''

    def __init__(self, player, host='', port=5000):
        self.player = player
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(str(player).encode())

        while True:
            data = client_socket.recv(2048)
            self._gamestate = pickle.loads(data)
            data = self.query(self._gamestate['message'])
            if data != ' ':
                client_socket.send(data.encode())


    def query(self, message):
        scr = self.build_screen()
        print(scr)
        if message == 'no input':
            reply = ' '
        else:
            reply = input(message)
            if reply == '':
                reply = 'no reply'
            elif reply.upper() == 'P':
                reply = 'PASS'
        return reply

    def build_hand_block(self, player):
        '''
        build text block of 5 rows and 17 columns containing all cards in a hand
        '''
        if player == -1:
            hand = []
        else:
            hand = self._gamestate['HANDS'][player]
        hand_block = []
        sS = 'S:'
        sH = 'H:'
        sR = 'R:'
        sK = 'K:'
        sS2 = '  '
        sH2 = '  '
        sR2 = '  '
        sK2 = '  '
        iS = 0
        iH = 0
        iR = 0
        iK = 0
        lh = len(hand)
        for i in range(lh):
            if hand[i][0] == 'S':
                if iS <= 6:
                    sS += ' ' + hand[i][1:]
                else:
                    sS2 += ' ' + hand[i][1:]
                iS += 1
            elif hand[i][0] == 'H':
                if iH <= 6:
                    sH += ' ' + hand[i][1:]
                else:
                    sH2 += ' ' + hand[i][1:]
                iH += 1
            elif hand[i][0] == 'R':
                if iR <= 6:
                    sR += ' ' + hand[i][1:]
                else:
                    sR2 += ' ' + hand[i][1:]
                iR += 1
            elif hand[i][0] == 'K':
                if iK <= 6:
                    sK += ' ' + hand[i][1:]
                else:
                    sK2 += ' ' + hand[i][1:]
                iK += 1

        sS = sS + (17 - len(sS)) * ' '
        sH = sH + (17 - len(sH)) * ' '
        sR = sR + (17 - len(sR)) * ' '
        sK = sK + (17 - len(sK)) * ' '

        hand_block.append(sS)
        if len(sS2) > 2:
            sS2 = sS2 + (17 - len(sS2)) * ' '
            hand_block.append(sS2)
        hand_block.append(sH)
        if len(sH2) > 2:
            sH2 = sH2 + (17 - len(sH2)) * ' '
            hand_block.append(sH2)
        hand_block.append(sR)
        if len(sR2) > 2:
            sR2 = sR2 + (17 - len(sR2)) * ' '
            hand_block.append(sR2)
        hand_block.append(sK)
        if len(sK2) > 2:
            sK2 = sK2 + (17 - len(sK2)) * ' '
            hand_block.append(sK2)

        if len(hand_block) == 4:
            hand_block.append(17* ' ')

        return hand_block

    def build_table_block(self):
        '''
        text block of 5 lines and 17 columns
        '''
        table = [ '%10s' % self._gamestate['TABLE'][0] + ' ' * 7,
                 ' ' * 17,
                  '%4s' % self._gamestate['TABLE'][3] + ' ' * 9 + '%4s' % self._gamestate['TABLE'][1],
                 ' ' * 17,
                  '%10s' % self._gamestate['TABLE'][2] + ' ' * 7]
        return table

    def build_bid_block(self):
        '''
        text block of 5+n lines and 17 columns
        '''
        show_bids = self._gamestate['SHOW_BIDS']
        show_all = self._gamestate['SHOW_ALL']
        bidb = []

        if show_bids or show_all:
            bids = self._gamestate['BIDS']
            bids += [''] * ((4 - (len(bids) % 4)) % 4)
            for line in range(len(bids)/4):
                bidb += [ ' %3s %3s %3s %3s ' % (bids[line*4+0][0:3], bids[line*4+1][0:3], bids[line*4+2][0:3], bids[line*4+3][0:3])]

        if len(bidb) < 5:
            bidb += [' ' * 17] * (5 - len(bidb))

        return bidb

    def build_round_block(self):
        '''
        text block of 15 lines and 17 columns
        '''
        show_rounds = self._gamestate['SHOW_ROUNDS']
        show_all = self._gamestate['SHOW_ALL']
        roundb = []

        if show_rounds or show_all:
            rounds = self._gamestate['ROUNDS']
            for line in rounds:
                roundb += [ ' %3s %3s %3s %3s ' % (line[0], line[1], line[2], line[3])]

        roundb += [' ' * 17] * (13 - len(roundb))
        roundb += ['_' * 17] + [' ' * 17]
        return roundb
 
    def build_statusbar(self):
        status = 'Player: %5s    Contract : %3s' % (self._gamestate['PLAYERS'][self.player], self._gamestate['CONTRACT'])
        if self._gamestate['DOUBLET'] and not self._gamestate['REDOUBLET']:
            status += ' (Doublet)'
        if self._gamestate['REDOUBLET']:
            status += ' (Redoublet)'
        status +=  '    Score (NS/EW): %r' % self._gamestate['SCORE']
        return status

    def build_screen(self):
        '''
        builds string block of 77x22 containing full screen
        when bidding rounds larger than
        '''
        player = self.player
        show_dummy = self._gamestate['SHOW_DUMMY']
        show_all = self._gamestate['SHOW_ALL']
        if player == 0 or (self._gamestate['DUMMY'] == 0 and show_dummy) or show_all:
            hand0 = self.build_hand_block(0)
        else:
            hand0 = self.build_hand_block(-1)
        if player == 1 or (self._gamestate['DUMMY'] == 1 and show_dummy) or show_all:
            hand1 = self.build_hand_block(1)
        else:
            hand1 = self.build_hand_block(-1)
        if player == 2 or (self._gamestate['DUMMY'] == 2 and show_dummy) or show_all:
            hand2 = self.build_hand_block(2)
        else:
            hand2 = self.build_hand_block(-1)
        if player == 3 or (self._gamestate['DUMMY'] == 3 and show_dummy) or show_all:
            hand3 = self.build_hand_block(3)
        else:
            hand3 = self.build_hand_block(-1)

        table = self.build_table_block()
        roundb = self.build_round_block()
        bidb = self.build_bid_block()
        status = self.build_statusbar()

        scr = '\n\n\n\n\n'
        scr +=  status + '\n'
        scr += ' ' * 17 + ' | ' + hand0[0] + ' | ' + ' ' * 17 + ' | ' + roundb[0]  + '\n'
        scr += ' ' * 17 + ' | ' + hand0[1] + ' | ' + ' ' * 17 + ' | ' + roundb[1]  + '\n'
        scr += ' ' * 17 + ' | ' + hand0[2] + ' | ' + ' ' * 17 + ' | ' + roundb[2]  + '\n'
        scr += ' ' * 17 + ' | ' + hand0[3] + ' | ' + ' ' * 17 + ' | ' + roundb[3]  + '\n'
        scr += ' ' * 17 + ' | ' + hand0[4] + ' | ' + ' ' * 17 + ' | ' + roundb[4]  + '\n'
        scr += '_' * 57                                       + ' | ' + roundb[5]  + '\n'
        scr += ' ' * 57                                       + ' | ' + roundb[6]  + '\n'
        scr += hand3[0] + ' | ' + table[0] + ' | ' + hand1[0] + ' | ' + roundb[7]  + '\n'
        scr += hand3[1] + ' | ' + table[1] + ' | ' + hand1[1] + ' | ' + roundb[8]  + '\n'
        scr += hand3[2] + ' | ' + table[2] + ' | ' + hand1[2] + ' | ' + roundb[9]  + '\n'
        scr += hand3[3] + ' | ' + table[3] + ' | ' + hand1[3] + ' | ' + roundb[10] + '\n'
        scr += hand3[4] + ' | ' + table[4] + ' | ' + hand1[4] + ' | ' + roundb[11] + '\n'
        scr += '_' * 57                                       + ' | ' + roundb[12] + '\n'
        scr += ' ' * 57                                       + ' | ' + roundb[13] + '\n'
        scr += ' ' * 17 + ' | ' + hand2[0] + ' | ' + ' ' * 17 + ' | ' + roundb[14] + '\n'
        scr += ' ' * 17 + ' | ' + hand2[1] + ' | ' + ' ' * 17 + ' | ' + bidb[0]    + '\n'
        scr += ' ' * 17 + ' | ' + hand2[2] + ' | ' + ' ' * 17 + ' | ' + bidb[1]    + '\n'
        scr += ' ' * 17 + ' | ' + hand2[3] + ' | ' + ' ' * 17 + ' | ' + bidb[2]    + '\n'
        scr += ' ' * 17 + ' | ' + hand0[4] + ' | ' + ' ' * 17 + ' | ' + bidb[3]    + '\n'
        scr += '_' * 77                                                            + '\n'
        scr += ' '
        scr += ' '

        return scr

