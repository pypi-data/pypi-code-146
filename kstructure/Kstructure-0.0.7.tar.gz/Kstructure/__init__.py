import os

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

if 1>0:
    print("Creating Project Folders!!!!")
    create_project()
else:
    print("Something went worng!!!!")