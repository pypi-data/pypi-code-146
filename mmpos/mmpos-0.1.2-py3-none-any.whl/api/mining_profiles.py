import mmpos.api.utils as utils


def get(farm_id):
    data = utils.call_api(f"{farm_id}/miner_profiles")
    for profile in data:
        profile["farm_id"] = farm_id

    return data


def get_all(farm_ids):
    data = []
    for id in farm_ids:
        profiles = get(id)
        data.append(profiles)

    return utils.flatten(data)
