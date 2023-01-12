import json, sys

class groups(object):

    def __init__(self, config):

        self.logger = config.pop('logger', None)
        self.swimlane_source = config.pop('swimlane_source', None)
        self.swimlane_target = config.pop('swimlane_target', None)

        if self.swimlane_source is None:
            raise  Exception('You must provide a swimlane_source object')

        if self.swimlane_target is None:
            raise  Exception('You must provide a swimlane_target object')

        self.remove_keys = ['createdDate', 'modifiedDate', 'createdByUser', 'modifiedByUser']
        self.group_exclustions = ['Everyone']
        self.mode = config['mode']

    def getGroups(self, swimlane_server):
        groups_response = swimlane_server.swimlane.request(
            'get',
            '/groups'
        )

        return json.loads(groups_response.text)


    def addGroup(self, swimlane_server, group):
        groups_response = swimlane_server.swimlane.request(
            'post',
            '/groups',
            json = group
        )

        return json.loads(groups_response.text)

    def updateGroup(self, swimlane_server, group_id, group):
        groups_response = swimlane_server.swimlane.request(
            'put',
            '/groups/{}'.format(group_id),
            json = group
        )

        return json.loads(groups_response.text)

    def lookupGroup(self, swimlane_server, name):
        groups_response = swimlane_server.swimlane.request(
            'get',
            '/groups/lookup?name={}'.format(name)
        )

        return json.loads(groups_response.text)

    def migrateGroups(self):
        sw_source_groups_raw = self.getGroups(self.swimlane_source)
        sw_target_groups_raw = self.getGroups(self.swimlane_target)

        for group in sw_source_groups_raw['groups']:
            if group['name'] not in self.group_exclustions:
                self.logger.info('Working with Group: {}'.format(group['name']))

                ## Process Users
                for user_members in group['users']:
                    source_user_obj = self.swimlane_source.swimlane.users.get(id=user_members['id'])
                    try:
                        target_user_obj = self.swimlane_target.swimlane.users.get(display_name=source_user_obj.display_name)
                        user_members['id'] = target_user_obj.id
                        user_members['name'] = target_user_obj.username
                    except ValueError as e:
                        ## Unable to find user - remove user association
                        self.logger.warn('User: {} not found removing from Group: {}'.format(source_user_obj.display_name, group['name']))
                        if self.mode == 'Live':
                            group['users'].remove(user_members)


                for group_members in group['groups']:
                    source_group_obj = self.swimlane_source.swimlane.groups.get(id=group_members['id'])
                    try:
                        target_group_obj = self.swimlane_target.swimlane.groups.get(name=source_group_obj.name)
                        group_members['id'] = target_group_obj.id
                        group_members['name'] = target_group_obj.name
                    except ValueError as e:
                        ## Unable to find group attempt to add
                        self.logger.warn('Group: {} not found attempting to add'.format(source_user_obj.name))
                        new_group = {}
                        new_group['id'] = source_group_obj.id
                        new_group['description'] = source_group_obj.description
                        new_group['name'] = source_group_obj.name
                        new_group['disabled'] =  source_group_obj.disabled
                        if self.mode == 'Live':
                            new_group = addGroup(self.swimlane_target, new_group)
                            sw_target_groups_raw['groups'].append(new_group)

                target_group_key = self.find_in_list(sw_target_groups_raw['groups'], 'name', group['name'])
                self.logger.info('Target Key: {}'.format(target_group_key))
                if target_group_key is None:
                    ## New Group
                    for key in self.remove_keys:
                        if key in group:
                            group.pop(key)

                    ## Had to wrap in try it seems that some groups don't get returned when you ask for the groups
                    try:
                        if self.mode == 'Live':
                            add_group = self.addGroup(self.swimlane_target, group)
                            sw_target_groups_raw['groups'].append(add_group)
                    except Exception as e:
                        update_group_obj = self.swimlane_target.swimlane.groups.get(name=group['name'])
                        update_group = update_group_obj._raw
                        update_group['users'] = group['users']
                        if self.mode == 'Live':
                            self.updateGroup(self.swimlane_target, update_group['id'], update_group)
                            sw_target_groups_raw['groups'].append(update_group)
                else:
                    update_group = sw_target_groups_raw['groups'][target_group_key]
                    update_group['users'] = group['users']
                    update_group['groups'] = group['groups']
                    if self.mode == 'Live':
                        self.updateGroup(self.swimlane_target, update_group['id'], update_group)

    def find_in_list(self, lst, key, value):
        for i, dic in enumerate(lst):
            if key in dic and dic[key] == value:
                return i
        return None



