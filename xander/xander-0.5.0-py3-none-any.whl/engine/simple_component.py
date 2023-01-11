from xander.engine.base import BaseComponent


class SimpleComponent(BaseComponent):
    """
    Basic execution component in the pipeline. It takes the input, runs the methods passed as parameter and returns
    the output that will be exported by the pipeline.
    """

    def __init__(self, pipeline_slug, slug, function, function_params, storage_manager, logger, disabled=True,
                 return_output=False, save_output=True):

        # Call the super object constructor.
        super().__init__(pipeline_slug, slug, function, function_params, storage_manager, logger, disabled, return_output,
                         save_output)
