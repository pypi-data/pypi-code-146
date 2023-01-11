#!/usr/bin/env python

import argparse
import importlib
import sys
import yaml

from .stores import StoreInterface
from .contexts.aws_assume_role import aws_assume_role

try:
    config = yaml.load(open(".secenv.yaml", "r"), Loader=yaml.Loader)
    if not config:
        config = yaml.load(open(".secenv.yml", "r"), Loader=yaml.Loader)
except FileNotFoundError:
    print("Config error: .secenv.yaml not found")
    sys.exit(0)


def parse_args(stores):
    parser = argparse.ArgumentParser()
    subparsers_group = parser.add_subparsers()
    subparsers = {}

    subparsers["contexts"] = subparsers_group.add_parser(
        "contexts", help="list available contexts"
    )

    subparsers["context"] = subparsers_group.add_parser(
        "context", help="generate an environment based on a context"
    )
    subparsers["context"].add_argument("context")

    for store in stores:
        type = config["stores"][store]["type"]
        subparsers[store] = subparsers_group.add_parser(
            store,
            help=f"query store '{store}' of type '{type}'",
        )
        stores[store].gen_parser(subparsers[store])

    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    return parser.parse_args()


def find_stores() -> dict[str, StoreInterface]:
    stores = {}

    for name in config["stores"]:
        infos = config["stores"][name]
        try:
            store = importlib.import_module(
                f".stores.{infos['type']}", package="secenv"
            )
        except ModuleNotFoundError:
            print(f"Config error: no store defined as '{infos['type']}'")
            sys.exit(1)
        stores[name] = store.Store(name, infos)

    return stores


def gen_environment(context, stores):
    context_config = config["contexts"][context]
    output = []

    if "vars" in context_config:
        for key, value in context_config["vars"].items():
            if type(value) == str:
                # raw value
                output.append(f"export {key}={value}")
            else:
                # get from secrets
                store = value["store"]
                if store not in stores:
                    print(f"Config error: store '{store}' not found in config")
                    sys.exit(1)

                value = {k: v for k, v in value.items() if k != "store" and v}
                res = stores[store].read_secret(**value)
                output.append(f"export {key}={res}")

    if "aws_assume_role" in context_config:
        creds = {}
        creds["key_id"] = context_config["aws_assume_role"]["aws_access_key_id"]
        creds["secret_key"] = context_config["aws_assume_role"]["aws_secret_access_key"]
        creds["role"] = context_config["aws_assume_role"]["role_arn"]

        for k, v in creds.items():
            # raw values are passed directly
            if type(v) == str:
                continue
            # and values from stores are computed first
            args = {k2: v2 for k2, v2 in v.items() if k2 != "store" and v2}
            creds[k] = stores[v["type"]].read_secret(**args)

        try:
            key_id, secret_key, token = aws_assume_role(
                creds["key_id"], creds["secret_key"], creds["role"]
            )
            output.append(f"export AWS_ACCESS_KEY_ID={key_id}")
            output.append(f"export AWS_SECRET_ACCESS_KEY={secret_key}")
            output.append(f"export AWS_SESSION_TOKEN={token}")
        except:
            print(f"AWS error: couldn't assume role '{creds['role']}', skipping")
            sys.exit(1)

    return "\n".join(output)


def main():
    stores = find_stores()
    args = parse_args(stores)

    # remove empty values and 'type' key
    args = {k: v for k, v in vars(args).items() if k != "type" and v}

    if "context" in sys.argv[1]:
        if sys.argv[1].endswith("s"):
            # list available contexts
            if "contexts" in config:
                print("\n".join(config["contexts"]))
                return
        else:
            # generate an environment from a context
            context = sys.argv[2]
            if "contexts" not in config or context not in config["contexts"]:
                print(f"Config error: context '{context}' not found")
                sys.exit(1)
            env = gen_environment(context, stores)
            print(env)
            return
        pass

    else:  # retrieving a specific secret
        store = stores[sys.argv[1]]
        result = store.read_secret(**args)
        print(result)
        return


if __name__ == "__main__":
    main()
