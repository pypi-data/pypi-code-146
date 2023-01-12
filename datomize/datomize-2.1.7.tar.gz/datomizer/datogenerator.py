import io

from datomizer import DatoTrainer
from datomizer.helpers.common_helper import get_flow, wait_for_step_type, get_generated_zip, get_generated_csv
from datomizer.helpers.generator.generator_helper import generate, assert_output_ratio
from datomizer.helpers.datasource.datasource_helper import create_target_private_datasource
from datomizer.utils.general import TARGET_DATASOURCE_ID, ERROR
from datomizer.utils.step_types import GENERATE


class DatoGenerator(object):
    dato_trainer: DatoTrainer
    synth_id = 0
    datasource_id = 0

    def __init__(self, dato_trainer: DatoTrainer):
        """Create DatoGenerator object for generating data using the trained generative model.
        Args:
            dato_trainer: the DatoTrainer object trained on the input data."""
        dato_trainer.next_step_validation()
        self.dato_trainer = dato_trainer

    @classmethod
    def restore(cls, dato_trainer: DatoTrainer, synth_id):
        dato_generator = cls(dato_trainer)
        dato_generator.synth_id = synth_id
        dato_generator.wait()
        return dato_generator

    def get_flow(self) -> dict:
        self.restore_validation()
        return get_flow(datomizer=self.dato_trainer.dato_mapper.datomizer,
                        business_unit_id=self.dato_trainer.dato_mapper.business_unit_id,
                        project_id=self.dato_trainer.dato_mapper.project_id,
                        flow_id=self.synth_id,
                        is_synth=True)

    def create_datasource(self) -> None:
        if self.datasource_id > 0:
            return
        self.datasource_id = create_target_private_datasource(self.dato_trainer.dato_mapper.datomizer)

    def generate(self, output_ratio: float = 1, wait=True) -> None:
        """Generate output data.
        Args:
            output_ratio: float represents the output ratio for generated data 0.1 - 20.0
            wait: use wait=False for asynchronous programming; True by default (awaits for the results)."""
        assert_output_ratio(output_ratio)

        self.create_datasource()
        if self.synth_id > 0:
            return
        self.synth_id = generate(self.dato_trainer, self.datasource_id, output_ratio)
        if wait:
            self.wait()

    def wait(self) -> None:
        """Wait until the generate method returns."""
        self.restore_validation()
        status = wait_for_step_type(datomizer=self.dato_trainer.dato_mapper.datomizer,
                                    business_unit_id=self.dato_trainer.dato_mapper.business_unit_id,
                                    project_id=self.dato_trainer.dato_mapper.project_id,
                                    flow_id=self.synth_id,
                                    is_synth=True,
                                    step_type=GENERATE)
        if status == ERROR:
            raise Exception("Synth Failed")
        self.datasource_id = self.get_flow()[TARGET_DATASOURCE_ID]

    def get_generated_data(self) -> None:
        self.restore_validation()
        print(get_generated_zip(datomizer=self.dato_trainer.dato_mapper.datomizer,
                                business_unit_id=self.dato_trainer.dato_mapper.business_unit_id,
                                project_id=self.dato_trainer.dato_mapper.project_id,
                                flow_id=self.synth_id))

    def get_generated_data_csv(self, table_name: str = None) -> io.StringIO:
        """Get the generated data in a csv format.
                Args:
                    table_name: the name of the generated data
                Returns:
                    StringIO object containing the generated data"""
        self.restore_validation()

        table_name = self.dato_trainer.dato_mapper.schema.table(table_name).name

        return get_generated_csv(datomizer=self.dato_trainer.dato_mapper.datomizer,
                                 business_unit_id=self.dato_trainer.dato_mapper.business_unit_id,
                                 project_id=self.dato_trainer.dato_mapper.project_id,
                                 flow_id=self.synth_id,
                                 table_name=table_name)

    def restore_validation(self):
        if not (self.synth_id > 0):
            raise Exception("synth id required for this step")
