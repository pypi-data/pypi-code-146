#######################
#   Lainupcomputer    #
#   ez_config v1.3.1    #
#######################
import json
import logging


logger = logging.getLogger()
_version = "1.3.1"


class Ez_Storage:
    def __init__(self, file_path=str("config")):
        self.enable_debug = True
        self.enable_logging = True
        self.storage_prefix = "ez_storage"
        self.on_file_creation_placeholder = "{\n\n}"
        self.internal_config = None

        self.filepath = file_path
        if self.check_file() == "data createddata found":
            self.restore_storage("b")

    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as f:
            file = json.load(f)
        return file

    @staticmethod
    def save(file_path, file):
        with open(file_path, "w") as f:
            json.dump(file, f, indent=2)

    def make_response(self, level, response):
        if self.enable_logging:
            logger.log(level, response)
        elif self.enable_debug:
            print(f"LEVEL:{level},msg:{response}")
        else:
            pass

    def check_file(self):
        file_found = False
        result = ""
        while not file_found:
            try:
                self.read_file(self.filepath)
                result += "data found"
                file_found = True

            except FileNotFoundError:
                with open(self.filepath, "w") as f:
                    f.write(self.on_file_creation_placeholder)
                    result += "data created"
                    file_found = False

        self.make_response(logging.INFO, f"[{self.storage_prefix}]:{result}")
        return result

    def add_storage(self, mode=str(), obj=None, data=None, value=None, array_data=None, override=False):
        if mode == "o":
            file = self.read_file(self.filepath)
            try:
                if override:
                    file[obj][data] = value
                    result = f"{obj}, {data}, {value} override"
                else:
                    result = f"{obj}, {data}, {value} override protected"
            except KeyError:
                file[obj] = {}
                file[obj][data] = value
                result = f"'{obj}, {data}, {value}' added as object"

            self.save(self.filepath, file)

        elif mode == "a":
            file = self.read_file(self.filepath)
            try:
                if override:
                    file[obj] = []
                    file[obj].append(array_data)
                    result = f"{obj}, {array_data} override"
                else:
                    file[obj].append(array_data)
                    result = f"{obj}, {array_data} appended"
            except KeyError:
                file[obj] = []
                file[obj].append(array_data)
                result = f"'{obj}, {array_data}' added as array"

            self.save(self.filepath, file)

        elif mode == "l":
            file = self.read_file(self.filepath)
            try:
                if override:
                    file[obj].clear()
                    for x in data:
                        file[obj].append(x)
                    result = f"{obj}, {data} override"
                else:
                    for x in data:
                        file[obj].append(x)
                    result = f"{obj}, {data} appended"
            except KeyError:
                file[obj] = []
                for x in data:
                    file[obj].append(x)
                result = f"'{obj}, {data}' added as list"

            self.save(self.filepath, file)

        else:
            result = f"Error: No defined for: mode'{mode}'"

        self.make_response(logging.INFO, f"[{self.storage_prefix}]:{result}")

    def get_storage(self, mode=str(), obj=None, data=None):
        file = self.read_file(self.filepath)
        if mode == "o":
            try:
                r_data = file[obj][data]
                self.make_response(logging.INFO, f"[{self.storage_prefix}]:get {obj} @ {data} in object mode: Success")
            except KeyError:
                r_data = None
                self.make_response(logging.INFO, f"[{self.storage_prefix}]:get {obj} @ {data} in object mode: KeyError")

            return r_data

        elif mode == "a":
            objects = []
            for file_obj in file[obj]:
                objects.append(file_obj)
            self.make_response(logging.INFO, f"[{self.storage_prefix}]:get {obj} in array mode: Success")
            return objects

        elif mode == "l":
            objects = []
            for file_obj in file[obj]:
                objects.append(file_obj)
            self.make_response(logging.INFO, f"[{self.storage_prefix}]:get {obj} in list mode: Success")
            return objects

        else:
            self.make_response(logging.INFO, f"[{self.storage_prefix}]:Error: No defined for: mode'{mode}'")

    def restore_storage(self, source=None, destination=None, mode=None):
        action_pass = False
        result = ""
        file = {"ez_storage": {}}
        file["ez_storage"]["version"] = _version

        if source == "b":
            result = " restored storage form source 'b': Success"
            action_pass = True

        elif source == "i":
            if mode == "o":
                file[destination] = {}
                for obj, val in self.internal_config:
                    file[destination][obj] = val
                result = " restored storage form source 'i', mode'o': Success"
                action_pass = True

            elif mode == "a":
                file[destination] = []
                file[destination].append(self.internal_config)
                result = " restored storage form source 'i', mode'a': Success"
                action_pass = True

            elif mode == "l":
                file[destination] = []
                for x in self.internal_config:
                    file[destination].append(x)
                result = " restored storage form source 'i', mode'l': Success"
                action_pass = True

            else:
                result = f"Error: No defined mode for: source 'i', mode'{mode}'"

        if action_pass:
            self.save(self.filepath, file)

        self.make_response(logging.INFO, f"[{self.storage_prefix}]:{result}")


class ez_config:

    def edit(self, cfg="Configuration", data=str(), value=str()):  # edit in settings
        try:
            file = self.read_file(self.file_path)
            file[str(cfg)][data] = value
            save(self.file_path, file)

        except KeyError:
            print(f"{value} for {cfg}>{data} Not Found")

    def add(self, cfg="Configuration", data=str()):  # Add Data to settings
        file = read_file(self.file_path)
        file[str(cfg)] = {}

        for entry in data.split("#"):
            split_value = entry.split(":")
            file[str(cfg)][str(split_value[0])] = split_value[1]

        save(self.file_path, file)
        print(f"added {cfg}>{data}")



