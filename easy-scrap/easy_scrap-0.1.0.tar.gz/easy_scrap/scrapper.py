"""
Main class that takes a query string as parameter & parses and saves images for that query
"""

import io
import logging
import os
from dataclasses import dataclass
from urllib.parse import quote

import requests
from PIL import Image

from .utils import download_page, scan_page

SEARCH_URL = 'https://www.google.com/search?q='
MAIN_DIR = "scrapped_images"


@dataclass
class GoogleImageScrapper:
    """Take a query string as argument and parse available images to download from Google Image
    search.

    Parameters
    ----------
    query : str
        keyword(s) to search for. May contain standard operators of google search, like site:{url}
    save_folder_name : Optional[str]
        name of the folder to save the images to. If not provided, query will be used as a name
        of the folder.
    n_images : int = 1
        maximal number of images to download
    extensions : iter = (".jpg", ".jpeg", ".png")
        extensions to search for


    Attributes
    ----------
    save_dir : str
        directory in which the images will be saved
    links : iter
        image urls parsed from Search Page
    count : int
        total number of downloaded images. Might not match with len(links) since there might be
        some broken links
    """
    query: str
    save_folder_name: str = None
    n_images: int = 1
    extensions: iter = (".jpg", ".jpeg", ".png")

    def __post_init__(self) -> None:
        """
        Create a search link based on given query & create a directory to save the scrapped
        images to
        """

        if self.save_folder_name is None:
            self.save_folder_name = self.query
        self.save_dir = os.path.join(MAIN_DIR, self.save_folder_name)
        os.makedirs(self.save_dir, exist_ok=True)

        search_url = SEARCH_URL + quote(self.query.encode("utf-8")) + "&tbm=isch"
        try:
            html_string = download_page(search_url)
        except Exception as exc:
            logging.error(str(exc))
            return  # Couldn't parse html

        self.links = scan_page(html=html_string, extensions=self.extensions, n_max=self.n_images)
        self.count = 0

    def download_all_images(self):
        """Scrap images and save them to predefined directory"""
        for j, link in enumerate(self.links):
            filename = f"{self.save_folder_name}_{str(j + 1)}"
            filepath = os.path.join(self.save_dir, filename)
            try:
                self.download_single_image(url=link, filepath=filepath)
                self.count += 1
            except Exception as exc:
                logging.error(str(exc))
        logging.info(f"Successfully downloaded %{self.count}% images out of {len(self.links)}")

    @staticmethod
    def download_single_image(url, filepath):
        """Download and save a single image from given url and save to filepath"""
        extension = url.rsplit(".", 1)[-1]
        response = requests.get(url, allow_redirects=True, timeout=30)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image.save(f"{filepath}.{extension}")
