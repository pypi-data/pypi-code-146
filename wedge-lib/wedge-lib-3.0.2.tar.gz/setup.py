#!/usr/bin/env python
import os
import setuptools

if __name__ == "__main__":
    version = os.environ.get("WEDGELIB_VERSION", "0.0.0")
    setuptools.setup(
        version=version,
    )
    if version == "0.0.0":
        print(
            "!!! Attention !!! \n"
            "La variable d'environnment WEDGELIB_VERSION n'est pas définie. "
            "Le build est configuré pour fonctionner automatiquement sur la création "
            "d'une release dans GitHub.\n"
            "NE PAS PUBLIER SUR PYPI CE BUILD"
        )
