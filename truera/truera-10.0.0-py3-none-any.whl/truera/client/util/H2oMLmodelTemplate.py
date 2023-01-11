import datetime

import yaml


class H2oMLmodelTemplate(yaml.YAMLObject):

    def noop(self, *args, **kw):
        pass

    yaml.emitter.Emitter.process_tag = noop

    def __init__(self, zip_file_name):
        flavor = {"category_name": "Binomial", "model_zip": zip_file_name}

        self.flavors = {"h2o_mojo": flavor}
        self.utc_time_created = datetime.datetime.utcnow().isoformat()
