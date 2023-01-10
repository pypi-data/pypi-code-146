import unittest
import os


class BesDBTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.environ[
            "PYPUSHFLOW_MONGOURL"
        ] = "mongodb://bes:bes@linsvensson.esrf.fr:27017/bes"
        os.environ["PYPUSHFLOW_CREATOR"] = "PyPushflowUnitTests"

    def tearDown(self) -> None:
        os.environ.pop("PYPUSHFLOW_MONGOURL", None)
        os.environ.pop("PYPUSHFLOW_CREATOR", None)
