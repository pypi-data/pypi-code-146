import json
from io import BytesIO
from copy import copy
from swimlane_migrator.utils import buildLogDictionary

class tasksEngine():

    def __init__(self, config):

        self.logger = config.pop('logger', None)
        self.swimlane_source = config.pop('swimlane_source', None)
        self.swimlane_target = config.pop('swimlane_target', None)

        if self.logger is None:
            raise  Exception('You must provide a logger object')

        if self.swimlane_source is None:
            raise  Exception('You must provide a swimlane_source object')

        if self.swimlane_target is None:
            raise  Exception('You must provide a swimlane_target object')

        self.log_dictionary = self.swimlane_target.log_dictionary['Tasks'] = {}

        self.sw_source_version = float(self.swimlane_source.swimlane.product_version[:-2])
        self.sw_target_version = float(self.swimlane_target.swimlane.product_version[:-2])

    def get(self, taskID, swimlane_svr):
        task_response = swimlane_svr.swimlane.request(
            'get',
            '/task/{}'.format(taskID),
        )

        task_raw = json.loads(task_response.text)

        return task_raw

    def delete(self, taskID, swimlane_svr):
        taskdelete_response = swimlane_svr.swimlane.request(
            'delete',
            '/task/{}'.format(taskID),
        )

    def update(self, task_obj, task_id, swimlane_svr):

        ## Create Tasks
        update_response = swimlane_svr.swimlane.request(
            'put',
            '/task/{}'.format(task_id),
            json = task_obj
        )

        return json.loads(update_response.text)


    def create(self, task_obj, swimlane_svr):

        ## Create Tasks
        create_response = swimlane_svr.swimlane.request(
            'post',
            '/task/',
            json = task_obj
        )

        create_raw = json.loads(create_response.text)

        ### Add to Menu
        #menu_obj = {
        #    "type": "task",
        #    "taskId": create_raw['id'],
        #    "name": create_raw['name'],
        #    "disabled": False
        #}
        #if 'applicationId' in task_obj:
        #    menu_obj["parentId"] = create_raw['applicationId']
        #    menu_obj["applicationId"] = create_raw['applicationId']
        ### Create Tasks
        #menu_response = swimlane_svr.swimlane.request(
        #    'post',
        #    '/task/menu',
        #    json = menu_obj
        #)
        swimlane_svr.task_dictionary = swimlane_svr.getTaskDictionary()

        return create_raw

    def removeOrphanTasks(self, target = True, source = False):

        if target:
            for task_name, task_info in list(self.swimlane_target.task_dictionary.items()):
                if 'applicationId' in task_info and self.swimlane_target.validateApp(byID=task_info['applicationId']) == False:
                    self.logger.info('Task {} has an invalid application ID'.format(task_name))
                    self.delete(task_info['id'], self.swimlane_target)

        self.swimlane_target.task_dictionary = self.swimlane_target.getTaskDictionary()

        if source:
            for task_name, task_info in list(self.swimlane_source.task_dictionary.items()):
                if 'applicationId' in task_info and self.swimlane_source.validateApp(byID=task_info['applicationId']) == False:
                    self.logger.info('Task {} has an invalid application ID'.format(task_name))
                    self.delete(task_info['id'], self.swimlane_source)

        self.swimlane_source.task_dictionary = self.swimlane_source.getTaskDictionary()


    def resolveRecordLinks(self, byTaskName = None, byTaskObj = None):
        task_obj = None

        if byTaskName is not None:
            task_id = self.swimlane_source.validateTask(byName=byTaskName)
            task_obj = self.get(task_id, self.swimlane_source)

        if byTaskObj is not None:
            task_obj = byTaskObj

        if task_obj is None:
            raise Exception('Unable to resolve task object')

        self.log_dictionary[task_obj['name']]['fields'] = []

        if 'applicationId' in task_obj:
            source_app_fields = self.swimlane_source.getFieldDictinoary(byID=task_obj['applicationId'])
            target_app_fields = self.swimlane_target.getFieldDictinoary(byName=self.swimlane_source.validateApp(byID=task_obj['applicationId']))

            if 'inputMapping' in task_obj:
                for task_input in task_obj['inputMapping']:
                    if 'type' in task_input:
                        if task_input['type'] == 'record' and 'value' in task_input:
                            source_field_name = self.swimlane_source.validateField(source_app_fields, byID=task_input['value'])
                            if source_field_name != False:
                                target_field_id = self.swimlane_source.validateField(target_app_fields, byName=source_field_name)
                                if target_field_id != False and task_input['value'] != target_field_id:
                                    self.log_dictionary[task_obj['name']]['fields'].append(buildLogDictionary('recordMapping', 'update', source_field_name, 'From: {}, To {}'.format(task_input['value'], target_field_id)))
                                    task_input['value'] = target_field_id

                        elif task_input['type'] == 'asset':
                            source_asset_name = self.swimlane_source.validateAsset(byID=task_input['value']).get('name')
                            if source_asset_name == False:
                                self.logger.critical('Task {} Output mapping asset id {} not found'.format(task_obj['name'], task_input['value']))
                                continue

                            target_asset_id = self.swimlane_target.validateAsset(byName=source_asset_name).get('id')
                            if target_asset_id == False:
                                self.logger.critical('Task {} Output mapping asset name {} not found'.format(task_obj['name'], source_asset_name))
                                continue

                            if target_asset_id != task_input['value']:
                                self.log_dictionary[task_obj['name']]['fields'].append(buildLogDictionary('assetMapping', 'update', source_asset_name, 'From: {}, To {}'.format(task_input['value'], target_asset_id)))
                                task_input['value'] = target_asset_id


            if 'outputs' in task_obj:
                for output in task_obj['outputs']:
                    if isinstance(output, dict) and 'mappings' in output:
                        for output_task in output['mappings']:
                            if 'value' in output_task:
                                source_field_name = self.swimlane_source.validateField(source_app_fields, byID=output_task['value'])
                                if source_field_name != False:
                                    target_field_id = self.swimlane_source.validateField(target_app_fields, byName=source_field_name)
                                    if target_field_id != False and output_task['value'] != target_field_id:
                                        self.log_dictionary[task_obj['name']]['fields'].append(buildLogDictionary('outputs', 'update', source_field_name, 'From: {}, To {}'.format(output_task['value'], target_field_id)))
                                        output_task['value'] = target_field_id

                    elif isinstance(output,dict) and output['type'] == 'referentialTask':
                        source_task_name = self.swimlane_source.validateTask(byID=output['taskId'])
                        target_task_id = self.swimlane_target.validateTask(byName=source_task_name)
                        if target_task_id == False:
                            self.logger.info('Task {} not found in Target'.format(source_task_name))
                            # source_task_name = self.swimlane_source.validateTask(byID = self.layout_obj['taskId'])
                            if source_task_name == False:
                                self.logger.error('FAILED TO FIND IN SOURCE: Orphan Task RAW Data: {}'.format(self.layout_obj['name']))
                                return False
                            else:
                                self.logger.info('Orphan Cross Reference APP: {}'.format(source_task_name))
                                task_raw = self.migrateTask(source_task_name)
                                if 'id' in task_raw:
                                    self.logger.info('Task ID found in target: {}'.format(task_raw['id']))
                                    output['taskId'] = task_raw['id']
                                    self.updates_made = True
                                else:
                                    self.logger.error('FAILED TO FIND: Target Task ID')
                                    return False
                        else:
                            output['taskId'] = target_task_id


        return task_obj


    def migrateTask(self, taskName):
        task_info = self.swimlane_source.validateTask(byName = taskName)
        if task_info != False:
            self.logger.info('Migrating Task {}'.format(taskName))

            full_task = self.get(task_info, self.swimlane_source)
            ##Remove Fields that shouldn't be migrated
            new_task = copy(full_task)
            new_task.pop('id', None)
            new_task.pop('createdByUser', None)
            new_task.pop('modifiedByUser', None)
            new_task.pop('createdDate', None)
            new_task.pop('modifiedDate', None)

            self.log_dictionary[taskName] = {}
            new_task = self.resolveRecordLinks(byTaskObj = new_task)

            if 'applicationId' in new_task:
                source_app_name = self.swimlane_source.validateApp(byID=new_task['applicationId'])
                if source_app_name != False:
                    new_task['applicationId'] = self.swimlane_target.validateApp(byName=source_app_name)
                    if new_task['applicationId'] == False:
                        raise Exception('Unable to find target application {}'.format(source_app_name))
                else:
                    raise Exception('Unable to find source application name for {}'.format(new_task['applicationId']))

            if 'packageDescriptorId' in new_task['action']:
                s_action = self.swimlane_source.action_dictionary[new_task['action']['packageDescriptorId']]
                s_version = s_action['version']
                found = False
                for k, t_act in self.swimlane_target.action_dictionary.items():
                    t_version = t_act.get('version')
                    if t_act['name'] == s_action['name'] and t_version == s_version:
                        new_task['action']['packageDescriptorId'] = t_act['id']
                        new_task['action']['descriptor']['id'] = t_act['id']
                        new_task['action']['descriptor']['packageDescriptor'] = t_act['packageDescriptor']
                        found = True
                        break
                if not found:
                    filename = '{}.swimbundle'.format(s_action['packageDescriptor']['name'])
                    self.logger.info('{} not found. Migrating...'.format(filename))
                    new_bundle = self.copy_swimbundle(s_action['packageDescriptor']['fileId'], filename)
                    self.swimlane_target.action_dictionary = self.swimlane_target.getActionDictionary()
                    for k, t_act in self.swimlane_target.action_dictionary.items():
                        if t_act['name'] == s_action['name'] and t_act['assetDependencyVersion'] == s_action['assetDependencyVersion']:
                            new_task['action']['packageDescriptorId'] = t_act['id']
                            new_task['action']['descriptor']['id'] = t_act['id']
                            new_task['action']['descriptor']['packageDescriptor'] = t_act['packageDescriptor']
                            found = True
                            break
                    if not found:
                        raise Exception('No action found on target named {} with version number {}'.format(s_action['name'],s_action['assetDependencyVersion']))

            if 'assetId' in new_task['action']:
                new_task['action']['assetId'] = self.convert_asset(new_task['action']['assetId'])

            for trigger in new_task['triggers']:
                if 'assetId' in trigger:
                    trigger['assetId'] = self.convert_asset(trigger['assetId'])

            for output in new_task['outputs']:
                if 'assetId' in output:
                    output['assetId'] = self.convert_asset(output['assetId'])

            target_task = self.swimlane_target.validateTask(byName = taskName)
            if target_task != False:
                self.logger.info('Task is on Target - Merge Changes with app ID: {}'.format(target_task))
                new_task['id'] = target_task
                self.log_dictionary[taskName]['action'] = 'update'
                return self.update(new_task, target_task, self.swimlane_target)
            else:
                self.log_dictionary[taskName]['action'] = 'create'
                return self.create(new_task, self.swimlane_target)



        else:
            raise Exception('Failed to find Task {}'.format(taskName))


    def convert_asset(self, src_asset_id):
        src_asset = self.swimlane_source.asset_dictionary_id[src_asset_id]
        try:
            target_asset = self.swimlane_target.asset_dictionary_name[src_asset['name']]
        except:
            raise Exception('No asset on target named {}'.format(src_asset['name']))
        if 'version' in src_asset:
            #if self.sw_source_version >= 10.3:
            #Removing as 10.10 is technically less than 10.3 in python
            if target_asset['descriptor']['version'] == src_asset['descriptor']['version']:
                dst_asset_id = target_asset['id']
                return dst_asset_id
            else:
                raise Exception('No asset on target named {} with version {}.'.format(src_asset['name'],
                                                                                      src_asset['version']))
            #else:
            #    if target_asset['version'] == src_asset['version']:
            #        dst_asset_id = target_asset['id']
            #        return dst_asset_id
            #   else:
            #        raise Exception('No asset on target named {} with version {}.'.format(src_asset['name'],
            #                                                                              src_asset['version']))
        else:
            dst_asset_id = target_asset['id']
            return dst_asset_id


    def copy_swimbundle(self, file_id, filename):
        stream = BytesIO()
        response = self.swimlane_source.swimlane.request('get', 'attachment/download/{}'.format(file_id), stream=True)
        for chunk in response.iter_content(1024):
            stream.write(chunk)
        stream.seek(0)

        upload = self.swimlane_target.swimlane.request('post', "/task/packages",
                                              files={'file': (filename, stream.read())})
        return upload.json()

