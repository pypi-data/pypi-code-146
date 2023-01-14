import mmpos.api.utils as utils
import threading
import mmpos.api.farms as farms

rig_name_table = {}


def get(farm_id):
    list = []
    if farm_id == "all":
        for farm in farms.farms():
            list.append(rigs(farm["id"]))
        return utils.flatten(list)
    else:
        list = rigs(farm_id)

    return list


def show(rig_id):
    pass


def all_rigs():
    all_rigs = []
    for farm in farms.farms():
        all_rigs.append(rigs(farm["id"]))
    return utils.flatten(all_rigs)


def rig_name_list(refresh=False):
    if len(rig_name_table) < 1 or refresh:
        for rig in all_rigs():
            rig_name_table[rig["id"]] = rig["name"]

    return rig_name_table

def get_rig(farm_id, rig_id):
    data = utils.call_api(f"{farm_id}/rigs/{rig_id}")
   
    return data

def rigs(farm_id):
    rigs = utils.call_api(f"{farm_id}/rigs")
    list = []
    for rig in rigs:
        list.append(rig)
    return list


def set_rig_control(action, farm_id, rig_id, simulate=False, block=None):
    if not simulate:
        utils.call_api(
            f"{farm_id}/rigs/{rig_id}/control", {}, {"control": action}, method="POST"
        )
    else:
        action = f"simulated-{action}"
    if block:
        rig_name = rig_name_list()[rig_id]
        block(rig_name, f"{action}")
    return True


def add_mining_profiles(farm_id, rig_id, mining_profile_id):
    pass


def set_mining_profiles(
    farm_id, rig_id, mining_profile_ids, simulate, block=lambda x, y: {}
):
    data = {"miner_profiles": [mining_profile_ids]}
    path = f"{farm_id}/rigs/{rig_id}/miner_profiles"
    action = "set mining profile"
    rig_name = rig_name_list()[rig_id]

    if simulate:
        out = f"simulated-{action}"
        resp = get_rig(farm_id, rig_id)
    else:
        resp = utils.call_api(path=path, params={}, data=data, method="POST")
        if "code" in resp:
            raise Exception(resp)
        else:
            out = action

    block(rig_name, out)
    return resp


def rig_control(action, rig_id, farm_id, simulate=False, block=None):
    if rig_id == "all":
        threads = []
        for rig in rigs(farm_id):
            x = threading.Thread(
                target=set_rig_control,
                args=(action.lower(), farm_id, rig["id"]),
                kwargs={"simulate": simulate, "block": block},
            )
            if utils.current_thread_count(threads) > utils.MAX_THREAD_COUNT:
                threads.pop(0).join()  # wait for the first thread to finish

            x.start()
            threads.append(x)
    else:
        set_rig_control(action.lower(), farm_id, rig_id, simulate=simulate, block=block)

    return
