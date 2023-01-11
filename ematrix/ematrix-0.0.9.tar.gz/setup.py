import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="ematrix",
    version="0.0.9",
    author="Zed",
    author_email="UnknowMan@example.com",
    description="A high performance matrix calculate package",
    long_description='long_description',
    long_description_content_type=long_description,
    url="https://github.com/lihua179/matrix_quant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)
