from zbus_cli.verb import VerbExtension
import zmq
import time
import json, msgpack


def nonnegative_int(inval):
    ret = int(inval)
    if ret < 0:
        # The error message here gets completely swallowed by argparse
        raise ValueError('Value must be positive or zero')
    return ret


def positive_float(inval):
    ret = float(inval)
    if ret <= 0.0:
        # The error message here gets completely swallowed by argparse
        raise ValueError('Value must be positive')
    return ret


class PubVerb(VerbExtension):
    """Publish a message to a topic."""

    def add_arguments(self, parser, cli_name):
        arg = parser.add_argument(
            'topic_name',
            help="Name of the ZBUS topic to publish to (e.g. '/chatter')")

        arg = parser.add_argument('values', help='Values to fill the message')

        group = parser.add_mutually_exclusive_group()
        group.add_argument('-r',
                           '--rate',
                           metavar='N',
                           type=positive_float,
                           default=1.0,
                           help='Publishing rate in Hz (default: 1)')
        group.add_argument('-1',
                           '--once',
                           action='store_true',
                           help='Publish one message and exit')

        group.add_argument('-t',
                           '--times',
                           type=nonnegative_int,
                           default=0,
                           help='Publish this number of times and then exit')

    def main(self, *, args, addr):
        times = args.times
        if args.once:
            times = 1
        return publisher(args.topic_name, args.values, 1. / args.rate, times,
                         addr)


def publisher(topic, msg, period, times, addr):
    try:
        context = zmq.Context()
        socket: zmq.sugar.context.ST = context.socket(zmq.PUB)
        socket.connect(addr["pub"])
        time.sleep(1)

        print('publisher: beginning loop')
        count = 0
        while times == 0 or count < times:
            json_msg = json.loads(msg)
            msg2send = msgpack.dumps(json_msg)
            socket.send_multipart([str.encode(topic), msg2send])
            count += 1
            print('publishing #%d: %r\n' % (count, msg))
            if times == 0:
                time.sleep(period)
            else:
                time.sleep(1)
    except Exception as e:
        return e
    return
