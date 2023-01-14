from looqbox.render.chatbot.components.text import ObjectToText
from looqbox.render.pdf.base_pdf_render import BasePDFRender
from looqbox.objects.visual.looq_message import ObjMessage
from looqbox.objects.visual.looq_table import ObjTable
from looqbox.view.response_frame import ResponseFrame
from looqbox.view.response_board import ResponseBoard
from looqbox.utils.utils import format as looq_format
from looqbox.render.abstract_render import BaseRender
from looqbox.objects.visual.looq_text import ObjText
from looqbox.objects.looq_pdf import ObjPDF
import re

non_text_objects = []


def add_to_text(text, add):
    if isinstance(add, str):
        if add:
            return text + re.sub("^ ", "", add)
        return text
    elif not add:
        return text
    elif isinstance(add, list):
        for item in add:
            text = add_to_text(text, item)
        return text
    elif isinstance(add, dict):
        if "text" in add:
            if "target" in add or "uri" in add:
                global non_text_objects
                non_text_objects.append(add)
                return text
            return add_to_text(text, add["text"])
        elif "children" in add:
            text = text + add.get("separator", "") if add["children"] and text else text
            return add_to_text(text, add["children"])

    return text


class BaseChatbotRender(BaseRender):

    file_extension_to_mime = {
        "pdf": "application/pdf",
        "csv": "text/csv",
        "png": "image/png",
    }

    formats = {
        "bold": {"start": "<b>", "end": "</b>"},
        "italic": {"start": "<i>", "end": "</i>"},
        "unispace": {"start": "<code>", "end": "</code>"},
        "none": {"start": "", "end": ""},
    }

    def response_board_render(self, board: ResponseBoard):

        pdf_obj = BasePDFRender()
        pdf_obj.response_board_render(board)
        pdf_filepath = pdf_obj.pdf.name
        pdf = ObjPDF(pdf_filepath)

        board.content.append(pdf)

        frames_json_list = [
            looq_obj.to_json_structure(self) for looq_obj in board.content
            if looq_obj.render_condition
        ]

        text = self._clean_text(add_to_text("", frames_json_list))

        content = [ObjectToText(text, self.formats).to_json_structure, *non_text_objects]

        for obj in content:
            if obj.get("text", "-").isspace():
                del obj["text"]

        json_content = {
                "content": content,
            }

        return self._dict_to_json(self.remove_json_nones(json_content.get("content", [])))
    
    def response_frame_render(self, frame: ResponseFrame):

        if type(frame.content) is not list:
            raise TypeError("Content is not a list")

        objects_json_list = [
            looq_object.to_json_structure(self) for looq_object in frame.content
            if looq_object is not None and looq_object.render_condition
        ]

        frame_title_obj = self._title_render(frame)

        objects_json_list.insert(0, frame_title_obj)

        return self.remove_json_nones(objects_json_list)
    
    def file_upload_render(self, obj_file_upload):
        # No need to render file upload
        ...
    
    def html_render(self, obj_html):
        if obj_html.html is None:
            return None
        tab_label = ObjectToText(obj_html.tab_label, self.formats).to_bold().to_json_structure
        html_text = ObjectToText(obj_html.html, self.formats).to_json_structure
        return self.remove_json_nones([tab_label, html_text])
    
    def pdf_render(self, obj_pdf):

        file_extension = obj_pdf.source.split(".")[-1]
        filename = obj_pdf.source.split("/")[-1]

        json_content = {
            "type": self.file_extension_to_mime.get(file_extension),
            "uri": obj_pdf.source,
            "title": obj_pdf.tab_label,
            "filename": filename,
            "text": " "
        }

        return self.remove_json_nones(json_content)
    
    def simple_render(self, obj_simple):
        if obj_simple.original_text is None:
            return None

        tab_label = ObjectToText(obj_simple.tab_label, self.formats).to_bold().to_json_structure
        text = ObjectToText(obj_simple.original_text, self.formats).to_json_structure
        return self.remove_json_nones([tab_label, text])
    
    def image_render(self, obj_image):
        ...
    
    def list_render(self, obj_list):
        objs = list()

        title = obj_list.title
        for link in obj_list.link_list:
            text = link.get("text")
            link = link.get("link", "").replace("looqfile://", "")
            file_extension = link.split(".")[-1]

            json_content = {
                "type": self.file_extension_to_mime.get(file_extension),
                "uri": link,
                "title": title,
                "text": text
            }

            objs.append(json_content)

        return objs
    
    def message_render(self, obj_message: ObjMessage):
        if obj_message.text is None:
            return None

        tab_label = ObjectToText(obj_message.tab_label, self.formats).to_bold().to_json_structure
        text = ObjectToText(obj_message.text, self.formats).to_json_structure
        return self.remove_json_nones([tab_label, text])
    
    def query_render(self, obj_query):
        # No need to render query
        ...
    
    def table_render(self, obj_table: ObjTable):
        tab_label = ObjectToText(obj_table.tab_label, self.formats).to_bold().to_json_structure

        title_obj = self._title_render(obj_table)
        data_obj = self._table_data_render(obj_table)
        total_obj = self._table_total_render(obj_table)

        return self.remove_json_nones([tab_label, title_obj, data_obj, total_obj])

    def _title_render(self, looq_obj):
        if not looq_obj.title:
            return None

        title_conversion_dict = {
            str: lambda x: x,
            list: lambda x: "\n".join(x),
            any: lambda x: str(x),
        }

        title_type = type(looq_obj.title)
        title = title_conversion_dict[title_type](looq_obj.title)

        return ObjectToText(title, self.formats).to_json_structure

    def _table_data_render(self, obj_table):
        # Default behavior on chatbot is to remove the table body

        if obj_table.total is None:
            obj_table.render_body = True

        if not obj_table.render_body:
            return None

        table_data = obj_table.data
        max_rows = 15  # TODO read from config
        max_cols = 5  # TODO read from config

        # Remove last columns if there are more than max_cols
        table_data = table_data.iloc[:, :max_cols]
        str_table = table_data.to_string(
                max_rows=max_rows, index_names=False, index=False, justify='right', sparsify=True,
                float_format=lambda x: '%.1f' % x
            )

        return ObjectToText(str_table, self.formats).to_unispace().to_json_structure

    def _table_total_render(self, obj_table):
        if not obj_table.total:
            return None

        total_format = obj_table.total_format or obj_table.col_format

        if isinstance(obj_table.total, list):
            total = [looq_format(x, total_format) for x in obj_table.total]
            total = {obj_table.data.columns[i]: total[i] for i in range(len(total))}
        elif isinstance(obj_table.total, dict):
            total = {k: looq_format(v, total_format) for k, v in obj_table.total.items()}
        else:
            raise TypeError("Total must be a list or a dict")

        total = self.remove_json_nones(total)

        # Remove column if total value is "Total", since it is redundant
        total_text = [
            f"{col} {looq_format(value, total_format.get(col, ''))}"
            for col, value in total.items() if str(value).lower() != "total"
        ]

        return ObjectToText("\n"+"\n\n".join(total_text), self.formats).to_json_structure

    def web_frame(self, obj_web):
        # No need to render web frame
        ...
    
    def text_render(self, obj_text: ObjText):
        return ObjectToText(obj_text.text, self.formats).to_json_structure
    
    def plotly_render(self, obj_plotly):
        ...
    
    def audio_render(self, obj_audio):
        ...
    
    def video_render(self, obj_video):
        ...
    
    def switch_render(self, obj_switch):
        # TODO add label to switch text
        return self._container_render(obj_switch, separator="")

    def tooltip_render(self, obj_tooltip):
        return self._container_render(obj_tooltip, separator="")
    
    def link_render(self, obj_link):
        link_json = self._container_render(obj_link, separator=" ")
        text = self._clean_text(add_to_text("", link_json))
        json_content = {
            "target": "blank",
            "uri": obj_link.question,
            "title": obj_link.tab_label,
            "text": text
        }
        return json_content
    
    def row_render(self, obj_row):
        return self._container_render(obj_row, separator=" ")

    def column_render(self, obj_column):
        return self._container_render(obj_column, separator="\n")

    def _container_render(self, obj_container, separator):
        children = [*obj_container.children]
        return {
            "type": "container",
            "children": [child.to_json_structure(self) for child in children],
            "separator": separator
        }

    def _clean_text(self, text):
        clean_text = ""
        for line in text.splitlines():
            to_add = re.sub("^ | $", "", line) + "\n"
            clean_text += to_add
        return self.remove_newlines(clean_text)

    @staticmethod
    def remove_newlines(text):
        new_line_groups = re.findall("(\n\n+)", text)
        if not new_line_groups:
            return text
        return re.sub("(.)\n(.)", r"\1 \2", text).replace("\n\n", "\n")

    def gauge_render(self, obj_gauge):
        ...
    
    def line_render(self, obj_shape):
        ...
    
    def embed_render(self, obj_embed):
        ...
    
    def obj_form_render(self, obj_form):
        ...
    
    def form_html_render(self, obj_form_html):
        ...
    
    def image_capture_render(self, obj_image_capture):
        ...
    
    def simple_table_render(self, obj_simple_table):
        ...
