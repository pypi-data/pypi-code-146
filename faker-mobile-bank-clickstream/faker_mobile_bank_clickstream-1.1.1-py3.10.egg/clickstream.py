import hashlib
import string
from datetime import datetime, timedelta
from random import choice, randint

from faker.providers import BaseProvider

from faker_mobile_bank_clickstream.event_constants import event_details, events
from faker_mobile_bank_clickstream.ip import ip_list
from faker_mobile_bank_clickstream.user_agents import user_agents


class ClickstreamProvider(BaseProvider):
    """
        A Provider for clickstream related test data.

        >>> from faker import Faker
        >>> from faker_mobile_bank_clickstream import ClickstreamProvider
        >>> fake = Faker()
        >>> fake.add_provider(ClickstreamProvider)
        >>> fake.session_clickstream()
    """

    def user_agent(self):
        """
        Generate random user agent.

        :return: User agent string
        """
        return choice(user_agents)

    def event(self):
        """
        Generate random event type name for mobile banking app.

        :return: Event type string
        """
        return choice(events)

    def session_clickstream(self, rand_session_max_size: int = 25, min_user_id:int  = 1, max_user_id: int=100000):
        """
        Generate session clickstream events.

        :param rand_session_max_size: Max number of possible events in session. Defaults to 25.
        :return: List of session events
        """

        # Initialize static session values
        session_events = list()
        session_event_names = list()
        user_id = _get_user_id(start = min_user_id, end = max_user_id)
        user_agent = self.user_agent()
        session_id = _get_session_id()
        ip = _get_ip()
        random_session_size = randint(1, rand_session_max_size)
        incremental_delta_delay = randint(1, 60)

        for s in range(random_session_size):
            # Mock time delay between events
            incremental_delta_delay = incremental_delta_delay + (s * randint(1, 60))
            event_time = _format_time(_get_event_time(delta=incremental_delta_delay))

            # No more events after loging out
            if len(session_event_names)>0:
                if session_event_names[-1] == 'Logout':
                    break       

            # Fetch a random event
            event = choice(event_details)
            # First event should be Login
            if len(session_events)==0:
                event = [e for e in event_details if e['name']=='Login'][0]

            if len(session_events)>0:
                # After Login event, add any of first_events which depends on Login
                event = choice([e for e in event_details if 'Login' in e['dependsOn']])

            # Handle event dependencies
            if len(session_events)>1 and len(event['dependsOn'])>0:
                if session_event_names[-1] not in event['dependsOn']:
                    try:
                        event = choice([e for e in event_details if session_event_names[-1] in e['dependsOn']])
                    except:
                        event = choice([e for e in event_details if 'Login' in e['dependsOn']])

            # Same event shouldn't repeat consecutively 
            if len(session_event_names)>0:
                if session_event_names[-1] == event['name']:
                    continue                          

            # Any event shouldn't occur more then max allowed 
            if session_event_names.count(event['name'])>=int(event['maxCount']):
                continue

            # Construct final event object
            r = {
                "ip": ip,
                "user_id": user_id,
                "user_agent": user_agent,
                "session_id": session_id,
                "event_time": event_time,
                "event_name": event['name']
            }
            session_events.append(r)
            session_event_names.append(r['event_name'])
        return session_events


def _get_session_id():
    """
    Generate session ID

    :return: Session ID string
    """
    return hashlib.sha256(
        ('%s%s%s' % (
            datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
            (''.join(choice(string.ascii_lowercase)) for _ in range(10)),
            'faker_clickstream'
        )).encode('utf-8')
    ).hexdigest()


def _get_user_id(start: int = 1, end: int = 100000):
    """
    Generate random user id from range 1 to 100000. Zero value may identify null user.

    :param start: Index start (Default: 1)
    :param end: Index end (Default: 100000)
    :return:
    """
    return randint(start, end)


def _get_event_time(delta):
    """
    Generate current event time, added by some delta value.

    :param delta: Delta time value in seconds
    :return: Event time
    """
    return datetime.now() + timedelta(seconds=delta)


def _format_time(t):
    """
    Format time to string.

    :param t: Time object
    :return: Time string in format like 28/03/2022 23:22:15.360252
    """
    return t.strftime("%d/%m/%Y %H:%M:%S.%f")


def _get_ip():
    """
    Get random IP address from list.

    :return: IP address string
    """
    return choice(ip_list)
