import datetime

import yaml


class MLeapMLmodelTemplate(yaml.YAMLObject):

    def noop(self, *args, **kw):
        pass

    yaml.emitter.Emitter.process_tag = noop

    def __init__(self, version):
        flavor = {"mleap_version": version, "model_data": "mleap/model"}

        self.flavors = {"mleap": flavor}
        self.utc_time_created = datetime.datetime.utcnow().isoformat()
