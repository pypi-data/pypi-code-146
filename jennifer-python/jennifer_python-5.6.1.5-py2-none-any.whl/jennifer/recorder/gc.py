import gc
import time
import os


class GCRecorder(object):
    def __init__(self):
        # if not hasattr(gc, 'callbacks'):  # python 3.3 or later
        if not hasattr(gc, 'get_stats'):  # python 3.4 or later
            print(os.getpid(), '[jennifer]', 'gc_info', "NOT SUPPORTED", "required: python >= 3.4")
            self.support = False
            return

        self.freezeSupport = hasattr(gc, 'get_freeze_count')  # python 3.7 or later
        self.support = True
        self.start_time = 0
        self.accumulate_time = 0
        self.gc_count = 0
        self.gc_gen_time = [0, 0, 0, 0]  # Python have 3 generation
        self.uncollectable_count = 0
        gc.callbacks.append(self.gc_callback)

    @staticmethod
    def _debug_log(text):
        if os.getenv('JENNIFER_PY_DBG'):
            try:
                log_socket = __import__('jennifer').get_log_socket()
                if log_socket is not None:
                    log_socket.log(text)
            except ImportError as e:
                print(e)

    def record(self):
        if not self.support:
            return 0, 0, [0, 0, 0, 0], 0

        return self.accumulate_time, self.gc_count, self.gc_gen_time, self.uncollectable_count

    def gc_callback(self, phase, info):

        if phase == 'start':
            self.start_time = time.time()
        elif phase == 'stop':  # phase end
            delta = int((time.time() - self.start_time) * 1000)
            self.accumulate_time += delta
            self.gc_count += 1
            self.gc_gen_time[info['generation']] += delta
            self.uncollectable_count += info['uncollectable']
            if self.freezeSupport:
                self.uncollectable_count += gc.get_freeze_count()

    def __del__(self):
        if not self.support:
            return
        if self.gc_callback in gc.callbacks:
            gc.callbacks.remove(self.gc_callback)
