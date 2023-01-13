from typing import IO

from .builders import PresentationBuilder
from .data_classes import ExerciseInfo
from .scheme_renderer import SchemeRenderer
from .html_renderer import HTMLRenderer
from . import assets
from .settings import (
                DEFAULT_SLIDE_TITLE,PRESENTATION_RATIO,
                ADDITIONAL_TABLE_POSITION, ADDITIONAL_TABLE_WIDTH,
                BASIC_TABLE_POSITION, BASIC_TABLE_WIDTH,
                LINKS_TABLE_POSTION,LINKS_TABLE_WIDTH,
                SCHEME_HEIGHT,SCHEME_WIDTH, SCHEME_POSITION,
                TITLE_POSITION,TITLE_SIZE, TITLE_BACKGROUND,TITLE_FOREGROUND,
                LOGO_POSITION,LOGO_WIDTH,NAME_POSITION
                )

class ReportRenderer:
    """A class rendering a report in pptx
    requires closing after work, or use 'with' expression
    
    with ReportRenderer() as rr:
        ..."""
    def __init__(self):
        self.presentation_builder=PresentationBuilder().with_ratio(PRESENTATION_RATIO)
        self._open_streams:list[IO]=[]
    def add_title_slide(self,name:str):

        text=f'Итоговая работа по теме: Техническая тренировка \nАвтор: {name}'
        slide=self.presentation_builder.create_slide()

        rfs_logo=assets.get_rfs_logo()
        self._open_streams.append(rfs_logo)
        
        slide.create_image(rfs_logo).at(LOGO_POSITION).set_size(LOGO_WIDTH,None)
        slide.create_text(text).at(NAME_POSITION)
    def add_exercise_slide(self,exercise:ExerciseInfo):

        title_text=f'{exercise.group}: {exercise.name}'
        #slide 1

        slide=self.presentation_builder.create_slide()
        title=slide.create_title(title_text).at(TITLE_POSITION).with_size(TITLE_SIZE)
        title.with_foreground(TITLE_FOREGROUND).with_background(TITLE_BACKGROUND)

        additional_params_iter=iter(exercise.additionals)  # we use iter so we get items in slices

        additional_info_table=slide.create_table().at(ADDITIONAL_TABLE_POSITION).with_width(ADDITIONAL_TABLE_WIDTH)
        counter_page_1=0 # counts how much additional params we want on page 1
        for additional_param in additional_params_iter:

            row=(additional_param.name,additional_param.value)
            additional_info_table.append_row(*row) 
            counter_page_1=counter_page_1+1
            if counter_page_1>10:
                break
         
        #maybe exercise info should return a tuples already

        links_table=slide.create_table().at(LINKS_TABLE_POSTION).with_width(LINKS_TABLE_WIDTH)
        links_table.append_row('ссылки')
        links_table.append_row('ссылки')

        #creating a scheme
        s=SchemeRenderer()
        image_stream=s.to_stream(exercise.scheme_main)
        self._open_streams.append(image_stream)
        slide.create_image(image_stream).at(SCHEME_POSITION).set_size(SCHEME_WIDTH,None)

        #slide 2
        
        slide=self.presentation_builder.create_slide()
        title=slide.create_title(title_text).at(TITLE_POSITION).with_size(TITLE_SIZE)
        title.with_foreground(TITLE_FOREGROUND).with_background(TITLE_BACKGROUND)

        #description
        decription_text=HTMLRenderer().render(exercise.description)
        basic_info_table=slide.create_table().at(BASIC_TABLE_POSITION).with_width(BASIC_TABLE_WIDTH)
        basic_info_table.append_row('Описание:')
        basic_info_table.append_row(decription_text)

        #additional table continue

        additional_info_table=slide.create_table().at(ADDITIONAL_TABLE_POSITION).with_width(ADDITIONAL_TABLE_WIDTH)
        for additional_param in additional_params_iter:
            row=(additional_param.name,additional_param.value)
            additional_info_table.append_row(*row) 


        # mayble here add default params iter


    def save(self,to:str):
        self.presentation_builder.save(to)

    def __enter__(self) -> 'ReportRenderer':
        return self
    def __exit__(self,type,value,traceback):
        self.close()
    def close(self):
        for stream in self._open_streams:
            stream.close()

