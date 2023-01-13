#!/usr/bin/env python3

import os
import argparse
from auterioncli.commands import available_commands

from auterioncli.meta_util import PersistentState, check_for_updates, get_version, eprint, get_device_serial


def main():
    persistent = PersistentState()
    selected_serial = persistent["selected_serial"]
    selected_address = persistent["selected_address"]
    have_selected_device = selected_serial is not None and selected_address is not None

    env_address = os.getenv('AUTERION_DEVICE_ADDRESS', "10.41.1.1")

    config = {
        "persistent": persistent,
        "persistent_dir": persistent.persistent_dir,
        "device_address": selected_address if have_selected_device else env_address,
        "device_serial": selected_serial if have_selected_device else None,
        "have_selected_device": have_selected_device
    }
    commands = available_commands(config)

    main_parser = argparse.ArgumentParser()
    main_parser.add_argument('--version', help='Print version of this tool', action='store_true')
    command_subparsers = main_parser.add_subparsers(title="command", metavar='<command>', dest="root_command")

    for name, command in commands.items():
        parser = command_subparsers.add_parser(name, help=command.help())
        command.setup_parser(parser)

    args = main_parser.parse_args()

    if args.version:
        print(get_version())
        exit(0)

    if args.root_command is None:
        main_parser.print_help()
        exit(1)

    check_for_updates(config["persistent"])

    # warn user if no device is selected
    if commands[args.root_command].needs_device(args):
        serial_at_address = get_device_serial(config['device_address'])
        if serial_at_address is None:
            eprint(f"Error: No device reachable at {config['device_address']}.\n"
                   f"       Use 'device discover' command to show available devices.\n"
                   f"Aborting.\n")
            exit(1)
        elif not config['have_selected_device']:
            eprint(f'Warn: No device serial selected.\n'
                  f'      Use \'device discover\' and \'device select\' commands to specify which device to use.\n'
                  f'      Falling back to device with serial {serial_at_address} on {config["device_address"]}\n')
        elif serial_at_address != config['device_serial']:
            eprint(f"Error: Device on {config['device_address']} has serial {serial_at_address}, which is different\n"
                  f"       from the selected device {config['device_serial']}. Re-select the device to interact with.\n"
                  f"Aborting.\n")
            exit(1)
    try:
        # Run command
        commands[args.root_command].run(args)
    except Exception as e:
        # Give command modules as chance to handle their exceptions
        commands[args.root_command].handle_exception(e)
    except KeyboardInterrupt:
        eprint("Aborting..")
        exit(1)

    config["persistent"].persist()


if __name__ == "__main__":
    main()
