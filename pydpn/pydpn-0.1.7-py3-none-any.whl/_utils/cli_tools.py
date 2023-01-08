import os, json

def check_config()->dict:
    usrdir = os.path.expanduser("~")
    configFile = os.path.join(usrdir, r".dpn/config.json")
    if os.path.isfile(configFile):
        return json.load(open(configFile, "r"))

    else:

        print(f'There is no "config.json" file at "{os.path.split(configFile)[0]}"')
        return None