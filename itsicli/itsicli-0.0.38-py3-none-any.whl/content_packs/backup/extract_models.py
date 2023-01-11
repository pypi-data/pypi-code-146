import re
from itsicli.content_packs.model_formats import IMAGE_MIMETYPE_TO_EXT
from itsicli.setup_logging import logger

from copy import deepcopy
from slugify import slugify

from itsimodels.core.base_models import KEY_FIELD_NAME, ValidationError
from itsimodels.correlation_search import CorrelationSearch
from itsimodels.deep_dive import DeepDive
from itsimodels.entity_type import EntityType
from itsimodels.event_management_state import EventManagementState
from itsimodels.glass_table import GlassTable
from itsimodels.glass_table_icon import GlassTableIcon
from itsimodels.glass_table_image import GlassTableImage
from itsimodels.kpi_base_search import KpiBaseSearch, SearchMetric
from itsimodels.kpi_threshold_template import KpiThresholdTemplate
from itsimodels.neap import NotableEventAggregationPolicy
from itsimodels.service import Kpi, Service
from itsimodels.service_analyzer import ServiceAnalyzer
from itsimodels.service_template import ServiceTemplate
from itsimodels.team import Team, GLOBAL_TEAM_KEY
from itsicli.content_packs.backup.field_decode import BackupFieldDecoder

DA_ITSI_CP_ICON_PREFIX = 'da-itsi-cp-icon-'
OOTB_CP_ID_PREFIX_CONTAINING_DASH = [
    'da-itsi-cp-aws-dashboards-', 'da-itsi-cp-cloud-foundry-',
    'da-itsi-cp-example-gts-', 'da-itsi-cp-itew-alerting-content-',
    'da-itsi-cp-microsoft-exchange-', 'da-itsi-cp-monitoring-alerting-',
    'da-itsi-cp-monitoring-splunk-', 'da-itsi-cp-netapp-dashboards-',
    'da-itsi-cp-shared-infra-', 'da-itsi-cp-splunk-infra-monitoring-',
    'da-itsi-cp-splunk-observability-', 'da-itsi-cp-splunk-synthetics-',
    'da-itsi-cp-thirdparty-apm-', 'da-itsi-cp-unix-dashboards-',
    'da-itsi-cp-vmware-dashboards-', 'da-itsi-cp-windows-dashboards-'
]
def extractor_registry():
    return {
        'base_service_template': (ServiceTemplate, Extractor),
        'correlation_search': (CorrelationSearch, ConfExtractor),
        'deep_dive': (DeepDive, Extractor),
        'entity_type': (EntityType, EntityTypeExtractor),
        'event_management_state': (EventManagementState, Extractor),
        'glass_table': (GlassTable, GlassTableExtractor),
        'glass_table_icons': (GlassTableIcon, GlassTableIconExtractor),
        'glass_table_images': (GlassTableImage, GlassTableImageExtractor),
        'home_view': (ServiceAnalyzer, ServiceAnalyzerExtractor),
        'kpi_base_search': (KpiBaseSearch, KpiBaseSearchExtractor),
        'kpi_threshold_template': (KpiThresholdTemplate, Extractor),
        'notable_aggregation_policy': (NotableEventAggregationPolicy, Extractor),
        'service': (Service, ServiceExtractor),
        'team': (Team, TeamExtractor)
    }


class Extractor(object):

    def __init__(self, model_class, remapped_keys, prefix='', skip_key_mapping=False):
        self.model_class = model_class
        self.remapped_keys = remapped_keys
        self.prefix = prefix
        self.skip_key_mapping = skip_key_mapping

    def extract(self, raw_data):
        models = []

        for content in raw_data:
            model_data = self.extract_model_data(content)
            if not model_data:
                continue

            try:
                logger.debug('Validating model_data="{}"'.format(model_data))

                model = self.model_class(model_data, field_decoder=BackupFieldDecoder())
            except ValidationError as exc:
                message = 'ERROR: Failed to extract {}'.format(self.model_class)
                print(message)
                logger.error(message)
                logger.exception(exc)
            else:
                models.append(model)

        return models

    def extract_model_data(self, raw_data):
        immutable = str(raw_data.get('_immutable', 0))
        if immutable == '1' or immutable.lower() == 'true':
            return None

        object_key = self.get_object_key(raw_data)
        if not object_key:
            return None

        object_title = self.get_object_title(raw_data)
        if not object_title:
            return None

        if not self.skip_key_mapping:
            old_object_key, new_object_key = self.apply_prefix(raw_data)
            self.remap_keys(old_object_key, new_object_key)
            raw_data[self.key_field] = new_object_key

        return raw_data

    def apply_prefix(self, raw_data):
        old_object_key = raw_data.get(self.raw_key_field)

        object_title = self.get_object_title(raw_data)

        cleaned_title = self.remove_cp_id_prefix(object_title)
        new_object_key = '{}{}'.format(self.prefix, slugify(cleaned_title))

        return old_object_key, new_object_key

    def remap_keys(self, old_object_key, new_object_key):
        if not old_object_key:
            return

        remapped_keys = self.remapped_keys.setdefault(self.model_class, {})
        remapped_keys[old_object_key] = new_object_key

    def get_object_key(self, raw_data):
        return raw_data.get(self.raw_key_field)

    def get_object_title(self, raw_data):
        return raw_data.get('title', '')

    def get_object_name(self, raw_data):
        return raw_data.get('name', '')

    def remove_cp_id_prefix(self, to_be_cleaned):
        """Remove cp id prefix from a title/string

        If we are repackaging a CP item into a different CP we
        would want to remove the old prefix first before applying
        another prefix.
        this will work for removing the common icon prefix as well
        because we are looking for a pattern that also works for
        it.
        Limitation:
        This will remove things like 'da-itsi-cp-xxxxxx-' or
        'da-itsi-cp-cust-xxxxx-'. However, it will not remove something
        like 'da-itsi-cp-unix-dashboards-' where the CP id contains '-'
        For future OOTB content pack, it is best to use '_' instead of
        '-' in the CP id. also see bug: https://splunk.atlassian.net/browse/ITSI-27626
        We are hard coding the pre-existing OOTB CP-id prefix for cleaning
        """

        for prefix in OOTB_CP_ID_PREFIX_CONTAINING_DASH:
            if to_be_cleaned.startswith(prefix):
                return(to_be_cleaned[len(prefix):])

        updated_string = to_be_cleaned
        if to_be_cleaned.startswith('da-itsi-cp-'):
            updated_string = re.sub(r'da-itsi-cp-([\w_]+?)-', '', to_be_cleaned)
        elif to_be_cleaned.startswith('da-itsi-cp-cust-'):
            updated_string = re.sub(r'da-itsi-cp-cust-([\w_]+?)-', '', to_be_cleaned)

        return updated_string

    @property
    def raw_key_field(self):
        key_field = getattr(self.model_class, KEY_FIELD_NAME)
        return key_field.alias

    @property
    def key_field(self):
        return self.raw_key_field

class ConfExtractor(Extractor):

    def extract_model_data(self, raw_data):
        content = super(ConfExtractor, self).extract_model_data(raw_data)

        data = deepcopy(content)
        data.pop('object_type', None)

        if self.skip_key_mapping:
            # correlation search doesn't have 'key' field
            # because we skipped key map in extract_model_data
            # we need to set it here
            data[self.key_field] = self.get_object_key(raw_data)

        return data

    def get_object_title(self, raw_data):
        return self.get_object_key(raw_data)

    @property
    def raw_key_field(self):
        return 'name'

    @property
    def key_field(self):
        return KEY_FIELD_NAME


