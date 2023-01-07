from zbus_cli.verb import VerbExtension
import zmq
from msgpack import dumps, loads


class EchoVerb(VerbExtension):
    """Output messages from a topic."""

    def add_arguments(self, parser, cli_name):
        arg = parser.add_argument(
            'topic_name',
            help="Name of the ZBUS topic to get type (e.g. '/chatter')")

        parser.add_argument('-r',
                            '--raw',
                            action='store_true',
                            help='Show raw messagge')

    def main(self, *, args, addr):
        try:
            context = zmq.Context()
            socket: zmq.sugar.context.ST = context.socket(zmq.SUB)
            socket.connect(addr["sub"])
            socket.subscribe(args.topic_name)

            while (1):
                message = socket.recv_multipart()
                topic = message[0].decode('utf8')
                if (topic == args.topic_name):
                    msg = loads(message[1])
                    print("------------")
                    if args.raw:
                        print("RAW: ", end="")
                        for x in message[1]:
                            print("0x%x" % x, end=" ")
                        print()
                    print(f'Received: {msg}')
        except Exception as e:
            return e
