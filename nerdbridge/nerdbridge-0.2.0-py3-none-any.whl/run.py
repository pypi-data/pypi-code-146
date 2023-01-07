#!/usr/bin/python

helptext = '''
bridge, the network-based bridge card game.
Usage: bridge [OPTIONS] [north/east/south/west]
       bridge [OPTIONS] [koen/jelle/frans/pieter]

OPTIONs:

\t-h, \t--help \t\t this help menu

Start server:
\t-s, \t--startserver \t start the bridgeserver
\t-p, \t--port=port \t port number of bridge server (default 5000)

Start client:
\t-H, \t--host=host \t connect to server host (default localhost)
\t-p, \t--port=port \t connect to server on port port (default 5000)

Example start server:       bridge -s
                            bridge -s -p 5001

Example start client:       bridge north
                            bridge -H hostname -p 5001 north
'''

import sys
import getopt
import socket

try:  # for when nerdbridge is intstalled as package
    from nerdbridge.server import BridgeServer
    from nerdbridge.textclient import BridgeTextClient
except:  # for when nerdbrigde code is simply copied and run from inside folder
    from server import BridgeServer
    from textclient import BridgeTextClient


def run():
    try:
        options, remainder = getopt.getopt(sys.argv[1:],
                'hsp:H:', ['help', 'startserver', 'port=', 'host='])
    except getopt.GetoptError as inst:
        print('Unrecognised commandline options: %s' % inst)
        options = [('--help', '')]
        remainder = []

    startserver = False
    port = 5000
    host = socket.gethostbyname(socket.gethostname())  

    for opt, arg in options:
        if opt in ('-h', '--help'):
            print(helptext)
            sys.exit()
        if opt in ('-s', '--startserver'):
            startserver = True
        if opt in ('-p', '--port'):
            port = int(arg)
        if opt in ('-H', '--host'):
            host = str(arg)

    if startserver:
        print('Starting Bridge Server (IP=%s)' % socket.gethostbyname(socket.gethostname()))
        bs = BridgeServer('', port)
        sys.exit()

    if  len(remainder) == 1 and remainder[0] in BridgeServer.PLAYERS:
        playernr = BridgeServer.PLAYERS.index(remainder[0])
        print('Starting Bridge Client as player "%s"' % remainder[0])
        tc = BridgeTextClient(playernr, host, port)
    elif  len(remainder) == 1 and remainder[0] in BridgeServer.PLAYERNAMES:
        playernr = BridgeServer.PLAYERNAMES.index(remainder[0])
        print('Starting Bridge Client as player "%s"' % remainder[0])
        tc = BridgeTextClient(playernr, host, port)
    else:
        print('to start client, bridge takes at least one argument: [north/east/south/west]')
        print('to start server, run bridge -s')
        print('for more help, run bridge -h')


if __name__ == '__main__':
    run()

