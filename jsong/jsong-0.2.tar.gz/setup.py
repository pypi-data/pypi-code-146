import setuptools

setuptools.setup(
    name = "jsong",
    version = "0.2",
    author = "OakTree",
    author_email = "thefirstoaktree@gmail.com",
    description = "Transorms website data from allmusic.com into usable json files",
    long_description = "jsong helps you avoid hours of manually copying data about musicians! Copy the link from the discography, or album of your choice musician and pass it to either of the methods (getDiscography & getAlbum). After a short time, you'll have a usable json file for your programming ventures!",
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)