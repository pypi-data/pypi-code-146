from .base.fields import fields

class cross_reference(fields):

    def validateTargetApplication(self):

        if self.swimlane_target.validateApp(byID = self.field_obj['targetId']) == False:
            self.logger.info('Cross Reference Target ID not found in Target: {}'.format(self.field_obj['targetId']))
            source_app_name = self.swimlane_source.validateApp(byID = self.field_obj['targetId'])
            if source_app_name == False:
                self.logger.error('FAILED TO FIND: Orphan Cross Reference APP: {}'.format(source_app_name))
                return False
            else:
                self.logger.info('Orphan Cross Reference APP: {}'.format(source_app_name))
                target_app_id = self.swimlane_target.validateApp(byName = source_app_name)

                if target_app_id != False:
                    self.logger.debug('Cross Reference App ID found in target: {}'.format(target_app_id))
                    self.field_obj['targetId'] = target_app_id
                    self.updates_made = True
                else:
                    self.logger.error('FAILED TO FIND: Target Application ID')
                    return False
        else:
            self.logger.debug('Cross Reference Field {} already valid'.format(self.field_obj['name']))

        return True

    def validateFieldColumns(self):
        app_name = self.swimlane_target.validateApp(byID = self.field_obj['targetId'])

        if app_name != False:
            source_ref_app_fields  = self.swimlane_source.getFieldDictinoary(byName=app_name)
            target_ref_app_fields = self.swimlane_target.getFieldDictinoary(byName=app_name)
            new_columns = []
            for ref_field in self.field_obj['columns']:
                if self.swimlane_target.validateField(target_ref_app_fields, byID=ref_field) == False:
                    ref_source_app_name = self.swimlane_source.validateField(source_ref_app_fields, byID=ref_field)
                    target_field_id = self.swimlane_target.validateField(target_ref_app_fields, byName=ref_source_app_name)
                    if target_field_id != False:
                        self.logger.info('Field {} migrated'.format(ref_source_app_name))
                        new_columns.append(target_field_id)
                        self.updates_made = True
                    else:
                        self.logger.error('CROSS REFERENCE COLUMNS: Field ID {} failed to find a match'.format(ref_field))
                        self.failed_fields.append(ref_field)
                else:
                    self.logger.debug('Field {} already valid'.format(self.swimlane_target.validateField(target_ref_app_fields, byID=ref_field)))
                    new_columns.append(ref_field)

            if len(new_columns) == len(self.field_obj['columns']):
                self.logger.debug('All Columns Migrated count: {}'.format(len(new_columns)))
                self.field_obj['columns'] = new_columns
                return True
            else:
                self.logger.error('FAILED TO MIGRATE COLUMNS: {}'.format(self.failed_fields))
                return False
        else:
            self.logger.critical('Cross Reference Field "{}" target application ID: "{}" could not be found'.format(self.field_obj['name'], self.field_obj['targetId']))
            return False
