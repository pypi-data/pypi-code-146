# ${copyright}

import json
import os

from collections import defaultdict

from itsicli.content_packs.backup.extract_models import extractor_registry
from itsicli.content_packs.backup.remap_keys import KeysUpdater
from itsicli.content_packs.content_types import get_content_type_for_model_class


BACKUP_DELIM = '___'


def get_backup_object_type(file_path):
    if not os.path.isfile(file_path):
        return None

    _, ext = os.path.splitext(file_path)
    if ext != '.json':
        return None

    filename = os.path.basename(file_path)
    parts = filename.split(BACKUP_DELIM)
    if len(parts) < 2:
        return None

    object_type = parts[1]

    return object_type


def read_backup_file(file_path):
    with open(file_path, 'r') as fobj:
        raw_data = fobj.read()

        try:
            data = json.loads(raw_data)
        except ValueError:
            data = []

    return data


class BackupConverter(object):

    def __init__(self, prefix='', skip_key_mapping=False):
        self.prefix = prefix
        self.remapped_keys = {}
        self.skip_key_mapping = skip_key_mapping

    def to_models(self, backup_dir):
        extracted_models = self.extract_models(backup_dir)

        updated_models = self.update_model_keys(extracted_models)
        return updated_models

    def extract_models(self, backup_dir):
        content_models = defaultdict(list)

        for root, _, files in os.walk(backup_dir):
            backup_files = [os.path.join(root, file_name) for file_name in files]

            for backup_file in backup_files:
                object_type = get_backup_object_type(backup_file)

                record = extractor_registry().get(object_type)
                if not record:
                    continue

                model_class, extractor_class = record

                raw_json = read_backup_file(backup_file)

                extractor = extractor_class(model_class, self.remapped_keys, self.prefix,
                                            self.skip_key_mapping)
                models = extractor.extract(raw_json)

                content_type = get_content_type_for_model_class(extractor.model_class)
                content_models[content_type].extend(models)

            break

        return content_models

    def update_model_keys(self, extracted_models):
        keys_updater = KeysUpdater(self.remapped_keys)

        for content_type, models in extracted_models.items():
            # we are replacing the ids of glass table images/icons still
            # even with skip_key_mapping=True. Thus, we still need to
            # do key updating for those images within glass tables.
            if self.skip_key_mapping and not content_type == 'glass_tables':
                continue
            for model in models:
                keys_updater.update(model)

        return extracted_models
