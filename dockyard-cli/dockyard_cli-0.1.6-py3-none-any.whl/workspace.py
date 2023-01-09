import requests
from tabulate import tabulate

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def _get_workspaces(config):
    url = config.get("default","url")
    cookie = config.get("default","cookie")
    r = requests.get(url + "/api/ds/workspaces/", cookies={"_oauth2_proxy": cookie}, verify=False)
    if r.status_code == 200:
        return r.json()
    else:
        print(r.text)
    return []

def list_workspaces(config):
    data = _get_workspaces(config)
    username = config.get("default","username")
    workspaces = [["id", "name", "status", "image", "memory(GB)", "cores", "gpu", "created"]]
    for workspace in data:
        w = Struct(**workspace)
        if w.owner != username:
            continue
        workspaces.append([w.id, w.name, w.status, w.image, w.memory, w.cpu_count, w.gpu_count, w.created_at])
    print(tabulate(workspaces, headers="firstrow", tablefmt="presto"))

def start_stop_workspace(config, name, op):
    url = config.get("default","url")
    cookie = config.get("default","cookie")
    data = _get_workspaces(config)
    workspace_exists = False
    for workspace in data:
        w = Struct(**workspace)
        if w.name == name :
            workspace_exists = True
            if op == "stop":
                print(f"stopping {w.name} ...", end="")
            else:
                print(f"starting {w.name} ...", end="")

            r = requests.post(url + f"/api/ds/workspaces/{w.id}/{op}", cookies={"_oauth2_proxy": cookie}, verify=False)
            if r.status_code == 200:
                print("done")
            else:
                print(r.text)
    if not workspace_exists: 
        print(f"Workspace {name} doesn't exist")