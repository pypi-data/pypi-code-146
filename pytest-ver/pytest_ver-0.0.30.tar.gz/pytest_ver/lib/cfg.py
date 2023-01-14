import json
import os
import re

import jsmin

from . import services
from .build_info import BuildInfo
from .constants import Constants
from .report.common.page_info import PageInfo


# -------------------
## Holds configuration functions and globals
class Cfg:
    # -------------------
    ## constructor
    def __init__(self):
        # --- Public - default settings
        ## holds path to cfg file
        self.cfg_path = 'cfg.json'
        ## holds path to output directory
        self.outdir = 'out'

        ## holds storage type
        self.storage_type = 'dev'
        ## holds run type: one of formal, dryrun, dev
        self.test_run_type = 'dev'
        ## holds run id
        self.test_run_id = 'dev-001'
        ## holds format to use for DTS
        self.dts_format = "%Y-%m-%d %H:%M:%S %Z"
        ## flag indicates to use UTC or local time
        self.use_utc = False
        ## holds page info e.g. headers and footers
        self.page_info = PageInfo()
        ## holds current test name
        self.test_script = None
        ## holds path to the requirements json file
        self.reqmt_json_path = None

        ## test protocol file name - no results
        self.tp_protocol_fname = 'test_protocol'
        ## test report file name - with results
        self.tp_report_fname = 'test_report'

        ## report types to generate, valid: txt, pdf, docx
        self.report_types = ['txt', 'pdf', 'docx']

        ## internal IUV use only; use to create JSON files or not
        self.iuv_create_files = True

    # -------------------
    ## initialize - step1
    # read cfg json file
    #
    # @param iuv_create_files used to suppress creation of out/*.json files (for reporting)
    # @return None
    def init(self, iuv_create_files):
        # TODO used to set the cfg path in IUV and UT, should come from CLI
        # services.logger.err(f'before: {self.cfg_path}')
        if 'PYTEST_VER_CFG' in os.environ:  # pragma: no cover
            # coverage: only set in IUV and UT
            self.cfg_path = os.environ['PYTEST_VER_CFG']
        # TODO delete if not needed
        # services.logger.err(f'after: {self.cfg_path}')

        self._read_ini()

        self.iuv_create_files = iuv_create_files

        if not os.path.isdir(self.outdir):  # pragma: no cover
            # coverage: in IUV and UT, outdir is created by scripts
            os.mkdir(self.outdir)

        self.page_info.check()

    # -------------------
    ## initialize - step2
    # get the current test name
    #
    # @return None
    def init2(self):
        self.test_script = None
        if 'PYTEST_CURRENT_TEST' in os.environ:  # pragma: no cover
            # coverage: in IUV and UT, variable is always set
            # eg.  ver/test_sample_ver1.py
            m = re.search(r'test_(\w+)\.py::(\w+)', os.getenv('PYTEST_CURRENT_TEST'))
            if m:
                self.test_script = m.group(1)

    # -------------------
    ## report configuration to the log
    #
    # @return None
    def report(self):
        services.logger.start('Cfg:')
        services.logger.line(f"  {'Cfg path': <20}: {self.cfg_path}")
        services.logger.line(f"  {'Output Dir': <20}: {self.outdir}")
        services.logger.line(f"  {'Storage Type': <20}: {self.storage_type}")
        services.logger.line(f"  {'Test Run ID': <20}: {self.test_run_id}")
        services.logger.line(f"  {'Req. json path': <20}: {self.reqmt_json_path}")
        if services.iuvmode:  # pragma: no cover
            # coverage: iuvmode is always set during IUV and UT runs
            services.logger.line(f"  {'IUV mode': <20}: {services.iuvmode}")
            services.logger.line(f"  {'Create Files': <20}: {self.iuv_create_files}")

        services.logger.line(f"  {'pytest version': <20}: {Constants.version}")
        services.logger.line(f"  {'git sha': <20}: {BuildInfo.git_sha}")
        services.logger.line(f"  {'git branch': <20}: {BuildInfo.git_branch}")
        services.logger.line(f"  {'git uncommitted': <20}: {BuildInfo.git_uncommitted}")
        services.logger.line(f"  {'git unpushed': <20}: {BuildInfo.git_unpushed}")

        services.logger.line('')

    # -------------------
    ## read the cfg json file
    # set attributes in this class based on content
    #
    # @return None
    def _read_ini(self):
        if not os.path.isfile(self.cfg_path):
            services.logger.warn(f'{self.cfg_path} not found')
            return

        # load json file
        with open(self.cfg_path, 'r', encoding='utf-8') as fp:
            cleanj = jsmin.jsmin(fp.read())
            j = json.loads(cleanj)

        # override and/or add to available attributes
        for key, value in j.items():
            if key == 'tp_report':
                self.page_info.init_tp_report(value)
            elif key == 'tp_protocol':
                self.page_info.init_tp_protocol(value)
            elif key == 'trace':
                self.page_info.init_trace(value)
            elif key == 'summary':
                self.page_info.init_summary(value)
            else:
                setattr(self, key, value)
