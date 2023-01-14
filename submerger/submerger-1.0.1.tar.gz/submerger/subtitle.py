from datetime import timedelta
from typing import List
import re


class Subtitle:
    def __init__(self, start_time: timedelta, end_time: timedelta, text: str) -> None:
        self.__start_time = start_time
        self.__end_time = end_time
        self.__text = text

    @property
    def start_time(self) -> timedelta:
        return self.__start_time

    @property
    def end_time(self) -> timedelta:
        return self.__end_time

    @property
    def text(self) -> str:
        return self.__text

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Subtitle):
            return NotImplemented

        # pylint: disable=protected-access
        return (self.__start_time == other.__start_time and
                self.__end_time == other.__end_time and
                self.__text == other.__text)
        # pylint: enable=protected-access

    def __str__(self) -> str:
        '''
        Returns subtitle's time line and text:
        '00:01:00,000 --> 00:02:00,000'
        SOME TEXT
        '''
        start_hours = ((self.__start_time.seconds // 3600) +
                       (self.__start_time.days * 24))
        start_minutes = (self.__start_time.seconds % 3600) // 60
        start_seconds = self.__start_time.seconds % 60
        start_milliseconds = self.__start_time.microseconds // 1000

        end_hours = ((self.__end_time.seconds // 3600) +
                     (self.__end_time.days * 24))
        end_minutes = (self.__end_time.seconds % 3600) // 60
        end_seconds = self.__end_time.seconds % 60
        end_milliseconds = self.__end_time.microseconds // 1000

        # pylint: disable-next=line-too-long
        return f'''{start_hours:02d}:{start_minutes:02d}:{start_seconds:02d},{start_milliseconds:03d} --> {end_hours:02d}:{end_minutes:02d}:{end_seconds:02d},{end_milliseconds:03d}
{self.__text}

'''

    @classmethod
    def from_srt(cls, raw_text: str) -> List['Subtitle']:
        pattern = re.compile(
            # pylint: disable-next=line-too-long
            r'\d+\n(?P<start_hours>\d{2}):(?P<start_minutes>\d{2}):(?P<start_seconds>\d{2}),(?P<start_milliseconds>\d{3}) --> (?P<end_hours>\d{2}):(?P<end_minutes>\d{2}):(?P<end_seconds>\d{2}),(?P<end_milliseconds>\d{3})\n(?P<text>.+(\n.+)*?)\n{2}')

        subtitle_list: List[Subtitle] = []
        for match in pattern.finditer(raw_text):
            start_time = timedelta(
                hours=int(match.group('start_hours')),
                minutes=int(match.group('start_minutes')),
                seconds=int(match.group('start_seconds')),
                milliseconds=int(match.group('start_milliseconds')),
            )

            end_time = timedelta(
                hours=int(match.group('end_hours')),
                minutes=int(match.group('end_minutes')),
                seconds=int(match.group('end_seconds')),
                milliseconds=int(match.group('end_milliseconds')),
            )

            text = match.group('text')

            subtitle_list.append(Subtitle(start_time, end_time, text))
        return subtitle_list

    @staticmethod
    def to_srt(subtitle_list: List['Subtitle']) -> str:
        subtitle_list = sorted(
            subtitle_list, key=lambda Subtitle: Subtitle.__start_time)

        return ''.join(f'{subtitle_counter}\n{sub}'
                       for subtitle_counter, sub in enumerate(subtitle_list, 1))
