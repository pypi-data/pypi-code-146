from base64 import b64encode
import base64
import os
from pathlib import Path
import abc
from os import listdir
from PIL import Image
from os.path import isfile, join


class ResourceManagement(abc.ABC):
    """
    Image management to include in txp_web
    """

    def __init__(self, file_name: str):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.file_name = file_name
        self.resource_name = self.get_resource_name()
        self.full_path = self._get_resource_path()
        self.resource_name = self.get_resource_name()
        self.resource64 = self._resource_to_bytes()

    @abc.abstractmethod
    def get_resource_name(self):
        pass

    def _get_resource_path(self):
        """
        get the relative path from any resource from its name.
        """
        full_path = os.path.join(self.current_directory, self.resource_name, self.file_name)
        return full_path

    @abc.abstractmethod
    def get_local_html_resource(self, width):
        """
        returns the html from a local resource as an resource-64.
        """
        pass

    @abc.abstractmethod
    def _resource_to_bytes(self):
        pass


class ImageManagement(ResourceManagement):
    """
    Image management to include in txp_web
    """

    def __init__(self, file_name: str):
        super(ImageManagement, self).__init__(
            file_name
        )

    def get_resource_name(self):
        return "images"

    def _resource_to_bytes(self):
        """
        method that converts image to bytes
        """
        img_bytes = Path(self.full_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded

    def get_local_html_resource(self, width=60):
        """
        returns the html img from a local resource as an image64.
        """
        return f'<img src="data:image/jpeg;base64,{self.resource64}" width={width} align=”middle”/>'

    def get_local_html_responsive_resource(self, width=60):
        """
            returns the html img from a local resource as an image64 responsive.
            """
        return f'<img class="centrado" src="data:image/jpeg;base64,{self.resource64}" width={width} align=”middle”/>'

    def get_PIL_image_list(self, sub_directory_name):
        """
        returns the list with PIL images from a sub_directory in image resources
        """
        current_directory = os.path.dirname(os.path.realpath(__file__))
        full_path = os.path.join(current_directory, "images", sub_directory_name)
        onlyfiles = [f for f in listdir(full_path) if isfile(join(full_path, f))]
        images = []
        for i in onlyfiles:
            image = Image.open(full_path + "/" + i)
            images.append(image)
        return images


class VideoManagement(ResourceManagement):
    """
    Image management to include in txp_web
    """

    def __init__(self, file_name: str):
        super(VideoManagement, self).__init__(
            file_name
        )

    def get_resource_name(self):
        return "videos"

    def _resource_to_bytes(self):
        """
        method that converts image to bytes
        """
        with open(self.full_path, "rb") as f:
            raw_data = f.read()
            data = b64encode(raw_data).decode("utf-8")
            return data

    def get_local_html_resource(self, width):
        """
        returns the html video from a local resource as an b64 encode.
        """
        return f'<video class="centrado" alt="test" loop="true" autoplay="autoplay" controls="controls" id="vid" muted> <source src="data:video/mp4;base64,{self.resource64}" type="video/mp4" width={width}/>'


def get_resource_video_path(file):
    """
    get the relative path from any resource from its name.
    """
    current_directory = os.path.dirname(os.path.realpath(__file__))
    resources_path = os.path.join(current_directory, "videos", file)
    return resources_path

def get_resource_image_path(file):
    """
    get the relative path from any resource from its name.
    """
    current_directory = os.path.dirname(os.path.realpath(__file__))
    resources_path = os.path.join(current_directory, "images", file)
    return resources_path