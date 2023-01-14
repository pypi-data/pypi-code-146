import mmpos.api.utils as utils


def get():
    farms = utils.call_api("/farms", {}, {})
    return list(map(lambda x: x, farms))


def farm_ids():
    return list(map(lambda x: x["id"], get()))


def farms():
    return get()


def show(farm_id):
    pass


def default_farm():
    return farms()[0]
