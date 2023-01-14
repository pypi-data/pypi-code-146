import shutil
import os


def blend_file_gen(blend_file_path):
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    blender_template_file = os.path.join(dir_path,'template_files', 'blender.blend')
    # file_name = os.path.basename(blend_file_path)
    shutil.copy(blender_template_file, blend_file_path)

def task_directories(working_file_path):
    if working_file_path[0] == '/':
        file_directory = f'{working_file_path[1:]}'
        base_svn_directory = f"{file_directory.split('/', 2)[1]}:/{file_directory.split('/', 2)[2]}"
    else:
        file_directory = f'{working_file_path}'
        base_svn_directory = f"{file_directory.split('/', 3)[2]}:/{file_directory.split('/', 3)[3]}"
    return file_directory, base_svn_directory
def format_file_name(name):
    formated_name = name.replace(' ', '_').lower()
    return formated_name