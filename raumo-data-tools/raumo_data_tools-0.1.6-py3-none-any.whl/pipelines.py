class Pipeline:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    def parse(self):
        ...
