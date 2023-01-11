from typing import List
from apna_python_experiment_sdk.base import Configuration, SinkSerializer, Sink
import rudder_analytics
from datetime import date, datetime
import logging
import os


# utils:
def rudderstack_error_handler(error, events):
    logging.warning(
        f'The following {len(events)} events: {events} on the Rudderstack was not able to get captured due to the following error:')
    logging.error(f'Error recevied in Rudderstack: {error}')


class RudderstackConf(Configuration):
    """Configuration for rudderstack.

    Needs the following variables:
        'AEXP_RUDDERSTACK_WRITE_KEY' (required*)
        'AEXP_RUDDERSTACK_DATAPLANE_URL' (required*)
        'AEXP_RUDDERSTACK_FLUSH_INTERVAL' (optional)
        'AEXP_RUDDERSTACK_FLUSH_AT' (optional)

    More configuration can be found at:
        <RUDDER_URL>
    """
    conf = dict(
        write_key=os.getenv('AEXP_RUDDERSTACK_WRITE_KEY'),
        data_plane_url=os.getenv('AEXP_RUDDERSTACK_DATAPLANE_URL'),
        flush_interval=int(os.getenv('AEXP_RUDDERSTACK_FLUSH_INTERVAL', 15)),
        flush_at=int(os.getenv('AEXP_RUDDERSTACK_FLUSH_AT', 200))
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().validate_conf(caller=type(self).__name__)


class RudderstackSerializer(SinkSerializer):
    def serialize(self, element):
        return {
            "user_id": element['context']['userId'],
            "type": "track",
            "event_name": "$experiment_started",
            "properties": {
                'Experiment name': element['feature'],
                'Variant name': element['variant']['name'],
            },
            "timestamp": datetime.now(),
            # "integrations": {
            #     "All"
            # }
        }


class RudderstackSink(Sink):
    client = None

    def __init__(self, configuration: Configuration = RudderstackConf, serializer: SinkSerializer = RudderstackSerializer):
        super().__init__(configuration, serializer)

        if self.client is None:
            # Initialize conf and serializer:
            self.configuration = configuration()
            self.serializer = serializer()

            conf = self.configuration.get_conf()

            # Initialize rudder client:
            rudder_analytics.default_client = rudder_analytics.Client(
                write_key=conf['write_key'],
                host=conf['data_plane_url'],
                flush_interval=conf['flush_interval'],
            )

            self.client = rudder_analytics
            self.client.write_key = conf['write_key']
            self.client.data_plane_url = conf['data_plane_url']
            self.client.on_error = rudderstack_error_handler

            logging.info('Ruddersink initialzed!')
        else:
            logging.warning(
                f'Ruddersink is already initialized. To recreate instance, you need to destroy exisiting one first.')

    def push(self, element: dict, **kwargs) -> bool:
        """This method calls the 'track' method of the rudderstack clients.
        It requires 'user_id', 'event' and 'properties'.

        Args:
            element (dict): The variant and user_id fetched from experiment_client.

        Returns:
            bool: Returns true if success.
        """
        serialized_data = self.serializer.serialize(element, **kwargs)

        try:
            self.client.track(
                user_id=serialized_data['user_id'],
                event=serialized_data['event_name'],
                properties=serialized_data['properties'],
                timestamp=serialized_data['timestamp']
            )
            logging.debug(f'Element: {serialized_data} tracked.')
        except Exception as e:
            logging.warning(f'Exception occured in RudderstackSink `push`: {e}')

        return True

    def bulk_push(self, serialized_elements: List[dict]) -> bool:
        raise NotImplementedError(
            f'This function is not implemented and not required in RudderstackSink.')

    def trigger(self):
        raise NotImplementedError(
            f'This function is not implemented and not required in RudderstackSink.')

    def trigger_condition(self) -> bool:
        raise NotImplementedError(
            f'This function is not implemented and not required in RudderstackSink.')
