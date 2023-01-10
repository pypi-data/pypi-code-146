import copy
import json
import os
from functools import lru_cache
from pathlib import Path
from slugify import slugify

from itsimodels.core.base_models import ConfModel, ImageModel

from itsicli.content_packs.backup.extract_models import DA_ITSI_CP_ICON_PREFIX
from itsicli.content_packs.model_formats import to_conf, to_image, image_file_extension
from itsicli.content_packs.content_types import ContentTypes
from itsicli.setup_logging import logger

CONTENT_PACK_SCREENSHOTS_DIR = ('appserver', 'static', 'screenshots')
ITSI_DIR = 'itsi'

class NullAttributeError(Exception):
    """Raised when attribute value is unexpected null"""
    pass

class ContentPackConfig(object):

    file_name = 'config.json'
    file_dir = ITSI_DIR
    attr_id = 'id'
    attr_title = 'title'
    attr_description = 'description'
    attr_version = 'version'

    def __init__(self, home_path):
        self.path = home_path.joinpath(self.file_dir, self.file_name)
        self.data = {}

        self.read()

        # cp_id = self.get_cp_id()
        # if cp_id:
        #     self.verify_dir_matches_cp_id(cp_id)

    def get_cp_id(self):
        if self.data and self.data.get('id'):
            return self.data.get('id')

    def get_cp_title(self):
        if self.data and self.data.get('title'):
            return self.data.get('title')

    def verify_dir_matches_cp_id(self, cp_id):

        if not cp_id:
            msg = "\nContent pack id not provided."
            logger.error(msg)
            raise InvalidWorkspace(msg)

        curr_dir_name = os.path.basename(os.getcwd())
        if not curr_dir_name == cp_id:
            msg = '\n'.join([
                "\nContent pack id {} does not match the working directory name {}".format(
                    cp_id, curr_dir_name
                ),
                "\nMake sure you're in the correct directory, or fix the content pack id ",
                "in your config.json to match the working directory name."
            ])
            logger.error(msg)
            raise InvalidWorkspace(msg)


    def read(self):
        if not self.exists():
            return

        with open(self.path, 'r') as fobj:
            contents = fobj.read()

        self.data = json.loads(contents)

    def update(self, data):
        self.data.update(data)

    def write(self):
        data = copy.deepcopy(self.data)

        data.setdefault(self.attr_description, '')
        data.setdefault(self.attr_version, '1.0.0')

        with open(self.path, 'w') as fobj:
            fobj.write(json.dumps(data, sort_keys=True, indent=4))

    def exists(self):
        return self.path.exists()

    def __getattr__(self, name):
        if name in (
                self.attr_id,
                self.attr_title,
                self.attr_description,
                self.attr_version
        ):
            return self.data.get(name)

        logger.error('attribute {} does not exist'.format(name))
        raise self.__getattribute__(name)


class ContentPackManifest(ContentPackConfig):

    file_name = 'manifest.json'
    file_dir = ITSI_DIR
    attr_main_screenshot = 'main_screenshot'
    attr_screenshots = 'screenshots'

    def add_content_model(self, content_model):
        content_type = content_model.content_type
        content_objects = self.data.setdefault(content_type, [])

        file_name = str(content_model.model_file.file_name)
        content_objects.append(file_name)

    def write(self):
        data = copy.deepcopy(self.data)

        data.setdefault(self.attr_main_screenshot, {
            'thumb': None,
            'path': None
        })
        data.setdefault(self.attr_screenshots, [])

        for content_type in ContentTypes.keys():
            content_objects = data.get(content_type, [])
            if not content_objects:
                continue

            data[content_type] = sorted(list(set(content_objects)))

        with open(self.path, 'w') as fobj:
            fobj.write(json.dumps(data, sort_keys=True, indent=4))

    def __getattr__(self, name):
        data_keys = list(ContentTypes.keys())
        data_keys.extend([
            self.attr_main_screenshot,
            self.attr_screenshots
        ])

        if name in data_keys:
            return self.data.get(name)

        logger.error('attribute {} does not exist'.format(name))
        raise self.__getattribute__(name)


class ModelFile(object):

    file_extension = 'json'

    def __init__(self, model, skip_key_mapping, prefix=''):
        self.model = model
        self.skip_key_mapping = skip_key_mapping
        self.prefix = prefix

    @property
    def contents(self):
        json_str = json.dumps(self.model.to_dict(), sort_keys=True, indent=4)
        return json_str.encode('utf-8')

    @property
    def file_name(self):
        if self.skip_key_mapping:
            title = self.model.get_title()
            if not title:
                raise NullAttributeError(f'title value is null for {type(self.model)} {self.model.get_key()}')

            slugified_title = slugify(title)
            if slugified_title.startswith(self.prefix) or \
                slugified_title.startswith(DA_ITSI_CP_ICON_PREFIX):
                prefix = ''
            else:
                prefix = self.prefix
            return Path(
                '{prefix}{model_title}.{ext}'.format(
                    prefix = prefix,
                    model_title=slugified_title,
                    ext=self.file_extension
                )
            )
        else:
            return Path(
                '{model_key}.{ext}'.format(
                    model_key=self.model.get_key(),
                    ext=self.file_extension
                )
            )

class ModelConfFile(ModelFile):

    file_extension = 'conf'

    @property
    def contents(self):
        return to_conf(self.model).encode('utf-8')


class ModelImageFile(ModelFile):

    @property
    def contents(self):
        return to_image(self.model)

    @property
    def file_extension(self):
        return image_file_extension(self.model)


    @property
    def file_name(self):
        # for both skip_key_mapping=True/False
        # we will take the key because this is
        # what is referenced eventually by the
        # glass table
        return Path(
            '{model_key}.{ext}'.format(
                model_key=self.model.get_key(),
                ext=self.file_extension
            )
        )

class ContentModel(object):

    model_file_types = {
        ConfModel: ModelConfFile,
        ImageModel: ModelImageFile
    }

    @classmethod
    def create_model_file(cls, model, skip_key_mapping=False, prefix=''):
        model_file_class = ModelFile

        for base_model_class, file_class in cls.model_file_types.items():
            if issubclass(model.__class__, base_model_class):
                model_file_class = file_class
                break

        return model_file_class(model, skip_key_mapping, prefix)

    def __init__(self, root_path, model, skip_key_mapping=False, prefix=''):
        self.skip_key_mapping = skip_key_mapping
        self.prefix = prefix
        self.root_path = root_path.joinpath(ITSI_DIR)
        self.model_file = self.create_model_file(model, self.skip_key_mapping, self.prefix)

    def write(self):
        os.makedirs(self.path.parent, exist_ok=True)

        with open(self.path, 'wb') as fobj:
            fobj.write(self.model_file.contents)

    @property
    @lru_cache(maxsize=1)
    def content_type(self):
        for content_type, model_class in ContentTypes.items():
            if model_class == self.model_file.model.__class__:
                return content_type
        return None

    @property
    def path(self):
        content_type_dir = self.root_path.joinpath(self.content_type)

        return content_type_dir.joinpath(self.model_file.file_name)

class InvalidWorkspace(Exception):
    """Thrown when the current path isn't a valid workspace"""
