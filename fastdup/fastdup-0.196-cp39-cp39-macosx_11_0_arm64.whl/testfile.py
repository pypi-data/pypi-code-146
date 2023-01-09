SUPPORTED_IMG_FORMATS = [".png", ".jpg", ".jpeg", ".giff", ".jpeg", ".tif", ".heic", ".heif"]
SUPPORTED_VID_FORMATS = ["mp4", ".avi"]
import os
import glob
import pandas as pd

def get_images_from_path(path):
    "List a subfoler recursively and get all image files supported by fastdup"
    # create list to store results

    assert os.path.isdir(path), "Failed to find directory " + path
    filenames = []
    ret = []
    # get all image files
    image_extensions = SUPPORTED_IMG_FORMATS
    image_extensions.extend(SUPPORTED_VID_FORMATS)
    filenames += glob.glob(f'{path}/**/*', recursive=True)

    for r in filenames:
        ext = os.path.splitext(r)
        if len(ext) < 2:
            continue
        ext = ext[1]
        if ext in image_extensions:
            ret.append(r)
    return ret


def list_subfolders_from_file(file_path):
    assert os.path.isfile(file_path)
    ret = []

    with open(file_path, "r") as f:
        for line in f:
            if os.path.isdir(line.strip()):
               ret += get_images_from_path(line.strip())

    assert len(ret), "Failed to find any folder listing from file " + file_path
    return ret


def shorten_path(path):
    if path.startswith('./'):
        path = path[2:]

    if path.endswith('/'):
        path = path[:-1]

    cwd = os.getcwd()
    if (path.startswith(cwd + '/')):
        path = path.replace(cwd + '/', '')

    return path

def check_if_folder_list(file_path):
    assert os.path.isfile(file_path), "Wrong file " + file_path
    if file_path.endswith('yaml'):
        return False
    with open(file_path, "r") as f:
        for line in f:
            return os.path.isdir(line.strip())
    return False

def save_as_csv_file_list(filenames, files_path):
     files = pd.DataFrame({'filename':filenames})
     files.to_csv(files_path)
     return files_path


def expand_list_to_files(the_list):
    assert len(the_list), "Got an emplty list for input"
    files = []
    for f in the_list:
        if f.startswith("s3://") or f.startswith("minio://"):
            assert False, "Unsupported mode: can not run on lists of s3 folders, please list all files in s3 and give a list of all files each one in a new row"
        if os.path.isfile(f):
            files.append(f)
        else:
            files.extend(get_images_from_path(f))
    assert len(files), "Failed to extract any files from list"
    return files

if __name__ == "__main__":
    print(expand_list_to_files(['../unittests/two_images','../unittests/one_image']))