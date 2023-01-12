import argparse
from pyhocon import ConfigFactory
import importlib.resources

def parse_args():
    parser = argparse.ArgumentParser(description='Spark Application')
    parser.add_argument(
        '-C',
        '--config',
        nargs='+',
        help=(
            'Property of the config that needs to be overridden. Set a number of key-value '
            'pairs(do not put spaces before or after the = sign). Ex: -C fabricName=dev '
            'dbConnection="db.prophecy.io" dbUserName="prophecy"'
        )
    )
    parser.add_argument('-f', '--file', help='Location of the hocon config file. Ex: -f /opt/prophecy/dev.json')
    parser.add_argument('-i', '--confInstance', help='Config instance name present in config directory. Ex.: -i default')
    args = parser.parse_args()

    return args


def parse_config(args):
    if args.file is not None:
        conf = ConfigFactory.parse_file(args.file)
    elif args.confInstance is not None:
        with importlib.resources.open_text("prophecy_config_instances", "{instance}.json".format(instance=args.confInstance)) as file:
            data = file.read()
            conf = ConfigFactory.parse_string(data)
    else:
        conf = ConfigFactory.parse_string('{}')

    # override the file config with explicit value passed
    if args.config is not None:
        for config in args.config:
            c = config.split('=', 1)
            conf.put(c[0], c[1])

    return conf
