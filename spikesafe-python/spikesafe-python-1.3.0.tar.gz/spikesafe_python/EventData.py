# Goal: Parse SpikeSafe events into an accessible object
# Example event 1: 102, External Paused Signal Stopped
# Example event 2: 200, Max Compliance Voltage; Channel(s) 1,2,3

import logging
import math

log = logging.getLogger(__name__)

class EventData():
    """ A class used to store data in a simple accessible object from 
    a SpikeSafe's event response

    ...

    Attributes
    ----------
    event : str
        Event response
    code : int
        Event code
    message : str
        Event message
    channel_list : int[]
        Channels affected by event as list of integers

    Methods
    -------
    parse_event_data(self, event_data)
        Parses SpikeSafe's event response into a simple accessible object
    """
    
    event = None

    code = 0

    message = None

    channel_list = []

    def __init__(self):
        pass
        
    # Goal: Helper function to parse event_data from SpikeSafe
    def parse_event_data(self, event_data):
        """Parses SpikeSafe's event response into a simple accessible object

        Parameters
        ----------
        event_data : str
            SpikeSafe's event response
        
        Returns
        -------
        EventData
            SpikeSafe's event response in a simple accessible object

        Raises
        ------
        Exception
            On any error
        """
        try:
            # populate object with extracted values
            self.event = event_data
            self.code = self.__parse_event_code__(event_data)                                     
            self.message = self.__parse_event_message__(event_data)                               
            self.channel_list = self.__parse_event_channel_list__(event_data)
            
            # return event data object to caller
            return self                                                             
        except Exception as err:
            # print any error to the log file and raise error to function caller
            log.error("Error parsing event data: {}".format(err))                             
            raise                                                               

    #Goal: Helper function parse event_data code from SpikeSafe message
    # e.g. parse "200" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    def __parse_event_code__(self, event_data):
        try:
            code = None
            # split event data by ",". e.g. [200, Max Compliance Voltage; Channel(s) 1,2,3]                                                                                                                                                    
            event_data_arr = event_data.split(',', 1)                                      
            # set integer code
            code = int(event_data_arr[0])                                                   

            # return code to caller
            return code
        except Exception as err:
            # print any error to the log file and raise error to function caller
            log.error("Error parsing event code: {}".format(err))                                   
            raise                                                                                

    #Goal: Helper function parse event_data message from SpikeSafe message data
    # e.g. parse "Max Compliance Voltage" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    def __parse_event_message__(self, event_data):
        try:
            message = None
            # split event data by ",". e.g. [200, Max Compliance Voltage; Channel(s) 1,2,3]                                                                      
            event_data_arr = event_data.split(',', 1)
            # split second section by ";". e.g. [ Max Compliance Voltage, Channel(s) 1,2,3]
            event_message_arr = event_data_arr[1].split(';')                               
            # remove all whitespace set message to value. e.g. Max Compliance Voltage
            message = event_message_arr[0].strip()                                      

            # return message to caller    
            return message                                                                      
        except Exception as err:
            # print any error to the log file & raise error to function caller
            log.error("Error parsing event message: {}".format(err))                                
            raise                                                                               

    #Goal: Helper function parse "Channel(s) 1,2,3" from "200, Max Compliance Voltage; Channel(s) 1,2,3"
    # note. Channel list is an optional section of the event data
    def __parse_event_channel_list__(self, event_data):
        try:
            # channel list to return to caller
            channel_list = []
            # find start of Channel(s) in event data. e.g. [200, Max Compliance Voltage; |C|hannel(s) 1,2,3]
            channels_index = event_data.find("Channel(s)")         

            # ensure Channel(s) was found
            if channels_index > -1:
                # sometimes messages are in this format: 110, "Pulsed Sweep shut down due to error; Channel(s) 1; Step Number: 12; Pulse Number: 1; Current: 0.040000"
                channel_list_end_index = event_data.find(';', channels_index)
                # grab the substring of just the channels. e.g. [1,2,3]
                if channel_list_end_index == -1:
                    channel_list_str = event_data[channels_index + 11:]
                else:
                    channel_list_str = event_data[channels_index + 11:channel_list_end_index]
                # split channel substring by ",". e.g. [1,2,3]
                channel_list_str_arr = channel_list_str.split(',')     

                # store all channels as integers in channel list
                for channel_str in channel_list_str_arr:                
                    channel_list.append(int(channel_str))

            # return channel list to caller
            return channel_list                                         
        except Exception as err:
            # print any error to the log file and raise error to function caller
            log.error("Error parsing event channel list: {}".format(err))   
            raise