""" Unit tests for the wfengine_remote module """
import uuid
import unittest
from testfixtures import compare
from fireworks.core.launchpad import LaunchPad
from fireworks.fw_config import LAUNCHPAD_LOC
from fireworks.user_objects.queue_adapters.common_adapter import CommonAdapter
from wfgenes.engine.wfengine_remote import WFEngineRemote
from wfgenes.engine.wfengine import WFEngine
from fireworks import Workflow
import threading

QADAPTER_DCT = {
    '_fw_name': 'CommonAdapter',
    '_fw_q_type': 'SLURM',
    'nodes': 1,
    'ntasks': 1,
    'pre_rocket': '. python-3.6.8/bin/activate',
    'queue': 'dev_single',
    'rocket_launch': 'rlaunch singleshot',
    'walltime': '00:01:00'
}


#@unittest.skip(reason="currently skipping remote tests")
class WFEngineRemoteTest(unittest.TestCase):
    """ test the WFEngine class """
    def setUp(self):
        if LAUNCHPAD_LOC:
            self.launchpad = LaunchPad.from_file(LAUNCHPAD_LOC)
        else:
            self.launchpad = LaunchPad()

        self.qadapter = CommonAdapter.from_dict(QADAPTER_DCT)
        self.launchdir = '/home/mehdi/work/AAA'
        self.sleep_time = 60
        self.name = str(uuid.uuid4())
        self.user = 'th7356'
        self.host = 'horeka.scc.kit.edu'
        self.conf = 'module load python/3'
        self.wf_query = {}
        
        #self.wfe_remote = WFEngineRemote(launchpad=self.launchpad, launchdir=self.launchdir,
         #                         qadapter=self.qadapter, wf_query=self.wf_query,
         #                   host=self.host, user=self.user, conf=self.conf)
         
         
        self.wf_file = "/home/mehdi/work/gitscc/wfgenes/src/wfgenes/intro_examples/rgg/wfGenes_output/random_graph/FireWorks/random_graph.yaml"
        self.wfe = WFEngine(launchpad=self.launchpad, launchdir=self.launchdir,
                            qadapter=self.qadapter, wf_query=self.wf_query,
                            )
    def tearDown(self):
        if self.wfe.thread is not None and self.wfe.thread.is_alive():
            self.wfe.stop()
            self.wfe.thread.join()

    @unittest.skip(reason="")
    def test_add_wf(self):
        workflow = Workflow.from_file(self.wf_file)
        self.wfe.add_workflow(workflow=workflow)
    
    #@unittest.skip(reason="")
    def test_launcher(self):
        #event  = threading.Event()
        #self.wfe.launcher(event)
        self.wfe.show_nodes_status()
        
if __name__ == '__main__':         
    unittest.main()
