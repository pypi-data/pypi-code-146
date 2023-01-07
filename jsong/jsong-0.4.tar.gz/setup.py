import setuptools

setuptools.setup(
    name = "jsong",
    version = "0.4",
    author = "OakTree",
    author_email = "thefirstoaktree@gmail.com",
    description = "Transorms website data from allmusic.com into usable json files",
    long_description = "jsong streamlines the process of copying data into json files\n\n For discographies: \n\tPick a link of your choice (e.g., https://www.allmusic.com/artist/taylor-swift-mn0000472102/discography, https://www.allmusic.com/artist/elton-john-mn0000796734/discography, etc.) and pass the url to the function getDiscography(URL_HERE)\n\nFor albums: \n\t Pick a link of your choice (https://www.allmusic.com/album/innervisions-mw0000192406, https://www.allmusic.com/album/a-night-at-the-opera-mw0000391519, etc.) and pass the url to the function getAlbum(URL_HERE)\n\nData is collected in part with the use of a Selenium webdriver; web pages will be periodically opened and closed in order to webscrape information. Please do not close these pages -- they will be automatically closed when the function has been executed. Thank you :)",
    long_description_content_type = "text/markdown",
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)