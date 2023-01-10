import json
from typing import Dict, Optional, Union, Iterable

import numpy as np
from pandas import DataFrame
from imaginairy import imagine, ImaginePrompt
from PIL import Image

from ..base_provider import BaseProvider
from lumipy.provider.metadata import ColumnMeta, ParamMeta, TableParam
from lumipy.typing.sql_value_type import SqlValType


class StableDiffusion(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('prompt', SqlValType.Text),
            ColumnMeta('shape', SqlValType.Text),
            ColumnMeta('array_str', SqlValType.Text),
        ]
        params = [
            ParamMeta('steps', SqlValType.Int, default_value=20),
            ParamMeta('prompt_strength', SqlValType.Double, default_value=15),
            ParamMeta('sampler_type', SqlValType.Text, default_value='DDIM'),
            ParamMeta('fix_faces', SqlValType.Boolean, default_value=False),
        ]
        table_params = [TableParam('prompts')]

        super().__init__(
            'test.stable.diffusion',
            columns=columns,
            parameters=params,
            table_parameters=table_params,
            description="A test provider that wraps the generation of images with stable diffusion (via imaginairy)"
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> Union[DataFrame, Iterable[DataFrame]]:

        prompts = params.get('prompts').values.flatten().tolist()

        prompt_objs = [
            ImaginePrompt(
                p,
                sampler_type=params.get('sampler_type'),
                steps=params.get('steps'),
                prompt_strength=params.get('prompt_strength'),
                fix_faces=params.get('fix_faces'),
                seed=np.random.randint(0, 1000000),
            )
            for p in prompts
        ]

        for prompt, result in zip(prompts, imagine(prompt_objs)):
            np_image = np.array(result.img)
            yield DataFrame([{
                'prompt': prompt,
                'shape': json.dumps(np_image.shape),
                'array_str': json.dumps(np_image.flatten().tolist())
            }])

    @staticmethod
    def img_from_row(row):
        return Image.fromarray(
            np.uint8(np.array(
                json.loads(row['array_str'])
            ).reshape(
                json.loads(row['shape'])
            ))
        )
