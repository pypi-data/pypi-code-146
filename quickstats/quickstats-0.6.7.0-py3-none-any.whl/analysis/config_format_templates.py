from quickstats import ConfigComponent

DEFAULT_SAMPLE_CONFIG_FORMAT = {
    "sample_dir": ConfigComponent(dtypes="STR", default="./",
                                  description="directory in which the input root samples are located"),
    "sample_subdir": ConfigComponent(dtypes="DICT[STR]", default_factory=dict,
                                     description="(optional) a dictionary mapping the sample type to the sub-directory "
                                                 "of input root samples in which the input root samples are located; "
                                                 "examples of sample type are the mc campaigns and data year for "
                                                 "mc and data samples respectively"),
    "samples": ConfigComponent(dtypes=["DICT[DICT[STR]]", "DICT[DICT[LIST[STR]]]"], required=True,
                               description="A map from the sample name to the sample path in the form "
                                           "{<sample_type>: <sample_path>}; if path is given by an "
                                           "absolute path, the absolute path is used, otherwise the path "
                                           "{sample_dir}/{sample_subdir}/{path} is used",
                               example='"sample_name": {"ggF": {"mc16a": "ggF_mc16a.root", "mc16d": "ggF_mc16d.root"}}'),
    "merge_samples": ConfigComponent(dtypes="DICT[LIST[STR]]", default_factory=dict,
                                     description="merge the given list of samples into a sample with a given name in "
                                                 "the form {<merged_sample_name>: <list_of_samples_to_be_merged>}",
                                     example='"merge_samples": {"H": ["ggF", "VBF", "VH", "ttH"]}')
}

