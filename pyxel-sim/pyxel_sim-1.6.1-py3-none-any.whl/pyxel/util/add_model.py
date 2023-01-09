#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Functions to add new models."""

import logging
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Tuple


def create_model(newmodel: str) -> None:
    """Create a new module using pyxel/templates/MODELTEMPLATE.py.

    Parameters
    ----------
    newmodel: modeltype/modelname

    Returns
    -------
    None
    """

    location, model_name = get_name_and_location(newmodel)

    # Is not working on UNIX AND Windows if I do not use os.path.abspath
    template_string = "_TEMPLATE"
    template_location = "_LOCATION"

    # Copying the template with the user defined model_name instead
    import pyxel

    src = os.path.abspath(os.path.dirname(pyxel.__file__) + "/templates/")
    dest = os.path.abspath(
        os.path.dirname(pyxel.__file__) + "/models/" + location + "/"
    )

    if not os.path.exists(src):
        raise FileNotFoundError(f"Folder {src!r} does not exists !")

    try:
        os.makedirs(dest, exist_ok=True)
        # Replacing all of template in filenames and directories by model_name
        for dirpath, subdirs, files in os.walk(src):
            for x in files:
                if x.startswith(".") or x.endswith(".pyc"):
                    continue

                pathtofile = os.path.join(dirpath, x)
                new_pathtofile = os.path.join(
                    dest, x.replace(template_string, model_name)
                )
                shutil.copy(pathtofile, new_pathtofile)
                # Open file in the created copy
                with open(new_pathtofile) as file_tochange:
                    # Replace any mention of template by model_name
                    new_contents = file_tochange.read().replace(
                        template_string, model_name
                    )
                    new_contents = new_contents.replace(template_location, location)
                    new_contents = new_contents.replace("%(date)", time.ctime())

                Path(new_pathtofile).write_text(new_contents)
                # Close the file other we can't rename it
                file_tochange.close()

            for x in subdirs:
                if x == "__pycache__":
                    continue

                pathtofile = os.path.join(dirpath, x)
                os.mkdir(pathtofile.replace(template_string, model_name))
            logging.info("Module " + model_name + " created.")
        print(f"Module {model_name!r} created in {dest!r}.")

    except FileExistsError:
        logging.info(f"{dest} already exists, folder not created")
        raise
    # Directories are the same
    except shutil.Error as e:
        logging.critical("Error while duplicating " + template_string + ": %s" % e)
        raise
    # Any error saying that the directory doesn't exist
    except OSError as e:
        logging.critical(model_name + " not created. Error: %s" % e)
        raise


def get_name_and_location(newmodel: str) -> Tuple[str, str]:
    """Get name and location of new model from string modeltype/modelname.

    Parameters
    ----------
    newmodel: str

    Returns
    -------
    location: str
    model_name: str
    """

    try:
        arguments = newmodel.split("/")
        location = f"{arguments[0]}"
        model_name = f"{arguments[1]}"
    except Exception:
        sys.exit(
            f"""
        Can't create model {arguments}, please use location/newmodelname
        as an argument for creating a model
        """
        )
    return location, model_name
