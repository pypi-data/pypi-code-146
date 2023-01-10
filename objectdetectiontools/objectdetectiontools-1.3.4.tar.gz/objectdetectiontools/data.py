def proportional_train_validation_split(data: list, validation_size: float, classes: list, random_state: int = 0):
    """
    Splits data into two lists named train and validation, where validation has a random sample of 'validation_size' from the total records in data, per class in `classes`.
    """
    import copy, random, math
    classList = copy.deepcopy(classes)
    random.seed(random_state)
    random.shuffle(classList)
    validation = []
    for name in classList:
        objs = [obj for obj in data if obj["name"] == name]
        filenames = list(set(obj["filename"] for obj in objs))
        sample_size = math.ceil(validation_size * float(len(filenames)))
        filenames = random.sample(filenames, k=sample_size)
        for obj in [obj for obj in data if obj["filename"] in filenames]:
            validation.append(obj)
        data = [obj for obj in data if not obj["filename"] in filenames]
    return data, validation

def stratified_test_split(data: list, test_size: float, random_state: int = 0):
    """
    Splits data into two lists, where the size of the second list is defined by `test_size` as a fraction of the total size of `data` in such a way that for each unique name in data an equal number of images will be selected by filenames to fill up `test_size`. Any name that appears in less images than 3 times the required number to fill the test will be removed as a sanity check. Aside from the 2 new lists, this function also returns a list of removed names, and the number of images that were selected per name.
    """
    import random, math
    random.seed(random_state)
    number_of_images = len(list(set(x["filename"] for x in data)))
    number_of_labels = len(list(set(x["name"] for x in data)))
    number_of_test_images = math.ceil(number_of_images * test_size / number_of_labels)
    test, selected, removed = [], [], []
    names = list(set(obj["name"] for obj in data))
    random.shuffle(names)
    for name in names:
        objs = [obj for obj in data if obj["name"] == name]
        filenames = list(set(obj["filename"] for obj in objs))
        if len(filenames) < number_of_test_images:
            removed.append(name)
        else:
            filenames = random.sample(filenames, k=number_of_test_images)
            for filename in filenames:
                selected.append({"name": name, "filename": filename})
            for obj in [obj for obj in data if obj["filename"] in filenames]:
                test.append(obj)
        data = [obj for obj in data if not obj["filename"] in filenames]
    for name in list(set(obj["name"] for obj in test)): # sanity check
        count = len(list(set(x["filename"] for x in data if x["name"] == name)))
        if count < 2 * number_of_test_images:
            test = [obj for obj in test if not obj["name"] == name]
            data = [obj for obj in data if not obj["name"] == name]
            selected = [x for x in selected if not x["name"] == name]
            removed.append(name)
    return data, test, selected, removed, number_of_test_images