class ServiceExtractor(Extractor):

    SERVICE_HEALTH_SEARCH_RE = r'`get_full_itsi_summary_service_health_events\((.+)\)`'

    def extract_model_data(self, raw_data):
        old_service_key = raw_data[self.raw_key_field]

        model_data = super(ServiceExtractor, self).extract_model_data(raw_data)

        if not self.skip_key_mapping:
            service_key = model_data[self.raw_key_field]

            kpi_remapped_keys = self.remapped_keys.setdefault(Kpi, {})

            kpis = raw_data.get('kpis', [])

            for kpi in kpis:
                old_kpi_key = kpi.get('_key', '')

                if kpi.get('type') == 'service_health':
                    new_kpi_key = 'SHKPI-{}'.format(service_key)

                    if old_kpi_key == new_kpi_key:
                        continue # already in new format

                    base_search = kpi.get('base_search', '')
                    kpi['base_search'] = base_search.replace(old_service_key, service_key)

                    search = kpi.get('search', '')
                    kpi['search'] = search.replace(old_service_key, service_key)
                else:
                    if old_kpi_key.startswith(self.prefix):
                        continue # already in new format

                    cleaned_key = self.remove_cp_id_prefix(old_kpi_key)
                    new_kpi_key = '{}{}'.format(self.prefix, cleaned_key)

                kpi['_key'] = new_kpi_key
                kpi_remapped_keys[old_kpi_key] = new_kpi_key

        service_tags = raw_data.get('service_tags', {})
        if isinstance(service_tags, list) and not service_tags:
            # The default value of service tags is unfortunately an empty list, but
            # the model definition expects a dictionary in order to pass model validation
            raw_data['service_tags'] = {}

        return model_data


class TeamExtractor(Extractor):

    def extract_model_data(self, raw_data):
        if raw_data[self.raw_key_field] == GLOBAL_TEAM_KEY:
            return None

        return super(TeamExtractor, self).extract_model_data(raw_data)


class GlassTableExtractor(Extractor):

    def extract_model_data(self, raw_data):
        definition = raw_data.get('definition')
        if not definition:
            return None

        self.fix_series_colors(definition)

        return super(GlassTableExtractor, self).extract_model_data(raw_data)

    def fix_series_colors(self, definition):
        visualizations = definition['visualizations']
        if not visualizations:
            return

        for key, value in visualizations.items():
            if value['type'] == 'viz.area' and value['options']:
                series_colors = value['options']['seriesColors']
                if not series_colors or isinstance(series_colors, list):
                    continue

                if not isinstance(series_colors, str):
                    continue

                # observed there's cases where instead of a list
                # backup contains the value a string: '[#FFFFFF]'
                # this causes problem when we are validating it as
                # a list field, thus converting to list if applicable
                series_colors = re.sub('[\[\]]', '', series_colors)
                series_colors_list = re.split(',', series_colors)
                value['options']['seriesColors'] = series_colors_list


class GlassTableImageExtractor(Extractor):

    def extract_model_data(self, raw_data):
        immutable = str(raw_data.get('immutable', 0))
        if immutable == '1' or immutable.lower() == 'true':

            return None

        object_key = self.get_object_key(raw_data)
        if not object_key:
            return None

        old_object_key, new_object_key = self.apply_prefix(raw_data)

        self.remap_keys(old_object_key, new_object_key)

        # for images, we are still doing key replacement to
        # help with image identification
        raw_data[self.raw_key_field] = new_object_key

        return raw_data


    def get_img_name_without_suffix(self, raw_data):
        object_name = self.get_object_name(raw_data)

        type = raw_data.get('type')
        if not type:
            return object_name

        suffix = IMAGE_MIMETYPE_TO_EXT[type]
        if suffix and object_name.endswith(suffix):
            return object_name[:-len(suffix)]

        return object_name


    def apply_prefix(self, raw_data):
        old_object_key = raw_data.get(self.raw_key_field)

        object_name = self.get_img_name_without_suffix(raw_data)

        if object_name.startswith(self.prefix):
            new_object_key = slugify(object_name)
        else:
            cleaned_name = self.remove_cp_id_prefix(object_name)
            new_object_key = '{}{}'.format(self.prefix, slugify(cleaned_name))

        return old_object_key, new_object_key


