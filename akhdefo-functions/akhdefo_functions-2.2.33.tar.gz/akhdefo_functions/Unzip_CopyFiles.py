


def unzip(zipdir, dst_dir ):

    """
    This program unzips all the zip products into one folder
   

    zipdir: path to directory contains all the zipfiles

    dst_dir: path to destination folder to copy all unzipped products.

    """
    import os 
    import shutil
    from zipfile import ZipFile
    import glob
    import os
    from os import listdir
    from os.path import isfile, join
    if not os.path.exists( dst_dir):
        os.makedirs( dst_dir)
    dst_dir=dst_dir
    zipdir=zipdir
    zip_list = [f for f in sorted(os.listdir(zipdir)) if isfile(join(zipdir, f))]

    for n in range (0, len(zip_list)):
        with ZipFile(join(zipdir,zip_list[n]), 'r') as zipObject:
            listOfFileNames = zipObject.namelist()
            for fileName in listOfFileNames:
                if fileName.endswith('.tif'):
                    # Extract a single file from zip
                    zipObject.extract(fileName, dst_dir)
                    print('All the tif files are extracted')


def copyImage_Data(path_to_unzipped_folders=r"", Path_to_raster_tifs=""):
    """
    This program copy all the raster images
    """
    import os 
    import shutil
    from zipfile import ZipFile
    import glob
    import os
    from os import listdir
    from os.path import isfile, join

    if not os.path.exists( Path_to_raster_tifs):
        os.makedirs( Path_to_raster_tifs)

    S2_path = os.path.join (path_to_unzipped_folders)

    for subdir, dirs, files in os.walk(S2_path):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith("BGRN_SR_clip.tif"):
                print (filepath)
                shutil.copy2(filepath, Path_to_raster_tifs)


def copyUDM2_Mask_Data(path_to_unzipped_folders=r"", Path_to_UDM2raster_tifs=r""):

    """
    This program copy all  raster masks
    """
    
    import os 
    import shutil
    from zipfile import ZipFile
    import glob
    import os
    from os import listdir
    from os.path import isfile, join

    if not os.path.exists( Path_to_UDM2raster_tifs):
        os.makedirs( Path_to_UDM2raster_tifs)

    S2_path = os.path.join (path_to_unzipped_folders)

    for subdir, dirs, files in os.walk(S2_path):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith("udm2_clip.tif"):
                print (filepath)
                shutil.copy2(filepath, Path_to_UDM2raster_tifs)

    