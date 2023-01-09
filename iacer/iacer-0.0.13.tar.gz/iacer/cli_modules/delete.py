# -*- coding: utf-8 -*-
import logging

from iacer.cli_modules.list import List
from iacer.stack import Stacks, Stack, Stacker
from iacer.termial_print import TerminalPrinter

LOG = logging.getLogger(__name__)


class Delete:
    '''
    Manually clean up the stacks which were created by Iacer
    '''

    def __init__(self, regions: str = None):
        '''
        :param regions: comma separated list of regions to delete from, default will scan all regions
        '''
        self.regions = regions

    @classmethod
    async def create(cls, regions: str = None):
        all_stacks = await List.create(regions)
        if not all_stacks:
            LOG.info('can not find stack to delete.')
            return
        LOG.info('Start delete above stacks')
        stacks = Stacks()
        stacks += [Stack.from_stack_response(stack) for stack in all_stacks]

        stacker = Stacker.from_stacks(stacks)
        await stacker.delete_stacks()
        printer = TerminalPrinter()
        await printer.report_test_progress(stacker)
