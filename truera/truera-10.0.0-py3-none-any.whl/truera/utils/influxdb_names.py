"""
Utility code for influx database.

NOTE(vivekb): Please keep this in sync with InfluxDbNames
"""

import re


class InfluxDbNames:

    def get_influx_datacollection_database_name(
        self, project_name, data_collection_name
    ):
        return '{0}{1}'.format(
            self.influx_safe_name(project_name),
            self.influx_safe_name(data_collection_name)
        )

    def get_influx_database_name(self, project_name, model_name):
        return '{0}{1}'.format(
            self.influx_safe_name(project_name),
            self.influx_safe_name(model_name)
        )

    def influx_safe_name(self, name):
        stripped_name = re.sub('[^A-Za-z0-9]+', '', name)
        return stripped_name
