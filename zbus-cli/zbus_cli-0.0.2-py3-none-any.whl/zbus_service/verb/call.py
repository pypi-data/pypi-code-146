from zbus_cli.verb import VerbExtension
import zmq
import time
import json, msgpack


class CallVerb(VerbExtension):
    """Call a service."""

    def add_arguments(self, parser, cli_name):
        arg = parser.add_argument(
            'service_name',
            help="Name of the ZBUS service to call to (e.g. '/add_two_ints')")

        arg = parser.add_argument('values', help='Values to fill the message')

        parser.add_argument('--raw',
                            action='store_true',
                            help='Show raw messagge')

        parser.add_argument('--rate',
                            metavar='N',
                            type=float,
                            help='Repeat the call at a specific rate in Hz')

    def main(self, *, args, addr):
        if args.rate is not None and args.rate <= 0:
            raise RuntimeError('rate must be greater than zero')
        period = 1. / args.rate if args.rate else None
        return requester(args.service_name, args.values, period, args.raw,
                         addr)


def zbus_name_check(name: str):
    if name == "" or name == "/" or '-' in name:
        return None
    if name[0] != '/':
        name = '/' + name
    return name


def requester(service_name, values, period, raw, addr):
    service_name = zbus_name_check(service_name)
    if service_name == None:
        return "service name invalid"
    context = zmq.Context()
    socket: zmq.sugar.context.ST = context.socket(zmq.REQ)

    socket.connect(addr['client'])
    print("Connecting to server...")
    try:
        request = json.loads(values)
    except Exception as e:
        return 'the value must be key value type'
    msg2send = msgpack.dumps(request)

    while True:
        try:
            socket.send_multipart(
                [str.encode("MDPC01"),
                 str.encode(service_name), msg2send])
            #  Get the reply.
            response = socket.recv_multipart()
            if len(response) != 4:
                return "unrecognized msg receive!frame size:{} ".format(
                    len(response))
            if response[1].decode('utf8') != "MDPC01":
                return "unkown protocl"
            if response[2].decode('utf8') != service_name:
                return "service name frame size error"

            msg = msgpack.loads(response[3])
            print("------------")
            if raw == True:
                print("RAW: ", end="")
                for x in response:
                    print("0x%x" % x, end=" ")
                print()
            print("response: ", msg)
            if period == None:
                break
            time.sleep(period)
        except Exception as e:
            return e

    return
