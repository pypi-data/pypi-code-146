
# importing the required modules
# check-private-packages-below-for-public-doppelgaenger
import os
import argparse
import requests
# end-of-private-packages

# error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .txt file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."

def validate_file(file_name):
    '''
    validate file path.
    '''
    if not valid_path(file_name):
        print(INVALID_PATH_MSG%(file_name))
        quit()
    return

 
def valid_path(path):
    # validate file path
    return os.path.exists(path)

def read(args):
    # get the file name/path
    file_name = args.read[0]

    # validate the file name/path
    # validate_file(file_name)
    validate_file(file_name)

    # read and print the file content
    with open(file_name, 'r') as f:
        return f.read()

def get_private_libraries(args):

    data = read(args)
    
    # parse out private libray section
    # beginning indicated by '# check-private-packages-below-for-public-doppelgaenger'
    # ending indicated by '# end-of-private-packages'
    try:
        data = data.split("# end-of-private-packages")[0]
        data = data.split("# check-private-packages-below-for-public-doppelgaenger")[-1]
    except:
        print("""Error in markings for private library section.\n
        Begin private library section with '# check-private-packages-below-for-public-doppelgaenger'.\n
        End private library section with '# end-of-private-packages'.""")
        return
    
    # parse out library names
    libraries = []
    
    for line in data.split():
        if line.split(" ")[0] in ["import","from"]:
            library = line.split(" ")[1]
            if "." in library:
                library = library.split(".")[0]
            libraries.append(library)
        elif len(line.strip()) > 1:
            library = line.split(" ")[0]
            if "." in library:
                library = library.split(".")[0]
            libraries.append(library)
    print(libraries)
    # check private libraries for public doppelgaengers
    doppelgaengers = []
    for library in libraries:
            public_url_path_to_check = f'https://www.pypi.org/project/{library}/'
            if requests.get(public_url_path_to_check).status_code == 200:
                doppelgaengers.append(library)
    if len(doppelgaengers) == 1:
        print(f'WARNING: doppelgaengers found for the following library: {doppelgaengers[0]}')
    elif len(doppelgaengers) > 1:
        print(f'WARNING: doppelgaengers found for the following libraries: {print(d) for d in doppelgaengers}')
    else:
        print("No doppelgaengers found for private libraries.")
            

def main():
    # create parser object
    parser = argparse.ArgumentParser(description = "A private vs public library checker!")
 
    # defining arguments for parser object
    parser.add_argument("-r", "--read", type = str, nargs = 1,
                        metavar = "file_name", default = None,
                        help = "Opens and reads the specified text file.")
    
    # parse the arguments from standard input
    args = parser.parse_args()
     
    # calling functions
    get_private_libraries(args)

 
 
if __name__ == "__main__":
    # calling the main function
    main()