import os
import pickle


# import fileio as io
# Path vs Directory
# Path is the directory to an object (a file)
# Path: Obj
# Directory: Folder


def get_subdirectories(baseDir):
    """ get sub-directories / sub-paths

    Args:
        baseDir (string or list): target directory(ies).

    Returns:
        list: (1d list): a *sorted* list of subdirectories / subpaths.
    """
    # Config
    skips = ['.DS_Store', '__pycache__', '.ipynb_checkpoints']

    if not isinstance(baseDir, list):
        baseDirs = [baseDir]

    dirList_all = []

    for basedir in baseDirs:
        dirList = os.listdir(basedir)

        for d in dirList:
            if os.path.basename(d) in skips:
                continue

            dirList_all.append(os.path.join(basedir, d))

    return sorted(dirList_all)  # Capital letter --> Small letter


def get_name_with_extion(dir):
    return os.path.basename(dir)


def get_name_without_extion(dir):
    return os.path.basename(dir).split('.')[0]


def make_dir(dir):
    try:
        os.makedirs(dir)
    except:
        return False
    return True


def write_pickle(save_dir, obj, obj_name='_test'):
    path = os.path.join(save_dir, '{}.pickle'.format(obj_name))

    with open(path, 'wb') as f:
        pickle.dump(obj, f)

    # In Python 2 document, while serializing, use '.pkl'
    # In Python 3 document, while serializing, use '.pickle'
    # # path == '../xxx.pkl'
    # with open(path, 'wb') as f:
    #     pickle.dump(obj, f)
    return None


def read_pickle(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj
