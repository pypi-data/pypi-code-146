# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Upgrade Views for ASGI
"""

import asyncio
import json
import os
from urllib.parse import parse_qs

from tailbone.views.asgi import WebsocketView
from tailbone.progress import get_basic_session


class UpgradeExecutionProgressWS(WebsocketView):

    # keep track of all "global" state for this socket
    global_state = {
        'upgrades': {},
    }

    new_messages = asyncio.Queue()

    async def __call__(self, scope, receive, send):
        app = self.get_rattail_app()

        # is user allowed to see this?
        if not await self.authorize(scope, receive, send, 'upgrades.execute'):
            return

        # keep track of client state
        client_state = {
            'uuid': app.make_uuid(),
            'disconnected': False,
            'scope': scope,
            'receive': receive,
            'send': send,
        }

        # parse upgrade uuid from query string
        query = scope['query_string'].decode('utf_8')
        query = parse_qs(query)
        uuid = query['uuid'][0]

        # first client to request progress for this upgrade, must
        # start a task to manage the collect/transmit logic for
        # progress data, on behalf of this and/or any future clients
        started_task = None
        if uuid not in self.global_state['upgrades']:

            # this upgrade is new to us; establish state and add first client
            upgrade_state = self.global_state['upgrades'][uuid] = {
                'clients': {client_state['uuid']: client_state},
            }

            # start task for transmit of progress data to all clients
            started_task = asyncio.create_task(self.manage_progress(uuid))

        else:

            # progress task is already running, just add new client
            upgrade_state = self.global_state['upgrades'][uuid]
            upgrade_state['clients'][client_state['uuid']] = client_state

        async def wait_for_disconnect():
            message = await receive()
            if message['type'] == 'websocket.disconnect':
                client_state['disconnected'] = True

        # wait forever, until client disconnects
        asyncio.create_task(wait_for_disconnect())
        while not client_state['disconnected']:

            # can stop if upgrade has completed
            if uuid not in self.global_state['upgrades']:
                break

            await asyncio.sleep(0.1)

        # remove client from global set, if upgrade still running
        if client_state['disconnected']:
            upgrade_state = self.global_state['upgrades'].get(uuid)
            if upgrade_state:
                del upgrade_state['clients'][client_state['uuid']]

        # must continue to wait for other clients, if this client was
        # the first to request progress
        if started_task:
            await started_task

    async def manage_progress(self, uuid):
        """
        Task which handles collect / transmit of progress data, for
        sake of all attached clients.
        """
        progress_session_id = 'upgrades.{}.execution_progress'.format(uuid)
        progress_session = get_basic_session(self.rattail_config,
                                             id=progress_session_id)

        # start collecting status, textout messages
        asyncio.create_task(self.collect_status(uuid, progress_session))
        asyncio.create_task(self.collect_textout(uuid))

        upgrade_state = self.global_state['upgrades'][uuid]
        clients = upgrade_state['clients']
        while clients:

            msg = await self.new_messages.get()

            # send message to all clients
            for client in clients.values():
                await client['send']({
                    'type': 'websocket.send',
                    'subtype': 'upgrades.execute_progress',
                    'text': json.dumps(msg)})

            await asyncio.sleep(0.1)

        # no more clients, no more reason to track this upgrade
        del self.global_state['upgrades'][uuid]

    async def collect_status(self, uuid, progress_session):

        upgrade_state = self.global_state['upgrades'][uuid]
        clients = upgrade_state['clients']
        while True:

            # load latest progress data
            progress_session.load()

            # when upgrade progress is complete...
            if progress_session.get('complete'):

                # maybe set success flash msg (for all clients)
                msg = progress_session.get('success_msg')
                if msg:
                    for client in clients.values():
                        user_session = self.get_user_session(client['scope'])
                        user_session.flash(msg)
                        user_session.persist()

                # push "complete" message to queue
                await self.new_messages.put({'complete': True})

                # there will be no more status coming
                break

            await asyncio.sleep(0.1)

    async def collect_textout(self, uuid):
        path = self.rattail_config.upgrade_filepath(uuid, filename='stdout.log')

        # wait until stdout file exists
        while not os.path.exists(path):

            # bail if upgrade is complete
            if uuid not in self.global_state['upgrades']:
                return

            await asyncio.sleep(0.1)

        offset = 0
        while True:

            # wait until we have something new to read
            size = os.path.getsize(path) - offset
            while not size:

                # bail if upgrade is complete
                if uuid not in self.global_state['upgrades']:
                    return

                # wait a whole second, then look again
                # (the less frequent we look, the bigger the chunk)
                await asyncio.sleep(1)
                size = os.path.getsize(path) - offset

            # bail if upgrade is complete
            if uuid not in self.global_state['upgrades']:
                return

            # read the latest chunk and bookmark new offset
            with open(path, 'rb') as f:
                f.seek(offset)
                chunk = f.read(size)
                textout = chunk.decode('utf_8')
            offset += size

            # push new chunk onto message queue
            textout = textout.replace('\n', '<br />')
            await self.new_messages.put({'stdout': textout})

            await asyncio.sleep(0.1)

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)

    @classmethod
    def _defaults(cls, config):
        config.add_tailbone_websocket('upgrades.execution_progress', cls)


def defaults(config, **kwargs):
    base = globals()

    UpgradeExecutionProgressWS = kwargs.get('UpgradeExecutionProgressWS', base['UpgradeExecutionProgressWS'])
    UpgradeExecutionProgressWS.defaults(config)


def includeme(config):
    defaults(config)
