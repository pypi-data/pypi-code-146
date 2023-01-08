import os

allext = ['csv', 'csv']
j = "\\"

def allsubfolders(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(allsubfolders(dirname))
    return subfolders

###SEE ALL SUBFOLDERS IN A FOLDER
def onelevelsubfolders(dirname):
    folders = []
    for file in os.listdir(dirname):
        d = os.path.join(dirname, file)
        if os.path.isdir(d):
            folders.append(d)
    return folders        

###SEE ALL FILES IN A FOLDER              
def allextfiles1level(dirname):
    allfiles = []
    for files in os.listdir(dirname):
        if files.endswith(allext):
            allfiles.append(dirname+j+files)
    return allfiles