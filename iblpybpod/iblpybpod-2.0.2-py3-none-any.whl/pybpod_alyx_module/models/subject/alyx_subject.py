import logging
import os

import pybpodgui_api
from pybpod_alyx_module.alyx_details import AlyxDetails
from pybpodgui_plugin.models.subject import SubjectUIBusy
from sca.formats import json

logger = logging.getLogger(__name__)


class AlyxSubject(SubjectUIBusy):

    def __init__(self, project):
        super(AlyxSubject, self).__init__(project)

    def add_alyx_info(self, jsondata):
        self.name = jsondata.get('nickname', None)
        self.alyx_id = jsondata.get('id', None)
        self._get_alyx_members_from_json(jsondata)

        if not hasattr(self, '_alyx_menu'):
            self._alyx_menu = self._tree.add_popup_menu_option('Alyx Details', self.showdetails, item=self.node)
        self._name.readonly = True

    def save(self):
        """
        Save subject data on filesystem.

        :ivar str project_path: Project path.  
        :return: Dictionary containing the setup info to save.  
        :rtype: dict
        """
        if not hasattr(self, 'alyx_id'):
            super().save()
            return

        if not self.name:
            logger.warning("Skipping subject without name")
            return None
        else:  
            if not os.path.exists(self.path): os.makedirs(self.path)

            if self.data:
                data = self.data
            else:
                data = json.scadict(
                    uuid4_id=self.uuid4,
                    software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                    def_url ='http://pybpod.readthedocs.org',
                    def_text='This file contains information about a subject used on PyBpod GUI.',
                )

            self._save_alyx_member_to_json(data)

            config_path = os.path.join(self.path, self.name+'.json')
            with open(config_path, 'w') as fstream: json.dump(data, fstream)

    def toJSON(self):
        if not hasattr(self, 'alyx_id'):
            return super().toJSON()

        data = json.scadict(
                    uuid4_id=self.uuid4,
                    software='PyBpod GUI API v'+str(pybpodgui_api.__version__),
                    def_url ='http://pybpod.readthedocs.org',
                    def_text='This file contains information about a subject used on PyBpod GUI.',
                )

        data['name'] = self.name
        data['uuid4'] = self.uuid4
        self._save_alyx_member_to_json(data)

        return json.dumps(data)

    def load(self, path):
        """
        Load subject data from filesystem

        :ivar str subject_path: Path of the subject
        :ivar dict data: data object that contains all subject info
        """
        self.name  = os.path.basename(path)

        try:
            with open( os.path.join(self.path, self.name+'.json'), 'r' ) as stream:
                self.data = data = json.load(stream)

            if data.get('alyx_id', None) is None:
                super().load(path)
                return

            self.uuid4 = data.uuid4 if data.uuid4 else self.uuid4
            self.alyx_id = data.get('alyx_id', None)
            self._get_alyx_members_from_json(data)

            self._alyx_menu = self._tree.add_popup_menu_option('Alyx Details', self.showdetails, item=self.node)
            self._name.readonly = True

        except:
            raise Exception('There was an error loading the configuration file for the subject [{name}]. File not found.'.format(name=self.name))

    def _get_alyx_members_from_json(self, data):
        self.alyx_nickname = data.get('nickname', None)
        self.alyx_url = data.get('url', None)
        self.alyx_responsible_user = data.get('responsible_user', None)
        self.alyx_birth_date = data.get('birth_date', None)
        self.alyx_age_weeks = data.get('age_weeks', None)
        self.alyx_death_date = data.get('death_date', None)
        self.alyx_species = data.get('species', None)
        self.alyx_sex = data.get('sex', None)
        self.alyx_litter = data.get('litter', None)
        self.alyx_strain = data.get('strain', None)
        self.alyx_source = data.get('source', None)
        self.alyx_line = data.get('line', None)
        self.alyx_projects = data.get('projects', [])
        self.alyx_lab = data.get('lab', None)
        self.alyx_genotype = data.get('genotype', [])
        self.alyx_description = data.get('description', None)
        self.alyx_alive = data.get('alive', None)
        self.alyx_weighings = data.get('weighings', [])
        self.alyx_water_administrations = data.get('water_administrations', [])
        self.alyx_reference_weight = data.get('reference_weight', None)
        self.alyx_last_water_restriction = data.get('last_water_restriction', None)
        self.alyx_expected_water = data.get('expected_water', None)
        self.alyx_remaining_water = data.get('remaining_water', None)

    def _save_alyx_member_to_json(self, data):
        data['nickname'] = self.alyx_nickname
        data['url'] = self.alyx_url
        data['alyx_id'] = self.alyx_id
        data['responsible_user'] = self.alyx_responsible_user
        data['birth_date'] = self.alyx_birth_date
        data['age_weeks'] = self.alyx_age_weeks
        data['death_date'] = self.alyx_death_date
        data['species'] = self.alyx_species
        data['sex'] = self.alyx_sex
        data['litter'] = self.alyx_litter
        data['strain'] = self.alyx_strain
        data['source'] = self.alyx_source
        data['line'] = self.alyx_line
        data['projects'] = self.alyx_projects
        data['lab'] = self.alyx_lab
        data['genotype'] = self.alyx_genotype
        data['description'] = self.alyx_description
        data['alive'] = self.alyx_alive
        data['weighings'] = self.alyx_weighings
        data['water_administration'] = self.alyx_water_administrations
        data['reference_weight'] = self.alyx_reference_weight
        data['last_water_restriction'] = self.alyx_last_water_restriction
        data['expected_water'] = self.alyx_expected_water
        data['remaining_water'] = self.alyx_remaining_water

    def create_treenode(self, tree):
        """
        Creates node for this board under the parent "Boards" node.

        This methods is called when the board is first created.

        The following actions get assigned to node:
            * *Remove*: :meth:`BoardTreeNode.remove`.

        Sets key events:
            * :meth:`BoardTreeNode.node_key_pressed_event`


        :param tree: the project tree
        :type tree: pyforms.controls.ControlTree
        :return: new created node
        :return type: QTreeWidgetItem
        """
        super().create_treenode(tree)

        # save the tree so we can add the pop-up on load and add_alyx_info for those subjects that require it
        self._tree = tree

        return self.node

    def showdetails(self):
        if not hasattr(self, 'detailswindow'):
            self.detailswindow = AlyxDetails(self)
        self.detailswindow.show()
        return self.detailswindow

    def collect_data(self, data):
        _data = super().collect_data(data)

        if not hasattr(self, 'alyx_id'):
            return _data

        _data.update({'nickname': self.alyx_nickname})
        _data.update({'url': self.alyx_url})
        _data.update({'alyx_id': self.alyx_id})
        _data.update({'responsible_user': self.alyx_responsible_user})
        _data.update({'birth_date': self.alyx_birth_date})
        _data.update({'age_weeks': self.alyx_age_weeks})
        _data.update({'death_date': self.alyx_death_date})
        _data.update({'species': self.alyx_species})
        _data.update({'sex': self.alyx_sex})
        _data.update({'litter': self.alyx_litter})
        _data.update({'strain': self.alyx_strain})
        _data.update({'source': self.alyx_source})
        _data.update({'line': self.alyx_line})

        _data.update({'projects': []})
        for item in self.alyx_projects:
            _data['projects'].append(item)

        _data.update({'lab': self.alyx_lab})

        _data.update({'genotype': []})
        for item in self.alyx_genotype:
            _data['genotype'].append(item)

        _data.update({'description': self.alyx_description})
        _data.update({'alive': self.alyx_alive})

        _data.update({'weighings': []})
        for item in self.alyx_weighings:
            _data['weighings'].append(str(item))

        _data.update({'water_administrations': []})
        for item in self.alyx_water_administrations:
            _data['water_administrations'].append(str(item))

        _data.update({'reference_weight': self.alyx_reference_weight})
        _data.update({'last_water_restriction': self.alyx_last_water_restriction})
        _data.update({'expected_water': self.alyx_expected_water})
        _data.update({'remaining_water': self.alyx_remaining_water})

        return _data
