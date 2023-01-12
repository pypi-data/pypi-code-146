#!/usr/bin/env python3

import json

def is_identical(fpath_1: str, fpath_2: str) -> bool:
    file_contents = []
    for i, fpath in enumerate([fpath_1, fpath_2]):
        try:
            with open(fpath, "rb") as f:
                file_contents.append(f.read())
        except FileNotFoundError:
            print(f"Could not find file {fpath}")
        except UnicodeError:
            print(f"Unicode error while trying to read {fpath}")
        except:
            print(f"Could not read file {fpath}")

    if len(file_contents) == 2:
        return file_contents[0] == file_contents[1]
    return False


def load_json(fpath: str) -> dict:
    with open(fpath, "r") as f:
        data = json.load(f)
    return data