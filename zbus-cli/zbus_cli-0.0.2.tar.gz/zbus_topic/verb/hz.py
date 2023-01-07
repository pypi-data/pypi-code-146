from zbus_cli.verb import VerbExtension
from argparse import ArgumentTypeError
import zmq
import time
import threading
import math

DEFAULT_WINDOW_SIZE = 10000


def positive_int(string):
    try:
        value = int(string)
    except ValueError:
        value = -1
    if value <= 0:
        raise ArgumentTypeError('value must be a positive integer')
    return value


class HzVerb(VerbExtension):
    """Print the average publishing rate to screen."""

    def add_arguments(self, parser, cli_name):
        arg = parser.add_argument(
            'topic_name',
            help="Name of the ZBUS topic to listen to (e.g. '/chatter')")

        parser.add_argument(
            '--window',
            '-w',
            dest='window_size',
            type=positive_int,
            default=DEFAULT_WINDOW_SIZE,
            help='window size, in # of messages, for calculating rate '
            '(default: %d)' % DEFAULT_WINDOW_SIZE,
            metavar='WINDOW')

    def main(self, *, args, addr):
        topic = args.topic_name
        window_size = args.window_size
        topic_hz = TopicHz(topic=topic, window_size=window_size)
        topic_hz.loop(addr)


class TopicHz(object):
    """TopicHz receives messages for a topic and computes frequency."""

    def __init__(self, topic, window_size):
        self.lock = threading.Lock()
        self.msg_t0 = -1
        self.msg_tn = 0
        self.times = []
        self.window_size = window_size
        self.topic = topic

    def loop(self, addr):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(addr["sub"])
        socket.subscribe(self.topic)

        while True:
            timeout = 1 * 1e9
            enter_t = time.time_ns()
            while time.time_ns() - enter_t < timeout:
                message = socket.recv_multipart()
                topic = message[0].decode('utf8')
                if topic == self.topic:
                    self.callback_hz()
            self.print_hz()

    def callback_hz(self):
        """Calculate interval time."""

        curr = time.time_ns()
        if self.msg_t0 < 0 or self.msg_t0 > curr:
            self.msg_t0 = curr
            self.msg_tn = curr
            self.times = []
        else:
            self.times.append(curr - self.msg_tn)
            self.msg_tn = curr

        if len(self.times) > self.window_size:
            self.times.pop(0)

    def get_hz(self):
        """
        Calculate the average publising rate.

        :param topic: topic name, ``list`` of ``str``
        :returns: tuple of stat results
            (rate, min_delta, max_delta, standard deviation, window number)
            None when waiting for the first message or there is no new one
        """

        # Get frequency every one minute
        if len(self.times) == 0:
            return
        times = self.times
        n = len(times)
        mean = sum(times) / n
        rate = 1. / mean if mean > 0. else 0

        # std dev
        std_dev = math.sqrt(sum((x - mean)**2 for x in times) / n)

        # min and max
        max_delta = max(times)
        min_delta = min(times)

        return rate, min_delta, max_delta, std_dev, n

    def print_hz(self):
        """Print the average publishing rate to screen."""
        ret = self.get_hz()
        if ret is None:
            return
        rate, min_delta, max_delta, std_dev, window = ret
        print(
            'average rate: %.3f\n\tmin: %.3fs max: %.3fs std dev: %.5fs window: %s'
            % (rate * 1e9, min_delta * 1e-9, max_delta * 1e-9, std_dev * 1e-9,
               window))
        return