class GlassTableIconExtractor(GlassTableImageExtractor):

    def update_title(self, new_title, raw_data):
        raw_data['title'] = new_title
        return raw_data

    def apply_prefix(self, raw_data):
        old_object_key = raw_data.get(self.raw_key_field)

        object_title = self.get_object_title(raw_data)

        # two icons are considered as the 'same' by IconService
        # when both the category and title are the same
        # (please refer to _validate_same_name_icon() in
        # IconService. It is used during the creation of
        # icons. (i.e. install of CP))
        # this means if two icons have different '_key' but
        # the same title and category, only first one will be
        # saved into the kv collection. The new one will be
        # rejected as duplicate.
        #
        # another caveat with icons is, backup on ITSI side
        # always includes ALL the icons as long as a glass
        # table is included. (regardless of full/partial backup).
        # it does not pick and backup only those which are
        # referenced by glasstables included in a partial backup.
        #
        # it is best if we don't reinstall the entire icon collection
        # on destination system each time if multiple CPs contain
        # glasstables. With the above said,
        # Below are some considerations involved in why we implemented
        # the below logic regarding different types of icons.
        #
        # 1. immutable icons: We can assume the 'same' icon will be on the
        # destination system (albeit with different _key). If a glass table
        # references an OOTB icon, but we don’t include the
        # immutable icons with a CP, we can almost guarantee that
        # the reference to such an OOTB icon will not work on the
        # destination system. Because the ‘SAME’ OOTB icon on the destination
        # system will have a different _key from what we are referencing when we built
        # the glass table on the source system. (Ideally, the OOTB
        # icons should have the same _key, but that’s not the case.)
        # Thus, in order to get OOTB icons working on the destination system,
        # we need to include all the OOTB icons and prefix their titles and _key.
        # This way they don't conflict with the ones on destination system. it will be
        # a common prefix to prevent repeat installation (meaning, if an icon is called
        # iphone, it will always be called PREFIX-iphone regardless which CP
        # it is packaged with.) This way the references will work on destination as well.
        # regardless which system we are on. during install of CP, we will skip over
        # if same icon is found on the system.
        #
        # 2. regular icons: Unlike OOTB icons, these usually shouldn't be on the destination.
        # However, because ALL icons are always packaged in backup and is not CP specific,
        # we will hit the same 'repeat' issue like OOTB icons as soon as we install
        # another CP that contains glass table.
        # in order to prevent multiple copies of the 'same' icon installed on the destination
        # we will also prefix their title/id with a common prefix. We will skip them during
        # install if they already exist on the system.
        #
        # in conclusion: we will prefix all icons (immutable or not) with
        # common prefix for the title and _key. During installation, we will skip them if
        # they already exist on the system. so there will be at most
        # one copy of all the icons.

        cleaned_title = self.remove_cp_id_prefix(object_title)
        new_title = '{}{}'.format(DA_ITSI_CP_ICON_PREFIX, cleaned_title)
        new_object_key = '{}{}'.format(DA_ITSI_CP_ICON_PREFIX, slugify(cleaned_title))

        self.update_title(new_title, raw_data)
        return old_object_key, new_object_key

    def extract_model_data(self, raw_data):
        object_key = self.get_object_key(raw_data)
        if not object_key:
            return None

        # Note: immutable icons are handled in the apply_prefix() method

        old_object_key, new_object_key = self.apply_prefix(raw_data)

        self.remap_keys(old_object_key, new_object_key)

        # for images, we are still doing key replacement to
        # help with image identification
        raw_data[self.raw_key_field] = new_object_key

        return raw_data

class KpiBaseSearchExtractor(Extractor):

    def extract_model_data(self, raw_data):
        model_data = super(KpiBaseSearchExtractor, self).extract_model_data(raw_data)
        if not model_data:
            return None

        if not self.skip_key_mapping:
            metric_remapped_keys = self.remapped_keys.setdefault(SearchMetric, {})

            metrics = raw_data.get('metrics', [])

            for metric in metrics:
                old_metric_key = metric.get(self.raw_key_field)
                new_metric_key = slugify(metric.get('title', ''))

                metric[self.raw_key_field] = new_metric_key
                metric_remapped_keys[old_metric_key] = new_metric_key

        return model_data


class ServiceAnalyzerExtractor(Extractor):

    def extract_model_data(self, raw_data):
        # default service analyzer record should be skipped. default
        # is generated on per user basis
        if raw_data['isDefault']:
            return None

        return super(ServiceAnalyzerExtractor, self).extract_model_data(raw_data)

class EntityTypeExtractor(Extractor):

    def extract_model_data(self, raw_data):
        # skip OOTB defaults if they are not modified
        is_from_conf = str(raw_data.get('_is_from_conf', 0))
        mod_source = raw_data.get('mod_source', '')
        if (is_from_conf == '1' or is_from_conf.lower() == 'true') and mod_source == 'ITSI default import':
            return None

        return super(EntityTypeExtractor, self).extract_model_data(raw_data)