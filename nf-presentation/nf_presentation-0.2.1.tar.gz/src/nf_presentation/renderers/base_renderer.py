from typing import IO
from abc import abstractmethod

from nf_presentation.builders import PresentationBuilder
from nf_presentation.data_classes import ExerciseInfo
from nf_presentation.scheme_renderer import SchemeRenderer
from nf_presentation.html_renderer import HTMLRenderer
from nf_presentation import assets
from nf_presentation.settings import (
                DEFAULT_SLIDE_TITLE,PRESENTATION_RATIO,
                ADDITIONAL_TABLE_POSITION, ADDITIONAL_TABLE_WIDTH,
                BASIC_TABLE_POSITION, BASIC_TABLE_WIDTH,
                LINKS_TABLE_POSTION,LINKS_TABLE_WIDTH,
                SCHEME_HEIGHT,SCHEME_WIDTH, SCHEME_POSITION,
                TITLE_POSITION,TITLE_SIZE, TITLE_BACKGROUND,TITLE_FOREGROUND,
                LOGO_POSITION,LOGO_WIDTH,NAME_POSITION
                )

class BaseRenderer:
    def __init__(self, ratio):
        self.presentation_builder=PresentationBuilder().with_ratio(ratio)
        self._open_streams:list[IO]=[]

    @abstractmethod
    def add_exercise_slide(self):
        pass

    def track_stream(self, stream : IO):
        """a method that marks a stream to be closed on __end__ or close() of renderer"""
        self._open_streams.append(stream)

    def save(self,to:str):
        self.presentation_builder.save(to)

    def __enter__(self) -> 'BaseRenderer':
        return self
    def __exit__(self,type,value,traceback):
        self.close()
    def close(self):
        for stream in self._open_streams:
            stream.close()





        
