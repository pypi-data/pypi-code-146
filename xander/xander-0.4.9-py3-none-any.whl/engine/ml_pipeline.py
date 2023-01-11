import logging

from xander.engine.base import BasePipeline
from xander.engine.ml_component import MLComponent, MLTrainerComponent
from xander.engine.standard_functions import xander_ingestion, xander_encoder, xander_splitter, \
    xander_feature_selection, xander_model_training, xander_model_evaluator
from xander.utils.utility import get_slug


class MLPipeline(BasePipeline):
    """
    This is a ML dedicated pipeline. It provides specific features for ML models.
    It manages the versioning of the input configuration files and also the output metrics.
    """

    def __init__(self, name, storage_manager, client, model, input_file_name, target_name, pipeline_configuration=None):
        # Initialize the super class
        super().__init__(name=name, storage_manager=storage_manager, client=client)

        # Input file name
        self.input_file_name = input_file_name

        # Model to be trained
        self.model = model

        # Name of target columns name
        self.target_name = target_name

        # Configuration of the pipeline
        self.pipeline_configuration = pipeline_configuration if pipeline_configuration else {}

        # Set standard ingestion component
        self.set_ingestion()
        # self.set_encoding()
        # self.set_split()
        # self.set_feature_selection()
        self.set_model_trainer()
        # self.set_evaluator()

    def link_component(self, name, function, custom_function, function_params, active=True, return_output=None,
                       save_output=True):
        """
        Link a new component to the ML pipeline.

        @param name:
        @param function:
        @param custom_function:
        @param function_params:
        @param active:
        @param return_output:
        @param save_output:
        @return:
        """

        # Compute the slug
        slug = get_slug(name)

        self.components[slug] = MLComponent(pipeline_slug=self.pipeline_slug,
                                            slug=slug,
                                            function=function,
                                            custom_function=custom_function,
                                            function_params=function_params,
                                            pipeline_configuration=self.pipeline_configuration,
                                            storage_manager=self.storage_manager,
                                            active=active,
                                            return_output=return_output,
                                            save_output=save_output)

        logging.debug('ML Pipeline {} -> new ML component added.'.format(self.pipeline_slug))
        return True

    def link_model_trainer(self, name, function, model, validation_function, test_function, function_params,
                           active=True, return_output=None, save_output=True):
        # Compute the slug
        slug = get_slug(name)

        self.components[slug] = MLTrainerComponent(pipeline_slug=self.pipeline_slug,
                                                   slug=slug,
                                                   function=function,
                                                   model=model,
                                                   validation_function=validation_function,
                                                   test_function=test_function,
                                                   function_params=function_params,
                                                   pipeline_configuration=self.pipeline_configuration,
                                                   storage_manager=self.storage_manager,
                                                   active=active,
                                                   return_output=return_output,
                                                   save_output=save_output)

        logging.debug('ML Pipeline {} -> new ML Trainer component added.'.format(self.pipeline_slug))
        return True

    def set_ingestion(self, ingestion_function=None):
        """
        Set the component responsible for the ingestion.

        @param ingestion_function: custom ingestion function
        @return: True
        """

        function_params = [
            ('file', self.input_file_name)
        ]

        # Link the component to the pipeline
        self.link_component(name='ingestor', function=xander_ingestion, custom_function=ingestion_function,
                            function_params=function_params)

        return True

    def set_encoding(self, encoding_function=None):
        """
        Set the component responsible for the encoding.

        @param encoding_function: custom encoding function
        @return: True
        """

        # Link the component to the pipeline
        self.link_component(name='encoder', function=xander_encoder, custom_function=encoding_function,
                            function_params=[])

        return True

    def set_split(self, split_function=None):
        """
        Set the component responsible for the splitting the dataset in train and test set.

        @param split_function: custom splitting function
        @return: True
        """

        # Link the component to the pipeline
        self.link_component(name='splitter', function=xander_splitter, custom_function=split_function,
                            function_params=[])

        return True

    def set_feature_selection(self, feature_selection_function=None):
        """
        Set the component responsible for the feature selection.

        @param feature_selection_function: custom feature selection function
        @return: True
        """

        # Link the component to the pipeline
        self.link_component(name='feature_selector', function=xander_feature_selection,
                            custom_function=feature_selection_function, function_params=[])

        return True

    def set_model_trainer(self, validation=None, test=None):
        # Link the component to the pipeline
        self.link_component(name='model_training', function=xander_model_training, custom_function=validation,
                            function_params=[])

        return True

    def set_evaluator(self, lime=None):
        """
        Set the component responsible for the feature selection.

        @return: True
        """

        # Link the component to the pipeline
        self.link_component(name='results_aggregation', function=xander_model_evaluator, function_params=[],
                            return_output=True, save_output=False)

        return True
