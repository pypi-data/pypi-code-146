import csv
from steam_sdk.utils.sgetattr import rsetattr, rgetattr
from steam_sdk.builders.BuilderModel import BuilderModel
import copy

class ParsimSweep:
    """

    """

    def __init__(self, ref_model: BuilderModel, verbose: bool = True):
        """
                If verbose is set to True, additional information will be displayed
        """
        # Unpack arguments
        self.verbose: bool = verbose
        self.ref_model = ref_model

        self.simulation_names = []
        self.simulation_numbers = []
        self.dict_BuilderModels = dict()  # key is simulation number

    def read_from_input(self, file_path: str, verbose: bool):

        # Open the CSV file
        with open(file_path, 'r') as csv_file:
            # Create a CSV reader
            reader = csv.DictReader(csv_file)
            # Iterate through the rows
            for i, row in enumerate(reader):
                self.simulation_numbers.append(row['simulation_number'])
                self.simulation_names.append(row['simulation_name'])
                if verbose:
                    print(f'changing these fields row nr {i}: {row}')
                # Iterate through the keys and values in the data dictionary
                new_BM = copy.deepcopy(self.ref_model)
                for key, value in row.items():
                    # Set the class variable using the key and value
                    try:
                        rsetattr(new_BM, key, value)
                    except:
                        try:
                            rsetattr(new_BM.model_data, key, value)
                        except:
                            print(f'Skipped column {key} - no corresponding entry in BuilderModel found.')
                # Append the row as a dictionary to the list
                self.dict_BuilderModels[self.simulation_numbers[i]] = new_BM
        if verbose:
            print('csv file read.')



