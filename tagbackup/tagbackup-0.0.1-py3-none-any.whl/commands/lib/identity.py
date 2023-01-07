from appdirs import user_config_dir
import machineid
from pathlib import Path
import yaml


def get_config_path():
    return Path(user_config_dir()) / "tagbackup.yaml"


def get_device_id():
    try:
        with open(get_config_path(), "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        device_id = config.get("device", "")
        if len(device_id) == 36:
            return device_id
    except:
        pass

    return None


def set_device_id(device_id):
    try:
        with open(get_config_path(), "w") as file:
            yaml.dump({"device": str(device_id)}, file)

        return True
    except:
        pass

    return False


def get_machine_id():
    return machineid.hashed_id("tagbackup")
