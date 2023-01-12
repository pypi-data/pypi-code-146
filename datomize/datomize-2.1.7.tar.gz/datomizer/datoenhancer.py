import io

from datomizer import DatoMapper
from datomizer.helpers import common_helper
from datomizer.helpers.train import enhance_ml_helper, train_helper
from datomizer.utils.general import ID, MODELS, ERROR
from datomizer.utils.messages import MISSING_TARGET_TABLE
from datomizer.utils.step_types import ML_TRAIN_AND_GENERATE
from datomizer.utils.enhance_ml import Metrics, Algorithms
from datomizer.utils.enhance_ml import assert_column_valid_for_eml
from datomizer.protos.autodiscoveryservice_pb2 import TableDTO, ColumnDTO


class DatoEnhancer(object):
    dato_mapper: DatoMapper
    train_id = 0
    models = []
    metric_list = []
    algorithm_list = []
    target_table: TableDTO
    target_column: ColumnDTO

    def __init__(self, dato_mapper: DatoMapper):
        """Create DatoEnhancer object for enhancing the mapped input data for a specific prediction target.
        Args:
            dato_mapper: the DatoMapper object for the input data."""
        dato_mapper.next_step_validation()
        self.dato_mapper = dato_mapper
        self.dato_mapper.get_schema()

    @classmethod
    def restore(cls, dato_mapper: DatoMapper, train_id):
        dato_enhancer = cls(dato_mapper)
        dato_enhancer.train_id = train_id
        dato_enhancer.wait()
        return dato_enhancer

    def generate(self, target_table: str = "", target_column: str = "",
                 metric_list: [Metrics] = [], algorithm_list: [Algorithms] = [], wait=True) -> None:
        self.validate_and_set_params(target_table, target_column, metric_list, algorithm_list)

        self.train_id = enhance_ml_helper.enhance_ml_generate(self.dato_mapper,
                                                              target_table=self.target_table.name,
                                                              target_column=self.target_column.name,
                                                              metric_list=self.metric_list,
                                                              algorithm_list=self.algorithm_list)
        if wait:
            self.wait()

    def wait(self) -> None:
        """Wait until the train method returns."""
        self.restore_validation()
        status = common_helper.wait_for_step_type(datomizer=self.dato_mapper.datomizer,
                                                  business_unit_id=self.dato_mapper.business_unit_id,
                                                  project_id=self.dato_mapper.project_id,
                                                  flow_id=self.dato_mapper.flow_id,
                                                  step_type=ML_TRAIN_AND_GENERATE,
                                                  train_id=self.train_id)
        if status == ERROR:
            raise Exception("Trainer Failed")
        train = train_helper.get_train_iteration(self.dato_mapper, self.train_id)
        self.models = train[MODELS]

    def validate_and_set_params(self, target_table, target_column, metric_list, algorithm_list):
        assert target_column, MISSING_TARGET_TABLE
        self.target_table = self.dato_mapper.schema.table(target_table)
        self.target_column = self.dato_mapper.schema.column(target_table, target_column)
        assert_column_valid_for_eml(self.target_column)
        self.metric_list = metric_list
        self.algorithm_list = algorithm_list

    def get_generated_data(self, is_full: bool = False) -> None:
        self.restore_validation()

        print(common_helper.get_generated_zip(datomizer=self.dato_mapper.datomizer,
                                              business_unit_id=self.dato_mapper.business_unit_id,
                                              project_id=self.dato_mapper.project_id,
                                              flow_id=self.dato_mapper.flow_id,
                                              model_id=self.get_model_id(is_full),
                                              train_id=self.train_id))

    def get_generated_data_csv(self, table_name: str = None) -> io.StringIO:
        """Get the generated data in a csv format.
                Args:
                    table_name: the name of the generated data
                Returns:
                    StringIO object containing the generated data"""
        self.restore_validation()

        table_name = self.dato_mapper.schema.table(table_name).name

        return common_helper.get_generated_csv(datomizer=self.dato_mapper.datomizer,
                                               business_unit_id=self.dato_mapper.business_unit_id,
                                               project_id=self.dato_mapper.project_id,
                                               flow_id=self.dato_mapper.flow_id,
                                               train_id=self.train_id,
                                               model_id=self.get_model_id(),
                                               table_name=table_name)

    def get_model_id(self):
        return self.models[0][ID]

    def restore_validation(self):
        if not (self.train_id > 0):
            raise Exception("train id required for this step")

    def next_step_validation(self):
        if not (self.train_id > 0):
            raise Exception("train id required for this step")
