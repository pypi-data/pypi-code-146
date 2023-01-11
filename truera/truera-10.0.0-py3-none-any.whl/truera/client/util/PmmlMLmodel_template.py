import datetime

import yaml


class PmmlMLmodelTemplate(yaml.YAMLObject):

    def noop(self, *args, **kw):
        pass

    yaml.emitter.Emitter.process_tag = noop

    def __init__(self, pmml_file_name, output_field):
        flavor = {"path": pmml_file_name}

        if output_field:
            flavor["predictionOutputFieldName"] = output_field

        self.flavors = {"pmml": flavor}
        self.utc_time_created = datetime.datetime.utcnow().isoformat()
