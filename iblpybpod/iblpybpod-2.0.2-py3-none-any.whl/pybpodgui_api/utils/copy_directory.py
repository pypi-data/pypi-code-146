import os
import shutil


def copy_directory(src, dest):
    '''
    Copies a directory's contents (including subfolders) to a destination directory.
    .. note:: Existing files in the destination folder will NOT be copied.

    :param src: The source directory
    :param dest: The destination directory
    :return:
    '''
    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dest)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            shutil.copy(src_file, dst_dir)
