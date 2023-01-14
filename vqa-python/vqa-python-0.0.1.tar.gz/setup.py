import setuptools
# f = open("./requirements.txt", "r")
# def process(txt):
#     return txt.replace("\n", "")
# requirements = list(map(process, f.readlines()))
requirements = ["streamlit",\
"pyyaml==5.1",\
"torch",\
"numpy",\
"transformers",\
"tensorflow",\
"unidecode",\
"torchvision",\
"gdown"]
setuptools.setup(
    name="vqa-python",
    version="0.0.1",
    author="Trương Xuân Linh",
    author_email="truonglinh1342001@gmail.com",
    description="mVQA tool",
    long_description="mVQA tool",
    long_description_content_type="text/markdown",
    url="https://github.com/truong-xuan-linh/mVQA-webapp",
    package_data={'': ['*.json', '*.yml']},
    install_requires= requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)