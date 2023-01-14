import os

from pytest_ver.lib.iuv.iuv import IUV
from . import services
from .cfg import Cfg
from .log.logger import Logger
from .log.logger_stdout import LoggerStdout
from .protocol import Protocol
from .report.report import Report
from .storage.storage import Storage
from .summary import Summary
from .trace_matrix import TraceMatrix
from .verifier import Verifier


# -------------------
## Holds the overall test harness
# initializes the services object
class PytestHarness:
    # -------------------
    ## constructor
    def __init__(self):
        services.harness = self

        ## holds the IUV object when needed
        self.iuv = None
        ## hplds reference to the protocol object
        self.proto = None
        ## holds reference to the verifier object
        self.ver = None
        ## holds reference to the logger object
        self.logger = None

        services.logger = LoggerStdout()
        services.logger.init()
        self.logger = services.logger

    # -------------------
    ## initialize - once per invocation
    #
    # @param iuv_create_files used to suppress creation of out/*.json files (for reporting)
    # @return None
    def init(self, iuv_create_files=True):
        if 'iuvmode' in os.environ and os.environ['iuvmode'] == 'True':  # pragma: no cover
            # coverage: iuvmode is only set during IUV and UT runs
            services.iuvmode = True
            self.iuv = IUV()
            self.iuv.init()

        services.cfg = Cfg()
        services.cfg.init(iuv_create_files)
        # uncomment to DEBUG
        # print(f'DBG: harness: cfg_path={services.cfg.cfg_path}')

        # after cfg indicates where log files are stored, can use normal logger
        services.logger = Logger()
        services.logger.init()

        services.storage = Storage.factory()
        services.summary = Summary()
        services.trace = TraceMatrix()
        services.proto = Protocol()

        self.proto = services.proto
        self.ver = Verifier()
        self.logger = services.logger

        services.cfg.init2()
        services.cfg.report()

        services.proto.init()
        services.storage.init()

        if services.iuvmode:  # pragma: no cover
            # coverage: iuvmode is only set during IUV and UT runs
            self.iuv.init2()

    # -------------------
    ## terminate
    #
    # @return None
    def term(self):
        services.proto.term()
        services.trace.term()
        services.summary.term()
        services.storage.term()

    # -------------------
    ## run a report
    #
    # @return None
    def report(self):
        rep = Report()
        rep.report()

    # -------------------
    ## abort the run
    #
    # @return None
    def abort(self):
        services.abort()
