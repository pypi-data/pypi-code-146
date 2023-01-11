import zipfile
from io import BytesIO

import pydicom as pydicom
import requests
from PIL import Image
import numpy as np
import cv2
from zipfile import ZipFile

from ango.sdk import SDK
from ango.plugins import ExportPlugin, run

HOST = 'https://apibeta.ango.ai'
API_KEY = "d378c1ed-4895-467f-af63-fb069fc19090"
PLUGIN_ID = "63903d917027f500125dfce0"
PLUGIN_SECRET = "81412d7f-2557-4854-98bd-dab0851cc0dd"

sdk = SDK(api_key=API_KEY, host=HOST)


def polygon_to_single_mask(project_id: str, data: dict):
    project_info = sdk.get_project(project_id)
    tool_list = project_info['data']['project']['categorySchema']['tools']

    class_name_list = []
    for tool in tool_list:
        if tool['tool'] == 'polygon':
            class_name = tool['title']
            class_name_list.append(class_name)

    class_mapping = {}
    for class_index, class_name in enumerate(class_name_list):
        class_mapping[class_name] = class_index + 1

    mem_zip = BytesIO()
    with zipfile.ZipFile(mem_zip, mode="w") as zf:
        for current_data in data:
            img_url = current_data['asset']
            file_type = img_url.split('.')[-1]

            response = requests.get(img_url)
            if file_type == 'dcm':
                dicom_data = pydicom.dcmread(BytesIO(response.content))
                img = dicom_data.pixel_array
            else:
                img = Image.open(BytesIO(response.content))
                img = np.array(img)

            task_id = current_data['tasks'][0]['taskId']
            objects = current_data['tasks'][0]['objects']

            # Semantic Segmentation
            mask_array = np.zeros(img.shape[0:2], dtype=np.uint8)
            for obj_ind, obj in enumerate(objects):
                if 'polygon' not in obj:
                    continue
                instance_mask_array = np.zeros(img.shape[0:2], dtype=np.uint8)
                class_name = obj['title']
                if class_name not in class_name_list:
                    continue

                class_index = class_name_list.index(class_name)
                polygon = obj['polygon']
                polygon = np.array(polygon)
                polygon = np.round(polygon).astype(int)

                instance_mask_array = cv2.fillPoly(instance_mask_array, pts=[polygon], color=(class_index + 1))

                x_indices, y_indices = np.where(instance_mask_array != 0)
                mask_array[x_indices, y_indices] = instance_mask_array[x_indices, y_indices]

            img = Image.fromarray(mask_array)
            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            zf.writestr(task_id + '.png', img_buffer.getvalue())
    return project_id+'.zip', mem_zip


plugin = ExportPlugin(id=PLUGIN_ID, secret=PLUGIN_SECRET,
                      api_key=API_KEY, callback=polygon_to_single_mask,
                      host=HOST)

run(plugin, host=HOST)