# Copyright (C) 2022 Indoc Research
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
from logging import DEBUG
from logging import ERROR

import httpx

from common.lineage.entity_object import Entity
from common.lineage.entity_object import FileDataAttribute
from common.lineage.lineage_object import Lineage
from common.lineage.lineage_object import LineageAttirbute
from common.logger import LoggerFactory
from common.lineage.entity_object import FileDataAttribute, Entity
from common.lineage.lineage_object import LineageAttirbute, Lineage


class LineageClient:
    def __init__(self, atlas_endpoint: str, username: str, password: str) -> None:
        self.atlas_endpoint = atlas_endpoint
        self.username = username
        self.password = password

        self.headers = {'content-type': 'application/json'}

        self.logger = LoggerFactory('LineageClient').get_logger()
        self.logger.setLevel(ERROR)

    async def debug_on(self):
        """
        Summary:
            The funtion will switch the log level to DEBUG
        """
        self.logger.setLevel(DEBUG)

        return

    async def debug_off(self):
        """
        Summary:
            The funtion will switch the log level to ERROR
        """
        self.logger.setLevel(ERROR)

        return

    async def update_entity(
        self,
        _id: str,
        file_name: str,
        path: str,
        container_code: str,
        owner: str,
        zone: int,
        entity_type: str,
        container_type: str = "project",
        archive: bool = False,
    ) -> dict:
        """
        Summary:
            The function will create a entity in the Atlas if it is not exist.
            It will update the entity that if **_id** exists in atlas.
            Note this function will only apply to {self.entity_type} type which is ONLY one in used

        Parameter:
            - _id(uuid4): the unique identifier in metadata service
            - file_name(str): file name in database
            - path(str): file path in database
            - owner(str): the owner of file
            - container_code(str): the container code
            - zone(int): indicate the whether the file is in the greenroom(0) or core(1)
            - archive(bool): the bool value to indicate if file/ffolder be archived
            - container_type(str): the type of container

        return:
            - dict
        """

        self.logger.info(f'Create entity of file {file_name}')

        # format the atlas entity
        attributes = FileDataAttribute(_id, file_name, path, zone, container_code, container_type, archive)
        entity = Entity(entity_type, attributes, owner)
        post_payload = {'entity': entity.json()}

        async with httpx.AsyncClient(verify=False) as client:
            self.logger.info('endpoint: ' + self.atlas_endpoint + '/api/atlas/v2/entity')
            self.logger.info('payload:')
            self.logger.info(post_payload)

            response = await client.post(
                self.atlas_endpoint + '/api/atlas/v2/entity',
                json=post_payload,
                auth=(self.username, self.password),
                headers=self.headers,
                timeout=60,
            )
            if response.status_code != 200:
                error_msg = f'Fail to create entity in Atlas with error: {response.text}'
                self.logger.error(error_msg)
                raise Exception(error_msg)

        return response.json()

    async def delete_entity(self, _id: str, entity_type: str):
        """
        Summary:
            The function will delete entity in atlas with target id

        Parameter:
            - _id(uuid4): the unique identifier in metadata service

        return:
            - dict
        """

        self.logger.info(f'Delete entity with {_id}')

        async with httpx.AsyncClient(verify=False) as client:
            response = await client.delete(
                self.atlas_endpoint + '/api/atlas/v2/entity/uniqueAttribute/type/{}'.format(entity_type),
                params={'attr:item_id': _id},
                auth=(self.username, self.password),
                timeout=60,
            )

            if response.status_code != 200:
                error_msg = f'Fail to delete entity in Atlas with error: {response.text}'
                self.logger.error(error_msg)
                raise Exception(error_msg)

        return response.json()

    async def get_lineage(self, _id: str, entity_type: str, direction: str = 'INPUT') -> dict:
        """
        Summary:
            The function will get the lineage in the Atlas by the id

        Parameter:
            - _id(uuid4): the unique identifier in metadata service
            - direction(str): can be INPUT or OUTPUT
            - entity_type(str): the type of entity, by default is file_data

        return:
            - dict
        """

        self.logger.info(f'Get lineage with {_id}')

        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(
                self.atlas_endpoint + '/api/atlas/v2/lineage/uniqueAttribute/type/{}'.format(entity_type),
                params={'attr:item_id': _id, 'depth': 50, 'direction': direction},
                auth=(self.username, self.password),
                timeout=60,
            )

            if response.status_code != 200:
                error_msg = f'Fail to get lineage in Atlas with error: {response.text}'
                self.logger.error(error_msg)
                raise Exception(error_msg)

            # here add conner case that no matter what the guidEntityMap in
            # lineage information will contains the input node with <_id>
            # add the placeholder of <_id> in guidEntityMap. In the loop below,
            # the logic will fetch entity from database.
            res = response.json()
            atlas_guid = res.get('baseEntityGuid')
            # and DON'T overwrite one if there is on in lineage
            if res['guidEntityMap'].get(atlas_guid) is None:
                res['guidEntityMap'].update({atlas_guid: {"guid": atlas_guid}})

            # then loop over each of entity to get the detail attribute
            for atlas_guid in res['guidEntityMap']:
                response = await client.get(
                    self.atlas_endpoint + '/api/atlas/v2/entity/guid/{}'.format(atlas_guid),
                    auth=(self.username, self.password),
                    timeout=60,
                )

                # then use the attribute to update return dict
                entity_attribute = response.json().get('entity', {}).get('attributes')
                res['guidEntityMap'][atlas_guid].update({"attributes": entity_attribute})

        return res

    async def create_lineage(
        self,
        input_id: str,
        output_id: str,
        input_name: str,
        output_name: str,
        project_code: str,
        pipeline_name: str,
        entity_type: str,
        description: str = '',
        created_time = time.time(),
    ):

        """
        Summary:
            The function will create a lineage between two entity in the Atlas

        Parameter:
            - input_id(uuid4): the unique identifier of input file in metadata
            - output_id(uuid4): the unique identifier of output file in metadata
            - input_name(str): full path of input file or name
            - output_name(int): full path of output file or name
            - project_code(str): the project code of file
            - pipeline_name(str): the name of pipeline operations (copy/delete)
            - entity_type(str): the type of entity, by default is file_data
            - description(str): description of operations
            - created_time(timestamp): default is current time. the timestamp that
                lineage is created.

        return:
            - dict
        """

        name = '{}:{}:{}:to:{}@{}'.format(
            project_code,
            pipeline_name,
            input_name,
            output_name,
            created_time,
        )

        # NOTE: the id is the uuid in metadata service NOT the guid in Atlas
        lineage_attirbute = LineageAttirbute(name, entity_type, input_id, entity_type, output_id, description)
        lineage = Lineage('Process', lineage_attirbute)
        atlas_post_form_json = {'entities': [lineage.json()]}

        async with httpx.AsyncClient(verify=False) as client:
            self.logger.info('endpoint: ' + self.atlas_endpoint + '/api/atlas/v2/entity')
            self.logger.info('payload:')
            self.logger.info(atlas_post_form_json)

            response = await client.post(
                self.atlas_endpoint + '/api/atlas/v2/entity/bulk',
                json=atlas_post_form_json,
                auth=(self.username, self.password),
                headers=self.headers,
                timeout=60,
            )
            if response.status_code != 200:
                error_msg = f'Fail to create lineage in Atlas with error: {response.text}'
                self.logger.error(error_msg)
                raise Exception(error_msg)

        return response.json()
