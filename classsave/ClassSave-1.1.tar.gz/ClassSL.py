import pickle
import os
import json
import copy

__version__ = '1.1'


class ClassSL:

    def __init__(self, class_path: str = None, rewrite_dict: bool = True, load: bool = True,
                 save_json: bool = False, json_private=True):
        self.__class_path = class_path if class_path is not None else f"classes/{self.__class__.__name__}.pkl"
        self.__rewrite_dict = rewrite_dict
        self.__load = load
        self._loaded = False
        self.__save_json = save_json
        self.__json_private = json_private

        self.load_class()

    def load_class(self):
        if self.__load and self.__class_path is not None and os.path.exists(self.__class_path):
            with open(self.__class_path, "rb") as f:
                loaded_class = pickle.load(f)
                loaded_dict = loaded_class.__dict__
                if self.__rewrite_dict:
                    self.__dict__ = loaded_dict
                else:
                    self.__dict__.update(loaded_dict)

            self._loaded = True
        return self._loaded

    def toDict(self):
        return self.__dict__

    def save_class(self):
        directory = os.path.dirname(self.__class_path)
        os.makedirs(directory, exist_ok=True)
        with open(self.__class_path, "wb") as f:
            pickle.dump(self, f)
        try:
            if self.__save_json:
                with open(os.path.splitext(self.__class_path)[0] + '.json', "w") as f:
                    save_dict = self.toDict()
                    if not self.__json_private:  # Remove private variables
                        save_dict_temp = copy.deepcopy(save_dict)
                        for key, value in save_dict.items():
                            if key.startswith("_"):
                                del save_dict_temp[key]
                        save_dict = save_dict_temp  # Replacing dictionary
                    json.dump(save_dict, f, indent=4)
        except Exception as e:
            print(str(e))
