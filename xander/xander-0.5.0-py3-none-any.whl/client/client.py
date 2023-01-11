import datetime
import json
import logging
import os
import socket
from pathlib import Path
from dotenv import load_dotenv

from xander.client.routes import *
from xander.utils.client_utils import update
from xander.utils.constants import *

load_dotenv(verbose=True)


def create_url(*args):
    """
    Receive a list of strings and create the url.

    @param args: list of strings
    @return: url
    """

    url = '/'.join(args)
    return url


class XanderClient:
    """
    Xander component that is responsible for the communication with the Xander server.
    """

    def __init__(self, server_address='35.192.211.33', server_port=5000, local_mode=False):

        # Credentials file path
        credentials_file_path = os.getenv("XANDER_CREDENTIALS_FILE")

        # Check if the credential file exists at the specified path
        if not Path("credentials.json").exists():
            logging.critical(
                f'Credentials file not found in the specified path: {os.path.join(os.getcwd(), credentials_file_path)}')

        self.local_mode = local_mode
        self.server_address = server_address if not local_mode else '127.0.0.1'
        self.server_port = server_port
        self.api = json.load(open(credentials_file_path, 'r'))

        # Indicates if the client is authenticated on the server. This means that the api token is valid.
        self.is_auth = False

        # Name of the host, it is fundamental to distinguish among different runs on different machine by the same user
        self.hostname = socket.gethostname()

        # In the case the engine is running in cloud mode
        if not local_mode:

            # Try to connect the client to the server, if some problems occurs an exception is raised but the
            # execution of the engine is not interrupted.
            try:

                # Send a post request to initialize the execution
                success, payload = self.make_post_request(url='api/startup', asynchronous=False)

                # If everything is ok, the client is set as authenticated, otherwise an Exception is raised and the
                # engine will execute in local mode.
                if success:

                    # Set the authentication flag as True
                    self.is_auth = True

                    logging.debug('You are logged as {} ({})'.format(self.api['user_name'], self.api['user_mail']))
                else:
                    raise Exception

            except FileNotFoundError as e:
                logging.debug('Local mode is active, API auth file not found!', exc_info=e)

            except Exception as e:
                logging.debug('Local mode is active, connection to server failed!', exc_info=e)

    def make_post_request(self, url, payload=None, asynchronous=True):
        """
        Function responsible for sending a POST request to the server.

        @param url: target url
        @param payload: body of the post request
        @param asynchronous: if True the request is made asynchronous
        @return: status code of the request
        """

        # In the case the engine is running in local mode all requests are skipped, and it is returned
        # a error in the same way the connection is not working.
        # TODO: implement a local server for next future instead of replying as offline
        if self.local_mode:
            return False, None

        # If the payload passed by the user is empty, it is set as empty dictionary
        # Otherwise, the argument passed is used as payload.
        payload = {} if payload is None else payload

        # Add user and project information to the payload
        payload[PROJECT_SLUG] = self.api['project_slug']
        payload[HOSTNAME] = self.hostname

        # Create the header setting the authentication api token
        headers = {'Authorization': 'api_token {}'.format(self.api['api_token'])}

        # Build the url to call
        url = 'http://{}:{}/{}'.format(self.server_address, self.server_port, url)

        return update(url=url, payload=payload, headers=headers, asynchronous=asynchronous)

    def start_new_run(self, execution):
        """
        Call the server alerting for a new run and requesting a new run id.

        @param execution: execution object of the engine. Contains the start_time.
        @return: run id
        """

        response, payload = self.make_post_request(url=create_url(API, START_NEW_RUN), payload=execution,
                                                   asynchronous=False)

        # Extract and return the run ID
        return payload[RUN_ID] if response else None, payload[VERSION] if response else None

    def complete_run(self, execution):
        """
        Call the server alerting for the completed run and requesting a new run id.

        @param execution: execution object of the engine. Contains the start_time.
        @return: response
        """

        # Add the exception to the execution object
        execution[END_TIME] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        response, payload = self.make_post_request(url=create_url(API, COMPLETE_RUN), payload=execution,
                                                   asynchronous=False)

        # Extract and return the run ID
        return response

    def kill_run(self, execution, exception):
        """
        Call the server alerting for the killed run.

        @param execution: execution object of the engine.
        @param exception: occurred exception.
        @return: response
        """

        # Add the exception to the execution object
        execution[EXCEPTION] = exception
        execution[END_TIME] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        response, payload = self.make_post_request(url=create_url(API, KILL_RUN), payload=execution, asynchronous=False)

        # Extract and return the run ID
        return response

    def save_pipeline(self, pipeline):
        """
        Call the server and add the pipeline.

        @param pipeline:
        @return:
        """

        if not self.is_auth:
            return None

        payload = {
            PIPELINE_NAME: pipeline.pipeline_name,
            PIPELINE_SLUG: pipeline.pipeline_slug,
            START_TIME: pipeline.start_time,
            END_TIME: pipeline.end_time,
            DURATION: pipeline.run_duration
        }

        return self.make_post_request(url=create_url(API, PUSH_PIPELINE), payload=payload)
