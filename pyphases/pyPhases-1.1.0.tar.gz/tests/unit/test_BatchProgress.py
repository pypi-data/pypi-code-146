import multiprocessing
import unittest
from time import sleep
from unittest.mock import MagicMock, call, patch

from pyPhases.util.BatchProgress import BatchProgress


class TestBatchProgress(unittest.TestCase):
    def test_init_with_batch_list(self):
        batchList = [1, 2, 3]
        bp = BatchProgress(batchList)
        self.assertEqual(bp.batchList, [1, 2, 3])
        self.assertEqual(bp.useMultiThreading, True)
        self.assertEqual(bp.startAt, 0)
        self.assertEqual(bp.threadCount, max(int(multiprocessing.cpu_count() / 2) - 1, 1))
        self.assertEqual(bp.tqdm, None)
        self.assertEqual(bp.threads, min(bp.threadCount, len(batchList), 40))

    def test_init_without_batch_list(self):
        bp = BatchProgress()
        self.assertEqual(bp.batchList, None)
        self.assertEqual(bp.useMultiThreading, True)
        self.assertEqual(bp.startAt, 0)
        self.assertEqual(bp.threadCount, max(int(multiprocessing.cpu_count() / 2) - 1, 1))
        self.assertEqual(bp.tqdm, None)
        self.assertEqual(bp.threads, None)

    def test_start_without_multithreading(self):
        function = MagicMock()
        bp = BatchProgress([1, 2, 3])
        bp.useMultiThreading = False

        bp.start(function)
        function.assert_has_calls([call(1), call(2), call(3)])

    def test_start_startAt(self):
        function = MagicMock()
        bp = BatchProgress()
        bp.useMultiThreading = False
        bp.startAt = 2

        bp.start(function, [1, 2, 3])
        function.assert_has_calls([call(3)])

    def test_start_afterBatch_multiple_batches(self):
        mock_afterBatch = MagicMock()
        function = MagicMock(return_value="r")
        function.side_effect = ["r0", "r1", "r2"]
        bp = BatchProgress([1, 2, 3])
        bp.threads = 1
        bp.useMultiThreading = False

        bp.start(function, afterBatch=mock_afterBatch)
        function.assert_has_calls([call(1), call(2), call(3)])

        mock_afterBatch.assert_has_calls([call(["r0"], 0), call(["r1"], 1), call(["r2"], 2)])

    # only works whith multi processor (so it will not work in the CI)
    # def test_start_afterBatch(self):
    #     mock_afterBatch = MagicMock()
    #     function = MagicMock(return_value="r")
    #     function.side_effect = ["r0", "r1", "r2"]
    #     bp = BatchProgress([1, 2, 3])
    #     bp.useMultiThreading = False

    #     bp.start(function, afterBatch=mock_afterBatch)
    #     function.assert_has_calls([call(1), call(2), call(3)])

    #     mock_afterBatch.assert_has_calls([call(["r0", "r1", "r2"], 0)])

    # only works whith multi processor (so it will not work in the CI)
    # def test_start_multithreading(self):
    #     function = MagicMock()
    #     bp = BatchProgress([1, 2, 3])
    #     bp.useMultiThreading = True
    #     bp.threads = 2

    #     with patch("multiprocessing.pool.Pool.map") as mock_map:
    #         bp.start(function)
    #         mock_map.assert_has_calls([
    #             call(function, [1, 2]),
    #             call(function, [3])
    #         ])

    def test_start_multithreadingWithOne(self):
        function = MagicMock()
        bp = BatchProgress([1, 2, 3])
        bp.useMultiThreading = True
        bp.threads = 1

        with patch("multiprocessing.pool.Pool.map") as mock_map:
            bp.start(function)
            mock_map.assert_has_calls([
                call(function, [1]),
                call(function, [2]),
                call(function, [3])
            ])

    def test_start_multithreading_asynchron(self):
        function = MagicMock()
        bp = BatchProgress([1, 2, 3])
        bp.useMultiThreading = True
        bp.threads = 2

        with patch("multiprocessing.pool.Pool.imap_unordered") as mock_map:
            bp.asynchronous = True
            bp.start(function)
            mock_map.assert_has_calls([
                call(function, [1, 2, 3])
            ])

    def test_start_multithreading_asynchron_afterbatch(self):
        function = MagicMock()
        mock_afterBatch = MagicMock()

        bp = BatchProgress([1, 2, 3])
        bp.useMultiThreading = True
        bp.threads = 2

        with patch("multiprocessing.pool.Pool.imap_unordered") as mock_map:
            mock_map.return_value = ["r0", "r1", "r2"]

            bp.asynchronous = True
            bp.start(function, afterBatch=mock_afterBatch)

            mock_map.assert_has_calls([
                call(function, [1, 2, 3])
            ])

            mock_afterBatch.assert_has_calls([
                call("r0"),
                call("r1"),
                call("r2"),
            ])

    def test_async_queue(self):

        def function(seconds):
            print("SLEEP FOR %s" % seconds)
            sleep(seconds)
            print("SLEEP FOR %s finished" % seconds)
            return seconds

        mock_afterBatch = MagicMock()

        bp = BatchProgress()
        bp.threads = 3
        bp.asyncQueue(function, [0.1, 0.2, 0.3, 0.05], update=mock_afterBatch)

        mock_afterBatch.assert_has_calls([
            call(0.1, 0.1),
            call(0.2, 0.2),
            call(0.3, 0.3),
            call(0.05, 0.05),
        ])
