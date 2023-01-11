import concurrent.futures
from multiprocessing import Pool, cpu_count

from tqdm import tqdm


class BatchProgress:
    def __init__(self, batchList=None) -> None:
        self.batchList = None
        self.threads = None
        self.useMultiThreading = True
        self.startAt = 0
        self.threadCount = max(int(cpu_count() / 2) - 1, 1)
        self.tqdm = None
        self.initBatchList(batchList)
        self.asynchronous = False

    def initBatchList(self, batchList):
        if batchList is not None:
            self.batchList = batchList if batchList is not None else self.batchList
            if self.startAt > 0:
                self.batchList = self.batchList[self.startAt:]
            length = len(batchList)
            self.threads = min(self.threadCount, length, 40)
        return self.batchList

    def start(self, batchFunc, batchList=None, afterBatch=None):
        pool = None
        data = None
        self.initBatchList(batchList)

        if self.useMultiThreading:
            pool = Pool(processes=self.threads)

        if self.asynchronous and self.useMultiThreading:
            processList = tqdm(range(len(self.batchList)))
            for data in pool.imap_unordered(batchFunc, self.batchList):
                processList.update(1)
                if afterBatch is not None:
                    afterBatch(data)
        else:
            processList = tqdm(range(0, len(self.batchList), self.threads))
            for dataIndex in processList:
                limit = dataIndex + self.threads

                if self.useMultiThreading:
                    data = pool.map(batchFunc, self.batchList[dataIndex:limit])
                else:
                    data = list(map(batchFunc, self.batchList[dataIndex:limit]))

                if afterBatch is not None:
                    afterBatch(data, dataIndex)

        if self.useMultiThreading:
            pool.close()

    def asyncQueue(self, function, entryList, update):
        """
        run a function asynchously with a entry from the entrylist as argument
        and call a update function when the next result in the sequence is ready
        """
        entryList = self.initBatchList(entryList)
        processList = tqdm(range(self.startAt, len(entryList)))
        with concurrent.futures.ThreadPoolExecutor(self.threads) as executor:
            # Use a list to store the futures and their corresponding file names
            array_futures = [(executor.submit(function, entry), entry) for entry in entryList]
            for future, entry in array_futures:
                processList.update(1)
                array = future.result()
                update(array, entry)
