"""
    Expose the classes in the API
"""
##############################
VERSION = '0.10.99'
##############################

import gettext
import locale
import os
import re

LOC = locale.getdefaultlocale()[0]
LOC = 'en_GB'

locales_exe = os.path.join(os.getcwd(), 'locale')
locales_run = '../bfgsupport/bfgsupport/locale'
if os.path.isdir(locales_exe):
    LOCALES_DIRECTORY = locales_exe
else:
    LOCALES_DIRECTORY = locales_run

# As a last resort hard code the location of the locales directory
# (used in Sphinx when documenting other projects).
if not os.path.isdir(LOCALES_DIRECTORY):
    LOCALES_DIRECTORY = '/locale'


translation = gettext.translation('bfg', localedir=LOCALES_DIRECTORY, languages=[LOC], fallback=False)
translation.install()
_ = translation.gettext


from ._version import __version__
VERSION = __version__

# from bfgsupport.source.images import Images
from .source.board import Board, Trick, Contract, Auction
from .source.hand import Hand
from .source.file_objects import Files
from .source.pbn import PBN
from .source.comment_xref import CommentXref, convert_text_to_html
from .source.strategy_xref import StrategyXref, strategy_descriptions
from .source.bridge_tools import Bid, Pass, Double
from .source.player import Player
from .source.dealer import Dealer
from .source.dealer_engine import DealerEngine
import bfgsupport.source.bfg_common as bfg_common
