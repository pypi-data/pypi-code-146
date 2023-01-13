import os
import json

BASE_PATH = "secrets/"


class ConfigHandler:
    def __init__(self, name):
        self.name = name
        self.load_config()

    def load_config(self):

        with open(f"{BASE_PATH}{self.name}.json") as f:
            config = json.load(f)
            self.__dict__.update(config)


if __name__ == "__main__":
    names = [f.split(".")[0] for f in os.listdir(BASE_PATH)]
    print(f"Found configs for:\n\t{', '.join(names)}")
    configs = {n: ConfigHandler(n) for n in names}
    print(configs["influx"].URL)
