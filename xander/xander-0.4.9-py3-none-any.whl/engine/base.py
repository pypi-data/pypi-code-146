import datetime
import logging
import os
import uuid

from xander.utils.utility import get_parameters, get_time, elapsed


class BasePipeline:
    """
    Base object for Pipeline.
    """

    def __init__(self, name, storage_manager, client, logger):
        # Unique identifier of the pipeline.
        self.pipeline_id = uuid.uuid4().hex

        # Name of the pipeline provided by the user.xw
        self.pipeline_name = name

        # Slug of the pipeline to better represent it in the system.
        self.pipeline_slug = '_'.join(self.pipeline_name.split(' ')).lower()

        # List of methods to be applied in the pipeline. If the pipeline performs correctly they are saved and reloaded
        # on cold start.
        self.components = {}

        # Storage manager
        self.storage_manager = storage_manager
        self.storage_manager.create_sub_destination_folder(self.pipeline_slug, self.pipeline_slug)

        # Xander client
        self.client = client

        # Stats and numbers
        self.start_time = None
        self.end_time = None
        self.run_duration = None

        self.logger = logger

    def run(self):
        """
        Run the pipeline.

        @return: return a list of results
        """

        # List of outputs, updated at each iteration
        start = datetime.datetime.now()

        # Update start time and push the change on the cloud server
        self.start_time = start.strftime('%Y-%m-%d %H:%M:%S')

        # List of outputs
        outputs = self.execute()

        # Update end time
        end = datetime.datetime.now()
        self.end_time = end.strftime('%Y-%m-%d %H:%M:%S')

        # Update delta time and push the change on the cloud server
        delta = end - start
        self.run_duration = delta.seconds if delta.seconds > 0 else 1

        return outputs

    def execute(self):
        """
        Run the pipeline using all specified components.

        @return: True if the execution has terminated successfully, otherwise False.
        """

        outputs = []

        for i, slug in enumerate(self.components):
            t1 = get_time()
            logging.info("{}: component {}/{}".format(self.pipeline_slug, i + 1, len(self.components)))

            component = self.components[slug]

            # The output of the previous component is passed to the current component, if the content is None or
            # non-needed nothing happens. The execution goes on.
            outputs = component.run(*outputs)
            logging.info("{}: component {}/{} completed in {}".format(self.pipeline_slug, i + 1, len(self.components),
                                                                      elapsed(t1)))

        return outputs


class BaseComponent:
    """
    Basic execution component in the pipeline. It takes the input, runs the methods passed as parameter and returns
    the output that will be exported by the pipeline.
    """

    def __init__(self, pipeline_slug, slug, function, function_params, storage_manager, logger, disabled=True,
                 return_output=False, save_output=True):
        """
        Class constructor.

        @param pipeline_slug: pipeline slug
        @param slug: slug of the component
        @param function: function passed by the user that will be executed by the component (Python method)
        @param function_params: input parameters of the function (tuple)
        @param storage_manager: storage manager to retrieve files if needed and exports output
        @param disabled: indicates if the component is active or not
        @param return_output: if set to True the output of the component is returned to the pipeline instead of saved
                              in the storage
        """

        self.pipeline_slug = pipeline_slug
        self.slug = slug
        self.function = function
        self.params = function_params
        self.storage_manager = storage_manager
        self.return_output = return_output
        self.save_output = save_output
        self.disabled = disabled
        self.logger = logger

        # Add a folder for the component in the pipeline directory
        self.storage_manager.create_sub_destination_folder(os.path.join(self.pipeline_slug, slug), slug)

    def run(self, *args):
        """
        Execute the component running the function with the specified parameters.
        The output is return to eventually passed to other components and it is saved in the storage.

        @return: returns the output of the process if the flag is set to True otherwise returns None
        """

        # Execute the component only if the flag is set to active. The parameter can be set by the user or by another
        # function.
        if self.disabled:
            return []

        # Read inputs
        inputs = self.handle_inputs(self.params, *args)

        # Attach logger
        inputs.append(self.logger)

        # Process inputs
        outputs = self.process(inputs)

        # Call the function that handle the output
        return self.handle_outputs(outputs)

    def handle_inputs(self, inputs, *args):

        # List of params
        params_list = get_parameters(self.storage_manager, inputs)

        # If the list of components is not None, they are added to the params list
        added_arguments = list(args)

        # Add the additional arguments to the params list if they are valid
        params_list.extend([a for a in added_arguments if a is not None])

        return params_list

    def process(self, inputs):
        """
        Standard process function.

        @param inputs: list of inputs
        @return: list of outputs
        """

        return self.function(*inputs)

    def handle_outputs(self, outputs):
        """
        Export the list of outputs on the base of their nature:
        1) storage --> save the output into a file
        2) database --> makes a query to store the output

        @param outputs: dictionary with outputs to export
        @return: True or the list of outputs
        """

        # Extract the list of outputs on the base of their nature (storage, database)
        storage_outputs, database_outputs = outputs['storage'], outputs['database']

        # If the flag to export the output in storage is True, StorageManager is called to export the output
        if self.save_output:
            # Export files with storage manager
            # self.storage_manager.export_to_storage(storage_outputs, self.slug)

            # Export queries with database connector
            self.storage_manager.export_to_database(database_outputs)

        # If the return output flag is set to true, the list of output is returned to the next component
        return [c[1] for c in outputs['storage']] if self.return_output else []
