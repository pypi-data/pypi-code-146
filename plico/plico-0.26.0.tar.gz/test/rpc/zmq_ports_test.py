#!/usr/bin/env python
import unittest
from plico.rpc.zmq_ports import ZmqPorts



class ZmqPortsTest(unittest.TestCase):


    def setUp(self):
        self._zmqPorts= ZmqPorts(None, None)



    def testHostname(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
