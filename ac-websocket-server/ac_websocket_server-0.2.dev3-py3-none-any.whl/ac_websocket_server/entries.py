'''Assetto Corsa entry_list.ini helper Class to re-order and re-write'''

import configparser
import json
from enum import Enum, auto
import logging
import random
import sys
from typing import Any, Dict, List


from ac_websocket_server.objects import EntryInfo
from ac_websocket_server.error import WebsocketsServerError


class EntryListIterationMethod(Enum):
    '''Iteration method to rewrite file in various manners.'''
    ORIGINAL = auto()
    FINISHING = auto()
    REVERSE = auto()
    RANDOM = auto()


class EntryList:
    '''A collection of individual Entry for the entry_list.ini file'''

    def __init__(self, file_name: str = None, entries: Dict[int, EntryInfo] = None) -> None:
        '''
        Create a new EntryList with optional input file and pre-populated entries.
        '''

        self.__logger = logging.getLogger('ac-ws.entries')

        if entries:
            self.entries = entries
        else:
            self.entries = {}

        self.file_name = file_name

        if file_name and not entries:
            self.parse_entries_file()

        self.iteration_method = EntryListIterationMethod.FINISHING

        self._entries_sorting_key = {}

        self._entries_total_time = {}

        for entry in self.entries.keys():
            self._entries_sorting_key[entry] = sys.maxsize

        self.elements: List[Any]
        self.index: int

    def __iter__(self):
        '''
        Create an Iterator based on EntryListIterationMethod
        '''

        self.elements = list(self.entries)
        self.index = 0

        if self.iteration_method == EntryListIterationMethod.RANDOM:
            for entry in self.entries.keys():
                self._entries_sorting_key[entry] = random.randrange(100)

        if self.iteration_method == EntryListIterationMethod.ORIGINAL:
            self.elements.sort(key=lambda entry: entry)
        elif self.iteration_method == EntryListIterationMethod.REVERSE:
            self.elements.sort(
                key=lambda entry: self._entries_sorting_key[entry], reverse=True)
        else:
            self.elements.sort(
                key=lambda entry: self._entries_sorting_key[entry])

        return self

    def __next__(self):
        '''Return the next Entry'''

        if self.index < len(self.elements):
            self.index += 1
            entry = self.entries[self.elements[self.index - 1]]
            entry.car_id = 'CAR_' + str(self.index - 1)
            return entry
            # return self.entries[self.elements[self.index - 1]]
        else:
            raise StopIteration

    def parse_entries_file(self):
        '''Parse the original entries file.'''

        if self.file_name:

            try:
                config = configparser.ConfigParser()
                config.read(self.file_name)

                for car_id in config.sections():

                    car = config[car_id]

                    self.entries[car_id] = \
                        EntryInfo(car_id=car_id,
                                  model=car.get('MODEL'),
                                  skin=car.get('SKIN'),
                                  spectator_mode=car.get('SPECTATOR_MODE'),
                                  drivername=car.get('DRIVERNAME'),
                                  team=car.get('TEAM'),
                                  guid=car.get('GUID'),
                                  ballast=car.get('BALLAST'),
                                  restrictor=car.get('RESTRICTOR', '')
                                  )
            except configparser.Error as error:
                raise WebsocketsServerError(error) from error

    def parse_result_file(self, result_file: str, track: str = None):
        '''Parse AC race results file'''
        # pylint: disable=invalid-name, logging-fstring-interpolation

        try:
            with open(result_file, 'r', encoding='UTF-8') as f:
                data = json.load(f)
        except OSError as error:
            self.__logger.error(f'Unable to read input file: {result_file}')
            raise OSError from error

        if track and track != data["TrackName"]:
            raise WebsocketsServerError(
                f'TrackName from {result_file} does not match {track}')

        results = data["Result"]

        position = 1

        try:

            for result in results:

                car_id = 'CAR_' + str(result['CarId'])
                total_time = result['TotalTime']

                if total_time > 0:
                    self.entries[car_id].drivername = result['DriverName']
                    self.entries[car_id].guid = result['DriverGuid']
                    self._entries_sorting_key[car_id] = position
                    position += 1
                else:
                    if self.iteration_method == EntryListIterationMethod.ORIGINAL:
                        self._entries_sorting_key[car_id] = sys.maxsize
                    if self.iteration_method == EntryListIterationMethod.REVERSE:
                        self._entries_sorting_key[car_id] = -sys.maxsize

        except KeyError as error:
            raise WebsocketsServerError(error) from error

    def __repr__(self):

        entries = ""

        position = 0
        for entry in iter(self):
            entry.position = position
            entries += str(entry)
            position += 1

        return entries

    def set_original_order(self):
        '''Set iteration to original cars order from entry list'''
        self.iteration_method = EntryListIterationMethod.ORIGINAL

    def set_standard_order(self):
        '''Set iteration to finishing order form last race'''
        self.iteration_method = EntryListIterationMethod.FINISHING

    def set_random_order(self):
        '''Set iteration to random'''
        self.iteration_method = EntryListIterationMethod.RANDOM

    def set_reversed_order(self):
        '''Set iteration to reversed grid from last race'''
        self.iteration_method = EntryListIterationMethod.REVERSE

    def show_entries(self) -> str:
        '''Returns a dictionary representation of all cars from entry_list.ini'''

        original_iteration_method = self.iteration_method

        self.iteration_method = EntryListIterationMethod.ORIGINAL

        entries = {}

        car_number = 1
        for entry in iter(self):
            if entry.drivername:
                driver_details = f'{entry.drivername} ({entry.guid})'
            else:
                driver_details = f'({entry.guid})'
            entries[str(car_number)] = f'{entry.model} {driver_details}'
            car_number += 1

        self.iteration_method = original_iteration_method

        return entries

    def show_grid(self) -> Dict[str, Any]:
        '''Returns a dictionary representation of the grid by player'''

        entries = {}

        position = 1
        for entry in iter(self):
            if entry.drivername != '':
                entries[str(position)] = entry.drivername
                position += 1

        return entries

    def write(self, output_file):
        '''Write updated entry list to output_file'''
        # pylint: disable=invalid-name, logging-fstring-interpolation

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(self))
                f.close()
        except OSError as err:
            self.__logger.error(f'Unable to write output file: {output_file}')
            raise OSError from err
