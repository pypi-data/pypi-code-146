import os
import shutil


class DataCollector:
    def __init__(self, data_abs_path):
        """
        Ensures data is copied to project datafolder
        """
        if not os.path.exists(data_abs_path):
            raise RunTimeError("Didn't find data folder")

        self.data_abs_path = data_abs_path

        data_folder_name = os.path.split(self.data_abs_path)[1]
        # All runs happens to levels under data folder
        self.data_relative_path = os.path.join("..", "..", data_folder_name)

        self.copied_original_paths = []
        self.copied_final_paths = []

    def collect(self, parameters_object):
        """
        Collects datafiles for parameter object

        Any parameter that has the is_filename set to True at creation will
        be handled by this method. The corresponding file is copied to the
        data_abs_path in the DataCollector object, and the filename parameter
        is updated with a new path that points to the copied file. In this way
        the user can copy the project to a cluster without worrying about
        files the simulation depends on, and it is saved for reproducibility.
        For this reason the new path is a relative path so the project folder
        can be moved without breaking absolute paths.
        Files are only copied once, if two datafiles have the same name, it
        will only be copied once, which is a potential problem.

        Parameters
        ----------

        parameters_object : Parameters object
            Parameters object that may have filenames included
        """

        for filename_par_name in parameters_object.get_filename_pars():
            self.collect_file(parameters_object, filename_par_name)

    def collect_file(self, parameters_object, filename_par_name):
        """
        Checks if a file has already been copied, if not copies it

        Parameters
        ----------

        parameters_object : Parameters object
            Parameters object that may have filenames included

        filename_par_name : str
            Parameter name that correspond to a filename
        """

        current_file_path = parameters_object[filename_par_name]

        # Check file has not already been copied
        if current_file_path in self.copied_original_paths:
            return

        if current_file_path.strip('"') in self.copied_original_paths:
            return

        if current_file_path in self.copied_final_paths:
            return

        if current_file_path.strip('"') in self.copied_final_paths:
            return

        if not os.path.exists(current_file_path):
            print(self.copied_original_paths)
            print(self.copied_final_paths)
            raise RuntimeError("File didn't exist!" + str(current_file_path))

        # Perform a copy operation
        filename = os.path.split(current_file_path)[1]
        new_abs_path = os.path.join(self.data_abs_path, filename)
        shutil.copyfile(current_file_path, new_abs_path)

        # Set new relative path
        new_path = os.path.join(self.data_relative_path, filename)
        parameters_object[filename_par_name] = '"' + new_path + '"'

        self.copied_original_paths.append(current_file_path)
        self.copied_final_paths.append(new_path)
