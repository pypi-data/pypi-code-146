from steam_sdk.parsers.ParserDakota import ParserDakota
import os


class ParsimDakota:
    """

    """

    def __init__(self, input_DAKOTA_yaml: str = None, output_file_full_path: str = None, verbose: bool = True):
        """
        Object is initialized by defining DAKOTA variable structure and file template.
        If verbose is set to True, additional information will be displayed
        """
        # Unpack arguments
        self.verbose: bool = verbose
        self.Parser_DAKOTA = ParserDakota(input_DAKOTA_yaml)
        #self.DAKOTA_data = self.Parser_DAKOTA.dakota_data

        #self.DAKOTA_folder = self.DAKOTA_data.WorkingFolders.output_path
        #self.Parser_DAKOTA.writeDAKOTA2in(output_file_full_path=output_file_full_path, verbose=verbose)
        #self.Parser_DAKOTA.writeDAKOTA2in(os.path.join(self.DAKOTA_folder, f'{self.DAKOTA_data.STEAMmodel.name}_Analysis'))
