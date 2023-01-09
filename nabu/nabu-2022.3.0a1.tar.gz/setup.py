# coding: utf-8

from setuptools import setup, find_packages
import os
from nabu import version


def setup_package():
    doc_requires = [
        "sphinx",
        "cloud_sptheme",
        "myst-parser",
        "nbsphinx",
    ]
    setup(
        name="nabu",
        author="Pierre Paleo",
        version=version,
        author_email="pierre.paleo@esrf.fr",
        maintainer="Pierre Paleo",
        maintainer_email="pierre.paleo@esrf.fr",
        packages=find_packages(),
        package_data={
            "nabu.cuda": [
                "src/*.cu",
                "src/*.h",
            ],
            "nabu.resources": [
                "templates/*.conf",
            ],
        },
        include_package_data=True,
        install_requires=[
            "psutil",
            "pytest",
            "numpy > 1.9.0",
            "scipy",
            "silx >= 0.15.0",
            "h5py>=3.0",
            "tomoscan >= 1.0.6",
            "tifffile",
        ],
        extras_require={
            "full": [
                "pyfftw",
                "scikit-image",
                "PyWavelets",
                "glymur",
                "pycuda",
                "scikit-cuda",
                "pycudwt",
            ],
            "doc": doc_requires,
        },
        description="Nabu - Tomography software",
        entry_points={
            "console_scripts": [
                "nabu=nabu.app.reconstruct:main",
                "nabu-config=nabu.app.bootstrap:bootstrap",
                "nabu-test=nabu.tests:nabu_test",
                "nabu-histogram=nabu.app.histogram:histogram_cli",
                "nabu-zsplit=nabu.app.nx_z_splitter:zsplit",
                "nabu-rotate=nabu.app.rotate:rotate_cli",
                "nabu-double-flatfield=nabu.app.double_flatfield:dff_cli",
                "nabu-generate-info=nabu.app.generate_header:generate_merged_info_file",
                "nabu-validator=nabu.app.validator:main",
                "nabu-helical=nabu.app.reconstruct_helical:main_helical",
                "nabu-helical-prepare-weights-double=nabu.app.prepare_weights_double:main",
                "nabu-stitching-config=nabu.app.bootstrap_stitching:bootstrap_stitching",
                "nabu-stitching=nabu.app.stitching:main",
                "nabu-cast=nabu.app.cast_volume:main",
                "nabu-compare-volumes=nabu.app.compare_volumes:compare_volumes_cli",
                "nabu-shrink-dataset=nabu.app.shrink_dataset:shrink_cli",
            ],
        },
        zip_safe=True,
    )


if __name__ == "__main__":
    setup_package()
