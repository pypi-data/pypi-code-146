import io

from datomizer import DatoMapper
from datomizer.helpers.common_helper import wait_for_step_type, get_generated_zip, get_generated_csv
from datomizer.helpers.train.train_helper import train, get_train_iteration, get_evaluation
from datomizer.helpers.wrapper.evaluation_wrapper import EvaluationWrapper
from datomizer.utils.general import ID, MODELS, ERROR
from datomizer.utils.step_types import TRAIN_AND_GENERATE


class DatoTrainer(object):
    dato_mapper: DatoMapper
    train_id = 0
    model_id = 0

    def __init__(self, dato_mapper: DatoMapper):
        """Create DatoTrainer object for training a generative model for the mapped input data.
        Args:
            dato_mapper: the DatoMapper object for the input data."""
        dato_mapper.next_step_validation()
        self.dato_mapper = dato_mapper
        self.dato_mapper.get_schema()

    @classmethod
    def restore(cls, dato_mapper: DatoMapper, train_id):
        dato_trainer = cls(dato_mapper)
        dato_trainer.train_id = train_id
        dato_trainer.wait()
        return dato_trainer

    def train(self, epochs_gan=500, epochs_vae=300, wait=True) -> None:
        """Train a generative model.
        Args:
            epochs_gan: number of epochs for gan model
            epochs_vae: number of epochs for vae model
            wait: use wait=False for asynchronous programming; True by default (awaits for the results)."""
        if self.train_id > 0:
            return
        self.train_id = train(self.dato_mapper, epochs_gan, epochs_vae)
        if wait:
            self.wait()

    def wait(self) -> None:
        """Wait until the train method returns."""
        self.restore_validation()
        status = wait_for_step_type(datomizer=self.dato_mapper.datomizer,
                                    business_unit_id=self.dato_mapper.business_unit_id,
                                    project_id=self.dato_mapper.project_id,
                                    flow_id=self.dato_mapper.flow_id,
                                    step_type=TRAIN_AND_GENERATE,
                                    train_id=self.train_id)
        if status == ERROR:
            raise Exception("Trainer Failed")
        self.model_id = get_train_iteration(self.dato_mapper, self.train_id)[MODELS][0][ID]

    def get_generated_data(self) -> None:
        self.next_step_validation()
        print(get_generated_zip(datomizer=self.dato_mapper.datomizer,
                                business_unit_id=self.dato_mapper.business_unit_id,
                                project_id=self.dato_mapper.project_id,
                                flow_id=self.dato_mapper.flow_id,
                                train_id=self.train_id,
                                model_id=self.model_id))

    def get_generated_data_csv(self, table_name: str = None) -> io.StringIO:
        """Get the generated data in a csv format.
                Args:
                    table_name: the name of the generated data
                Returns:
                    StringIO object containing the generated data"""
        self.next_step_validation()

        table_name = self.dato_mapper.schema.table(table_name).name

        return get_generated_csv(datomizer=self.dato_mapper.datomizer,
                                 business_unit_id=self.dato_mapper.business_unit_id,
                                 project_id=self.dato_mapper.project_id,
                                 flow_id=self.dato_mapper.flow_id,
                                 train_id=self.train_id,
                                 model_id=self.model_id,
                                 table_name=table_name)

    def get_evaluation(self) -> EvaluationWrapper:
        self.next_step_validation()
        return get_evaluation(dato_mapper=self.dato_mapper, model_id=self.model_id)

    def restore_validation(self):
        if not (self.train_id > 0):
            raise Exception("flow id required for this step")

    def next_step_validation(self):
        self.restore_validation()
        if not (self.model_id > 0):
            raise Exception("DatoTrainer not ready")
