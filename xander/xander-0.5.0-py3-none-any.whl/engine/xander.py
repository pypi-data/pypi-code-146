import json
import logging
import os
import importlib

from xander.utils.utility import now, get_time, elapsed
from dotenv import load_dotenv

from xander.client.client import XanderClient, START_TIME, END_TIME, DURATION, PIPELINES, RUN_ID, HOSTNAME, VERSION
from xander.engine.pipeline import Pipeline
from xander.engine.storage_manager import StorageManager

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'), verbose=True)


class XanderEngine:
    """
    The core of ML OPS tool.
    It is the object to be initialized by the user.
    """

    def __init__(self, logger=None):
        """
        Class constructor.
        """

        # Load the file with the project structure
        path = os.path.join(os.getcwd(), os.getenv('XANDER_PROJECT_FILE'))
        self.project_structure = json.load(open(path, 'r'))

        # Load the file with the project configuration
        path = os.path.join(os.getcwd(), os.getenv('XANDER_CONFIGURATION_FILE'))
        self.configuration = json.load(open(path, 'r'))

        # Initialize the client. During the initialization the client connects to server.
        self.client = XanderClient(local_mode=self.configuration['server']['local_mode'])

        # Execution info
        self.execution = {
            VERSION: None,
            RUN_ID: None,
            START_TIME: None,
            END_TIME: None,
            DURATION: 0,
            PIPELINES: 0
        }

        # Initialize the pipelines list
        self.pipelines = {}

        self.logger = logging if logger is None else logger

        # Initialize the storage manager
        self.storage_manager = StorageManager(configuration=self.configuration, logger=self.logger)

        # When all components are loaded and ready, Xander read the project structure configuration file and configure
        # the Engine
        self.setup()

        self.logger.warning('Xander ML Engine is ready.')

    def instance_new_run(self):
        """
        Environment setup of the current run.
        """

        # Update the start time of the current run
        self.execution[START_TIME] = now()

        # Call the server and updates it update the run
        run_id, version = self.client.start_new_run(self.execution)

        # Configure the storage manager for the current run
        self.execution[VERSION], self.execution[RUN_ID] = self.storage_manager.configure(version=version, run_id=run_id)

        self.logger.debug(f'Current version: {self.execution[VERSION]}')
        self.logger.debug(f'Current run ID: {self.execution[RUN_ID]}')

    def setup(self):
        """
        Read the project configuration and create all pipelines and their components.

        @return: True
        """

        # Read the first level of the project structure
        for pipeline in self.project_structure['pipelines']:

            # Get the name of the pipeline
            pipeline_name = pipeline['pipeline_name']

            # Create a new simple pipeline
            self.add_pipeline(name=pipeline_name)

            # Read the second level of the project structure
            for component in pipeline["components"]:
                # Get the name of the component
                component_name = component['component_name']

                # Load the module where the entry point is stored
                component_module = importlib.import_module(component['entry_point'])

                # Get the input dictionary to be passed to the component
                inputs = component['component_input']

                # Get components output flags
                return_output, save_output = component['return_output'], component['save_output']

                # Get status flag
                disabled = component['disabled']

                # Create the component and links it to the pipeline
                self.set_component(pipeline_name=pipeline_name, component_name=component_name,
                                   function=component_module.main, function_params=inputs,
                                   return_output=return_output, save_output=save_output, disabled=disabled)

        return True

    def run(self):
        """
        Run the engine. All pipelines are executed with their components.
        """

        # Environment setup before the run
        self.instance_new_run()

        t0 = get_time()
        self.logger.warning("Xander Engine is running.")

        for i, name in enumerate(self.pipelines):
            t1 = get_time()
            self.logger.info("Running pipeline '{}' ({}/{})".format(name, i + 1, len(self.pipelines)))

            pipeline = self.pipelines[name]

            try:
                # Run pipeline
                pipeline.run()

            except Exception as e:
                message = f"Failed pipeline '{pipeline.pipeline_slug}' ({i+1}/{len(self.pipelines)})"
                exception = str(e)

                # Alert the server for the fail and print out on the stdout the message
                self.client.kill_run(execution=self.execution, exception=message)
                self.logger.critical(f"{message}, {exception}")
                self.logger.critical(exception, exc_info=e)
                self.logger.critical(f"Killing the current Xander execution...")
                self.logger.critical(f"Xander ML Engine has terminated with errors. [{elapsed(t0)}]")
                exit(0)

            self.logger.info(f"Completed pipeline '{pipeline.pipeline_slug}' ({i+1}/{len(self.pipelines)}) in {elapsed(t1)}")

        # Update the end time
        self.execution[END_TIME] = now()

        # Push the end of the execution on the server
        self.client.complete_run(execution=self.execution)
        self.logger.warning(f"Xander ML Engine has terminated successfully. [{elapsed(t0)}]")

    def add_pipeline(self, name):
        """
        Add a new pipeline to the engine.

        @param name: name of the pipeline
        @return: the created pipeline
        """

        # Add the pipeline to the list to be executed
        self.pipelines[name] = Pipeline(name=name,
                                        storage_manager=self.storage_manager,
                                        client=self.client,
                                        logger=self.logger)

        self.logger.info("Pipeline '{}' added to the engine".format(self.pipelines[name].pipeline_name))

        return True

    # def add_ML_pipeline(self, name, model, input_file_name, target_name, pipeline_configuration):
    #     """
    #     Add a new machine learning pipeline to the engine.
    #     The pipeline is configured in standard way.
    #
    #     @param pipeline_configuration: configuration dictionary
    #     @param model: object model to be trained
    #     @param input_file_name: name of the file that contains data
    #     @param target_name: name of the column in the input file data that is used as target for the model
    #     @param name: name of the pipeline
    #     @return: the created pipeline
    #     """
    #
    #     # Add the pipeline to the list to be executed
    #     self.pipelines[name] = MLPipeline(name=name, storage_manager=self.storage_manager, client=self.client,
    #                                       model=model, input_file_name=input_file_name, target_name=target_name,
    #                                       pipeline_configuration=pipeline_configuration)
    #
    #     logging.info("ML Pipeline '{}' added to the engine".format(name))
    #
    #     return True

    def set_component(self, pipeline_name, component_name, function, function_params, return_output, save_output,
                      disabled):

        try:
            if pipeline_name in self.pipelines:
                self.pipelines[pipeline_name].set_component(name=component_name, function=function,
                                                            function_params=function_params, logger=self.logger,
                                                            return_output=return_output, save_output=save_output,
                                                            disabled=disabled)
        except Exception as e:
            self.logger.error(f'New component not set correctly. {e}', exc_info=e)

        return True

    def set_ingestion(self, pipeline_name, ingestion_function):

        try:
            if pipeline_name in self.pipelines:
                self.pipelines[pipeline_name].set_ingestion(ingestion_function=ingestion_function)
        except:
            self.logger.error('Ingestor not set correctly.')

        return True

    def set_encoding(self, pipeline_name, encoding_function):

        try:
            if pipeline_name in self.pipelines:
                self.pipelines[pipeline_name].set_encoding(encoding_function=encoding_function)
        except:
            self.logger.error('Encoder not set correctly.')

        return True

    def set_split(self, pipeline_name, split_function):

        try:
            if pipeline_name in self.pipelines:
                self.pipelines[pipeline_name].set_split(split_function=split_function)
        except:
            self.logger.error('Splitter not set correctly.')

        return True

    def set_feature_selection(self, pipeline_name, feature_selection_function):

        try:
            if pipeline_name in self.pipelines:
                self.pipelines[pipeline_name].set_feature_selection(
                    feature_selection_function=feature_selection_function)
        except:
            self.logger.error('Feature selection not set correctly.')

        return True

    def set_validation_test(self, pipeline_name, validation, test):

        try:
            if pipeline_name in self.pipelines:
                self.pipelines[pipeline_name].set_model(validation=validation, test=test)
        except:
            self.logger.error('Model not set correctly.')

        return True
