from copy import copy
from sys import exit
from swimlane_migrator.utils import find_in_list
from swimlane_migrator.layouts.tasks import tasksEngine
import re

class workflowEngine():

    def __init__(self, appName, config):

        self.logger = config.pop('logger', None)
        self.swimlane_source = config.pop('swimlane_source', None)
        self.swimlane_target = config.pop('swimlane_target', None)

        if self.logger is None:
            raise  Exception('You must provide a logger object')

        if self.swimlane_source is None:
            raise  Exception('You must provide a swimlane_source object')

        if self.swimlane_target is None:
            raise  Exception('You must provide a swimlane_target object')

        self.appName = appName
        self.mode = config['mode']

        self.logger.info('Workflow Engine is running in {} mode.'.format(self.mode))

        self.logger.info('Load Target App Details')
        self.target_app_raw = self.swimlane_target.loadApp(appName=appName)
        self.target_fields = self.swimlane_target.getFieldDictinoary(byName = appName)

        self.logger.info('Load Source App Details')
        self.source_app_raw = self.swimlane_source.loadApp(appName=appName)
        self.source_fields = self.swimlane_source.getFieldDictinoary(byName = appName, forceReload = True)

        self.source_workflow = self.swimlane_source.loadWorkflow(appName=appName)
        self.target_workflow = self.swimlane_target.loadWorkflow(appName=appName)

        self.task_engine = tasksEngine(config={'logger': self.logger, 'swimlane_source': self.swimlane_source, 'swimlane_target': self.swimlane_target})

        self.current_workflow_label = ''
        self.migrated_ids = []

    def migrateWorkflow(self):
        new_workflow = copy(self.source_workflow)

        for stage in new_workflow['stages']:
            stage = self.fix_field_ids(stage, 'fieldId')
            stage['parentId'] = self.target_workflow['id']

        self.target_workflow['stages'] = new_workflow['stages']
        if self.mode == 'Live':
            try:
                self.swimlane_target.updateWorkflow(AppName=self.appName, workflow=self.target_workflow)
            except Exception as e:
                raise Exception(e)


    def fixReadWriteFields(self, search_dict):
        new_fieldState = {}
        new_fieldState['$type'] = search_dict['fieldStates']['$type']

        self.logger.debug('Working on Read/Write Acition Named: {}'.format(search_dict['name']))
        self.logger.debug(search_dict['fieldStates'])
        for field_id, field_perm in list(search_dict['fieldStates'].items()):
            if field_id != '$type':
                source_field_name = self.swimlane_source.validateField(self.source_fields, byID=field_id)
                if source_field_name == False:
                    self.logger.error('Action: {} with Field ID {}, not found in source.'.format(search_dict['name'], field_id))
                    continue

                target_field_id = self.swimlane_target.validateField(self.target_fields, byName=source_field_name)
                if target_field_id == False:
                    self.logger.critical('Read Write Field Name {}, not found in target.'.format(source_field_name))
                    continue

                self.logger.info('Updating Field Permissions for {} to {}'.format(source_field_name, field_perm))
                new_fieldState[target_field_id] = field_perm

        search_dict['fieldStates'] = new_fieldState
        return search_dict

    def fixFieldSetValues(self, search_dict):
        current_value = search_dict['value']
        if isinstance(current_value, str):
            matches = re.findall('{{(.*?)}}', current_value, re.DOTALL)
            for field_id in matches:
                self.logger.debug('Lookup Field ID: {}'.format(field_id))
                source_field_name = self.swimlane_source.validateField(self.source_fields, byID=field_id)
                if source_field_name == False:
                    self.logger.error('FieldSetValue: {} with Field ID {}, not found in source.'.format(search_dict['name'], field_id))
                    continue

                self.logger.debug('Lookup Field Name: {}'.format(source_field_name))
                target_field_id = self.swimlane_target.validateField(self.target_fields, byName=source_field_name)
                if target_field_id == False:
                    self.logger.critical('FieldSetValue: Field Name {}, not found in target.'.format(source_field_name))
                    continue

                current_value = current_value.replace(field_id, target_field_id)

            search_dict['value'] = current_value

        return search_dict

    def fixTaskIdValues(self, search_dict):
        current_id = search_dict['taskId']
        for task, value in self.swimlane_source.task_dictionary.items():
            if value['id'] == current_id:
                task_name = value['name']
                self.logger.debug('Converting Task Id for: {}'.format(task_name))
                found = False
                for task, value in self.swimlane_target.task_dictionary.items():
                    if value['name'] == task_name:
                        new_id = value['id']
                        search_dict['taskId'] = new_id
                        found = True
                        break
                if not found:
                    if self.mode == "Live":
                        new_task = self.task_engine.migrateTask(task_name)
                        new_id = new_task['id']
                        search_dict['taskId'] = new_id
                break
        return search_dict

    def fixConditionValue(self, search_dict):
        if 'fieldId' in search_dict and 'value' in search_dict:
            source_field_name = self.swimlane_source.validateField(self.source_fields, byID=search_dict['fieldId'])
            if source_field_name == False:
                self.logger.critical('{} ConditionValue: Field ID {}, not found in source. Raw Data:  {}'.format(self.current_workflow_label, search_dict['fieldId'], search_dict))
                return search_dict

            target_field_id = self.swimlane_target.validateField(self.target_fields, byName=source_field_name)
            if target_field_id == False:
                self.logger.critical('{} ConditionValue: Field Name {}, not found in target.'.format(self.current_workflow_label, source_field_name))
                return search_dict

            ## Validate for Value List
            if self.source_fields[source_field_name]['$type'] == 'Core.Models.Fields.ValuesListField, Core':
                try:
                    source_value_obj_key = find_in_list(self.source_fields[source_field_name]['values'], 'id', search_dict['value'], self.logger)
                    if source_value_obj_key is None:
                        self.logger.critical('"{}" ConditionValue: Field Value ID "{}" not found in Field "{}" with ID "{}" in source value List'.format(self.current_workflow_label, search_dict['value'], source_field_name, search_dict['fieldId']))
                        return search_dict

                    source_value_obj = self.source_fields[source_field_name]['values'][source_value_obj_key]
                    target_value_obj_key = find_in_list(self.target_fields[source_field_name]['values'], 'name', source_value_obj['name'], self.logger)
                    if target_value_obj_key is None:
                        self.logger.critical('{} ConditionValue: Field Value {}, not found in target value List.'.format(self.current_workflow_label, source_value_obj['name']))
                        return search_dict

                    search_dict['value'] = self.target_fields[source_field_name]['values'][target_value_obj_key]['id']
                except Exception as e:
                    raise Exception('Error in Fix Condition: {}, Raw Dict: {}'.format(e, search_dict))

        return search_dict


    def fix_field_ids(self, search_dict, field):
        remove_keys = []


        if '$type' in search_dict:
            if search_dict['$type'] == 'Core.Models.Workflow.Stage, Core' or search_dict['$type'] == 'Core.Models.Workflow.Actions.FieldSetAction, Core':
                self.current_workflow_label = search_dict['name']

            if search_dict['$type'] == 'Core.Models.Workflow.Condition, Core':
                search_dict = self.fixConditionValue(search_dict)

            elif search_dict['$type'] == 'Core.Models.Workflow.Actions.FieldStateAction, Core':
                if 'fieldStates' in search_dict and search_dict['id'] not in self.migrated_ids:
                    search_dict = self.fixReadWriteFields(search_dict)
                    self.migrated_ids.append(search_dict['id'])

            elif search_dict['$type'] == 'Core.Models.Workflow.Actions.FieldSetAction, Core':
                if 'value' in search_dict and search_dict['id'] not in self.migrated_ids:
                    search_dict = self.fixFieldSetValues(search_dict)
                    if 'id' in search_dict:
                        self.migrated_ids.append(search_dict['id'])

            elif search_dict['$type'] == 'Core.Models.Workflow.Actions.IntegrationAction, Core':
                if 'taskId' in search_dict and search_dict['id'] not in self.migrated_ids:
                    search_dict = self.fixTaskIdValues(search_dict)
                    if 'taskId' in search_dict:
                        self.migrated_ids.append(search_dict['taskId'])

        for key, value in search_dict.items():
            if key == field:

                source_field_name = self.swimlane_source.validateField(self.source_fields, byID=value)
                if source_field_name == False:
                    if 'name' in search_dict:
                        label = search_dict['name']
                    else:
                        label = search_dict

                    self.logger.critical('Failed to Migrate Workflow Object {}: {}, source Field ID {} Not Found.'.format(self.current_workflow_label, label, value))
                else:
                    target_field_id = self.swimlane_target.validateField(self.target_fields, byName=source_field_name)
                    if target_field_id == False:
                        self.logger.critical('Failed to Migrate Workflow Object: {}, target Field Not Found.'.format(source_field_name))
                    else:
                        if 'name' in search_dict:
                            label = search_dict['name']
                        else:
                            label = search_dict
                        self.logger.debug('Updated Field : {}'.format(label))
                        search_dict[key] = target_field_id


            elif isinstance(value, dict):
                search_dict[key] = self.fix_field_ids(value, field)

            elif isinstance(value, list):
                search_dict[key] = []
                for item in value:
                    if isinstance(item, dict):
                        search_dict[key].append(self.fix_field_ids(item, field))
                    else:
                        search_dict[key] = value

        for key in remove_keys:
            search_dict.pop(key)

        return search_dict