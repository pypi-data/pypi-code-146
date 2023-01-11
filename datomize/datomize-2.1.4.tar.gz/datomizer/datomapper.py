import tempfile
from pathlib import Path
from datomizer import Datomizer
from datomizer.helpers.datasource.datasource_helper import create_origin_private_datasource_from_path, save_df_to_csv, validate_data_size_limits
from datomizer.helpers.common_helper import get_flow, wait_for_step_type
from datomizer.helpers.business_unit_project.business_unit_project_helper import get_default_business_unit_project
from datomizer.helpers.autodiscovery.autodiscovery_helper import discover, get_schema_discovery, put_schema_discovery
from datomizer.helpers.wrapper.schema_wrapper import SchemaWrapper
from datomizer.utils.general import ORIGIN_DATASOURCE_ID, ERROR
from datomizer.utils.step_types import COLUMN_DISCOVERY


class DatoMapper(object):
    datomizer: Datomizer
    business_unit_id = 0
    project_id = 0
    datasource_id = 0
    flow_id = 0
    schema: SchemaWrapper = None

    def __init__(self, datomizer: Datomizer):
        """Create DatoMapper object for extracting the structure of the input data.
        Args:
            datomizer: the Datomizer authentication object."""
        datomizer.next_step_validation()
        self.datomizer = datomizer
        self.business_unit_id, self.project_id = get_default_business_unit_project(self.datomizer)

    @classmethod
    def restore(cls, datomizer: Datomizer, flow_id):
        dato_mapper = cls(datomizer)
        dato_mapper.flow_id = flow_id
        dato_mapper.wait()
        return dato_mapper

    def get_flow(self) -> dict:
        self.restore_validation()
        return get_flow(self.datomizer, self.business_unit_id, self.project_id, self.flow_id)

    def create_datasource(self, path, df_map, delimiter):
        self.set_datasource_validation()
        with tempfile.TemporaryDirectory() as temp_dir:
            if df_map is not None:
                save_df_to_csv(df_map, temp_dir)
                path = temp_dir
            validate_data_size_limits(path, delimiter)
            self.datasource_id = create_origin_private_datasource_from_path(self.datomizer, path)

    def discover(self, path=None, df_map=None, sample_percent: int = 1, title: str = "sdk_flow",
                 wait=True, delimiter: str = ',') -> None:
        """Extract the structure of the input data.
        Args:
            path: full path for the input data
            df_map: a map of {"table1": df1, "table2": df2} containing the input data
            sample_percent: the sampling ratio; 1 (100%) by default.
            title: the name of the created task in Datomize; "sdk_flow" by default.
            wait: use wait=False for asynchronous programming; True by default (awaits for the results).
            delimiter: default "," used for number of columns validation"""
        self.create_datasource(path, df_map, delimiter)

        self.pre_run_validation()
        self.flow_id = discover(self.datomizer,
                                self.business_unit_id, self.project_id, self.datasource_id,
                                sample_percent, title)
        if wait:
            self.wait()

    def wait(self) -> None:
        """Wait until the discovery method returns."""
        self.restore_validation()
        status = wait_for_step_type(datomizer=self.datomizer,
                                    business_unit_id=self.business_unit_id,
                                    project_id=self.project_id,
                                    flow_id=self.flow_id,
                                    step_type=COLUMN_DISCOVERY)
        if status == ERROR:
            raise Exception("Auto Discovery Failed")
        self.datasource_id = self.get_flow()[ORIGIN_DATASOURCE_ID]
        self.get_schema()

    def get_schema(self) -> SchemaWrapper:
        """Get a data mapping object for the input data.
        Returns:
            Datomize mapping dictionary"""
        self.restore_validation()
        self.schema = SchemaWrapper(get_schema_discovery(self.datomizer,
                                                         self.business_unit_id, self.project_id, self.flow_id))
        return self.schema

    def set_schema(self) -> SchemaWrapper:
        """Set a data mapping object for the input data.
        Returns:
            Datomize mapping dictionary"""
        self.restore_validation()
        self.schema = SchemaWrapper(put_schema_discovery(self.datomizer,
                                                         self.business_unit_id, self.project_id, self.flow_id,
                                                         self.schema.schema))
        return self.schema

    def base_validation(self):
        assert (self.business_unit_id > 0 and self.project_id > 0), "missing base properties"

    def set_datasource_validation(self):
        self.base_validation()
        assert self.datasource_id == 0, "datasource id cannot be mutated"

    def pre_run_validation(self):
        self.base_validation()
        assert self.datasource_id > 0, "datasource id required for this step"

    def restore_validation(self):
        self.base_validation()
        assert self.flow_id > 0, "flow id required for this step"

    def next_step_validation(self):
        self.restore_validation()
        assert self.schema, "DatoMapper not ready"
