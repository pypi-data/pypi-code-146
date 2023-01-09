import time

class Retl:
    def __init__(self, filepath: str):
        self.filepath = filepath
        
    def start(self):
        self.file = open(self.filepath, 'a')
        
    def log(self, message: str, severity: str):
        self.start()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.file.write(f'[{timestamp}] {severity}: {message}\n')
        self.close()
        
    def close(self):
        self.file.close()