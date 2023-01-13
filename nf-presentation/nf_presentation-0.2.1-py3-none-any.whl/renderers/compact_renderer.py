from nf_presentation.renderers.base_renderer import BaseRenderer
from nf_presentation.data_classes import SingleExerciseInfo
from nf_presentation.html_renderer import HTMLRenderer
from nf_presentation.scheme_renderer import SchemeRenderer

from nf_presentation._settings import compact_layout as current_layout
import nf_presentation.settings as base_settings

class CompactRenderer(BaseRenderer):
    def __init__(self):
        super().__init__(ratio=base_settings.PRESENTATION_RATIO)
    def add_exercise_slide(self, exercise_data:dict):
        exercise=SingleExerciseInfo(raw_data=exercise_data)
        slide=self.presentation_builder.create_slide()

        title=slide.create_title(base_settings.DEFAULT_SLIDE_TITLE).at(current_layout.TITLE_POSITION).with_size(current_layout.TITLE_SIZE)
        title.with_foreground(current_layout.TITLE_FOREGROUND).with_background(current_layout.TITLE_BACKGROUND)

        decription_text=HTMLRenderer().render(exercise.description)
        right_table=slide.create_table().at(current_layout.RIGHT_TABLE_POSITION).with_width(current_layout.RIGHT_TABLE_WIDTH)
        right_table.append_row(decription_text)
        # mayble here add default params iter

        left_table=slide.create_table().at(current_layout.LEFT_TABLE_POSITION).with_width(current_layout.LEFT_TABLE_WIDTH)
        left_table.append_row(exercise.title)
        left_table.append_empty_row()
        left_table.append_empty_row()
        for row in list(exercise.additional_params.items()):
           left_table.append_row(*row) 
        left_table.append_empty_row()
        left_table.append_row('ссылки')
        #maybe exercise info should return a tuples already

        s=SchemeRenderer()
        image_stream=s.to_stream(exercise.schemes[0])
        self._open_streams.append(image_stream)
        slide.create_image(image_stream).at(current_layout.SCHEME_POSITION).set_size(current_layout.SCHEME_WIDTH,None)

