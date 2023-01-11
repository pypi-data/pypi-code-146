import abc
import enum
from typing import List, Dict, Union
import pandas as pd
from plotly.graph_objects import Figure
from google.cloud import bigquery
from txp.common.utils import bigquery_utils
import json
import logging
from txp.common.config import settings
import datetime
import dataclasses
from PIL import Image
import io
import base64
import plotly.graph_objects as go
import pytz


log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class SectionInputEnum(enum.Enum):
    RAW_TIME = 'RAW_TIME'
    FFT = 'FFT'
    PSD = 'FFT'
    EVENTS = 'EVENTS'
    STATES = 'STATES'


class ReportSection(abc.ABC):
    """
    TODO: Define the structure of the time_configuration object (and the name)
    """

    def __init__(
            self,
            tenant_id: str,
            section_id: str,
            start_datetime: str,
            end_datetime: str,
            **kwargs
    ):
        self.creation_timestamp = datetime.datetime.strptime(end_datetime, settings.time.datetime_zoned_format).\
            strftime(settings.time.datetime_format)
        self.tenant_id = tenant_id
        self.section_id = section_id
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    @abc.abstractmethod
    def get_table_registry(self, **kwargs) -> Dict:
        """Returns a Dict with the appropriate structure to be stored
        in the DB."""
        pass

    @classmethod
    @abc.abstractmethod
    def required_inputs(cls) -> List[SectionInputEnum]:
        """Returns the List of required inputs to compute the section result
        """
        pass

    @classmethod
    @abc.abstractmethod
    def load(cls, serialized_section: Dict) -> 'ReportSection':
        """Implementation code to read the serialized section from the DB layer"""
        pass

    @classmethod
    @abc.abstractmethod
    def compute(cls, inputs: Dict[SectionInputEnum, pd.DataFrame], section_event_payload: Dict) -> Dict:
        """Children concrete sections should implement the compute code in order to
        obtain the desired output.

        The return type is child specific.
        """
        pass

    def get_dynamic_plot(self) -> Union[Figure]:
        """Returns a Dynamic Image supported by third party libs.
        """
        return None

    @classmethod
    def get_image_plot(cls, **kwargs) -> Image:
        return None

    @classmethod
    def serialize_image(cls, image) -> str:
        with io.BytesIO() as output:
            image.save(output, format="JPEG")
            return str(base64.b64encode(output.getvalue()), 'utf-8')

    @classmethod
    def deserialize_image(cls, image_str) -> Image:
        return Image.open(io.BytesIO(base64.b64decode(bytes(image_str, 'utf-8'))))

    @classmethod
    def get_input_data(
            cls,
            pubsub_msg: Dict,
            inputs: List[SectionInputEnum],
            bigquery_client: bigquery.Client,
            time_table,
            fft_table,
            psd_table,
            time_metrics_table,
            psd_metrics_table,
            fft_metrics_table,
            events_table,
            states_table
    ) -> Dict[SectionInputEnum, pd.DataFrame]:
        """Inspect the required inputs and downloads the required dataframes

        TODO: When time configuration is available, then all the utility code
            to download tables from database should go here.

        TODO: for time data we should pass parameters with edge_logical_ids and perceptions,
            and the bigquery module should support that query

        TODO: for the data passed to states, we can allow the section user to define
            which assets_ids are going to be processed.

        TODO: We should code the other inputs
        """
        # TODO USE format at settings.toml
        d: [SectionInputEnum, pd.DataFrame] = {}
        start_datetime: datetime.datetime = datetime.datetime.strptime(
            pubsub_msg['start_datetime'],
            settings.time.datetime_zoned_format
        )
        # TODO USE format at settings.toml
        end_datetime: datetime.datetime = datetime.datetime.strptime(
            pubsub_msg['end_datetime'],
            settings.time.datetime_zoned_format
        )
        for input in inputs:
            if input == SectionInputEnum.RAW_TIME:
                if 'edge_logical_ids' in pubsub_msg['parameters']:
                    edge_logical_ids = pubsub_msg['parameters']['edge_logical_ids']
                    d[input] = bigquery_utils.get_all_signals_for_asset(
                        pubsub_msg['tenant_id'],
                        table_name=time_table,
                        edge_logical_ids=edge_logical_ids,
                        start_datetime=start_datetime,
                        end_datetime=end_datetime,
                        client=bigquery_client,
                        dataset_versions=[]
                    )
                else:
                    log.error("TIME generated data requires edge_logical_ids parameter.")

            elif input == SectionInputEnum.EVENTS:
                log.info(f"Downloading {SectionInputEnum.EVENTS.name} "
                         f"for tenant {pubsub_msg['tenant_id']}")
                asset_ids = pubsub_msg['parameters']['assets']
                d[input] = bigquery_utils.get_all_task_predictions_for_tenant_within_interval(
                    pubsub_msg['tenant_id'],
                    table_name=events_table,
                    start_datetime=start_datetime,
                    asset_ids=asset_ids,
                    end_datetime=end_datetime,
                    client=bigquery_client
                )
                log.info(f"Successfully downloaded {d[input].size} rows "
                         f"dataframe for {SectionInputEnum.EVENTS.name}")

            elif input == SectionInputEnum.STATES:
                log.info(f"Downloading {SectionInputEnum.STATES.name} "
                         f"for tenant {pubsub_msg['tenant_id']}")
                asset_ids = pubsub_msg['parameters']['assets']
                d[input] = bigquery_utils.get_all_task_predictions_for_tenant_within_interval(
                    pubsub_msg['tenant_id'],
                    table_name=states_table,
                    start_datetime=start_datetime,
                    asset_ids=asset_ids,
                    end_datetime=end_datetime,
                    client=bigquery_client
                )
                log.info(f"Successfully downloaded {d[input].size} rows "
                         f"dataframe for {SectionInputEnum.STATES.name}")

        return d

    @staticmethod
    def _convert_plotly_to_pil(fig: go.Figure) -> Image:
        img_buff = io.BytesIO()
        fig_jpeg = fig.to_image(format="jpeg")
        img_buff.write(fig_jpeg)
        img_pil = Image.open(img_buff)
        return img_pil


