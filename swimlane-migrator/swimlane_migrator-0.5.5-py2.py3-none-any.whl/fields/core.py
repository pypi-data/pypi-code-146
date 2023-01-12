from . import types
from copy import copy
from sys import exit
from swimlane_migrator.utils import buildLogDictionary, find_in_list

class fieldsEngine():

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

        self.logger.info('Field Engine Running in {} mode'.format(self.mode))

        self.appName = appName

        self.logger.debug('Load Source App Details')
        self.source_app_raw = self.swimlane_source.loadApp(appName=appName)
        self.source_fields = self.swimlane_source.getFieldDictinoary(byName = appName)

        self.logger.debug('Load Target App Details')

        if appName not in self.swimlane_target.apps_dictionary:
            description = ''
            if 'description' in self.source_app_raw:
                description = self.source_app_raw['description']
            if self.mode == 'Live':
                self.swimlane_target.createEmptyApp(appName, acronym = self.source_app_raw['acronym'], id = self.source_app_raw['id'], name = self.source_app_raw['name'], description=description)
            self.logger.info('Create New Application {}'.format(appName))

        self.target_app_raw = self.swimlane_target.loadApp(appName=appName)
        self.target_fields = self.swimlane_target.getFieldDictinoary(byName = appName)

        self.update_field_list = ['required','readOnly','helpTextType', 'layoutId', 'lengthType', 'visualize', 'visualizeMode', 'selectionType', 'controlType', 'inputType', 'name']

        self.migrate_fields_types = ['numeric','valuesList']

        self.migrated_fields = []

        self.temp_field_postfix = 'migration_field_temp'

        self.enable_data_migration = False

        self.log_dictionary = self.swimlane_target.log_dictionary['Fields'] = {}

    def repairTargetFields(self):
        #self.deleteTargetFields(False)
        self.syncTargetFieldInfo()
        self.deleteTargetFields(False)
        self.syncPermissions()

        if self.mode == 'Live':
            self.swimlane_target.saveApp(self.appName)

            if len(self.migrated_fields) > 0 and self.enable_data_migration:
                self.migrateRecordData()

            self.swimlane_target.saveApp(self.appName)

    def deleteTargetFields(self, leaveMigrateFields = True):
        self.log_dictionary['Delete'] = []
        diff_fields = list(set(self.target_fields) - set(self.source_fields))
        check_fields = []
        for df in diff_fields:
            check_fields.append(self.target_fields[df])
        for field in check_fields:

            target_field_info_key = find_in_list(self.target_app_raw['fields'], 'id', field['id'], self.logger)
            if target_field_info_key is None:
                raise Exception('Unable to find field key for: {}'.format(field))

            if self.temp_field_postfix not in field or leaveMigrateFields:
                self.log_dictionary['Delete'].append(buildLogDictionary('field', 'delete', field))
                self.logger.info('Deleting Field {} from target app'.format(field['name']))
                self.target_app_raw['fields'].pop(target_field_info_key)
            else:
                root_field_name = field['name'].replace('_{}'.format(self.temp_field_postfix), '')
                self.migrated_fields.append(root_field_name)

    def syncTargetFieldInfo(self):
        self.log_dictionary['Fields'] = []

        ## Cycle through fields
        for field_obj in self.source_app_raw['fields']:
            self.logger.debug('----------------------------------------------')
            self.logger.debug('Working with Field: {}'.format(field_obj['name']))

            # if field_obj['name'] == 'INC-Did GWO approve closure of ticket?':
            #   self.logger.critical(field_obj)
            '''
            if 'fieldType' in field_obj and field_obj['fieldType'] != 'tracking':
              target_field_info_key = find_in_list(self.target_app_raw['fields'], 'id', field_obj['id'], self.logger)
            else:
              target_field_info_key = find_in_list(self.target_app_raw['fields'], 'name', field_obj['name'], self.logger)
            '''
            target_field_info_key = find_in_list(self.target_app_raw['fields'], 'id', field_obj['id'], self.logger)
            if target_field_info_key is None:
                target_field_info_key = find_in_list(self.target_app_raw['fields'], 'name', field_obj['name'], self.logger)
            if target_field_info_key is None:
                self.logger.info('New Field {} add to field list'.format(field_obj['name']))
                new_field = copy(field_obj)
                self.target_app_raw['fields'].append(new_field)
                current_field_obj = self.target_app_raw['fields'][-1]
                self.log_dictionary['Fields'].append(buildLogDictionary('field', 'add', new_field['name']))

            else:

                self.logger.debug('Current Field')
                current_field_obj = self.target_app_raw['fields'][target_field_info_key]
                ## Validate Field Types Match
                if ('fieldType' in field_obj and 'fieldType' in current_field_obj) and (
                        field_obj['fieldType'] == current_field_obj['fieldType'] or
                        ( field_obj['fieldType'] == 'text' and current_field_obj['fieldType'] in self.migrate_fields_types and self.enable_data_migration)
                ):

                    if field_obj['fieldType'] != current_field_obj['fieldType']:
                        self.log_dictionary['Fields'].append(buildLogDictionary('field', 'migrate', field_obj['name'], 'from {} to {}'.format(field_obj['fieldType'], current_field_obj['fieldType'])))

                        ## Add to migrated list
                        self.migrated_fields.append(field_obj['name'])

                        temp_field_name = '{}_{}'.format(field_obj['name'], self.temp_field_postfix)
                        temp_field_check = find_in_list(self.target_app_raw['fields'], 'name', temp_field_name, self.logger)

                        ## Rename Orginal Field for data migration
                        if temp_field_check is None:
                            current_field_obj['name'] = temp_field_name

                            ##Add New Object
                            new_field = copy(field_obj)
                            self.target_app_raw['fields'].append(new_field)
                            self.logger.critical('Renaming Import field {} to Temp Name {} for migration of data'.format(field_obj['name'], temp_field_name))
                    else:
                        updated_fields = []
                        for update_field in self.update_field_list:
                            if update_field in field_obj:

                                if update_field not in current_field_obj or (current_field_obj[update_field] != field_obj[update_field]):
                                    updated_fields.append(update_field)
                                    self.logger.info('Changing field {} {} from {} to {}'.format(field_obj['name'],update_field,current_field_obj[update_field], field_obj[update_field]))

                                current_field_obj[update_field] = field_obj[update_field]
                            else:

                                current_field_obj.pop(update_field, None)

                        if len(updated_fields) > 0:
                            self.log_dictionary['Fields'].append(buildLogDictionary('field', 'update', field_obj['name'], 'Modified Fields: {}'.format(updated_fields)))

                        if '$type' in current_field_obj:
                            if current_field_obj['$type'] == 'Core.Models.Fields.Reference.ReferenceField, Core':
                                cross_ref_field = types.cross_reference(field_obj = current_field_obj, config=copy(self.config))
                                cross_ref_field.validateTargetApplication()
                                cross_ref_field.validateFieldColumns()
                                if cross_ref_field.updates_made:
                                    current_field_obj = cross_ref_field.field_obj

                            if current_field_obj['$type'] == 'Core.Models.Fields.ValuesListField, Core':
                                value_list_obj = types.valuelist(field_obj=current_field_obj, source_obj=field_obj ,config=copy(self.config))
                                current_field_obj = value_list_obj.migrateValues()
                else:
                    if ('fieldType' in field_obj and 'fieldType' in current_field_obj):
                        self.logger.critical('Unable to migrate Field: {}, Source Field Type: {}  Target Field Type: {}'.format(field_obj['name'], field_obj['fieldType'], current_field_obj['fieldType']))
                    else:
                        self.logger.critical('Unable to migrate Field: {}, Field Type Missing Cannot validate')


            ## Global Modification Fields
            if current_field_obj['$type'] == 'Core.Models.Fields.UserGroupField, Core':
                usergroup_fields = types.usergroups(field_obj = current_field_obj, source_obj=field_obj, config=copy(self.config))
                current_field_obj = usergroup_fields.migrateMembers()
            self.target_fields = self.swimlane_target.getFieldDictinoary(byName = self.appName)
            self.logger.debug('----------------------------------------------')

    def syncPermissions(self):
        self.log_dictionary['Permissions'] = []

        orginal_target_permissions = copy(self.target_app_raw['permissions'])
        self.target_app_raw['permissions'] = {}

        for perm_id, perm in list(self.source_app_raw['permissions'].items()):
            new_perm_dict = None
            target_role_id = None

            if perm_id != '$type':
                if perm['type'] == 'Role':
                    self.logger.info('Update Application Permission for Role: {}'.format(perm['name']))
                    target_role_id = self.swimlane_target.validateRole(byName=perm['name'])

                    if target_role_id == False:
                        self.logger.critical('Failed to find Role: {}, in Target'.format(perm['name']))
                        continue

                    if target_role_id in orginal_target_permissions:
                        self.logger.debug('Role already in target')
                        perm_log = {'group' : 'role', 'action' : 'update', 'name': perm['name'], 'fields' : []}
                    else:
                        self.logger.debug('Add role in target')
                        perm_log = {'group' : 'role', 'action' : 'add', 'name': perm['name'], 'fields' : []}

                    new_perm_dict = copy(perm)
                    new_perm_dict['id'] = target_role_id

                    new_field_perm = {}
                    for field_id, field_perm  in list(new_perm_dict['fields'].items()):
                        if field_id != '$type':

                            source_target_name = self.swimlane_source.validateField(self.source_fields, byID=field_id)
                            if source_target_name == False:
                                self.logger.critical('Failed to assign Field Permissions, ID {} not found in source'.format(field_id))
                                continue

                            target_field_id = self.swimlane_target.validateField(self.target_fields, byName=source_target_name)
                            if target_field_id == False:
                                self.logger.critical('Failed to assign Field Permissions, Name {} not found in target'.format(source_target_name))
                                continue

                            if target_role_id in orginal_target_permissions:
                                if target_field_id in orginal_target_permissions[target_role_id]['fields']:
                                    if field_perm != orginal_target_permissions[target_role_id]['fields'][target_field_id]:
                                        self.logger.info('Updating Permission for Field: {}, Old: {}  New: {}'.format(source_target_name, orginal_target_permissions[target_role_id]['fields'][target_field_id], field_perm))
                                        perm_log['fields'].append(buildLogDictionary('field', 'update', source_target_name, 'Old: {}, New {}'.format(orginal_target_permissions[target_role_id]['fields'][target_field_id], field_perm)))
                                else:
                                    self.logger.info('Adding Permission for Field: {}, Set to: {}'.format(source_target_name, field_perm))
                                    perm_log['fields'].append(buildLogDictionary('field', 'add', source_target_name, 'New {}'.format(field_perm)))

                                new_field_perm[target_field_id] = field_perm
                            else:
                                #self.logger.critical('Target Role ID not found {}'.format(target_role_id))
                                self.logger.info('Adding Permission for Field: {}, Set to: {}'.format(source_target_name, field_perm))
                                perm_log['fields'].append(buildLogDictionary('field', 'add', source_target_name, 'New {}'.format(field_perm)))
                                if len(perm_log['fields']) > 0:
                                    self.log_dictionary['Permissions'].append(perm_log)
                                new_field_perm[target_field_id] = field_perm
                                new_perm_dict['fields'] = new_field_perm
                    if len(perm_log['fields']) > 0:
                        self.log_dictionary['Permissions'].append(perm_log)

                    new_perm_dict['fields'] = new_field_perm

                else:
                    raise Exception('Unhandled Permission Type {}'.format(perm['type']))

            if new_perm_dict is not None and target_role_id is not None:
                self.target_app_raw['permissions'][target_role_id] = new_perm_dict

    def migrateRecordData(self):
        current_app = self.swimlane_target.swimlane.apps.get(name=self.appName)
        search_results = current_app.records.search(('Tracking Id', 'doesNotEqual', ''))
        for record in search_results:
            for field_name in self.migrated_fields:
                self.logger.critical(field_name)
                temp_field_name = '{}_{}'.format(field_name, self.temp_field_postfix)
                if record[temp_field_name] is not None:
                    record[field_name] = str(record[temp_field_name])
                self.logger.critical(record[temp_field_name])
            record.save()

        self.deleteTargetFields(leaveMigrateFields=False)
        self.swimlane_target.saveApp(self.appName)
