from looqbox.json_encoder import JsonEncoder
from abc import ABC, abstractmethod
from multimethod import multimethod
import json


class BaseRender(ABC):

    remove_nones = True

    @staticmethod
    def _dict_to_json(object_as_dict: dict or list) -> json:
        """"
        Convert a dict to Looqbox's json structure
        """
        json_content = json.dumps(object_as_dict, indent=1, allow_nan=True, cls=JsonEncoder)
        return json_content

    @multimethod
    def remove_json_nones(self, json_dict: dict) -> dict:
        # Used in tests to check if the json structure is correct
        if not self.remove_nones:
            return json_dict

        # Get all the keys from empty (None) dict values
        if isinstance(json_dict, (dict, list)):
            empty_key_vals = [key for key, value in json_dict.items() if not value and self._is_not_a_valid_value(value)]
            # Delete the empty keys
            for key in empty_key_vals:
                del json_dict[key]

            json_dict = self.remove_nones_from_children_fields(json_dict)
        return json_dict

    @multimethod
    def remove_json_nones(self, json_list: list) -> list:
        # Remove nones from list
        json_list = [self.remove_json_nones(json_component) for json_component in json_list if json_component]
        return json_list

    @multimethod
    def remove_json_nones(self, json_none):
        return json_none

    def remove_nones_from_children_fields(self, json_dict):
        for key in json_dict.keys():
            if isinstance(json_dict[key], list):
                json_dict[key] = [self.remove_json_nones(json_component) for json_component in json_dict[key]]
            elif isinstance(json_dict[key], dict):
                json_dict[key] = self.remove_json_nones(json_dict[key])
        return json_dict

    @staticmethod
    def _is_not_a_valid_value(value) -> bool:
        return not isinstance(value, bool) and not isinstance(value, int) and not isinstance(value, float)

    @abstractmethod
    def response_board_render(self, board):
        """
        Method used to convert local objects to Looqbox's front-end syntax
        """

    @abstractmethod
    def response_frame_render(self, frame):
        pass

    @abstractmethod
    def file_upload_render(self, obj_file_upload):
        pass

    @abstractmethod
    def html_render(self, obj_html):
        pass

    @abstractmethod
    def pdf_render(self, obj_pdf):
        pass

    @abstractmethod
    def simple_render(self, obj_simple):
        pass

    @abstractmethod
    def image_render(self, obj_image):
        pass

    @abstractmethod
    def list_render(self, obj_list):
        pass

    @abstractmethod
    def message_render(self, obj_message):
        pass

    @abstractmethod
    def query_render(self, obj_query):
        pass

    @abstractmethod
    def table_render(self, obj_table):
        pass

    @abstractmethod
    def web_frame(self, obj_web):
        pass

    @abstractmethod
    def text_render(self, obj_text):
        pass

    @abstractmethod
    def plotly_render(self, obj_plotly):
        pass

    @abstractmethod
    def audio_render(self, obj_audio):
        pass

    @abstractmethod
    def video_render(self, obj_video):
        pass

    @abstractmethod
    def switch_render(self, obj_switch):
        pass

    @abstractmethod
    def tooltip_render(self, obj_tooltip):
        pass

    @abstractmethod
    def link_render(self, obj_link):
        pass

    @abstractmethod
    def row_render(self, obj_row):
        pass

    @abstractmethod
    def column_render(self, obj_column):
        pass

    @abstractmethod
    def gauge_render(self, obj_gauge):
        pass

    @abstractmethod
    def line_render(self, obj_shape):
        pass

    @abstractmethod
    def embed_render(self, obj_embed):
        pass

    @abstractmethod
    def obj_form_render(self, obj_form):
        pass

    @abstractmethod
    def form_html_render(self, obj_form_html):
        pass

    @abstractmethod
    def image_capture_render(self, obj_image_capture):
        pass
    
    @abstractmethod
    def simple_table_render(self, obj_simple_table):
        pass