class Plot2dSection(ReportSection, abc.ABC):
    """This class implements all the internal code to deal with
    2D in concrete implementations for use cases.

    """

    @dataclasses.dataclass()
    class Plot2DLine:
        x_values: List[Union[int, float, str]]
        y_values: List[Union[int, float, str]]
        name: str = ""

    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            axes_names: List[str],
            lines: List[Plot2DLine],
            **kwargs
    ):
        super(Plot2dSection, self).__init__(
            tenant_id, section_id, start_datetime, end_datetime, **kwargs
        )
        self.lines = lines
        self.axes_names = axes_names

        # Proceeds to validate the data types to check if they're
        #   JSON serializable
        for i, line in enumerate(lines):
            if not all(
                    map(
                        lambda x: type(x) in {int, float, str}, line.x_values
                    )
            ):
                raise ValueError(f"Format error on line {i + 1}. "
                                 f"Plot2dSection requires all of x_values to be of type: [int, float, str]")

            if not all(
                    map(
                        lambda y: type(y) in {int, float, str}, line.y_values
                    )
            ):
                raise ValueError(f"Format error on line {i + 1}."
                                 f"Plot2dSection requires all of y_values to be of type: [int, float, str]")

    def get_table_registry(self, **kwargs) -> Dict:
        x_y_vals = []
        for line in self.lines:
            x_y_vals.append(
                {
                    'x': line.x_values,
                    'y': line.y_values,
                    'name': line.name
                }
            )

        data_json = {
            'axes_names': self.axes_names,
            'lines': x_y_vals
        }

        img = self.get_image_plot(**kwargs)
        if img is not None:
            data_json['image'] = self.serialize_image(img)

        data_str = json.dumps(data_json)

        row = {
            'tenant_id': self.tenant_id,
            'section_id': self.section_id,
            'start_timestamp': self.start_datetime,
            'creation_timestamp': self.creation_timestamp,
            'end_timestamp': self.end_datetime,
            'data': data_str,
            'type': type(self).__name__
        }

        return row

    @classmethod
    def load(cls, serialized_section: Dict) -> 'ReportSection':
        """Implementation code to read the serialized section from the DB layer"""
        data_field = json.loads(
            serialized_section['data']
        )
        lines = []
        for d in data_field['lines']:
            lines.append(Plot2dSection.Plot2DLine(d['x'], d['y'], d['name']))

        return cls(
            serialized_section['tenant_id'],
            serialized_section['section_id'],
            serialized_section['start_timestamp'],
            serialized_section['end_timestamp'],
            data_field['axes_names'],
            lines
        )


class DataframeSection(ReportSection, abc.ABC):
    def __init__(
            self,
            tenant_id,
            section_id,
            start_datetime: str,
            end_datetime: str,
            dataframe: pd.DataFrame,
            **kwargs
    ):
        super(DataframeSection, self).__init__(tenant_id, section_id, start_datetime, end_datetime, **kwargs)
        self.dataframe = dataframe

    def get_table_registry(self, **kwargs) -> Dict:

        data_json = {
            'dataframe': self.dataframe.to_string(),
        }

        img = self.get_image_plot(**kwargs)
        if img is not None:
            data_json['image'] = self.serialize_image(img)

        data_str = json.dumps(data_json)

        row = {
            'tenant_id': self.tenant_id,
            'section_id': self.section_id,
            'start_timestamp': self.start_datetime,
            'creation_timestamp': self.creation_timestamp,
            'end_timestamp': self.end_datetime,
            'data': data_str,
            'type': type(self).__name__
        }

        return row

    @classmethod
    def load(cls, serialized_section: Dict) -> 'ReportSection':
        """Implementation code to read the serialized section from the DB layer"""
        data_field = json.loads(
            serialized_section['data']
        )
        df_str = data_field["dataframe"]
        df = pd.read_csv(io.StringIO(df_str), sep='\s+')

        return cls(
            serialized_section['tenant_id'],
            serialized_section['section_id'],
            serialized_section['start_timestamp'],
            serialized_section['end_timestamp'],
            df
        )
