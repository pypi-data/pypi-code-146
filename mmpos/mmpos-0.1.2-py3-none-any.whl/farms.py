import mmpos.api.utils as utils

def list():
  farms = utils.call_api('/farms', {}, {})
  return list(map(lambda x: x, farms))

def farms():
  return list()

def show(farm_id):
  pass


def default_farm():
    return farms()[0]
