import os
from typing import Callable, Dict, List
import numpy as np
from glob import glob
import h5py
from .util import hdf5_tools as h5t
import matplotlib.pyplot as plt
import matplotlib
from tqdm.auto import tqdm
from multiprocessing import Pool

# Type hints own types :

CommandStr = str

# Const defs :

N_PARAM_GROUPS = 4

# PyCfs class :


class PyCfs:
    def __init__(
        self,
        project_name: str,
        cfs_install_dir: str,
        init_params: np.ndarray,
        cfs_params_names: List = [],
        material_params_names: List = [],
        trelis_params_names: List = [],
        additional_param_fun: Callable = None,
        additional_file_name: str = "additional.csv",
        trelis_version: str = "trelis",
        cfs_proj_path: str = "./",
        templates_path: str = "./templates",
        init_file_extension: str = "init",
        mat_file_name: str = "mat",
        result_type: str = "txt",
        n_threads: int = 1,
        res_manip_fun: Callable = None,
        quiet_mode: bool = False,
        detail_mode: bool = False,
        clean_finish: bool = False,
        save_hdf_results: bool = False,
        array_fill_value: any = np.nan,
        parallelize: bool = False,
        n_jobs_max: int = np.inf,
    ):
        """

        OpenCFS and Trelis/CoreformCubit python interfacing package. The main
        goal of this module is to make an easy to use interface which provides
        a class that handles the automatic simulation setup from given CFS and
        Trelis parameters and the result storage.

        Args:
            project_name (str): Name of the simulation project (needs to be
            the same as the .xml file name)

            cfs_install_dir (str): Install path of CFS.

            init_params (np.ndarray): Array containing the initial set of
            parameters. First trelis parameters and then cfs (xml) ones.

            cfs_params_names (list): List of trelis parameter names as defined in
                                        the associated .jou file.

            material_params_names (list): List of trelis parameter names as defined in
                                        the associated .jou file.

            trelis_params_names (list): List of trelis parameter names as defined in
                                        the associated .jou file.

            additional_param_fun (Callable): Handle to a function which modifies the
                                           additional parameters.

            additional_file_name (str): Additional file containing parameters changed
                                       by the additional_param_fun.

            trelis_version (str, optional): If 'coreform_cubit' is installed use it
                                            so that the correct one is run. Defaults
                                            to 'trelis'.

            parallelize (bool): Flag which chooses whether to parallelize the runs for
                                the given parameter matrices. Defaults to False.

            n_jobs_max (int): Max number of jobs to constrain the pool manager. Defaults
                              to inf.

            templates_path (str, optional): Path to template files. Defaults to "templates".

            cfs_proj_path (str, optional): Project path. Defaults to "./".

            init_file_extension (str): Extension added to project_name to identify
                                     init files which are used as templates.

            mat_file_name (str): Material file name. (default = "mat")

            n_threads (int): Number of threads to be used by OpenCFS. (default = 1).

            quiet_mode (bool): Turns a more conservatice OpenCFS output on. (default = false).

            detail_mode (bool): Write detailed OpenCFS output to file. (default = false).

            clean_finish (bool): Delete all generated simulation files. Does not touch
                                result files. Defaults to False.


        """
        # Set init params from args :
        self.project_name = project_name
        self.sim_file = cfs_proj_path + project_name
        self.cfs_proj_path = cfs_proj_path
        self.cfs_install_dir = cfs_install_dir
        self.templates_path = templates_path
        self.n_threads = n_threads
        self.result_type = result_type
        self.quiet_mode = quiet_mode
        self.detail_mode = detail_mode
        self.clean_finish = clean_finish
        self.save_hdf_results = save_hdf_results
        self.array_fill_value = array_fill_value
        self.parallelize = parallelize
        self.n_jobs_max = n_jobs_max
        self.additional_param_fun = additional_param_fun
        self.additional_file_name = additional_file_name
        self.mat_file_name = mat_file_name
        self.init_file_extension = init_file_extension
        self.res_manip_fun = res_manip_fun
        self.trelis_version = trelis_version

        self.params = init_params.reshape(1, -1)
        self.n_params = len(self.params)

        self.trelis_params_names = trelis_params_names
        self.n_trelis_params = len(trelis_params_names)

        self.mat_params_names = material_params_names
        self.n_mat_params = len(material_params_names)

        self.cfs_params_names = cfs_params_names
        self.n_cfs_params = len(cfs_params_names)

        # Initialize placeholders :
        self._init_placeholders()

        # Set up paths and folder structure for results :
        self._init_paths()

        # finalize parameter setup :
        self._init_param_setup()

        # Generate file names :
        self._init_file_names()

        # Set functions -> less branches in code :
        self._init_functions()

        # Set commands :
        self._init_commands()

        # Directory setup :
        self._make_hist_directory()

        # Make initial forward pass :
        self._run_pipeline()
        self._clean_sim_files_if_on()

        # Set values to not changed :
        self._set_all_params_changed_status(False)

        # Get history data files :
        self._get_tracked_results()

        self.print_init_info()

        self._clean_hist_results()

    def __call__(self: object, X: np.ndarray) -> None:
        """

        Simulation forward function. Performs the simulation for the passed
        parameter combinations. Does not return anything as the results are
        stored in the self.results dictionary.

        Args:
            self (object): PyCfs class object.
            X (np.ndarray): N x M Array containing the simulation parameters. Here
                            the M is the number of parameters in total.

        Returns:
            None
        """
        self._forward(X)

    def _forward_parallel(self, X):
        """

        Performs the forward pass over all data in a parallel manner. Does the
        preprocessing step where the passed matrix is prepared for parallel computation
        and determines the number of parameter combinations N. Allocates the
        result arrays and stores the results of the performed calculations.

        Args:
            self (object): PyCfs class object.
            X (np.ndarray): N x M Array containing the simulation parameters. Here
                            the M is the number of parameters in total.

        Returns:
            None.
        """

        self.N = X.shape[0]
        self._init_results()

        self._init_params_parallel(X)

        # generate data indices for parallel computing :
        data_list = np.arange(0, self.N)

        # determine number of jobs :
        n_jobs = min(len(data_list), self.n_jobs_max)

        # construct pool and pass jobs - starts the computation also:
        with Pool(processes=n_jobs) as p:
            p.map(self._forward_once_parallel, data_list)

        for ind in range(self.N):
            files = self._get_hist_files_parallel(ind)
            self._set_results_txt(ind, files=files)
            print("done", ind)

        self._clean_hist_results_parallel()
        self._clean_sim_files_parallel()

    def _forward_once_parallel(self, ind: int) -> None:
        """

        Runs one process from the pool of currently active ones. Does
        this for the process with id = ind.

        Args:
            ind (int): job index to get correct parameters for simulation
                       and to read correct results from the result dir.
        """

        self._set_all_params_changed_status(True)
        self._run_pipeline(ind)

    def _init_placeholders(self) -> None:
        self.files = []
        self.results_name = []
        self.results_type = []
        self.results_num = []
        self.results_elem = []
        self.sim_files = []
        self.params_changed = np.ones((N_PARAM_GROUPS,), dtype=bool)

        self.results = dict()
        self.results_keys = []
        self.ind = 0

    def _init_commands(self) -> None:
        """

        Generates default commands for trelis and cfs with all optional flags.

        """
        self.trelis_comm = (
            f"{self.trelis_version} -batch -nographics -nojournal " + self.jou_file
        )
        cfs_options = self._get_cfs_options()
        self.cfs_comm = self.cfs_install_dir + "cfs" + cfs_options + self.sim_file[2:]

    def _init_paths(self) -> None:
        """

        Initializes path variables and generates result paths if not present.

        """
        self.history_path = self.cfs_proj_path + "history/*"
        self.hdf_res_path = f"results_hdf5/{self.project_name}"
        self.hdf_file_path = f"./results_hdf5/{self.project_name}.cfs"

        if not os.path.exists("results_hdf5"):
            os.makedirs("results_hdf5")

        if not os.path.exists(self.hdf_res_path):
            os.makedirs(self.hdf_res_path)

    def _init_functions(self) -> None:
        """

        Initializes the functions to avoid branches in the code based on some
        logical flags.

        """
        self._forward = (
            self._forward_parallel if self.parallelize else self._forward_serial
        )
        self.get_results = (
            self._get_results_txt
            if self.result_type == "txt"
            else self._get_results_hdf
        )
        self._clean_sim_files_if_on = (
            self._clean_sim_files if self.clean_finish else self.dummy_fun
        )
        self._save_hdf_results_if_on = (
            self._save_hdf_results if self.save_hdf_results else self.dummy_fun
        )
        self._allocate_result_arrays = (
            self._allocate_result_arrays_txt
            if self.result_type == "txt"
            else self.dummy_fun
        )
        self._set_results = (
            self._set_results_txt
            if self.result_type == "txt"
            else self._set_results_hdf
        )
        self._init_results = (
            self._init_results_hdf
            if self.result_type == "hdf5"
            else self._allocate_result_arrays
        )
        self.print_init_info = (
            self._print_hdf_info if self.result_type == "hdf5" else self._print_txt_info
        )
        self.res_manip_fun = (
            self._default_external_result_manip
            if self.res_manip_fun is None
            else self.res_manip_fun
        )

    def _init_file_names(self) -> None:
        """

        Generate names for the different simulation files which are used.

        """
        self.cfs_file_init = (
            f"{self.templates_path}/{self.project_name}_{self.init_file_extension}.xml"
        )
        self.mat_file_init = (
            f"{self.templates_path}/{self.mat_file_name}_{self.init_file_extension}.xml"
        )
        self.jou_file_init = (
            f"{self.templates_path}/{self.project_name}_{self.init_file_extension}.jou"
        )
        self.cfs_file = f"{self.sim_file}.xml"
        self.jou_file = f"{self.sim_file}.jou"
        self.mat_file = f"{self.mat_file_name}.xml"
        self.sim_files = [
            self.cfs_file,
            self.jou_file,
            self.mat_file,
            f"{self.sim_file}.info.xml",
            f"{self.project_name}.cdb",
        ]

    def _init_param_setup(self) -> None:
        """

        Initializes the parameters by splitting these into the main groups.

        """

        # Additional params setup :
        self.additional_params_exist = False

        if self.additional_param_fun is not None:
            self.additional_params_exist = True
            self.additional_param_fun = self.additional_param_fun
            self.params_changed[3] = True

        # Parameter setup :
        self.n_base_params = (
            self.n_cfs_params + self.n_mat_params + self.n_trelis_params
        )

        self._init_params_parallel(self.params)

        # Concatenate all params names :
        self.params_names = (
            self.cfs_params_names + self.mat_params_names + self.trelis_params_names
        )

    def _init_params_parallel(self, X: np.ndarray) -> None:
        """

        Initializes the parameters for parallel execution. Essenatially
        splits up the parameter matrix X into the 4 different parameter
        groups which are used within the simulations.

        Args:
            X (np.ndarray): N x M Array containing the simulation parameters. Here
                            the M is the number of parameters in total.
        """

        self.cfs_params = X[:, 0 : self.n_cfs_params]
        self.mat_params = X[
            :, self.n_cfs_params : self.n_cfs_params + self.n_mat_params
        ]
        self.trelis_params = X[
            :, self.n_cfs_params + self.n_mat_params : self.n_base_params
        ]
        self.add_params = X[
            :, self.n_cfs_params + self.n_mat_params + self.n_trelis_params :
        ]

    def _forward_serial(self, X):
        """

        Performs the forward pass over all data. Determines number of parameter
        combinations N. Allocates the result arrays and stores the results
        of the performed calculations.

        Args:
            self (object): PyCfs class object.
            X (np.ndarray): N x M Array containing the simulation parameters. Here
                            the M is the number of parameters in total.

        Returns:
            None.
        """

        self.N = X.shape[0]
        self._init_results()

        for ind in tqdm(range(self.N)):
            self.ind = ind
            x = X[ind : ind + 1, :]
            self._forward_once_serial(x, ind)
            self._save_hdf_results_if_on(ind)

        self._clean_sim_files_if_on()

    def _forward_once_serial(self, x, ind):
        """

        Performs the forward pass for one parameter configuration. Updates the
        simulation files. Runs the pipeline (trelis, cfs calculation), gets the
        results, stores them and cleans the history files from the history folder.

        Args:
            self (object): PyCfs class object.
            x (np.ndarray): Array containing the simulation parameters. Here
                            the M is the number of parameters in total.
            ind (int): Index of current parameter array out of the total N
                       configurations.

        Returns:
            None.
        """

        self._update_params(x)
        self._run_pipeline()
        self._set_all_params_changed_status(False)

        self._get_hist_files()
        self._set_results(ind)
        self.res_manip_fun(self)
        self._clean_hist_results()

    def _get_tracked_results(self) -> None:
        """

        Retrieves the results after the initial run. Generates a result index
        depending on the chosen result type :

        NOTE : this ought to be changed in future to nicer handling of results.

        """
        if self.result_type == "txt":
            self._get_hist_files()
            self._build_result_tree()
        elif self.result_type == "hdf5":
            self._set_hdf_names()
            self._construct_hdf_name_mapping()

    def _set_hdf_names(self) -> None:
        """

        Sets the names of the results for the hdf result case.

        """
        self.tracked_results, self.result_regions = h5t.get_result_names_list(
            self.hdf_file_path
        )

    def _get_hdf_curr_package(self) -> Dict[str, np.ndarray]:
        """

        Gets the hdf package for the current simulation run by extracting all
        results from the hdf file for the result regions defined in the inital
        run.

        Returns:
            Dict[str,np.ndarray]: Dict containing all of the results for all of
                                  the different regions where the results are defined.
        """
        return h5t.get_all_results(self.hdf_file_path, regions=self.result_regions)

    def _init_results_hdf(self) -> None:
        """

        Initializes an empty list for storing the hdf file results into.

        """
        self.results = []

    def _make_hist_directory(self) -> None:
        """

        Checks if the history directory is present and if not creates one.

        """
        if not os.path.exists(self.cfs_proj_path + "history/"):
            os.mkdir(self.cfs_proj_path + "history/")

    def _construct_hdf_name_mapping(self) -> None:
        """

        Constructs map for the result names such that the results can
        be indexed with the initial printout id's.

        """

        res_ind = 0
        access_ind = 0
        self.ind_to_name = {}
        for key0 in self.tracked_results:
            for key1 in self.result_regions[res_ind]:
                self.ind_to_name[access_ind] = (key0, key1)
                access_ind += 1
            res_ind += 1

    def _print_hdf_info(self) -> None:
        """

        Prints the initial info for the set up problem. In this case for
        the hdf file results which have a different structure than the
        hist results.

        """
        print("\n ########################## \n")
        print(" Optimization params vector elements are : \n")
        for ind in range(self.n_base_params):
            print(f"   [{ind}] {self.params_names[ind]}")

        print("\n Stored results are : ")

        res_ind = 0
        access_ind = 0
        for key0 in self.tracked_results:
            print(f"\n   > {key0} : ")

            for key1 in self.result_regions[res_ind]:
                print(f"   |     [{access_ind}] {key1}")
                access_ind += 1

            res_ind += 1

        print("\n ########################## \n")

    def _run_pipeline(self, ind: int = None) -> None:
        """

        Performs a check to see which parameters changes. If the parameter
        group in question did change then the appropriate file gets updated
        and if necessary further actions carried out. If any parameter
        group changed then the simulation is carried out.

        Args:
            self (object): PyCfs class object.
            ind (int): Pool job index to get correct parameters for simulation
                       and to read correct results from the result dir.

        Returns:
            None.
        """

        # Check if CFS xml parameters changed :
        if self.params_changed[0]:
            self._update_cfs_xml(ind)

        # Check if CFS mat parameters changed :
        if self.params_changed[1]:
            self._update_mat_xml(ind)

        # Check if Trelis parameters changed :
        if self.params_changed[2] and ((ind is None) or (not self.parallelize)):
            self._update_trelis_jou(ind)
            # self._run("rm *.cdb")
            self._run(self.trelis_comm)

        # Check if additional parameters changed :
        if self.additional_params_exist and self.params_changed[3]:
            self.additional_param_fun(self.add_params)

        # If any config changes happened run simulation :
        if self.parallelize or np.any(self.params_changed):
            cfs_comm = (
                self._make_cfs_command(ind) if self.parallelize else self.cfs_comm
            )
            self._run(cfs_comm)

    def _set_all_params_changed_status(self, flag: bool) -> None:
        """

        Sets the params changed variable elements all to the given flag.

        Args:
            flag (bool): Value to set params changed variable elements to.
        """
        self.params_changed = np.full((4,), flag)

    def _default_external_result_manip(self, obj) -> None:
        """

        Dummy function for external results manipulation. If no external
        result manipulation function is passed this one is executed and
        does nothing which is the goal.

        Args:
            obj (object): pycfs object instance.
        """
        pass

    def _make_cfs_command(self, ind: int = None) -> CommandStr:

        """

        Generates a cfs command str. If from Pool of processes ind won't be
        None and it will generate correct command for the current process.

        Args:
            ind (int): job index to get correct parameters for simulation
                       and to read correct results from the result dir.
                       Default : None.

        Returns:
            CommandStr: A string containing a command runnable in the shell.
        """

        cfs_options = self._get_cfs_options()

        ind_ext = "" if ind is None else f"_{ind}"
        subsim_name = f" {self.sim_file[2:]}{ind_ext}"

        return (
            self.cfs_install_dir
            + "cfs"
            + cfs_options
            + "-p"
            + subsim_name
            + ".xml"
            + subsim_name
        )

    ############################################################
    ################## PUBLIC FUNCTIONS ########################
    ############################################################
    def dump_results(self, path: str) -> None:
        """

        Dumps the current results to the specified path as a npy binary
        data file.

        Args:
            path (str): Path where to save the results to.
        """

        datadir = "/".join(path.split("/")[:-1]) + "/"
        if not os.path.exists(datadir):
            os.makedirs(datadir)

        np.save(path, self.results, allow_pickle=True)

    def _get_results_txt(self, res_id: int = 0, res_ind: int = 0) -> np.ndarray:
        """

        Returns the results selected by the result id. The result
        ids are shown in the initial setup print out. If needed
        these can also be shown by calling `print_init_info()`.

        Args:
            self (object): PyCfs class object.
            res_id (int, optional): Id of the results
                             to be returned. Defaults to 0.

        Returns:
            np.ndarray: Numpy array containing the results.
        """
        keys = self.results_keys[res_id]
        return self.results[keys[0]][keys[1]][keys[2]]["data"]

    def _get_results_hdf(self, res_id: int = 0, res_ind: int = None) -> None:
        """

        Function used to retrieve hdf results internally for given
        result id and result index.

        Args:
            res_id (int, optional): Result id which is given in the
                                    initial printout. Defaults to 0.
            res_ind (int, optional): Result index - if multiple simulation
                                     runs were performed and one wants to
                                     access only one run results. Defaults to None.

        """
        result, region = self.ind_to_name[res_id]

        if res_ind is None:
            results = []
            for res in self.results:
                results.append(res[result][region])
        else:
            results = self.results[res_ind][result][region]

        return results

    def get_all_of(self, res_name: str) -> List[np.ndarray]:
        """_summary_

        Args:
            res_name (str): Result name string which is generated in the simulation.
                            Can be any cfs result string stored within the sim.

        Returns:
            List[np.ndarray]: List containing the same result for all runs.
        """
        results = []
        for res in self.results:
            results.append(res[res_name])
        return results

    def _set_results_hdf(self, ind: int) -> None:
        """

        Reads the hdf results from the current file and appends the generated packet
        to the list of hdf results.

        Args:
            ind (int): TODO job index to get correct parameters for simulation
                       and to read correct results from the result dir.
        """
        hdf_package = self._get_hdf_curr_package()
        self.results.append(hdf_package)

    def set_result_hdf(self, name: str, result: np.ndarray) -> None:
        """

        To be used in external manip function to set hdf results directly
        so that the order is not disturbed.

        Args:
            name (str): result name which we want to add.
            result (np.ndarray): array containing the results we want to store.
        """
        self.results[-1][name] = result

    def _print_txt_info(self) -> None:
        """

        Prints the simulation info. First part contains information
        about the set simulation variables. The second part shows
        the expected results with the result ids given in [res_id].

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """

        print("\n ########################## \n")
        print(" Optimization params vector elements are : \n")
        for ind in range(self.n_base_params):
            print(f"   [{ind}] {self.params_names[ind]}")

        print("\n Stored results are : ")

        res_ind = 0
        for key0 in self.results.keys():
            print(f"\n   > {key0} : ")
            for key1 in self.results[key0].keys():
                print(f"   |  > {key1} : ")
                for key2 in self.results[key0][key1].keys():
                    print(f"   |     [{res_ind}] {key2}")
                    res_ind += 1

        print("\n ########################## \n")

    ###########################################################
    ############# END PUBLIC FUNCTIONS ########################
    ###########################################################

    def _build_result_tree(self):

        """

        Builds up the results as nested dictionary from intial
        forward pass. And sets the initial shapes of the expected
        results.

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """

        level0 = {"data": [], "shape": [], "ndim": 0}

        for file in self.files:

            # Split file at - and remove simulation name
            name_parts = file.split("-")[1:]

            # Remove .hist at the last split item if it has it :
            if name_parts[-1][-5:] == ".hist":
                name_parts[-1] = name_parts[-1][:-5]
            else:
                name_parts.pop(-1)

            # In case of element or node result remove
            # number of element/node
            if len(name_parts) > 3:
                name_parts.pop(2)

            self.results_keys.append(name_parts)

            # Build tree of results from the parts :
            if name_parts[0] not in self.results.keys():
                self.results[name_parts[0]] = {
                    name_parts[1]: {name_parts[2]: level0.copy()}
                }
            elif name_parts[1] not in self.results[name_parts[0]].keys():
                self.results[name_parts[0]][name_parts[1]] = {
                    name_parts[2]: level0.copy()
                }
            elif name_parts[2] not in self.results[name_parts[0]][name_parts[1]].keys():
                self.results[name_parts[0]][name_parts[1]][
                    name_parts[2]
                ] = level0.copy()

            data = self._load_hist_file(file)
            self.results[name_parts[0]][name_parts[1]][name_parts[2]][
                "shape"
            ] = data.shape
            self.results[name_parts[0]][name_parts[1]][name_parts[2]]["ndim"] = len(
                data.shape
            )

    def _load_hist_file(self, file) -> np.ndarray:
        """

        Loads the data from the hist file with path `file`.

        Args:
            self (object): PyCfs class object.
            file (str): Path of the file to be loaded.

        Returns:
            np.ndarray: Array containing the results from the current
                        hist file.
        """
        return np.loadtxt(file, dtype=np.float32)

    def _get_hist_files_parallel(self, ind: int = None) -> List[str]:
        """

        Gets the history file results for the parallel execution mode.
        TODO : make just one function for parallel and serial - easy.

        Args:
            ind (int, optional): Index for the history results if in
                                 parallel execution mode. Defaults to None.

        Returns:
            List[str]: List of history file paths.
        """
        files_path = f"{self.history_path[:-2]}/{self.sim_file[2:]}_{ind}-*"
        files = glob(files_path)
        files.sort(key=lambda x: x.split("-")[-1][:-5])
        return files

    def _get_hist_files(self) -> None:
        """

        Scans the history file location for files, sorts the files
        according to the name and updates the file list.

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """

        self.files = glob(self.history_path)
        self.files.sort(key=lambda x: x.split("-")[-1][:-5])
        self.n_hist_files = len(self.files)

    def _clean_hist_results(self) -> None:
        """

        Removes all files from the hist folder and resets the
        file list.

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """
        self._clean_files(self.files)
        self.files = []

    def _clean_sim_files_parallel(self) -> None:
        self._run("rm *.xml *.jou *.info.xml")

    def _clean_hist_results_parallel(self) -> None:
        self._run("rm history/*.hist")

    def _clean_sim_files(self) -> None:
        """

        Removes all generated simulation files from the hist folder and resets the
        file list.

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """
        # self._reset_param_changed_status()
        self._clean_files(self.sim_files)

    def _clean_files(self, files: List[str]) -> None:
        """

        Removes all files from the passed files list.

        Args:
            self (object): PyCfs class object.
            files (List[str]): List of paths to files to delete.

        Returns:
            None.
        """
        for file in files:
            os.remove(file)

    def _set_results_txt(self, ind: int, files: List[str] = None) -> None:
        """

        Loads the results from the hist files and updates the results
        dictionary with these results.

        Args:
            ind (int): Index of the current parameter set.
            files (List[str]): List of result file paths.

        Returns:
            None.
        """
        used_files = self.files if files is None else files

        for file, keys in zip(used_files, self.results_keys):
            self.results[keys[0]][keys[1]][keys[2]]["data"][
                ind, :
            ] = self._load_hist_file(file)

    def _allocate_result_arrays_txt(self) -> None:
        """

        Loops through all the result fields in the results nested dict
        and allocates the arrays as zero arrays with shape determined
        by the number of the passed param. combinations and the shape of
        the results themselves.

        e.g. Results with shape 2x3 for a input with N=3 param. combinations
        would give an array of shape (3,2,3).

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """
        for key0 in self.results.keys():
            for key1 in self.results[key0].keys():
                for key2 in self.results[key0][key1].keys():
                    d_shape = self.results[key0][key1][key2]["shape"]
                    self.results[key0][key1][key2]["data"] = np.full(
                        [self.N, *[x for x in d_shape]],
                        self.array_fill_value,
                        dtype=np.float32,
                    )

    def _save_hdf_results(self, ind: int = 0) -> None:
        """

        Moves the current hdf results to another folder for saving purposes.
        TODO : this function is redundant with extended cfs command as implemented
               for the parallel case. fix this.

        Args:
            ind (int, optional): Index of the parameter set to relate to.
                                 Defaults to 0.
        """

        cmd = f"cp results_hdf5/{self.project_name}.cfs {self.hdf_res_path}/{self.project_name}_{ind}.cfs"
        self._run(cmd)

    def dummy_fun(self, ind: int = 0):
        pass

    #########################################
    #### Updating ( params ) functions : ####
    #########################################

    def _update_params(self, params: np.ndarray) -> None:
        """

        Updates only parameters which changed and sets these in the param.
        arrays. If any group changed the appropriate flag is also set.

        Args:
            self (object): PyCfs class object.
            params (np.ndarray): Array containing all of the M parameters.

        Returns:
            None.
        """

        if ~np.all(self.cfs_params == params[:, 0 : self.n_cfs_params]):
            self.cfs_params = params[:, 0 : self.n_cfs_params]
            self.params_changed[0] = True

        if ~np.all(
            self.mat_params
            == params[:, self.n_cfs_params : self.n_cfs_params + self.n_mat_params]
        ):
            self.mat_params = params[
                :, self.n_cfs_params : self.n_cfs_params + self.n_mat_params
            ]
            self.params_changed[1] = True

        if ~np.all(
            self.trelis_params
            == params[:, self.n_cfs_params + self.n_mat_params : self.n_base_params]
        ):
            self.trelis_params = params[
                :, self.n_cfs_params + self.n_mat_params : self.n_base_params
            ]
            self.params_changed[2] = True

        if ~np.all(
            self.add_params
            == params[:, self.n_cfs_params + self.n_mat_params + self.n_trelis_params :]
        ):
            self.add_params = params[
                :, self.n_cfs_params + self.n_mat_params + self.n_trelis_params :
            ]
            self.params_changed[3] = True

    def _update_cfs_xml(self, ind: int = None) -> None:
        """

        Updates the main cfs xml file with the new parameters.

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """
        self._update_file(
            self.cfs_file_init,
            self.cfs_file,
            self.cfs_params,
            self.cfs_params_names,
            ind,
        )

    def _update_mat_xml(self, ind: int = None) -> None:
        """

        Updates the material cfs xml file with the new parameters.

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """
        self._update_file(
            self.mat_file_init,
            self.mat_file,
            self.mat_params,
            self.mat_params_names,
            ind,
        )

    def _update_trelis_jou(self, ind: int = None) -> None:
        """

        Updates the trelis journal file with the new parameters.

        Args:
            self (object): PyCfs class object.

        Returns:
            None.
        """
        self._update_file(
            self.jou_file_init,
            self.jou_file,
            self.trelis_params,
            self.trelis_params_names,
            ind,
        )

    def _update_file(
        self,
        init_file_name: str,
        file_out_name: str,
        params: np.ndarray,
        param_names: List[str],
        ind: int = None,
    ) -> None:
        """

        Main update function for the individual files. Loads the init (template) file.
        Sets the parameter values and writes this to the appropriate simulation file.

        Args:
            self (object): PyCfs class object.
            init_file_name (str): Name of the init file.
            file_out_name (str): Name of the output file.
            params (np.ndarray): Array of parameter values to be set.
            param_names (List[str]): Names of the parameters to be set.

        Returns:
            None.
        """

        end_ext = file_out_name.split(".")[-1]
        ind_ext = f".{end_ext}" if ind is None else f"_{ind}.{end_ext}"
        ind_int = 0 if ind is None else ind

        if len(param_names) > 0:
            params = params[ind_int, :]

        file_out_name = file_out_name.replace(f".{end_ext}", ind_ext)

        init_file = open(init_file_name, "r")
        data = init_file.read()
        init_file.close()

        for param, pname in zip(params, param_names):
            data = data.replace(pname, str(param))

        # dirty fix for now :
        data = data.replace('file="mat.xml"', f'file="mat{ind_ext}"')

        final_file = open(file_out_name, "w")
        final_file.write(data)
        final_file.close()

    #############################################
    ############ CMD functions : ################
    #############################################

    def _run(self, cmd: CommandStr) -> None:
        """

        Runs the passed command line command.

        Args:
            self (object): PyCfs class object.
            cmd (CommandStr): Command to be executed.

        Returns:
            None.
        """
        os.system(cmd)

    #############################################
    ############## CFS functions : ##############
    #############################################

    def _get_cfs_options(self) -> str:
        """

        Constructs the CFS command with the selected
        optional arguments.

        Args:
            self (object): PyCfs class object.

        Returns:
            (str): String with the cfs options.
        """
        cfs_options = f" -t {self.n_threads} "

        # Enable quiet mode
        if self.quiet_mode:
            cfs_options += " -q "

        # Enable detailed mode to "info.xml" file
        if self.detail_mode:
            cfs_options += " -d "

        return cfs_options

    ##### Post processing functions : ######
    #! NOTE : very experimental - not to be trusted !!

    def read_cfs_results(self):

        file = h5py.File(f"results_hdf5/{self.sim_file}.cfs", "r")

        nodes_id = {}
        elems_id = {}
        nodes_reg = {}
        elems_reg = {}
        region_res = {}
        elems_nodes = {}
        elems_mid = {}

        regions = file["Mesh"]["Regions"]
        nodes = file["Mesh"]["Nodes"]["Coordinates"][:]
        elems = file["Mesh"]["Elements"]["Connectivity"][:]
        results = file["Results"]["Mesh"]["MultiStep_1"]["Step_1"]

        for key in list(regions.keys()):
            nodes_id[key] = regions[key]["Nodes"][:]
            nodes_reg[key] = nodes[nodes_id[key] - 1]

            elems_id[key] = regions[key]["Elements"][:]
            elems_reg[key] = elems[elems_id[key] - 1]
            is_zero = elems_reg[key] == 0
            n_elems = np.count_nonzero(~is_zero[0, :])
            elems_nodes[key] = nodes[elems_reg[key][~is_zero] - 1]
            elems_nodes[key] = elems_nodes[key].reshape(
                elems_reg[key].shape[0], n_elems, 3
            )

            elems_mid[key] = elems_nodes[key].mean(axis=1)

        for restype in list(results.keys()):
            data_tmp = {}
            for region in list(results[restype].keys()):
                res_type = list(results[restype][region].keys())[0]
                data_tmp[region] = results[restype][region][res_type]["Real"][:]

            region_res[restype] = data_tmp

        return nodes_reg, elems_mid, region_res

    def get_region_names(
        self, region_res: dict, res_type: str, regions: List[str]
    ) -> List[str]:
        regions_out = []
        result_keys = region_res[res_type].keys()
        for key in result_keys:
            if regions[0] == "all" or key in regions:
                regions_out.append(key)

        return regions_out

    def clean(self):
        self._clean_sim_files()

    def plot_scalar(self, res_type, regions, zero_dim=2):

        nodes_reg, elems_nodes, region_res = self.read_cfs_results()
        regions = self.get_region_names(region_res, res_type, regions)

        values = np.zeros((1,))
        nodes = np.zeros((1, 2))

        fig, ax = plt.subplots()

        for region in regions:

            values = np.concatenate(
                (
                    values,
                    np.sqrt(np.sum(region_res[res_type][region] ** 2, axis=1)),
                )
            )
            nodes = np.row_stack((nodes, elems_nodes[region][:, :2]))

        ax.scatter(nodes[:, 0][:, None], nodes[:, 1][:, None], c=values[:, None])

        plt.show()

        return nodes, values

    def plot_quiver(self, res_type, regions, Nth: int = 1):

        nodes_reg, elems_nodes, region_res = self.read_cfs_results()

        coord = np.zeros((1, 3))
        Ev = np.zeros((1, 3))
        E = np.zeros((1,))

        for region in regions:
            pruner = np.arange(0, elems_nodes[region].shape[0], Nth)
            coord = np.row_stack((coord, elems_nodes[region][pruner, :]))
            Ev = np.row_stack((Ev, region_res[res_type][region][pruner, :]))
            E = np.concatenate(
                (
                    E,
                    np.sqrt(np.sum(region_res[res_type][region] ** 2, axis=1)[pruner]),
                )
            )

        ax = plt.figure().add_subplot(projection="3d")

        norm = matplotlib.colors.Normalize()
        norm.autoscale(E)
        cm = matplotlib.cm.jet

        sm = matplotlib.cm.ScalarMappable(cmap=cm, norm=norm)
        sm.set_array([])

        q = ax.quiver(
            coord[:, 0],
            coord[:, 1],
            coord[:, 2],
            Ev[:, 0],
            Ev[:, 1],
            Ev[:, 2],
            cmap="jet",
            length=0.001,
            normalize=True,
        )
        q.set_array(E)

        plt.colorbar(sm)
