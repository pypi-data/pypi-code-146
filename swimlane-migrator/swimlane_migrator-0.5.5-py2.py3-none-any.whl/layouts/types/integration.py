from .base.layouts import layouts

class integration(layouts):

    def validateTaskID(self, taskEngine, mode):
        if 'taskId' in self.layout_obj:
            source_task_name = self.swimlane_source.validateTask(byID=self.layout_obj['taskId'])
            target_task_id = self.swimlane_target.validateTask(byName= source_task_name)
            if target_task_id == False:
                self.logger.info('Task {} not found in Target'.format(source_task_name))
                #source_task_name = self.swimlane_source.validateTask(byID = self.layout_obj['taskId'])
                if source_task_name == False:
                    self.logger.error('FAILED TO FIND IN SOURCE: Orphan Task RAW Data: {}'.format(self.layout_obj['name']))
                    return False
                else:
                    self.logger.info('Orphan Cross Reference APP: {}'.format(source_task_name))
                    if mode == 'Live':
                        task_raw = taskEngine.migrateTask(source_task_name)
                    else:
                        task_raw = {}
                    # target_task_id = self.swimlane_target.validateTask(byName = source_task_name)
                    if 'id' in task_raw:
                        self.logger.info('Task ID found in target: {}'.format(task_raw['id']))
                        self.layout_obj['taskId'] = task_raw['id']
                        self.updates_made = True
                    else:
                        self.logger.error('FAILED TO FIND: Target Task ID')
                        return False


            else:
                self.logger.debug('Integration Task {} is valid'.format(source_task_name))
                self.layout_obj['taskId'] = target_task_id
                self.updates_made = True
        else:
            self.logger.critical('Task Button {} has no taskID'.format(self.layout_obj['name']))
