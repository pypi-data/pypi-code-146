import json, sys

class roles(object):

    def __init__(self, config):

        self.logger = config.pop('logger', None)
        self.swimlane_source = config.pop('swimlane_source', None)
        self.swimlane_target = config.pop('swimlane_target', None)

        if self.swimlane_source is None:
            raise  Exception('You must provide a swimlane_source object')

        if self.swimlane_target is None:
            raise  Exception('You must provide a swimlane_target object')

        self.remove_keys = ['createdDate', 'modifiedDate', 'createdByUser', 'modifiedByUser']
        self.role_exclustions = ['Administrator']
        self.mode = config['mode']


    def getRoles(self, swimlane_server):
        roles_response = swimlane_server.swimlane.request(
            'get',
            '/roles'
        )

        return json.loads(roles_response.text)

    def addRole(self, swimlane_server, role):
        role_response = swimlane_server.swimlane.request(
            'post',
            '/roles',
            json = role
        )

        return json.loads(role_response.text)

    def updateRole(self, swimlane_server, role_id, role):
        role_response = swimlane_server.swimlane.request(
            'put',
            '/roles/{}'.format(role_id),
            json = role
        )

        return json.loads(role_response.text)


    def migrateRoles(self):
        sw_source_roles_raw = self.getRoles(self.swimlane_source)
        sw_target_roles_raw = self.getRoles(self.swimlane_target)

        for role in sw_source_roles_raw:
            if role['name'] not in self.role_exclustions:
                self.logger.info('----------------------------------------')
                self.logger.info('Working on Role: {}'.format(role['name']))
                ## Process Users
                for user_members in role['users']:
                    self.logger.info('Working on User: {}'.format(user_members['name']))
                    source_user_obj = self.swimlane_source.swimlane.users.get(id=user_members['id'])
                    try:
                        target_user_obj = self.swimlane_target.swimlane.users.get(display_name=source_user_obj.display_name)
                        user_members['id'] = target_user_obj.id
                        user_members['name'] = target_user_obj.username
                    except ValueError as e:
                        ## Unable to find user - remove user association
                        self.logger.warn('User: {} not found removing from Role: {}'.format(source_user_obj.display_name, role['name']))
                        if self.mode == 'Live':
                            role['users'].remove(user_members)

                ## Process Groups
                for group_members in role['groups']:
                    self.logger.info('Working on Group: {}'.format(group_members['name']))
                    source_group_obj = self.swimlane_source.swimlane.groups.get(id=group_members['id'])
                    try:
                        target_group_obj = self.swimlane_target.swimlane.groups.get(name=source_group_obj.name)
                        group_members['id'] = target_group_obj.id
                        group_members['name'] = target_group_obj.name
                    except ValueError as e:
                        ## Unable to find group attempt to add
                        self.logger.warn('Group: {} not found attempting to add'.format(source_user_obj.name))
                        if self.mode == 'Live':
                            new_group = {}
                            new_group['id'] = source_group_obj.id
                            new_group['description'] = source_group_obj.description
                            new_group['name'] = source_group_obj.name
                            new_group['disabled'] =  source_group_obj.disabled
                            new_group = addGroup(self.swimlane_target, new_group)

                target_role_key = self.find_in_list(sw_target_roles_raw, 'name', role['name'])
                self.logger.info('Target Key: {}'.format(target_role_key))
                if target_role_key is None:
                    ## New Group
                    for key in self.remove_keys:
                        if key in role:
                            role.pop(key)

                    ## Had to wrap in try it seems that some groups don't get returned when you ask for the groups
                    if self.mode == 'Live':
                        add_role = self.addRole(self.swimlane_target, role)
                        sw_target_roles_raw.append(add_role)

                else:
                    update_role = sw_target_roles_raw[target_role_key]
                    update_role['users'] = role['users']
                    update_role['groups'] = role['groups']
                    if self.mode == 'Live':
                        self.updateRole(self.swimlane_target, update_role['id'], update_role)

    def find_in_list(self, lst, key, value):
        for i, dic in enumerate(lst):
            if key in dic and dic[key] == value:
                return i
        return None