import os
import random
import re


def validate_data(data):
    """Validates if the data is in correct GAIuS digestible format.
    Returns True if data validates.  Returns False if data does not validate."""
    if not isinstance(data, dict):
        raise Exception("Incorrect data type.  Must be a dictionary.")
    if "vectors" not in list(data.keys()) or "emotives" not in list(data.keys()) or "strings" not in list(
            data.keys()):
        raise Exception('Dictionary requires "vectors", "emotives", and "strings" as keys!')
    for key in list(data.keys()):
        if key not in ["vectors", "emotives", "strings"]:
            raise Exception("Key: %s, should not be in the data dictionary!")
    if data["strings"]:
        if not isinstance(data["strings"], list):
            raise Exception('"strings" must be a list of strings.  List not provided!')
        for item in data["strings"]:
            if not (isinstance(item, str) or isinstance(item, str)):
                raise Exception('"strings" must be a list of strings or unicode objects!')
    if data["emotives"]:
        if not isinstance(data["emotives"], dict):
            raise Exception('"emotives" must be a dict of <str, float>. Dict not provided!')
        for item in data["emotives"]:
            if not isinstance(item, (int, float)):
                raise Exception('"emotives" must be a dict of <str, float>!')
    if data['vectors']:
        if not isinstance(data["vectors"], list):
            raise Exception('"vectors" must be a list of arrays.  List not provided!')
        for item in data["vectors"]:
            if not isinstance(item, list):
                raise Exception('"vectors" must be a list of arrays (i.e. lists)!')
    return True


def raw_in_count(filename):
    return int(os.popen("sed -n '$=' '%s'" % filename).readline().split()[0])


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split(r'(\d+)', text)]


class DataRecords:
    """Splits data into random sets for training and testing."""

    def __init__(self, original_dataset, DR, DF, shuffle, folder=True):
        """
        DR = fraction of total data to use for testing and training.
        DF = fraction of the DR to use for training.  The rest of the DR is used for testing.
        """
        if folder:
            original_dataset = [original_dataset + '/' + f for f in os.listdir(original_dataset) if
                                not f.startswith('.') and not f.startswith('_')]
            original_dataset.sort(key=natural_keys)
        DR = DR / 100
        DF = DF / 100
        try:
            if DR == 1 and DF == 1:
                self.train_sequences = original_dataset
                self.test_sequences = []
            else:
                if shuffle:
                    random.shuffle(original_dataset)

                num_files = len(original_dataset)
                num_use_files = int(num_files * DR)  ## use a fraction of the whole set

                num_train_sequences = int(num_use_files * DF)  ## train 2/3rds, test 1/3rd
                num_test_sequences = num_use_files - num_train_sequences

                self.train_sequences = original_dataset[:num_train_sequences]
                self.test_sequences = original_dataset[num_train_sequences:(num_train_sequences + num_test_sequences)]
        except Exception as exception:
            print(f'DataRecords BROKE by {exception.args}')
            raise


class Data:
    def __init__(self, data_directories=None, dataset=None):
        """Supply either a list of data_directories, or a dataset."""
        if data_directories is not None:
            self.data_directories = data_directories
            self.dataset = None
        elif dataset is not None:
            self.data_directories = None
            self.dataset = dataset
        self.train_sequences = []
        self.test_sequences = []
        self.train_sequences_classes = []
        self.test_sequences_classes = []

    def prep(self, percent_of_dataset_chosen, percent_reserved_for_training, shuffle=False):
        if self.data_directories:
            data = [DataRecords(d, percent_of_dataset_chosen, percent_reserved_for_training, shuffle, folder=True) for d
                    in self.data_directories]  ## It's a list because the user may pick several data file directories.
        elif self.dataset:
            data = [DataRecords(self.dataset, percent_of_dataset_chosen, percent_reserved_for_training, shuffle,
                                folder=False)]

        self.train_sequences = []
        self.test_sequences = []
        for d in data:
            self.train_sequences += d.train_sequences
            self.test_sequences += d.test_sequences
