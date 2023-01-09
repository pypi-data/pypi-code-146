import json

import questionary


class DictQuestionaire:
    def __init__(self, obj: dict) -> None:
        self.obj = obj

    def __confirm_val(self, v, tree_path, custom_handlers={}):
        if tree_path in custom_handlers:
            if not custom_handlers[tree_path]():
                return

        if v == None:
            v = questionary.text(f"Please Enter {tree_path} : ").ask()
        else:
            v = questionary.text(f"Please Enter {tree_path} : ", default=str(v)).ask()
        return v

    def __confirm_list_val(self, v, tree_path, custom_handlers={}):
        if tree_path in custom_handlers:
            if not custom_handlers[tree_path]():
                return

        temp_v = questionary.text(f"Please Enter {tree_path} : ", default=str(v)).ask()
        temp_v = str(temp_v).replace("'", '"')
        v = json.loads(temp_v)
        return v

    # TODO: add unit test for get_all_values function
    def __get_all_values(self, dicts, tree_path="", custom_handlers={}):
        if tree_path in custom_handlers:
            if not custom_handlers[tree_path]():
                return None
        if tree_path != "":
            tree_path += "."

        for k, v in dicts.items():
            if isinstance(v, dict):
                dicts[k] = self.__get_all_values(v, tree_path + k, custom_handlers)
            elif isinstance(v, list):
                if len(v) != 0 and isinstance(v[0], dict):
                    for i, vi in enumerate(v):
                        self.__get_all_values(
                            vi, tree_path + k + "[" + i + "]", custom_handlers
                        )
                else:
                    dicts[k] = self.__confirm_list_val(
                        v, tree_path + k, custom_handlers
                    )
            else:
                dicts[k] = self.__confirm_val(v, tree_path + k, custom_handlers)
        return dicts

    def ask(self, custom_handlers={}):
        return self.__get_all_values(self.obj, custom_handlers=custom_handlers)
