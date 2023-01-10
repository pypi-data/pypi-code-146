import os

LEVELS = 2

def old_tree(root_path: str, depth: int = 0) -> None:
    """
    Prints a tree of directories and files.
    """
    # exclude hidden files
    files_list = os.listdir(root_path)
    files_list = [f for f in files_list if not f.startswith('.')]

    # print the directories
    for dir in os.listdir(root_path):
        if os.path.isdir(os.path.join(root_path, dir)):
            tree(os.path.join(root_path, dir), depth + 1)
    for dir_name in files_list:
        dir_path = os.path.join(root_path, dir_name)
        if os.path.isdir(dir_path):
            # full file_name (path)
            file_name = os.path.join(root_path, dir_name)
            if not file_name.startswith('.'):
                print(' ' * depth * LEVELS , file_name)
                tree(dir_path, depth + 1)
        else:
            file_name = os.path.join(root_path, dir_name)
            if not file_name.startswith('./.git'):
                print(' ' * depth * LEVELS, file_name)
                
                
def tree(path,show_files=False,full_path=0, indentation=2,file_output=False):
    """
    Shows the content of a folder in a tree structure.
    path -(string)- path of the root folder we want to show.
    show_files -(boolean)-  Whether or not we want to see files listed.
                            Defaults to False.
    indentation -(int)- Indentation we want to use, defaults to 2.   
    file_output -(string)-  Path (including the name) of the file where we want
                            to save the tree.
    """
    tree = []
    
    if not show_files:
        for root, dirs, files in os.walk(path):
            if not root.startswith('./.'): # TODO: parametrize this
                level = root.replace(path, '').count(os.sep)
                indent = ' '*indentation*(level)
                tree.append('{}{}/'.format(indent,os.path.basename(root)))

    if show_files:
        for root, dirs, files in os.walk(path):
            if not root.startswith('./.'): # TODO: parametrize this
                level = root.replace(path, '').count(os.sep)
                indent = ' '*indentation*(level)
                tree.append('{}{}/'.format(indent,os.path.basename(root)))    
                for f in files:
                    if full_path: f = os.path.join(root, f)
                    subindent=' ' * indentation * (level+1)
                    tree.append('{}{}'.format(subindent,f))

    if file_output:
        output_file = open(file_output,'w')
        for line in tree:
            output_file.write(line)
            output_file.write('\n')
    else:
        # Default behaviour: print on screen.
        for line in tree:
            print(line)