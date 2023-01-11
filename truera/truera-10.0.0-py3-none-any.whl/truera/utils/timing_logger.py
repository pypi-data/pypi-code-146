import cProfile
import io
import logging
import os
import pstats
import tempfile
import time


class TimingLogger(object):
    """Used to profile function calls and log them.

    Usage:
        with TimingLogger(...) as logger:
            ... code to profile ...
    
    """

    def __init__(
        self,
        tag: str,
        log_detailed_output=False,
        tmpfiledir: str = None,
        num_to_filter: int = 40
    ):
        self.tmpfiledir = tmpfiledir
        self.num_to_filter = num_to_filter
        self.pr = None
        self.tag = tag
        self.log_detailed_output = log_detailed_output
        self.started = None

    def __enter__(self):
        if self.log_detailed_output:
            self.pr = cProfile.Profile()
            self.pr.enable()
        self.started = time.time()
        return self

    def __exit__(self, type, value, traceback):
        elapsed = time.time() - self.started
        outfile_path = None
        if self.log_detailed_output:
            self.pr.disable()
            outfile_fd, outfile_path = tempfile.mkstemp(
                suffix=".txt", prefix=self.tag, dir=self.tmpfiledir
            )
            os.close(outfile_fd)
            s = io.StringIO()
            pstats.Stats(self.pr,
                         stream=s).sort_stats('cumulative').print_stats(40)
            outfile = open(outfile_path, 'w')
            outfile.write(s.getvalue())
            outfile.close()
        logging.getLogger(__name__).info(
            "{} took {}s. Logged to {}".format(
                self.tag, round(elapsed, 3), outfile_path
            )
        )
