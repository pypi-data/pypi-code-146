# -------------------------------------------------------------------------
# Copyright (c) Switch Automation Pty Ltd. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import json
from typing import List, Union
import uuid
from switch_api._utils._utils import ApiInputs
import requests
import switch_api as sw
from ...models.step import SwitchGuideStepComponent
from .form_data import FormData, SectionData, FieldData, RowData


def define_ui_component(form_id: str, form_keys: List[str] = [], options = [], data = []) -> SwitchGuideStepComponent:
    """
    Defines a basic Forms Viewer Component to be displayed on the UI.

    Parameters
    ----------
    form_id: UUID
        Form Definition Id
    form_keys: List[str]
        Optional, list of form keys used to scope data to a specific form instance
    options: List[dict]
        Optional, list of configuration options
    data: List[dict]
        Optional, list of data prepopulate the form

    Returns SwitchGuideStepComponent
    -------
    """

    component = SwitchGuideStepComponent(
        type='Vue',
        id='FormsViewer',
        attributes={
            'formId': form_id,
            # Set in check_ui_component()
            'formDataKeys': [],
            'configurationOptions': [
                {
                    "section": 1,
                    "fields": [],
                    "rows": []
                }
            ],
            'configData': [
                {
                    "section": 1,
                    "fields": [],
                    "rows": []
                }
            ]
        }
    )

    if form_keys and len(form_keys) > 0:
        component.attributes['formDataKeys'] = form_keys

    if options and len(options) > 0:
        component.attributes['configurationOptions'] = options

    if data and len(data) > 0:
        component.attributes['configData'] = data

    return component


def get_data(api_inputs: ApiInputs, form_id: uuid.UUID, form_key: str = '') -> Union[FormData, None]:
    """
    Retrieves the data from a form instance in the Switch platform.

    Parameters
    ----------
    api_inputs: ApiInputs
        Object returned by initialize() function.
    form_id: UUID
        Form Definition Id
    form_key_value: str
        Optional, form key used to form scope data to a specific form instance
        When not provided, will scope data to the Portfolio

    Returns
    -------
    """

    headers = api_inputs.api_headers.integration

    if not form_key:
        form_key = str(uuid.UUID(int=0))
    
    url = f"{api_inputs.api_projects_endpoint}/{api_inputs.api_project_id}/jsonforms/{form_id}/keyvalue/{form_key}"
    response = requests.get(url, headers=headers)

    response_status = '{} {}'.format(response.status_code, response.reason)

    if response.status_code != 200:
        sw.pipeline.logger.error(f"Error retrieving form data: {response_status}")
        return None
    elif len(response.text) == 0:
        sw.pipeline.logger.error(f"Empty form data retrieved: {response_status}")
        return None

    response_json = json.loads(response.text)

    form_data = _extract_form_data(response_json)

    return form_data

def _extract_form_data(form_data) -> FormData:
    section_data: dict[int, SectionData] = {}

    if len(form_data) == 0:
        return None

    try:
        for section in form_data['data']['data']:
            section_data[section['id']] = SectionData(
                id=section['id'],
                name=section['name'],
                type=section['type'],
                fields=_extract_fields(section['data']),
                rows=_extract_rows(section['data'])
            )
    except:
        sw.pipeline.logger.error(f"Form data extraction failed", exc_info=True)

    form = FormData(sections=section_data)

    return form

def _extract_fields(fields: List[dict]) -> List[FieldData]:
    field_data: List[FieldData] = []

    for field in fields['variables']:
        field_data.append(FieldData(
            id=field['id'],
            label=field['label'],
            value=field['value'],
            type=field['type']
        ))

    return field_data

def _extract_rows(rows: List[dict]) -> List[RowData]:
    row_data: List[RowData] = []

    for row in rows['data']:
        row_data.append(RowData(
            variables=_extract_fields(row),
            id=row['id']
        ))

    return row_data
