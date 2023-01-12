from . import types, tasks
from copy import copy
from swimlane_migrator.utils import buildLogDictionary, get_recursively
from sys import exit

class layoutEngine():

    def __init__(self, appName, config):

        self.config = copy(config)

        self.logger = config.pop('logger', None)
        self.swimlane_source = config.pop('swimlane_source', None)
        self.swimlane_target = config.pop('swimlane_target', None)
        self.mode = config.pop('mode', 'Validation')

        if self.logger is None:
            raise  Exception('You must provide a logger object')

        if self.swimlane_source is None:
            raise  Exception('You must provide a swimlane_source object')

        if self.swimlane_target is None:
            raise  Exception('You must provide a swimlane_target object')

        self.logger.info('Layout Engine Running in {} mode'.format(self.mode))

        self.appName = appName

        self.logger.debug('Load Target App Details')
        self.target_app_raw = self.swimlane_target.loadApp(appName=appName)
        self.target_fields = self.swimlane_target.getFieldDictinoary(byName = appName)

        self.logger.debug('Load Source App Details')
        self.source_app_raw = self.swimlane_source.loadApp(appName=appName)
        self.source_fields = self.swimlane_source.getFieldDictinoary(byName = appName)

        self.task_engine = tasks.tasksEngine(config={'logger':self.logger, 'swimlane_source' : self.swimlane_source, 'swimlane_target' : self.swimlane_target})
        self.migrated_tasks = []

        self.log_dictionary = self.swimlane_target.log_dictionary['Layout'] = {}

        self.update_fields = ['html', 'id', 'row', 'col', 'sizex', 'sizey']

    def updateLayout(self):
        if self.mode == 'Live':
            self.logger.info('Remove Orphan Tasks')
            self.task_engine.removeOrphanTasks()

        # # Process Layout
        new_layout = copy(self.source_app_raw['layout'])

        self.log_dictionary['Fields'] = []
        for layout_obj in new_layout:
            self.logger.debug('-------------------------------------')
            layout_obj = self.fix_field_ids(layout_obj, 'fieldId')
            self.logger.debug('-------------------------------------')

        self.target_app_raw['layout'] = new_layout

        if self.mode == 'Live':
            self.swimlane_target.saveApp(self.appName)

    def fix_field_ids(self, search_dict, field):
        for key, value in search_dict.items():
            if key == field:
                source_field_name = self.swimlane_source.validateField(self.source_fields, byID=value)
                if source_field_name == False:
                    self.logger.critical('LAYOUTS->FIX_FIELD_ID : Unable to find source field name: {}'.format(value))
                    continue

                target_field_id = self.swimlane_target.validateField(self.target_fields, byName=source_field_name)
                if target_field_id == False:
                    self.logger.critical('LAYOUTS->FIX_FIELD_ID : Unable to find Target Field Name: {} Field ID: {}'.format(source_field_name, value))
                    target_layout_obj_list = get_recursively(self.target_app_raw['layout'], 'fieldId', [target_field_id])
                else:
                    target_layout_obj_list = []

                ##updateField
                if len(target_layout_obj_list) == 1:
                    # self.logger.critical('##LAYOUT FIELD: {}'.format(source_field_name))
                    modified_fields = []
                    target_layout_obj = target_layout_obj_list[0]
                    for field in self.update_fields:
                        if field in search_dict and field in target_layout_obj:
                            # self.logger.critical('old: {} new: {}'.format(target_layout_obj[field], search_dict[field]))
                            if search_dict[field] != target_layout_obj[field]:
                                # self.logger.critical('Updateing')
                                modified_fields.append(field)
                    # self.logger.critical('Count: {}'.format(len(modified_fields)))
                    if len(modified_fields) > 0:
                        # self.logger.critical('Field {} should be in logger'.format(source_field_name))
                        self.log_dictionary['Fields'].append(buildLogDictionary('fields', 'update', source_field_name, txt = 'Modifed Fields: {}'.format(modified_fields)))
                else:
                    self.log_dictionary['Fields'].append(buildLogDictionary('fields', 'add', source_field_name))

                search_dict[key] = target_field_id


            if '$type' in search_dict and search_dict['$type'] == 'Core.Models.Layouts.IntegrationLayout, Core' and search_dict['id'] not in self.migrated_tasks:
                self.logger.debug('----------------------------------------------')
                layout_obj_build = types.integration(layout_obj = search_dict, config=copy(self.config))
                layout_obj_build.validateTaskID(self.task_engine, self.mode)
                self.migrated_tasks.append(search_dict['id'])
                search_dict = layout_obj_build.layout_obj
                if layout_obj_build.updates_made:
                    self.logger.debug('Modifications Made')
                    #search_dict = layout_obj_build.layout_obj
                self.logger.debug('----------------------------------------------')

            elif isinstance(value, dict):
                search_dict[key] = self.fix_field_ids(value, field)

            elif isinstance(value, list):
                search_dict[key] = []
                for item in value:
                    if isinstance(item, dict):
                        search_dict[key].append(self.fix_field_ids(item, field))
                    else:
                        search_dict[key].append(value)

        return search_dict