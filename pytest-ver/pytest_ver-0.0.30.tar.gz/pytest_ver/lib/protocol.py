from . import services
from .utils import Utils


# -------------------
## Holds information about the current protocol
class Protocol:
    # -------------------
    ## constructor
    def __init__(self):
        ## holds the list of protocol info found in test cases
        self._protocols = {}
        ## holds the current protocol
        self._protocol = None
        ## holds the current step
        self._step = None
        ## holds the current test script name
        self._current_test_script = None
        ## holds if the output json file needs to be saved
        self._dirty = False

    # -------------------
    ## initialize
    #
    # @return None
    def init(self):
        self._protocol = None
        self._step = None

    # -------------------
    ## terminate
    #
    # @return None
    def term(self):
        self.save()

    # -------------------
    ## create new protocol
    #
    # @param proto_id    the protocol id
    # @param desc        the protocol description
    # @return None
    def protocol(self, proto_id: str, desc):
        self._check_test_change()

        dts = Utils.get_dts(use_cfg_fmt=True)
        self._protocol = {
            'proto_id': proto_id.upper(),
            'desc': desc,
            'location': Utils.get_location(levels=2),
            'executed_by': 'automated',
            'start_date': dts,
            'dut_version': 'N/A',
            'dut_serialno': 'N/A',
            'objectives': [],
            'preconditions': [],
            'deviations': [],
            'steps': [],
        }
        self._dirty = True

        if self._protocol['proto_id'] in self._protocols:
            prev_loc = self._protocols[self._protocol['proto_id']]['location']
            services.logger.err(f'{self._protocol["proto_id"]} protocol id is already in use:')
            services.logger.err(f'   location: {self._protocol["location"]}')
            services.logger.err(f'   previous: {prev_loc}')
            services.abort()
        else:
            self._protocols[self._protocol['proto_id']] = self._protocol
            self._dirty = True

        self._step = None
        self.save()

    # -------------------
    ## check if the test script name has changed,
    # if so, save the current content and re-init protocols info
    #
    # @return None
    def _check_test_change(self):
        if self._current_test_script != services.cfg.test_script:
            if self._current_test_script is not None:
                self.save()
            self._current_test_script = services.cfg.test_script
            self._protocols = {}
            self._dirty = True

            services.trace.check_test_script()
            services.summary.check_test_script()

    # -------------------
    ## set the version for the Device Under Test (DUT)
    #
    # @param version     the version value
    # @return None
    def set_dut_version(self, version):
        self._check_test_change()

        if self._protocol is None:
            services.abort('set_dut_version(): missing pth.proto.protocol(), exiting')

        self._protocol['dut_version'] = version
        self._dirty = True

    # -------------------
    ## set the serial number for the Device Under Test (DUT)
    #
    # @param serialno     the serial number value
    # @return None
    def set_dut_serialno(self, serialno):
        self._check_test_change()

        if self._protocol is None:
            services.abort('set_dut_serialno(): missing pth.proto.protocol(), exiting')

        self._protocol['dut_serialno'] = serialno
        self._dirty = True

    # -------------------
    ## an objective of the current test case
    #
    # @param desc     the description
    # @return None
    def add_objective(self, desc):
        self._check_test_change()

        if self._protocol is None:
            services.abort('add_objective(): missing pth.proto.protocol(), exiting')

        self._protocol['objectives'].append(desc)
        self._dirty = True

    # -------------------
    ## a precondition of the current test case
    #
    # @param desc     the description
    # @return None
    def add_precondition(self, desc):
        self._check_test_change()

        if self._protocol is None:
            services.abort('add_precondition(): missing pth.proto.protocol(), exiting')

        self._protocol['preconditions'].append(desc)
        self._dirty = True

    # -------------------
    ## a devidation of the current test case
    #
    # @param desc     the description
    # @return None
    def add_deviation(self, desc):
        self._check_test_change()

        if self._protocol is None:
            services.abort('add_deviation(): missing pth.proto.protocol(), exiting')

        self._protocol['deviations'].append(desc)
        self._dirty = True

    # -------------------
    ## create a mew step in the current test protocol
    #
    # @param desc     the description
    # @return None
    def step(self, desc):
        self._check_test_change()

        if self._protocol is None:
            services.abort('step(): missing pth.proto.protocol(), exiting')

        dts = Utils.get_dts(use_cfg_fmt=False)
        self._step = {
            'desc': desc,
            'dts': dts,
            'comments': [],
            'results': [],
        }
        self._protocol['steps'].append(self._step)
        self._dirty = True
        self.save()

    # -------------------
    ## add a comment
    #
    # @param msg     the comment to add
    # @return None
    def comment(self, msg):
        self._check_test_change()

        if self._protocol is None:
            services.abort('comment(): missing pth.proto.protocol(), exiting')

        if self._step is None:
            services.abort('comment(): missing pth.proto.step(), exiting')

        self._step['comments'].append(msg)
        self._dirty = True

    # -------------------
    ## add a result to the current step
    # save the data to storage
    #
    # @param rs     the result summary to associate with this step
    # @return None
    def add_result(self, rs):
        if self._protocol is None:
            services.abort('add_result(): missing pth.proto.protocol(), exiting')

        if self._step is None:
            services.abort('add_result(): missing pth.proto.step(), exiting')

        self._step['results'].append(rs)
        self._dirty = True

        if rs.reqids is not None:
            services.trace.add_proto(rs.reqids, self._protocol['proto_id'], rs.location)

        services.summary.add_result(rs.reqids, self._protocol['proto_id'], rs.result)
        self.save()

    # -------------------
    ## save protocol info to storage
    #
    # @return None
    def save(self):
        services.storage.save_protocol(self._protocols)
        self._dirty = False

    # === for IUV only

    # -------------------
    ## (IUV only) get current protocol info
    #
    # @return protocol object
    def iuv_get_protocol(self):
        return self._protocol

    # -------------------
    ## (IUV only) get current dirty flag
    #
    # @return dirty flag
    def iuv_get_dirty(self):
        return self._dirty
