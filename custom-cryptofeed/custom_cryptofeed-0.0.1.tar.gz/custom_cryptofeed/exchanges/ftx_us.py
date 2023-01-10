'''
Copyright (C) 2017-2022 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
'''
import logging

from custom_cryptofeed.connection import RestEndpoint, Routes, WebsocketEndpoint
from custom_cryptofeed.defines import FTX_US, L2_BOOK, ORDER_INFO, TICKER, TRADES, FILLS
from custom_cryptofeed.exchanges.ftx import FTX
from custom_cryptofeed.exchanges.mixins.ftx_rest_us import FTXUSRestMixin


LOG = logging.getLogger('feedhandler')


class FTXUS(FTX, FTXUSRestMixin):
    id = FTX_US
    websocket_endpoints = [WebsocketEndpoint('wss://ftx.us/ws/', options={'compression': None})]
    rest_endpoints = [RestEndpoint('https://ftx.us', routes=Routes('/api/markets'))]

    websocket_channels = {
        L2_BOOK: 'orderbook',
        TRADES: 'trades',
        TICKER: 'ticker',
        ORDER_INFO: 'orders',
        FILLS: 'fills',
    }
