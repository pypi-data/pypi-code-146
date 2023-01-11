def xander_ingestion(configuration, ingestion_function, dataset):
    """
    Standard xander.py function used for data ingestion.

    @param configuration:
    @param ingestion_function:
    @param dataset: dataset to be ingested
    @return: dataset
    """

    if ingestion_function:
        dataset = ingestion_function(configuration, dataset)

    return dataset


def xander_encoder(configuration, encoding_function, dataset):
    """
    Standard xander.py function used for data encoding.

    @param configuration:
    @param encoding_function:
    @param dataset: dataset to be ingested
    @return: dataset
    """

    if encoding_function:
        dataset = encoding_function(configuration, dataset)

    return dataset


def xander_splitter(configuration, split_function, dataset):
    """
    Standard xander.py function used for dataset split.

    @param configuration:
    @param split_function:
    @param dataset: dataset to be ingested
    @return: dataset
    """

    train, test = dataset, dataset

    if split_function:
        train, test = split_function(configuration, dataset)

    return train, test


def xander_feature_selection(configuration, feature_selection_function, train, test):
    """
    Standard xander.py function used for feature selection.

    @param test: test dataset
    @param train: train dataset
    @param configuration:
    @param feature_selection_function:
    @return: dataset
    """

    features_selected = []

    if feature_selection_function:
        features_selected = feature_selection_function(configuration, train, test)

    return train, test, features_selected


def xander_model_training(configuration, model, validation_func, test_func, train, test, features_selected):
    """
    Standard xander.py function used for model training, validation and test.

    @param features_selected:
    @param test:
    @param train:
    @param test_func:
    @param validation_func:
    @param model:
    @param configuration:
    @return: dataset
    """

    performance = {}

    model.fit(train[features_selected])

    return model, performance, train, test, features_selected


def xander_model_evaluator(confgiuration, model, performance, train, test, features_selected):

    return confgiuration, model, performance, train, test, features_selected
