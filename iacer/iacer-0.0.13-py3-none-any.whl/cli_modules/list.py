# -*- coding: utf-8 -*-
import asyncio
import logging

from iacer.generate_params import IAC_NAME
from iacer.plugin.ros import StackPlugin
from iacer.stack import SYS_TAGS

LOG = logging.getLogger(__name__)


class List:
    '''
    List stacks which were created by Iacer for all regions.
    '''

    def __init__(self, regions: str = None):
        '''
        :param regions:  comma separated list of regions to delete from, default will scan all regions
        '''
        self.regions = regions

    @classmethod
    async def create(cls, regions: str = None):
        if regions:
            regions = regions.split(',')
        else:
            region_plugin = StackPlugin(region_id='cn-hangzhou')
            regions = await region_plugin.get_regions()
        list_tasks = []
        for region in regions:
            stack_plugin = StackPlugin(region_id=region)
            list_tasks.append(
                asyncio.create_task(stack_plugin.fetch_all_stacks(SYS_TAGS))
            )
        stacks = await asyncio.gather(*list_tasks)
        all_stacks, project_length, test_length, stack_name_length = cls._get_all_stacks(stacks)
        if not all_stacks:
            LOG.info('can not find any stack.')
            return
        header = f'ProjectName{" "*project_length}TestName{" "*test_length}StackName{" "*stack_name_length}Region'
        LOG.info(header)
        column = '{}           {}        {}         {}'
        for stack in all_stacks:
            project_name = cls._format_name(stack['ProjectName'], project_length)
            test_name = cls._format_name(stack['TestName'], test_length)
            stack_name = cls._format_name(stack['StackName'], stack_name_length)
            LOG.info(column.format(project_name, test_name, stack_name, stack['RegionId']))
        return all_stacks

    @classmethod
    def _get_all_stacks(cls, stacks):
        all_stacks = []
        longest_project_name = ''
        longest_test_name = ''
        longest_stack_name = ''
        for region_stacks in stacks:
            for stack in region_stacks:
                stack_name = stack['StackName']
                if len(stack_name) > len(longest_stack_name):
                    longest_stack_name = stack_name
                tags = stack['Tags']
                for tag in tags:
                    if tag['Key'] == f'{IAC_NAME}-test-name':
                        test_name = tag['Value']
                        if len(test_name) > len(longest_test_name):
                            longest_test_name = test_name
                        stack['TestName'] = test_name
                    elif tag['Key'] == f'{IAC_NAME}-project-name':
                        project_name = tag['Value']
                        if len(project_name) > len(longest_project_name):
                            longest_project_name = project_name
                        stack['ProjectName'] = project_name
                    elif tag['Key'] == f'{IAC_NAME}-id':
                        stack['TestId'] = tag['Value']
                all_stacks.append(stack)

        return all_stacks, len(longest_project_name), len(longest_test_name), len(longest_stack_name)

    @classmethod
    def _format_name(cls, name, length):
        if len(name) < length:
            name += f'{" " * (length - len(name))}'
        return name
