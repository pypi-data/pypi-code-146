import os
import shutil
def create_project():
    current_directory = os.getcwd()
    folders_to_create = ['config', 'data', 'docs', 'models', 'notebooks', 'utils']
    for i in folders_to_create:
        final_directory = os.path.join(current_directory, i)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)


    # READ ME file creation

    with open(os.path.join(current_directory, 'README.txt'), 'w') as file:
        l1 = "Project Description : \n\n\n"
        l2 = "Step to run the app: \n\n\n"
        l3 = "Primary Contact : \n\n\n"
        l4 = "Secondary contact : \n\n\n"
        file.writelines([l1, l2, l3, l4])

    # Requirement.txt
    with open(os.path.join(current_directory, 'requirements.txt'), 'w') as reqfile:
        reqfile.writelines(['django'])
        
content = """
import sys\n\n

REQUIRED_PYTHON = "python3"\n\n


def main():\n\
    system_major = sys.version_info.major\n
    if REQUIRED_PYTHON == "python":\n
        required_major = 2\n
    elif REQUIRED_PYTHON == "python3":\n
        required_major = 3\n
    else:
        raise ValueError("Unrecognized python interpreter: {}".format(\n
            REQUIRED_PYTHON))\n

    if system_major != required_major:\n
        raise TypeError(\n
            "This project requires Python {}. Found: Python {}".format(\n
                required_major, sys.version))\n
    else:\n
        print(">>> Development environment passes all tests!")\n\n


if __name__ == '__main__':\n
    main()\n


"""
try:
    print("Creating Project Folders!!!!")
    create_project()
    current_directory = os.getcwd()
    with open(os.path.join(current_directory, 'test_environment.py'), 'w') as testfile:
        testfile.writelines([content])
except:
    print("Something went worng!!!!")