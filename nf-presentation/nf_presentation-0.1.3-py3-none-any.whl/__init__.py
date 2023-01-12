"""A module for creating pptx from Nanofootball server request 

use create_pptx(...) for real data
or create_from_test_data(...)

Example 1:
----------
    from nf_presentation import create_pptx

    create_pptx(input_data=training_data_dict,output_file='output.pptx')

Example 2:
----------

    import io
    from nf_presentation import create_pptx

    with io.BytesIO() as f:
        create_pptx(input_data=training_data_dict, output_file=f)
        send_file(f)  # your server response to client

Example 3:
----------

    from nf_presentation import create_from_test_data

    create_from_test_data(output_file='output.pptx')

Example 4:
----------

    from nf_presentation import create_from_test_data

    with io.BytesIO() as f:
        create_from_test_data(output_file=f)
        send_file(f)  # your server response to client

"""

import json
import io
from typing import Union,IO

from .report_renderer import ReportRenderer
from .data_classes import TrainingInfo
from . import assets


def create_pptx(input_data:dict,output_file:Union[str,IO,None] =  None):
    """A function creating a pptx file from giant dict request from Nanofootball server
    Arguments:
        input_data: dict
            a dict-like object containing server request for making a pptx file
        output_file: str|file|None
            a destination for rendering pptx, may be a string for saving locally,
            or a file-like object

        if None, the the function will return a byte-array

    Output:
        None
           if output_file is defined, or
        Byte-array 
            if output_file is None. This data can be written to file or be send over http
    """

    target_stream= output_file or io.BytesIO()  # a stream to write pptx
                                                # a new BytesIO() wont be created if outputfile not None


    t=TrainingInfo(data=input_data)
    with ReportRenderer() as renderer:
        renderer.add_title_slide(name=t.trainer_name)
        for exercise in t.exercises:
            print(exercise.name)
            renderer.add_exercise_slide(exercise=exercise)
        renderer.save(to=target_stream)
    if output_file is None:
        target_stream.seek(0)
        return target_stream.read()

def create_from_test_data(output_file:Union[str,IO,None] = None, short_data=True):
    """A function creating a pptx file from test request, saved inside a packet
    Should be used to test this module works right on a target machine

    Arguments:
        output file: str | file | None
            a destination for rendering pptx, may be a string for saving locally,
            or a file-like object,

            if None, the the function will return a byte-array
        short_data: bool
            you can use short(2 exercise) and long(6-exercise test data)
            by default using short data, but use long data with short_data=False

    Output:
        None
           if output_file is defined, or
        Byte-array 
            if output_file is None. This data can be written to file or be send over http
    """
    with assets.get_test_data() as f:
        test_data=json.load(f)

    return create_pptx(input_data=test_data,output_file=output_file)