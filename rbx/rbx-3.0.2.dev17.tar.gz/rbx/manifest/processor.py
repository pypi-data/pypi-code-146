import json
import operator
import zipfile
from collections import namedtuple
from collections.abc import MutableSequence
from enum import Enum, auto
from io import BytesIO

import cv2
import numpy as np
import requests

from .utils import flatten, make_transparent_image, make_white_image, px_to_int
from ..aws.s3 import S3Bucket
from ..exceptions import FatalException

CreativeVariant = namedtuple("CreativeVariant", ["filename", "name", "image"])
Variant = namedtuple("Variant", ["name", "multiplier"])


class FetchMode(Enum):
    S3 = auto()
    HTTP = auto()


class Modal(type):
    def __call__(cls, mode, *args, **kwargs):
        if mode is FetchMode.S3:
            return type.__call__(S3AssetFetcher, *args, **kwargs)
        else:
            return type.__call__(HttpAssetFetcher)


class AssetFetcher(metaclass=Modal):
    Mode = FetchMode

    def get_image(self, *args, **kwargs):
        return NotImplementedError

    def get_manifest(self, *args, **kwargs):
        return NotImplementedError


class HttpAssetFetcher(AssetFetcher):
    def __init__(self):
        self.base_url = None

    def get_image(self, url, base_url=None):
        """Retrieve Image from http, decode it using opencv and return the decoded image.

        Parameters:
            url (str):
                The location of the image to retrieve.
            base_url (str):
                The base location of the image to retrieve, if overriding the manifest.

        Returns:
            ndarray:
                An opencv representation of the retrieved image,
        """
        if self.base_url is None and base_url is None:
            raise FatalException(f"A Base URL must be provided: {url}")

        else:
            base_url = base_url if base_url is not None else self.base_url
            response = requests.get(f"{base_url}{url}")
            if not response.status_code == 200:
                raise FatalException(
                    f"Image not found at specified location: {base_url}{url}"
                )
            img_data = response.content
        decoded_image = cv2.imdecode(
            np.asarray(bytearray(img_data)), cv2.IMREAD_UNCHANGED
        )
        # if the image fails to be read, then it will be None
        if decoded_image is None:
            raise FatalException(f"Image has an invalid format: {base_url}{url}")
        return decoded_image

    def get_manifest(self, url):
        """Retrieve Manifest from HTTP (expecting a JSON format) and return the decoded dict.

        Parameters:
            url (str):
                The location of the manifest to retrieve.

        Returns:
            dict:
                The decoded JSON, stored as a dict.
        """
        response = requests.get(url)
        if response.status_code != 200:
            raise FatalException(f"Manifest not found at specified location: {url}")
        try:
            manifest = response.json()
        except json.decoder.JSONDecodeError:
            raise FatalException(f"Manifest has an invalid format: {url}")

        self.base_url = manifest.get("base_url")
        if self.base_url.startswith("//"):
            self.base_url = f"http:{self.base_url}"
        return manifest


class S3AssetFetcher(AssetFetcher):
    def __init__(self, bucket=None, region=None, endpoint_url=None):
        """
        Setup the asset fetcher and prepare a client.

        Parameters:
            bucket (str):
                The bucket to use when retrieving from S3.
            region (str):
                The region to use when retrieving from S3.
            endpoint_url (str):
                Override the endpoint. Only used for testing and should normally not be set.
        """
        self.client = S3Bucket(name=bucket, region=region, endpoint_url=endpoint_url)

    def get_image(self, url):
        """Retrieve Image from S3, decode it using opencv and return the decoded image.

        Parameters:
            url (str):
                The location of the image to retrieve.

        Returns:
            ndarray:
                An opencv representation of the retrieved image,
        """
        image = self.client.get_key(f"{url}")
        if image is None:
            raise FatalException(
                f"Image not found at specified location: " f"{self.client.name}/{url}"
            )
        img_data = image.get()["Body"].read()

        decoded_image = cv2.imdecode(
            np.asarray(bytearray(img_data)), cv2.IMREAD_UNCHANGED
        )
        # if the image fails to be read, then it will be None
        if decoded_image is None:
            raise FatalException(
                "Image has an invalid format: {}{}".format(
                    self.client.name + "/",
                    url,
                ),
            )
        return decoded_image

    def get_manifest(self, url):
        manifest_data = self.client.get_key(url)
        if manifest_data is None:
            raise FatalException(
                f"Manifest not found at specified location: {self.client.name}/{url}"
            )
        try:
            file_content = manifest_data.get()["Body"].read()
            manifest = json.loads(file_content)
        except UnicodeDecodeError:
            raise FatalException(f"Manifest has an invalid format: {url}")

        return manifest


class ComponentSequence(MutableSequence):
    """A mutable sequence of components."""

    def __init__(self):
        self.components = []

    def __len__(self):
        """The length includes the length of its components."""
        length = len(self.components)
        for component in self.components:
            length += len(component)
        return length

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value):
        self.components[key] = value

    def __delitem__(self, key):
        del self.components[key]

    def append(self, component, client, variant):
        result = make_component(component, client, variant)
        self.components.append(result)

    def insert(self, value):
        self.components.insert(value)


