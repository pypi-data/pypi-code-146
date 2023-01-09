import setuptools
from DePTH import __version__

with open("DESCRIPTION", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

HLA_I_model_name = 'HLA_I_all_match_one_hot_n_pos_3854_n_neg_19270_0001_dense2_n_units_64_16_dropout_p_2'
HLA_II_model_name = 'HLA_II_all_match_one_hot_n_pos_6622_n_neg_33110_0001_dense1_n_units_64_dropout_p_5'
data_file_list = ['data/for_encoders/*.csv', \
                  'data/for_encoders/*.tsv', \
                  'data/trained_models/'+HLA_I_model_name+'/assets', \
                  'data/trained_models/'+HLA_I_model_name+'/saved_model.pb', \
                  'data/trained_models/'+HLA_I_model_name+'/variables/*', \
                  'data/trained_models/'+HLA_II_model_name+'/assets', \
                  'data/trained_models/'+HLA_II_model_name+'/saved_model.pb', \
                  'data/trained_models/'+HLA_II_model_name+'/variables/*']

setuptools.setup(
    name = "DePTH",
    version = __version__,
    author="Si Liu",
    author_email="liusi2019@gmail.com",
    description = "DePTH provides neural network models for sequence-based TCR and HLA association prediction",
    long_description = long_description,
    long_description_content_type = "text/plain",
    url = "https://github.com/Sun-lab/DePTH",
    project_urls = {
        "Documentation": "https://github.com/Sun-lab/DePTH",
        "Bug Tracker": "https://github.com/Sun-lab/DePTH/issues",
    },
    license='MIT',
    entry_points={
        "console_scripts": ["DePTH=DePTH.main:main"]
        },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    #packages = setuptools.find_packages(where="DePTH"),
    #packages = ["DePTH"],
    packages = setuptools.find_packages(),
    include_package_data=True,
    package_data={'DePTH': data_file_list},
    python_requires = ">=3.9",
    install_requires=[
        'scikit-learn >= 1.0.2',
        'tensorflow >= 2.4.1',
        'pandas >= 1.4.2',
        'numpy >= 1.21.5',
        ]
)
