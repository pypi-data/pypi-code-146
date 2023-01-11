import threading


# A dynamic group of locks, useful for parameter based locking.
class LockGroup(object):

    def __init__(self):
        self.lock_dict = {}
        self.lock = threading.Lock()

    # Returns a lock object, unique for each unique value of param.
    # The first call with a given value of param creates a new lock, subsequent
    # calls return the same lock.
    def get_lock(self, param) -> threading.Lock():
        with self.lock:
            if param not in self.lock_dict:
                self.lock_dict[param] = threading.Lock()
            return self.lock_dict[param]