class CreativeBuilder:
    """Builds and returns all variations of Creatives that the manifest describes.

    As there can potentially be many variations of creatives, the creative builder is responsible
    for calculating all variations, passing one variant to each Creative for rendering.
    This allows us to calculate and apply the variant logic in a central location.
    """

    def __init__(self, manifest_url, client):
        self.manifest = client.get_manifest(manifest_url)
        self.client = client
        self.variations = self.unpack_variants()

    def unpack_variants(self):
        """Calculates all variations that need to be generated for a given manifest.

        Returns:
            list:
                A list of Variant objects that describe the changes that need to be applied to the
                creative.
        """
        variations = []

        pixel_ratios = self.manifest.get("pixel_ratios")

        for pixel_multiplier, pixel_name in pixel_ratios.items():
            variations.append(
                Variant(name=pixel_name, multiplier=int(pixel_multiplier))
            )
        return variations

    def build(self):
        """Builds and returns all possible variations of Creatives, as described in the Manifest.

        Returns:
            list:
                A list of CreativeVariant objects that describe the filename, human readable name
                and image data.
        """
        creatives = []

        for variant in self.variations:
            creative = Creative(
                manifest=self.manifest, client=self.client, variant=variant
            )

            creatives.append(
                CreativeVariant(
                    filename=f"final_image{variant.name}.png",
                    name=creative.name,
                    image=creative.render(),
                )
            )

        return creatives


class Creative:
    def __init__(self, client, manifest, variant):
        self.manifest = manifest
        self.client = client
        self.variant = variant

        root = self.manifest.get("root_component")
        self.height = px_to_int(root["css"]["height"]) * variant.multiplier
        self.width = px_to_int(root["css"]["width"]) * variant.multiplier
        self.left = px_to_int(root["css"]["left"]) * variant.multiplier
        self.top = px_to_int(root["css"]["top"]) * variant.multiplier

        self.root_component = make_component(root, self.client, variant)

    @property
    def name(self):
        """Uses the creative variant details to return the appropriate human readable name.

        Returns:
            str:
                The human readable name.
        """
        name = "Creative"

        if self.variant.multiplier > 1:
            name = f"Retina {name} {self.variant.multiplier}x Ratio"

        return name

    def render(self):
        """Builds an opencv image representation of the manifest and return.

        We start by making a white canvas, whose size is defined by the root component. We then
        call the compile function of the root component, which should call the nested compile/render
        functions of all sub components. This is then returned as a nested, ordered list of images
        that are ready to be flattened and applied to the solid root image (base canvas).

        Returns:
            ndarray:
                An opencv representation of the final image.
        """

        root_image = make_white_image(height=self.height, width=self.width)

        ordered_images = self.root_component.compile()

        flattened_images = list(flatten(ordered_images))
        for entry in flattened_images:
            root_image = merge_images(
                background_image=root_image,
                overlay_image=entry,
                left=self.left,
                top=self.top,
                transparent_background=False,
            )

        return root_image


class Component(ComponentSequence):
    def __init__(self, component, client, variant):
        super(Component, self).__init__()
        self.client = client
        self.variant = variant
        self.top = px_to_int(component["css"]["top"]) * variant.multiplier
        self.left = px_to_int(component["css"]["left"]) * variant.multiplier
        self.height = px_to_int(component["css"]["height"]) * variant.multiplier
        self.width = px_to_int(component["css"]["width"]) * variant.multiplier
        self.z_index = component["css"]["z-index"]


class LayoutComponent(Component):
    """A Component which has child Component."""

    def __init__(self, component, client, variant):
        """Initialises the ImageComponent.

        For a LayoutComponent, we need to add the child components that it has underneath it.

        Parameters:
            component (dict): The details of the component.
            client (S3Bucket): The S3 client to use instead of http, if needed.
            variant (Variant): The variant details to apply to the component.
        """
        super(LayoutComponent, self).__init__(
            component=component, client=client, variant=variant
        )
        children = component.get("component_manifests")

        for child_component in children:
            self.append(child_component, self.client, self.variant)

    def compile(self):
        """
        Gets all sub-components of the layer and applies each of them to a transparent canvas.

        This allows the positional data of both the image and the layer to be correctly applied, for
        an accurate final merge with the base canvas.

        Returns:
            list:
                A list of ndarray images, each applied to the transparent canvas.
        """
        transparent_image = make_transparent_image(self.height, self.width)

        images = []

        for entry in sorted(self.components, key=operator.attrgetter("z_index")):
            flattened_entry = flatten(entry.compile())
            for flat_entry in flattened_entry:
                images.append(
                    merge_images(
                        background_image=transparent_image,
                        overlay_image=flat_entry,
                        left=entry.left,
                        top=entry.top,
                        transparent_background=True,
                    )
                )

        return images


