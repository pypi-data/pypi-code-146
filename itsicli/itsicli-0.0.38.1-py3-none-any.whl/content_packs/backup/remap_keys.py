# ${copyright}

import importlib
import re

from itsicli.setup_logging import logger
from itsimodels.core.fields import (
    DictField,
    ForeignKey,
    ForeignKeyList,
    ForeignKeyListStr,
    ForeignKeyMultiEmbeddedStr,
    ListField,
    TypeField
)
from itsimodels.core.base_models import BaseModel
from itsimodels.team import GLOBAL_TEAM_KEY

FIELDS_TO_REMAP = {
    'action.itsi_event_generator.param.service_ids': 'itsimodels.service.Service',
    'action.itsi_event_generator.param.ad_at_kpi_ids': 'itsimodels.service.Kpi'
}


class KeysUpdater(object):

    def __init__(self, remapped_keys):
        self.remapped_keys = remapped_keys

    def update(self, model):
        for field_name, field in model.fields.items():
            field_value = getattr(model, field_name, None)
            if field_value is None:
                continue

            if isinstance(field, ForeignKeyListStr):
                self.update_foreign_key_list_str(model, field_name, field)

            elif field_name in FIELDS_TO_REMAP.keys():
                self.update_field_keys_list_str(model, field_name)

            elif isinstance(field, ForeignKeyMultiEmbeddedStr):
                self.update_foreign_key_multi_embedded_str(model, field_name, field)

            elif isinstance(field, ForeignKey):
                self.update_foreign_key(model, field_name, field)

            elif isinstance(field, ForeignKeyList):
                self.update_foreign_key_list(model, field_name, field)

            elif isinstance(field, ListField) and field.subtype and issubclass(field.subtype, BaseModel):
                self.update_list_of_models(field_value)

            elif isinstance(field, DictField) and field.subtype and issubclass(field.subtype, BaseModel):
                self.update_dict_of_models(field_value)

            elif isinstance(field, TypeField) and field.type and issubclass(field.type, BaseModel):
                self.update(field_value)

        return model

    def update_foreign_key(self, model, field_name, field):
        old_key = getattr(model, field_name)

        if not old_key or (field.refers and field.refers == 'itsimodels.team.Team' and
                           field_name == 'team_id' and old_key == GLOBAL_TEAM_KEY):
            return

        if field.key_regex:
            match = re.search(field.key_regex, old_key, flags=re.IGNORECASE)
            if not match:
                logger.warning(
                    'WARNING: Not able to find match for replacement in field_name={} with value={} using regex={} model={}'.format(
                        field_name, old_key, field.key_regex, model
                    ))
                return

            parsed_old_key = match.groups()[0]

            remapped_key = self.get_remapped_key(field.refers, parsed_old_key)

            new_key = old_key.replace(parsed_old_key, remapped_key)

        else:
            new_key = self.get_remapped_key(field.refers, old_key)

        if not new_key:
            logger.warning(
                'WARNING: Keep old key because not able to find any new key to map to old key={} for model={} field_name={}'.format(
                    old_key, model, field_name
                ))
        elif new_key == old_key:
            logger.warning(
                'WARNING: Old key={} is the same as new key for Service template object having it in field_name={}. '
                'Please verify that this key is valid and is not a dangling pointer.'.format(
                    old_key, field_name
                ))
        else:
            setattr(model, field_name, new_key)

    def update_foreign_key_list(self, model, field_name, field):
        foreign_key_list = getattr(model, field_name)

        if not foreign_key_list:
            return

        new_keys = []

        for old_key in foreign_key_list:
            new_key = self.get_remapped_key(field.refers, old_key)
            if new_key == old_key:
                logger.warning(
                    'WARNING: Old key={} is the same as new key for Service template object having it in field_name={}. '
                    'Please verify that this key is valid and is not a dangling pointer.'.format(
                        old_key, field_name
                    ))
            new_keys.append(new_key)

        setattr(model, field_name, new_keys)

    def get_unique_keys(self, matched_keys, model, field_name, old_key_str):
        unique_keys = set()
        if not matched_keys:
            return unique_keys

        # depending on the regex, if there are multiple groups
        # the matched_keys would be a list of tuples where each tuple contains
        # the same number of groups where some will be filled in if a match
        # was found. some can be empty ''
        # if there's only 1 matching group then it is a list of matched strings
        for item in matched_keys:
            if isinstance(item, str):
                if item: unique_keys.add(item)
            elif isinstance(item, tuple):
                unique_keys.update((match_key for match_key in item if match_key))
            else:
                logger.error('ERROR: Invalid matched_key type {}. Not able to process \
keys for old key str={} for model={} field_name={}'.format(
                    type(item), old_key_str, model, field_name)
                )

        return unique_keys

    def get_matched_old_key_to_new_key(self, model, field_name, field):
        old_key_str = getattr(model, field_name)

        old_to_new_key = {}
        if not old_key_str:
            return old_to_new_key

        match = re.findall(field.key_regex, old_key_str)
        if not match:
            logger.warning('WARNING: Not able to find any foreign keys to replace for old \
key str={} for model={} field_name={}'.format(
                old_key_str, model, field_name
            ))
            return old_to_new_key

        unique_old_keys = self.get_unique_keys(match, model, field_name, old_key_str)

        # logger.info('****** unique_old_keys={}'.format(unique_old_keys))
        valid_warnings = 0
        for parsed_old_key in unique_old_keys:

            # if the old key starts with da-itsi-cp most likely it was already
            # replace in extractor logic, otherwise, should check if something is
            # amiss
            if parsed_old_key.startswith('da-itsi-cp-'):
                continue

            remapped_key = self.get_remapped_key(field.refers, parsed_old_key)
            if remapped_key == parsed_old_key:
                logger.warning(
                    'WARNING: Old key={} is the same as new key for Service template object having it in field_name={}. '
                    'Please verify that this key is valid and is not a dangling pointer.'.format(
                        parsed_old_key, field_name
                    ))
            if not remapped_key or remapped_key == parsed_old_key:
                logger.warning(
                    'WARNING: Not able to find any new key to map to old key={} for model={} field_name={}'.format(
                        parsed_old_key, model, field_name
                    ))
                valid_warnings += 1
                if not remapped_key: remapped_key = parsed_old_key

            # we will keep the mapping even if the old and new are the same
            # this is useful for foreign key list str where we are replacing
            # the entire str
            old_to_new_key[parsed_old_key] = remapped_key

        if not old_to_new_key and valid_warnings > 0:
            logger.warning(
                'WARNING: Not able to find any new key to map to any old keys str={} for model={} field_name={}'.format(
                    old_key_str, model, field_name
                ))
        else:
            logger.info('Will remap these keys from old-->new {} for old keys str={} model={} field_name={}'.format(
                old_to_new_key, old_key_str, model, field_name))
        return old_to_new_key

    def update_foreign_key_list_str(self, model, field_name, field):

        old_to_new_key_map = self.get_matched_old_key_to_new_key(model, field_name, field)

        if not old_to_new_key_map:
            return

        # assuming this type of foreign key string is a list of keys
        # separated by , we only need the new keys
        new_key_list = []
        for new_key in old_to_new_key_map.values():
            new_key_list.append(new_key)

        setattr(model, field_name, ','.join(new_key_list))

    def update_foreign_key_multi_embedded_str(self, model, field_name, field):
        old_key_str = getattr(model, field_name)
        if not old_key_str:
            return

        old_to_new_key_map = self.get_matched_old_key_to_new_key(model, field_name, field)
        if not old_to_new_key_map:
            return

        for old_key, new_key in old_to_new_key_map.items():
            replaced_str = old_key_str.replace(old_key, new_key)
            old_key_str = replaced_str

        setattr(model, field_name, replaced_str)

    def update_list_of_models(self, child_models):
        for child_model in child_models:
            self.update(child_model)

    def update_dict_of_models(self, dict_models):
        for _, child_model in dict_models.items():
            self.update(child_model)

    def get_remapped_key(self, model_import_name, old_key):
        if model_import_name:
            parts = model_import_name.split('.')
            pkg_name = '.'.join(parts[:-1])
            model_name = parts[-1]

            try:
                pkg = importlib.import_module(pkg_name)
            except ImportError as exc:
                logger.exception('ERROR: not able to import module {}'.format(pkg_name))
                return old_key

            model_class = getattr(pkg, model_name)

            new_keys = self.remapped_keys.get(model_class, {})

            new_key = new_keys.get(old_key, old_key)

            return new_key
        else:
            # this foreign key has no 'refers', which means we don't know
            # what kind of object key this belongs to(i.e. url in glass table
            # eventHandlers(event_handlers)-->options-->url)
            # we will go through all objects' remapped keys
            for _, model_key_map_dict in self.remapped_keys.items():
                new_key = model_key_map_dict.get(old_key, None)

                if new_key:
                    return new_key

            return old_key

    # this method maps comma separated keys in a string to new key format
    def update_field_keys_list_str(self, model, field_name):
        old_key_ids = getattr(model, field_name)
        updated_key_str_list = ''
        for old_key_id in old_key_ids.split(','):
            new_key_id = self.get_remapped_key(FIELDS_TO_REMAP.get(field_name), old_key_id)
            if new_key_id == old_key_id:
                logger.warning(
                    'WARNING: Old key={} is the same as new key for Service template object having it in field_name={}. '
                    'Please verify that this key is valid and is not a dangling pointer.'.format(
                        old_key_id, field_name
                    ))
            if updated_key_str_list == '':
                updated_key_str_list = updated_key_str_list + new_key_id
            else:
                updated_key_str_list = updated_key_str_list + ',' + new_key_id
        setattr(model, field_name, updated_key_str_list)
