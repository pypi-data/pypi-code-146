from quickstats.interface.root.TObject import TObject

from quickstats.interface.root.macros import load_macros, load_macro

from quickstats.interface.root.TArrayData import TArrayData
from quickstats.interface.root.TH1 import TH1
from quickstats.interface.root.TH2 import TH2
from quickstats.interface.root.TF1 import TF1
from quickstats.interface.root.RooRealVar import RooRealVar
from quickstats.interface.root.RooAbsData import RooAbsData
from quickstats.interface.root.RooDataSet import RooDataSet
from quickstats.interface.root.RooAbsPdf import RooAbsPdf
from quickstats.interface.root.RooArgSet import RooArgSet
from quickstats.interface.root.RooMsgService import RooMsgService

load_macros()

import quickstats
quickstats.load_corelib()