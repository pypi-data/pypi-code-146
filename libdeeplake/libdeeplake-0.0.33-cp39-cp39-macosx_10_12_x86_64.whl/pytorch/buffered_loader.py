

class BufferedLoader:
    def __init__(self, loader, buffer, batch_size, drop_last):
        self.loader = loader
        self.buffer = buffer
        self.batch_size = batch_size
        self.drop_last = drop_last

    def __iter__(self):
        next_batch = []
        for batch in self.loader:
            for sample in batch:
                sample = self.buffer.exchange(sample)
                if sample is not None:
                    next_batch.append(sample)
                if len(next_batch) == self.batch_size:
                    yield next_batch
                    next_batch = []

        while not self.buffer.emtpy():
            sample = self.buffer.exchange(None)
            next_batch.append(sample)
            if len(next_batch) == self.batch_size:
                yield next_batch
                next_batch = []

        if not self.drop_last and len(next_batch) > 0:
            yield next_batch

    def __len__(self):
        return len(self.loader)

    def __next__(self):
        return next(iter(self))

