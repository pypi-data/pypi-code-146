from .base.fields import fields
from copy import copy
import sys

class usergroups(fields):

    def __init__(self, field_obj, source_obj, config ):
        super(usergroups, self).__init__(field_obj, config)
        self.source_object = source_obj

    def migrateMembers(self):
        source_members = self.source_object['members']
        new_members_list = []

        for member in self.source_object['members']:
            new_member = copy(member)

            if member['itemType'] == 'group':
                try:
                    self.logger.info('Looking up Group: {}'.format(member))
                    sw_group = self.swimlane_target.swimlane.groups.get(name=member['name'])
                    new_member['id'] = sw_group.id
                    new_members_list.append(new_member)
                except ValueError as e:
                    self.logger.error('Group: {} not found removing'.format(member['name']))


            elif member['itemType'] == 'user':
                try:
                    self.logger.info('Looking up User: {}'.format(member))
                    sw_user = self.swimlane_target.swimlane.users.get(display_name=member['name'])
                    new_member['id'] = sw_user.id
                    new_members_list.append(new_member)
                except ValueError as e:
                    self.logger.error('User: {} not found removing'.format(member['name']))

        self.field_obj['members'] = new_members_list

        return self.field_obj