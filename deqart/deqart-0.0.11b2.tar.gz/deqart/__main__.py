import json
import logging
import sys
from pathlib import Path

import deqart

from .exceptions import DeqartBaseException

logger = logging.getLogger("deqart-python-sdk")


def ask_token():
    config_dir = Path.home() / ".config" / "deqart"
    config_filename = "config.json"
    config_file = config_dir / config_filename
    if config_file.is_file():
        yes_no = input(f"File {config_file} exists. Do you want to overwrite? [y/n] : ")
        if yes_no != "y":
            return
    token = input("Input the SDK token deqart.com : ")
    config_dir.mkdir(exist_ok=True, parents=True)
    if config_file.is_file():
        existing_config = json.load(open(config_file))
        existing_config["token"] = token
        json.dump(existing_config, open(config_file, "w"), indent=4)
        logger.info("Configuration file %s successfully updated.", config_file)
    else:
        json.dump(
            {
                "token": token,
                "main_endpoint": "https://firebasetestserver-aclbgnvcha-uc.a.run.app",
                "ssl_verify": True,
            },
            open(config_file, "w"),
            indent=4,
        )
        logger.info("Configuration file %s successfully created.", config_file)


def main():
    available_commands = "Available commands to deqart CLI are: init version"
    if len(sys.argv) == 1:
        raise DeqartBaseException(
            0, "No command given to deqart CLI. " + available_commands
        )
    command = sys.argv[1]

    if command == "init":
        ask_token()
    elif command == "version":
        print(f"Deqart Python SDK version {deqart.__version__}")
    else:
        raise DeqartBaseException(
            0,
            "Wrong command " + command + " to deqart CLI. " + available_commands,
        )


if __name__ == "__main__":
    main()
