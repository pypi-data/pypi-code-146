from xander.engine.simple_component import BaseComponent


class MLComponent(BaseComponent):

    def __init__(self, pipeline_slug, slug, function, custom_function, function_params, pipeline_configuration,
                 storage_manager, active=True, return_output=True, save_output=False):
        # Set the pipeline configuration
        self.pipeline_configuration = pipeline_configuration

        # Custom function provided by the user
        self.custom_function = custom_function

        # Call the super object constructor.
        super().__init__(pipeline_slug, slug, function, function_params, storage_manager, active, return_output,
                         save_output)

    def process(self, inputs):
        """
        Execute the passed function with the passed inputs as arguments.

        @param inputs: list of arguments.
        @return: output of the function
        """

        return self.function(self.pipeline_configuration, self.custom_function, *inputs)


class MLTrainerComponent(BaseComponent):

    def __init__(self, pipeline_slug, slug, function, model, validation_function, test_function,
                 function_params, pipeline_configuration, storage_manager, active=True, return_output=True,
                 save_output=False):

        self.model = model
        self.validation_function = validation_function
        self.test_function = test_function
        self.pipeline_configuration = pipeline_configuration

        # Call the super object constructor.
        super().__init__(pipeline_slug, slug, function, function_params, storage_manager, active, return_output,
                         save_output)

    def process(self, inputs):
        """
        Execute the passed function with the passed inputs as arguments.

        @param inputs: list of arguments.
        @return: output of the function
        """

        return self.function(self.pipeline_configuration, self.model, self.validation_function, self.test_function, *inputs)
