import json
import os


class ConfigManager:
    INFRA_CONFIG = "infra_config"
    TARGET_REPO_CONFIG = "target_repo_config"
    INSTALLATION_CONFIG = "installation_config"

    __config_dir = os.path.join(os.path.expanduser("~"), ".truefoundry", "config")

    __config_file_map = {
        INFRA_CONFIG: "infra-config.json",
        INSTALLATION_CONFIG: "installation-config.json",
        TARGET_REPO_CONFIG: "target-repo-config.json",
    }

    def __init__(self) -> None:
        os.makedirs(self.__config_dir, exist_ok=True)

    def get_config(self, config_key: str) -> any:
        if config_key not in self.__config_file_map:
            raise Exception(f"Config key {config_key} not found")

        file_path = os.path.join(self.__config_dir, self.__config_file_map[config_key])
        if os.path.exists(file_path):
            with open(file_path, "r") as config:
                return json.loads(config.read())
        else:
            return None

    def save_config(self, config_key: str, config: any):
        if config_key not in self.__config_file_map:
            raise Exception(f"Config key {config_key} not found")

        file_path = os.path.join(self.__config_dir, self.__config_file_map[config_key])
        with open(file_path, "w") as config_file:
            config_file.write(json.dumps(config))
