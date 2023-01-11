from typing import Dict, List

from rudder_analytics import client
from apna_python_experiment_sdk.base import Configuration, SinkSerializer, Sink
import rudder_analytics
from datetime import date, datetime
import logging
import os
import time
from mixpanel import Mixpanel, BufferedConsumer


class MixpanelExperimentConfiguration(Configuration):
    """Configuration for mixpanel, needs the following parameters:
        'AEXP_MIXPANEL_TOKEN' : Token required for mixpanel APIs (seperate for staging and production.)
        'AEXP_MIXPANEL_PROJECT_SECRET': Project secret required for mixpanel APIs (seperate for staging and production.)
        'AEXP_MIXPANEL_SINK_BUFFER_SIZE': Buffer size for this sink. Defaults to 2000.
    """

    conf = dict(
        api_token=os.getenv('AEXP_MIXPANEL_TOKEN'),
        project_secret=os.getenv('AEXP_MIXPANEL_PROJECT_SECRET'),
        buffer_size=int(os.getenv('AEXP_MIXPANEL_SINK_BUFFER_SIZE', 2000))
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().validate_conf(caller=type(self).__name__)
        # Maximum buffer size can be 2000
        self.conf['buffer_size'] = min(self.conf['buffer_size'], 2000)
        


class MixpanelExperimentSerializer(SinkSerializer):
    def serialize(self, element, **kwargs):
        variant = 'default'
        if 'variant' in element.keys():
            variant = element['variant']['name']
        
        return dict(
            distinct_id=element['context']['userId'],
            event_name='$experiment_started',
            properties={
                'Experiment name': element['feature'],
                'Variant name': variant,
            },
            timestamp=time.time()
        )


class MixpanelExperimentSink(Sink):
    client = None

    def __init__(self, configuration: Configuration = MixpanelExperimentConfiguration, serializer: SinkSerializer = MixpanelExperimentSerializer):
        super().__init__(configuration, serializer)

        if client is not None:
            # Initialize conf and serializer:
            self.configuration = configuration()
            self.serializer = serializer()

            # Initialze mixpanel client:
            conf = self.configuration.get_conf()

            # Creating custom buffered consumer:
            custom_buffered_consumer = BufferedConsumer()
            # Over-ridding the max size manually:
            custom_buffered_consumer._max_size = conf['buffer_size']
            self.client = Mixpanel(
                conf['api_token'], consumer=custom_buffered_consumer)

            logging.info(f'MixpanelExperimentSink initialzed with batch size: {custom_buffered_consumer._max_size}')
        else:
            logging.warning('MixpanelExperimentSink is already initialized!')

    def __del__(self):
        """This is a custom destructor for this sink in order to flush all the events
        present in the mixpanel's buffer before terminating the object/program.
        """
        logging.warning(f'MixpanelSink destructor called. Now flushing the events.')
        self.flush()
        logging.warning('Done, now destroying MixpanelSink')
        
        
    def flush(self):
        num_events = len(self.client._consumer._buffers["imports"])
        if num_events > 0:
            logging.warning(f'Flushing {num_events} events in the buffer to mixpanel.')
            self.client._consumer.flush()
            logging.warning(f'Flushed.')
        else:
            logging.info(f'No events was there to flush in MixpanelSink.')
            return

    def push(self, element: dict, **kwargs) -> bool:
        """This method calls the import_data method of the mixpanel client to send around 2000 events per API
        call.

        Args:
            element (dict): The variant and user_id fetched from experiment_client.

        Returns:
            bool: Returns true if success.
        """
        serialized_data = self.serializer.serialize(element=element, **kwargs)
        conf = self.configuration.get_conf()

        try:
            self.client.import_data(
                api_key=conf['api_token'],
                api_secret=conf['project_secret'],
                **serialized_data)
        except Exception as e:
            logging.warning(
                f'Error while pushing data into MixpanelExperimentSink: {e}')

        return True

    def bulk_push(self, serialized_elements: List[dict]) -> bool:
        raise NotImplementedError(
            f'This function is not implemented and not required in MixpanelExperimentSink.')
        
    def trigger(self):
        raise NotImplementedError(
            f'This function is not implemented and not required in MixpanelExperimentSink.')

    def trigger_condition(self) -> bool:
        raise NotImplementedError(
            f'This function is not implemented and not required in MixpanelExperimentSink.')
