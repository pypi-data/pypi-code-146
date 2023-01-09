"""Generators Class with helper methods to generate dummy data"""

import logging
import socket
import time
from random import randrange


def generate_unique_name(prefix):
    dt_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    host = socket.gethostname()
    rand = randrange(999)

    unique_str = '{0} {1} {2} {3}'.format(prefix, dt_str, rand, host)
    if len(unique_str) > 60:
        unique_str = '{0}..'.format(unique_str[:58])

    logging.debug('generate::unique_name == {0}'.format(unique_str))

    return unique_str


def generate_unique_file_name():
    epoch_str = str(time.time())  # Length == 17

    # host Max length => 60 - (17 + 8) = 35!
    host = str(socket.gethostname())[0:34]  # 0 - 34 == 35

    unique_file = "cal.{0}_{1}.h5".format(epoch_str, host)
    logging.debug('generate::unique_file_name == {0}'.format(unique_file))

    return unique_file


def generate_timestamp_str(secs=None):
    epoch_time = int(time.time())

    if secs is None:
        additional_secs = -randrange(60)
    else:
        additional_secs = secs

    ts = time.gmtime(epoch_time + additional_secs)
    dt_str = time.strftime('%Y-%m-%dT%H:%M:%S.000+00:00', ts)

    logging.debug('generate_timestamp_str == {0}'.format(dt_str))
    return dt_str