DEFAULT_ANALYSIS_CONFIG_FORMAT = {
    "paths": {
        "ntuples": ConfigComponent(dtypes="STR", default="./ntuples",
                                   description="path to analysis data in root format as precursor to analysis "
                                               "data arrays"),
        "arrays" : ConfigComponent(dtypes="STR", default="./arrays",
                                   description="path to analysis data in csv/h5 format used for "
                                               "model training and statistical analysis"),
        "outputs": ConfigComponent(dtypes="STR", default="./outputs",
                                   description="path to analysis outputs"),
        "models": ConfigComponent(dtypes="STR", default="./models",
                                  description="path to machine learning models"),
        "*": ConfigComponent(dtypes="STR",
                             description="any named path")
    },
    "samples": {
        "all": ConfigComponent(dtypes="LIST[STR]", default_factory=list,
                               description="list of all analysis samples"),
        "extra": ConfigComponent(dtypes="LIST[STR]", default_factory=list,
                                 description="list of additional analysis samples that exist only "
                                             "in the form of data arrays (i.e. not ntuples)"),
        "*"  : ConfigComponent(dtypes="LIST[STR]",
                               description="list of analysis samples belonging to a group with the given key",
                               example='"signal": ["ggH", "VBF", "VH", "ttH"]')
    },
    "kinematic_regions": ConfigComponent(dtypes="LIST[STR]", default_factory=list,
                                         description="kinematic regions of the analysis; if defined, input "
                                                     "datasets are assumed to be split according to these "
                                                     "regions; these regions typically correpond to the "
                                                     "relevant analysis channels",
                                         example='"kinematic_regions": ["zero_jet", "one_jet", "two_jet"]'),
    "variables":{
        "all": ConfigComponent(dtypes="LIST[STR]", default_factory=list,
                               description="list of all input variables"),
        "*"  : ConfigComponent(dtypes="LIST[STR]",
                               description="list of input variables belonging to a group with the given key",
                               example='"jets": ["jet1_pt", "jet1_eta", "jet2_pt", "jet2_eta"]')
    },
    "names": {
        "tree_name": ConfigComponent(dtypes="STR", default="output",
                                     description="tree name of ntuples used in the analysis"),
        "event_number": ConfigComponent(dtypes="STR", default="event_number",
                                        description="variable name that describes the event number of an event"),
        "*": ConfigComponent(dtypes="STR",
                             description="name of any key object in the analysis"),
    },
    "observable":{
        "name": ConfigComponent(dtypes="STR",
                                description="name of discriminant variable"),
        "eval_expr": ConfigComponent(dtypes=["STR", "NONE"], default=None,
                                     description="expression to evaluate to the discriminant from existing input variables"),
        "bin_range": ConfigComponent(dtypes="LIST[FLOAT]",
                                     description="bin range"),
        "blind_range": ConfigComponent(dtypes=["LIST[FLOAT]", "NONE"], default=None,
                                       description="blind range"),
        "n_bins": ConfigComponent(dtypes="INT",
                                  description="number of bins"),
    },    
    "training": {
        "datasets":{
            "specification": {
                "*": {
                    "selection": ConfigComponent(dtypes="STR",
                                                 description="selection applied to obtain the given dataset",
                                                 example='"training":{"specification":{"train_dataset": "event_number % 4 <= 2"'
                                                         ', "test_dataset": "event_number %4 == 3}})'),
                    "variables": ConfigComponent(dtypes="LIST[STR]", default_factory=list,
                                                 description="list of variables that should be loaded on top of the "
                                                             "training variables to perform the dataset selection"),
                    "effective_weight": ConfigComponent(dtypes="FLOAT", default=1,
                                                        description="effective weight of the dataset with respect "
                                                                    "to the inclusive data")
                }
            },
            "split_method": ConfigComponent(dtypes="STR", default="kfold",
                                            description="how to split the dataset for training; custom = use the "
                                                        "datasets defined in `specification`; kfold = split the "
                                                        "full dataset (or a dataset in `specification`) into k folds "
                                                        "; index = select data from a given set of indices (per-sample) "
                                                        "which can be the entry number or a column number;"
                                                        " manual = use a custom function to split data;",
                                            choice=["custom", "kfold", "index", "manual"]),
            "split_options": {
                "*": ConfigComponent(dtypes="ANY",
                                     description="option specific to a given split method")
            }
        },
        "sample_transformation":{
            "normalize_weight": ConfigComponent(dtypes="BOOL", default=False,
                                                description="whether to normalize the event weight in each sample")
        },
        "dataset_transformation":{
            "scale_weight_by_mean": ConfigComponent(dtypes="BOOL", default=False,
                                                    description="whether to rescale the event weight by the mean in"
                                                                 " the train/val/test datasets after samples are"
                                                                 " merged to the corresponding classes"),
            "negative_weight_mode": ConfigComponent(dtypes="INT", default=0,
                                                    description="how to treat negative weights: 0 = no action performed; "
                                                                "1 = set weight to 0; 2 = set weight to absolute value",
                                                    choice=[0, 1, 2]),
            "random_state": ConfigComponent(dtypes=["INT", "NONE"], default=-1,
                                            description="random state for shuffling data; if negative, "
                                                        "no shuffling will be made; if None, the global "
                                                        "random state instance from numpy.random will "
                                                        "be used (so every shuffle will give a different "
                                                        "result)")
        }
    },
    "categorization":{
        "boundary_scan":{
            "selection": ConfigComponent(dtypes="DICT[STR]", default_factory=dict,
                                         description="(per-sample) selection applied when performing boundary scan"),
            "datasets": ConfigComponent(dtypes=["LIST[STR]", "None"], default_factory=list,
                                        description="dataset(s) that should take non-zero weight when peroforming "
                                                    "boundary scan; this is typically the test dataset; if empty, "
                                                    "the full dataset is used"),
            "adaptive_dataset": ConfigComponent(dtypes="BOOL", default=True,
                                                description="use full dataset for samples not used in training and "
                                                            "the specified dataset for samples used in training")
        },
        "evaluation":{
            "datasets": ConfigComponent(dtypes=["LIST[STR]", "None"], default_factory=list,
                                        description="dataset(s) that should take the total weight when saving "
                                                    "the categorized outputs; this is typically the test dataset; "
                                                    "if empty, the full dataset is used"),
            "adaptive_dataset": ConfigComponent(dtypes="BOOL", default=True,
                                                description="use full dataset for samples not used in training and "
                                                            "the specified dataset for samples used in training")
        },
        "save_variables": ConfigComponent(dtypes="LIST[STR]", default_factory=list,
                                          description="additional variables to save in the categorized outputs"),
    },
    "data_storage":{
        "analysis_data_arrays": {
            "storage_format": ConfigComponent(dtypes="STR", default="csv",
                                              description="file format used to store the data",
                                              choice=["csv", "h5"]),
            "storage_options": ConfigComponent(dtypes="DICT", default_factory=dict,
                                               description="storage options specific to a given storage format",
                                               example='csv format: no storage options required; '
                                                       'h5 format: {"key": "analysis_data", "complevel": 5}')
        }
    },
    "channels":{
        "*":{
            "selection": ConfigComponent(dtypes=["STR", "NONE"], default=None,
                                         description="selection applied on the input variables to isolate the phase "
                                                     "space for the given channel",
                                         example='"channel": {"LowPtRegion": {"selection": "jet_pt < 125"}}'),
            "selection_variables": ConfigComponent(dtypes=["LIST[STR]", "NONE"], default=None,
                                                   description="variables used for applying the channel selection"), 
            "kinematic_region": ConfigComponent(dtypes=["STR", "NONE"], default=None,
                                                description="kinematic region corresponding to the given channel"),
            "train_samples": ConfigComponent(dtypes="LIST[STR]",
                                             description="training samples used for the given channel (group label is allowed)",
                                             example='"channel": {"LowPtRegion": {"train_samples": ["signal", "yj", "yy"]}}'),
            "test_samples": ConfigComponent(dtypes="LIST[STR]",
                                            description="test samples used for the given channel (group label is allowed); "
                                                        "categorized outputs will be produced for these samples",
                                            example='"channel": {"LowPtRegion": {"test_samples": ["all"]}}'),
            "train_variables": ConfigComponent(dtypes="LIST[STR]",
                                               description="training variables used for the given channel (group label is allowed)",
                                               example='"channel": {"LowPtRegion": {"train_variables": ["jets", "pt_H", "m_H"]}}'),
            "class_labels":ConfigComponent(dtypes="DICT[LIST[STR]]",
                                           description="a dictionary that maps the class label used in training "
                                                       "to the corresponding samples",
                                           example='"channel": {"LowPtRegion": {"class_labels": {"0": '
                                                   '["yj", "yy"], "1": ["signal"]}}}'),
            "hyperparameters": ConfigComponent(dtypes="DICT", default_factory=dict,
                                               description="a dictionary specifying the hyperparameters used in the training",
                                               example='"channel": {"LowPtRegion": {"hyperparameters": '
                                                       '{"learning_rate": 0.01, "batchsize": 100}}}'),
            "SF": ConfigComponent(dtypes="DICT", default_factory=dict,
                                  description="a dictionary that maps the scale factor applied to the weight "
                                              "of a sample used in the training",
                                  example='"channel": {"LowPtRegion": {"SF": {"ggF": 100, "VBF": 50}}}'),
            "counting_significance":{
                "?":{
                    "signal": ConfigComponent(dtypes="LIST[STR]",
                                              description="the samples designated as signals when evaluating the counting "
                                                          "significance in score boundary scans (group label is allowed)",
                                              example='"channel": {"LowPtRegion": {"counting_significance": '
                                                      '{"signal": ["ggF", "VBF"]}}}'),
                    "background": ConfigComponent(dtypes="LIST[STR]",
                                                  description="the samples designated as backgrounds when evaluating the "
                                                              "counting significance in score boundary scans (group label "
                                                              "is allowed)",
                                                  example='"channel": {"LowPtRegion": {"counting_significance": '
                                                          '{"background": ["yj", "yy"]}}}'),
                    "n_bins": ConfigComponent(dtypes="INT",
                                              description="Number of bins used in score boundary scan; notice the "
                                                          "scan time and memory consumption grow exponentially with "
                                                          "the number of bins used"),
                    "n_boundaries": ConfigComponent(dtypes="INT",
                                                    description="Number of score boundaries to apply; you will get "
                                                                "(n_boundaries + 1) categories for the given channel "
                                                                "if all categories are kept"),
                    "min_yield": ConfigComponent(dtypes="DICT[FLOAT]", default_factory=dict,
                                                 description="Minimum yield of specific samples required in all score regions",
                                                 example='"channel": {"LowPtRegion": {"counting_significance": '
                                                         '{"min_yield": {"yy": 2}}}}')
                }
            },
            "exclude_categories": ConfigComponent(dtypes="LIST[LIST[INT]]", default_factory=list,
                                                  description="Remove specific categories from the analysis by their "
                                                              "category index; [0] is the first bin of a 1D (binary "
                                                              "class) boundary scan, [0, 0] is the first bin of a 2D "
                                                              "(multiclass, e.g. [score_signal_1, score_signal_2]) "
                                                              "boundary scan",
                                                  example='"channel": {"LowPtRegion": {"exclude_categories": [[0]]')
        }
    }
}