class ImageComponent(Component):
    """A component that describes an image."""

    def __init__(self, component, client, variant):
        """Initialises the ImageComponent, storing the location of the Image file.

        Parameters:
            component (dict): The details of the component.
            client (S3Bucket): The S3 client to use instead of http, if needed.
            variant (Variant): The variant details to apply to the component.
        """
        super(ImageComponent, self).__init__(
            component=component, client=client, variant=variant
        )
        self.url = component.get("url")
        self.ext = component.get("ext")

    def compile(self):
        """Return the rendered image in an iterable format.

        Returns:
            list:
                Returns the image in an iterable, for easier handling in the base render function.
        """
        return [self.render()]

    def render(self):
        """Retrieve Image from http or S3, decode it using opencv and return the decoded image.

        Returns:
            ndarray:
                An opencv representation of the retrieved image,
        """
        return self.client.get_image(f"{self.url}{self.variant.name}{self.ext}")


def generate_name(multiplier):
    """Takes a retina multiplier and returns the appropriate human readable name.

    Parameters:
        multiplier (int): The retina multiplier associated with the image.

    Returns:
        str:
            The human readable name.
    """
    name = "Creative"

    if multiplier > 1:
        name = f"Retina {name} {multiplier}x Ratio"

    return name


def make_component(component, client, variant):
    """Takes a component and returns the appropriate sub-component.

    Parameters:
        component (dict): The details of the component.
        client (S3Bucket): The S3 client to use instead of http, if needed.
        variant (Variant): The variant details to apply to the component.

    Returns:
        any:
            A instance of a component sub-type.
    """
    component_type = component.get("component_type")

    if component_type == "layout":
        return LayoutComponent(component, client, variant)

    elif component_type == "image":
        return ImageComponent(component, client, variant)


def merge_images(
    background_image, overlay_image, left, top, transparent_background=False
):
    """Puts the overlay image on top of the background image.

    Will use the left and top to calculate the position of the overlay image relative to the
    background image. Any transparency the top image has will be applied, showing the background
    image where applicable. If transparent_background is set, the overlay image will completely
    overwrite the underlying image.

    This logic was sourced from https://stackoverflow.com/questions/14063070/14102014#14102014 with
    minor modifications to fit our needs.

    Parameters:
        background_image (ndarray):
            The opencv representation of the background image, on which the new image will apply.
        overlay_image (ndarray):
            The opencv representation of the overlay image, which is placed over background image.
        left (int):
            How far, in pixels, from the left the overlay image should be applied.
        top (int):
            How far, in pixels, from the top the overlay image should be applied.
        transparent_background (boolean):
            If the background is transparent, and therefore should be overwritten.

    Returns:
        ndarray:
            An opencv representation of the combined image.
    """
    # we need to copy the initial background/overlay params otherwise the originals get mutated
    background_copy = background_image.copy()
    overlay_copy = overlay_image.copy()

    # if the background doesn't have an alpha layer, add one (will always be solid)
    if background_copy.shape[-1] < 4:
        b_channel, g_channel, r_channel = cv2.split(background_copy)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        background_copy = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    # if the overlay doesn't have an alpha layer, add one (will always be solid)
    if overlay_copy.shape[-1] < 4:
        b_channel, g_channel, r_channel = cv2.split(overlay_copy)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        overlay_copy = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    # reposition overlay image
    y1, y2 = top, top + overlay_copy.shape[0]
    x1, x2 = left, left + overlay_copy.shape[1]

    # if the background is transparent, overwrite all pixels in the background with the overlay
    if transparent_background:
        background_copy[y1:y2, x1:x2] = overlay_copy
    else:
        # apply overlay image to solid background image, keeping the background solid and blending
        # the colour and transparency of the overlay with the background colour to create an
        # accurate combined image

        # blend alpha channels
        alpha_s = overlay_copy[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        # merge colours and transparency for final effect
        for c in range(0, 3):
            background_copy[y1:y2, x1:x2, c] = (
                alpha_s * overlay_copy[:, :, c]
                + alpha_l * background_copy[y1:y2, x1:x2, c]
            )
    return background_copy


def zip_creatives(images, filename=None):
    """Combine all creatives in the iterable to a ZIP format.

    Parameters:
        images (list):
            A list of CreativeVariants with the filename, human name and ndarray image data.
        filename (str):
            The name of the zip file to output. If None, then returns a buffer representation.

    Returns:
        any:
            Returns either None if writing to file or BytesIO buffer if not saving file.
    """
    buffer = None
    if filename is None:
        buffer = BytesIO()
        zipf = zipfile.ZipFile(buffer, "w")
    else:
        zipf = zipfile.ZipFile(f"{filename}.zip", "w", zipfile.ZIP_DEFLATED)

    for data in images:
        retval, buf = cv2.imencode(".png", data.image)
        zipf.writestr(data.filename, buf)

    zipf.close()
    return buffer
