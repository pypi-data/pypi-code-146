# Goal: Read all Spikesafe events from event queue
# SCPI Command: *SYST:ERR?
# SpikeSafe events are parsed into EventData class
# Example event 1: 102, External Paused Signal Stopped
# Example event 2: 200, Max Compliance Voltage; Channel(s) 1,2,3

import logging
from .EventData import EventData
from .SpikeSafeError import SpikeSafeError

log = logging.getLogger(__name__)

def read_all_events(spike_safe_socket, enable_logging = None):
    """Returns an array of all events from the SpikeSafe event queue.

    Parameters
    ----------
    spike_safe_socket : TcpSocket
        Socket object used to communicate with SpikeSafe
    enable_logging : bool, Optional
        Overrides spike_safe_socket.enable_logging attribute (default to None will use spike_safe_socket.enable_logging value)
    
    Returns
    -------
    EventData[]
        All events from SpikeSafe in a list of EventData objects

    Raises
    ------
    SpikeSafeError
        Raises an exception if an unexpected level 200 event or greater is read

    Exception
        Throws an exception for all other unexpected errors
    """    
    try:
        # event list to be returned to caller
        event_data_list = []

        # initialize flag to check if event queue is empty 
        is_event_queue_empty = False                                                                                                                      

        # run as long as there is an event in the SpikeSafe queue
        while is_event_queue_empty == False:
            # request SpikeSafe events and read data
            spike_safe_socket.send_scpi_command('SYST:ERR?', enable_logging)                                        
            event_response = spike_safe_socket.read_data(enable_logging)                                        

            if event_response != '':
                 # parse all valid event responses from SpikeSafe into event_data class                                                           
                event_data = EventData().parse_event_data(event_response)

                if event_data.code != 0:
                    # events with code greater than 0 are valid, add these to event data list
                    event_data_list.append(event_data)

                    if event_data.code >= 200:
                        # event codes 200 and greater correspond to SpikeSafe Errors. Operation should stop for these
                        raise SpikeSafeError(event_data.code, event_data.message, event_data.channel_list, event_response)

                else:
                    # Example message: 0, OK
                    event_data_list.append(event_data)
                    # When "0,OK is read the SpikeSafe event queue is empty
                    is_event_queue_empty = True                                             
            else:
                # unexpected response detected from SpikeSafe, end checking
                raise Exception('No event response from SpikeSafe: {}'.format(event_response))  

        # return event list to caller        
        return event_data_list                                                                  
    except Exception as err:
        # print any error to the log file and raise error to function caller
        log.error("Error emptying event queue: {}".format(err))                                     
        raise

def read_until_event(spike_safe_socket, code, enable_logging = None):
    """Returns an array of all events from the SpikeSafe event queue until a specific event is read.

    Parameters
    ----------
    spike_safe_socket : TcpSocket
        Socket object used to communicate with SpikeSafe
    code: int
        Event code for desired event
    enable_logging : bool, Optional
        Overrides spike_safe_socket.enable_logging attribute (default to None will use spike_safe_socket.enable_logging value)
    
    Returns
    -------
    EventData[]
        All events from SpikeSafe leading to the desired event in a list of EventData objects

    Raises
    ------
    SpikeSafeError
        Raises an exception if an unexpected level 200 event or greater is read

    Exception
        Throws an exception for all other unexpected errors
    """
    try:
        # event list to be returned to caller
        event_data_list = []

        # initialize flag to check if event queue is empty 
        has_desired_event_occurred = False                                                                                                                      

        # run as long as there is an event in the SpikeSafe queue
        while has_desired_event_occurred == False:
            # request SpikeSafe events and read data
            spike_safe_socket.send_scpi_command('SYST:ERR?', enable_logging)                                        
            event_response = spike_safe_socket.read_data(enable_logging)                                        

            if event_response != '':
                # parse all valid event responses from SpikeSafe into event_data class                                                           
                event_data = EventData().parse_event_data(event_response)

                if event_data.code != code:
                    # add all events prior to the desired event to the returned list
                    event_data_list.append(event_data)

                    if event_data.code >= 200:
                        # event codes 200 and greater correspond to SpikeSafe Errors
                        # if an error occurs and we are not specifically waiting for that error, we want to take action
                        raise SpikeSafeError(event_data.code, event_data.message, event_data.channel_list, event_response)

                else:
                    event_data_list.append(event_data) 
                    # Example message: 100, Channel Ready; Channel(s) 1
                    has_desired_event_occurred = True                                                 
            else:
                # unexpected response detected from SpikeSafe, end checking
                raise Exception('No event response from SpikeSafe: {}'.format(event_response))  

        # return event list to caller        
        return event_data_list                                                                  
    except Exception as err:
        # print any error to the log file and raise error to function caller
        log.error("Error emptying event queue: {}".format(err))                                     
        raise

def log_all_events(spike_safe_socket):
    """Reads all SpikeSafe events from event queue and prints them to the log file

    Parameters
    ----------
    spike_safe_socket : TcpSocket
        Socket object used to communicate with SpikeSafe

    Remarks
    ----------
    It is recommended to only call log_all_events when spike_safe_socket.enable_logging is False, otherwise duplicate logging messages may appear.
    """
    event_data = read_all_events(spike_safe_socket)   # read all events in SpikeSafe event queue and store in list
    for event in event_data:                        # print all SpikeSafe events to the log file
        log.info(event.event)                                                                             

