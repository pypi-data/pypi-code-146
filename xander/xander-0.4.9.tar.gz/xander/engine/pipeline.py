import logging
import os

from xander.engine.base import BasePipeline
from xander.engine.simple_component import SimpleComponent
from xander.utils.utility import get_slug


class Pipeline(BasePipeline):
    """
    Pipeline is a core and basic component of the ML Engine. It will be expanded by other specific Pipeline components.
    """

    def __init__(self, name, storage_manager, client, logger):
        # List of methods to be applied in the pipeline. If the pipeline performs correctly they are saved and reloaded
        # on cold start.
        super().__init__(name, storage_manager, client, logger)

    def set_component(self, name, function, function_params, logger, return_output=False, save_output=True,
                      disabled=False):
        """
        Add a new component to the pipeline.

        @param save_output:
        @param name: name of the component
        @param function: function to be executed
        @param function_params: input params for the function
        @param return_output: flag that indicates if the output is passed to the next component

        @return: True
        """

        # Compute the slug
        slug = get_slug(name)

        # Initialize the new component
        component = SimpleComponent(pipeline_slug=self.pipeline_slug, slug=slug, function=function, logger=logger,
                                    function_params=function_params, storage_manager=self.storage_manager,
                                    return_output=return_output, save_output=save_output, disabled=disabled)

        # Add a folder for the component in the pipeline directory
        self.storage_manager.create_sub_destination_folder(os.path.join(self.pipeline_slug, slug), slug)

        # If the component already exists, then overwrites it
        self.components[slug] = component

        logging.info('Pipeline {} -> new component added.'.format(self.pipeline_slug))
        return True
