import txp.common.reports.section as sections
from typing import List, Dict
import datetime
import pandas as pd
import pytz
from txp.common.config import settings
from PIL import Image
import os


class MockDoubleLine(sections.Plot2dSection):
    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            axes_names: List[str],
            lines: List,
            **kwargs
    ):
        super(MockDoubleLine, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime,
            axes_names, lines, **kwargs
        )

    @classmethod
    def required_inputs(cls) -> List[sections.SectionInputEnum]:
        """Returns the List of required inputs to compute the section result
        """
        return [sections.SectionInputEnum.RAW_TIME]

    @classmethod
    def compute(cls, inputs: Dict[str, pd.DataFrame], section_event_payload: Dict) -> Dict:
        line_1 = MockDoubleLine.Plot2DLine(
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5]
        )
        line_2 = MockDoubleLine.Plot2DLine(
            [1, 2, 3, 4, 5],
            [1, 4, 9, 16, 25]
        )
        section = cls(
            section_event_payload['tenant_id'],
            section_event_payload['section_id'],
            section_event_payload['start_datetime'],
            section_event_payload['end_datetime'],
            ['vertical', 'horizontal'],
            [line_1, line_2]
        )
        return section.get_table_registry()

    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        file_path = os.path.realpath(__file__)
        txp_path = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
        resources = os.path.join(os.path.join(os.path.join(os.path.join(txp_path, "devices"), "drivers"), "mock"),
                                 "resources")
        image = Image.open(os.path.join(resources, "puppy.jpeg"))
        return image
