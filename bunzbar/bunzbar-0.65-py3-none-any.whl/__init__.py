import os
import time
import argparse
import bunzbar.config


CFGFILE = os.path.join(os.path.expanduser('~'), '.config/bunzbar/config.json')


class bar:
    def __init__(self, cfgdir, config):
        self.cfgdir = cfgdir
        self.config = config

    def compose(self):
        mstr = ""
        for name in self.config.active():
            mstr += name.upper() + " "
            mstr += self.config.getf(name)
            mstr += " | "
        return mstr

    def shift(self, s, k):
        return (((s+" ")[-k-1:-1])+((s+" ")[0:-k-1]))

    def serve(self, speed=1):
        try:
            while True:
                compstr = self.compose()
                shift = round((time.time()*(1/speed)) % len(compstr))
                sstr = self.shift(compstr, shift)
                resp = os.system(f'xsetroot -name "{sstr}"')
                if resp:
                    print("exiting")
                    exit()
                print("resp:", resp)
                time.sleep(speed)
        except KeyboardInterrupt:
            exit(0)


def __main__():
    parser = argparse.ArgumentParser(
        prog='bunzbar',
        description='display information in status bar',
        epilog='stay hydrated kidz'
    )

    exclusice = parser.add_mutually_exclusive_group()
    exclusice.add_argument("-i", "--info", action="store_true")
    exclusice.add_argument("-c", "--config", action="store_true")

    parser.add_argument("-t", "--toggle", metavar="<info>",
                        type=str, nargs='+')  # For info toggles
    parser.add_argument("-s", "--set")  # For config options
    parser.add_argument("-l", "--list",
                        action="store_true")  # For info toggles or options

    parser.add_argument('-d', "--daemon", action="store_true")
    args = vars(parser.parse_args())
    c = bunzbar.config.config()
    b = bar(CFGFILE, c)

    if args["info"]:
        if args["list"]:
            print("List of available info toggles:")
            print(c.available("info"))
        if args["toggle"]:
            c.toggle(args['toggle'])
    elif args["config"]:
        if args["list"]:
            print("List of available config options:")
            print(c.available("config"))
        if args["set"]:
            print("config set")

    if args["daemon"]:
        b.serve()


if __name__ == "__main__":
    __main__()
