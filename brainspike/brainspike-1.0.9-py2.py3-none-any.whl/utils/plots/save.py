"""
save.py 

Utility functions for saving figure plots. 

"""

import os 

import matplotlib.pyplot as plt

###################################################################################################
###################################################################################################

def create_path(figdir, figname, figextension): 
    """
    Creates path and directory to save figures within a set subfolder and with a figurename. 
    
    Arguments
    ---------
    path (str): 
        basefolder name
    
    figname (str): 
        figure name
        
    file_extension (str): 
        file extension
    
    Returns
    -------
    Creates directory and outptus figure path for saving
    
    """

    isExist = os.path.exists(figdir) 
    if not isExist:
        os.makedirs(figdir)
        print(f"The new directory is created for {figdir}")
    fname = os.path.join(figdir, figname + figextension) # original df before visual inspection
    
    return fname

def save_figure(fig, image_name, image_set_name, image_dir, sizes, image_sets, scalew=1, scaleh=1, ext='png'):
    plt.figure(fig.number)

    if image_set_name not in image_sets:
        image_sets[image_set_name] = { size_name: [] for size_name in sizes }

    for size_name, size in sizes.items():
        fig.set_size_inches(size*scalew, size*scaleh)

        image_file = os.path.join(image_dir, "%s_%s.%s" % (image_name, size_name, ext))
        plt.savefig(image_file)

        image_sets[image_set_name][size_name].append(image_file)

    plt.close()