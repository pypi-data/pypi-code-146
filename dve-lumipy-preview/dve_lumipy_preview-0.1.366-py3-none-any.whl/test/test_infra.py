import io
import json
import os
import sys
import traceback as tb
import unittest
from multiprocessing import Process, Queue
from unittest import TestLoader, TestSuite, TextTestRunner
from unittest.suite import _ErrorHolder

import lumipy as lm


def load_secrets_into_env_if_local_run():
    """


    """

    if 'LOCAL_INT_TEST_SECRETS_PATH' in os.environ:
        path = os.environ['LOCAL_INT_TEST_SECRETS_PATH']
        print(f'Loading secrets from {path}')
        env_var_map = {
            'lumiApiUrl': 'FBN_LUMI_API_URL',
            'tokenUrl': 'FBN_TOKEN_URL',
            'username': 'FBN_USERNAME',
            'password': 'FBN_PASSWORD',
            'clientId': 'FBN_CLIENT_ID',
            'clientSecret': 'FBN_CLIENT_SECRET'
        }

        with open(path, 'r') as f:
            creds = json.load(f)['api']
            for k1, k2 in env_var_map.items():
                os.environ[k2] = creds[k1]


class BaseIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        load_secrets_into_env_if_local_run()
        cls.client = lm.get_client()


class BaseIntTestWithAtlas(BaseIntTest):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.atlas = lm.get_atlas()


class LumipyTestWorker(Process):

    def __init__(self, manifest, verbosity, queue: Queue):
        super().__init__()
        self.manifest = manifest
        self.verbosity = verbosity
        self.queue = queue

    def run(self):
        loader = TestLoader()
        suite = TestSuite(map(loader.loadTestsFromTestCase, self.manifest))

        stream = io.StringIO()
        sys.stdout = stream
        sys.stderr = stream

        runner = TextTestRunner(verbosity=self.verbosity, stream=stream).run(suite)

        try:
            def test_name(c):
                if isinstance(c, _ErrorHolder):
                    method, cls = c.description.split()
                    cls = cls.split('.')[-1].strip(')')
                    return f'{cls}.{method}'

                return f'{type(c).__name__}.{c._testMethodName}'

            result = [
                runner.testsRun,
                [(f'{test_name(case)}', trace) for case, trace in runner.errors],
                [(f'{test_name(case)}', trace) for case, trace in runner.failures],
            ]

            stream.seek(0)
            for line in stream.readlines():
                self.queue.put((self.name, 'log_line', line))

            self.queue.put((self.name, 'result', result))

        except Exception as e:
            self.queue.put((self.name, 'exception', ''.join(tb.format_exception(*sys.exc_info()))))
