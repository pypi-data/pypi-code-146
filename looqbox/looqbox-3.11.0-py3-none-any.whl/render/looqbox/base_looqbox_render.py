from looqbox.objects.visual.looq_simple_table import ObjSimpleTable
from looqbox.render.pdf.base_pdf_render import BasePDFRender
from looqbox.objects.visual.table_footer import TableFooter
from looqbox.objects.visual.table_head import TableHead
from looqbox.objects.visual.table_body import TableBody
from looqbox.view.response_frame import ResponseFrame
from looqbox.render.abstract_render import BaseRender
from looqbox.view.response_board import ResponseBoard
from looqbox.global_calling import GlobalCalling
from collections import OrderedDict
from looqbox.objects.api import *
import plotly.graph_objs as go
import numpy as np
import shutil
import os


class BrowserRender(BaseRender):
    """
    Since Looqbox desktop and mobile application contains a fair similarity  they both ara placed in the same class
    allowing that specific changes might be made for desired output
    """

    def response_board_render(self, board: ResponseBoard):
        board_type = ["panel-default"]

        frames_json_list = [
            looq_frame.to_json_structure(self) for looq_frame in board.content
            if looq_frame.render_condition
        ]

        json_content = {
                'class': board_type,
                'type': 'board',
                'dispose': board.dispose,
                'action': board.action,
                'content': frames_json_list
            }

        # Transforming in JSON
        json_content = self.remove_json_nones(json_content)
        board_json = self._dict_to_json(json_content)

        return board_json

    def response_frame_render(self, frame: ResponseFrame):
        # Dynamic error message to help the users to understand the error
        if type(frame.content) is not list:
            raise TypeError("Content is not a list")

        objects_json_list = [
            looq_object.to_json_structure(self) for looq_object in frame.content
            if looq_object is not None and looq_object.render_condition
        ]

        json_content = {
                'type': 'frame',
                'class': frame.frame_class,
                'content': objects_json_list,
                'style': frame.style,
                'stacked': frame.stacked,
                'title': frame.title,
                'tabView': frame.tab_view,
                'insights': frame.insights
            }

        return self.remove_json_nones(json_content)

    def file_upload_render(self, obj_file_upload: ObjFileUpload):

        json_content = {
            "objectType": "fileUpload",
            "title": obj_file_upload.title,
            "content": obj_file_upload.content,
            "filepath": obj_file_upload.filepath,
            'tabLabel': obj_file_upload.tab_label
        }

        return self.remove_json_nones(json_content)

    def html_render(self, obj_html: ObjHTML):

        json_content = {
            "objectType": "html",
            "html": obj_html.html,
            'tabLabel': obj_html.tab_label
        }

        return self.remove_json_nones(json_content)

    def pdf_render(self, obj_pdf: ObjPDF):

        if 'https://' not in obj_pdf.source:
            # From global variable looq
            if os.path.dirname(obj_pdf.source) == GlobalCalling.looq.temp_dir:
                obj_pdf.source = "/api/tmp/download/" + os.path.basename(obj_pdf.source)
            else:
                template_file = os.path.join(GlobalCalling.looq.response_dir() + "/" + obj_pdf.source)
                temporary_file = GlobalCalling.looq.temp_file(obj_pdf.source)
                shutil.copy(template_file, temporary_file)
                obj_pdf.source = "/api/tmp/download/" + os.path.basename(temporary_file)

        height_array = [str(obj_pdf.height)]

        json_content = {
            "objectType": "pdf",
            "src": obj_pdf.source,
            "style": {
                "height": height_array,
            },
            "initialPage": obj_pdf.initial_page,
            'tabLabel': obj_pdf.tab_label
        }

        return self.remove_json_nones(json_content)

    def simple_render(self, obj_simple: ObjSimple):

        json_content = {
            "objectType": "simple",
            "text": obj_simple.text
        }

        return self.remove_json_nones(json_content)

    def image_render(self, obj_image: ObjImage):

        source = obj_image.source
        if 'https://' not in obj_image.source:
            # From global variable looq
            if os.path.dirname(obj_image.source) == GlobalCalling.looq.temp_dir:
                source = "/api/tmp/download/" + os.path.basename(obj_image.source)
            else:
                template_file = os.path.join(GlobalCalling.looq.response_dir() + "/" + obj_image.source)
                temporary_file = GlobalCalling.looq.temp_file(obj_image.source)
                shutil.copy(template_file, temporary_file)
                source = "/api/tmp/download/" + os.path.basename(temporary_file)

        width_array = [str(obj_image.width)]
        height_array = [str(obj_image.height)]

        style_array = {
            "width": width_array,
            "height": height_array
        }

        if len(obj_image.style) != 0:
            for key, value in obj_image.style.items():
                obj_image.style[key] = [str(value)]
            style_array.update(obj_image.style)

        json_content = {
            "objectType": "image",
            "src": source,
            "style": style_array,
            "link": obj_image.link,
            "tooltip": obj_image.tooltip,
            'tabLabel': obj_image.tab_label
        }

        return self.remove_json_nones(json_content)

    def list_render(self, obj_list: ObjList):

        if not isinstance(obj_list.title, list):
            obj_list.title = [obj_list.title]

        json_content = OrderedDict(
            {
                "objectType": "list",
                "title": obj_list.title,
                "list": obj_list.link_list,
                'tabLabel': obj_list.tab_label
            }
        )

        return self.remove_json_nones(json_content)

    def message_render(self, obj_message: ObjMessage):

        json_content = {
            'objectType': 'message',
            'text': [obj_message.text],
            'type': obj_message.text_type,
            'style': {"text-align": [obj_message.text_align]},
            'tabLabel': obj_message.tab_label
        }

        # Adding the dynamic style parameters
        for style in list(obj_message.text_style.keys()):
            json_content['style'].setdefault(style, []).append(obj_message.text_style[style])

        return self.remove_json_nones(json_content)

    def query_render(self, obj_query: ObjQuery):

        json_content = OrderedDict(
            {
                "objectType": "query",
                "queries": obj_query.queries,
                "totalTime": str(obj_query.total_time)
            }
        )

        return self.remove_json_nones(json_content)

    def table_render(self, obj_table: ObjTable):
        obj_table.convert_depreciated_attributes()
        obj_table.apply_body_format_to_footer()

        # TODO refactor on table objects inheritance would be a better approach


        table_head = TableHead(table_content=obj_table.data,
                               head_link=obj_table.head_link,
                               head_style=obj_table.head_style,
                               head_class=obj_table.head_class,
                               head_tooltip=obj_table.head_tooltip,
                               head_filter=obj_table.head_filter,
                               head_format=obj_table.head_format,
                               head_group=obj_table.head_group,
                               head_group_link=obj_table.head_group_link,
                               head_group_style=obj_table.head_group_style,
                               head_group_class=obj_table.head_group_class,
                               head_group_tooltip=obj_table.head_group_tooltip,
                               head_group_format=obj_table.head_group_format,
                               head_group_row_link=obj_table.head_group_row_link,
                               head_group_row_style=obj_table.head_group_row_style,
                               head_group_row_class=obj_table.head_group_row_class,
                               head_group_row_tooltip=obj_table.head_group_row_tooltip,
                               head_group_row_format=obj_table.head_group_row_format,
                               show_head=obj_table.show_head,
                               drill_text=obj_table.drill_text.get("header"))

        table_body = TableBody(table_content=obj_table.data,
                               value_link=obj_table.cell_link,
                               value_style=obj_table.cell_style,
                               value_class=obj_table.cell_class,
                               value_tooltip=obj_table.cell_tooltip,
                               value_format=obj_table.cell_format,
                               row_link=obj_table.row_link,
                               row_style=obj_table.row_style,
                               row_class=obj_table.row_class,
                               row_tooltip=obj_table.row_tooltip,
                               row_format=obj_table.row_format,
                               row_range=obj_table.row_range,
                               col_link=obj_table.col_link,
                               col_style=obj_table.col_style,
                               col_class=obj_table.col_class,
                               col_tooltip=obj_table.col_tooltip,
                               col_format=obj_table.col_format,
                               col_range=obj_table.col_range,
                               null_as=obj_table.null_as,
                               collapsible=obj_table.collapsible,
                               row_hierarchy=obj_table.row_hierarchy,
                               drill_text=obj_table.drill_text.get("column"),
                               render_body=obj_table.render_body)

        table_footer = TableFooter(table_content=obj_table.data,
                                   value_format=obj_table.cell_format,
                                   total=obj_table.total,
                                   total_link=obj_table.total_link,
                                   total_style=obj_table.total_style,
                                   total_tooltip=obj_table.total_tooltip,
                                   total_class=obj_table.total_class,
                                   total_format=obj_table.total_format,
                                   total_row_class=obj_table.total_row_class,
                                   total_row_style=obj_table.total_row_style,
                                   total_row_format=obj_table.total_row_format,
                                   total_row_link=obj_table.total_row_link,
                                   total_row_tooltip=obj_table.total_row_tooltip,
                                   subtotal=obj_table.subtotal,
                                   subtotal_format=obj_table.subtotal_format,
                                   subtotal_style=obj_table.subtotal_style,
                                   subtotal_link=obj_table.subtotal_link,
                                   subtotal_tooltip=obj_table.subtotal_tooltip,
                                   subtotal_class=obj_table.subtotal_class,
                                   subtotal_row_format=obj_table.subtotal_row_format,
                                   subtotal_row_style=obj_table.subtotal_row_style,
                                   subtotal_row_link=obj_table.subtotal_row_link,
                                   subtotal_row_tooltip=obj_table.subtotal_row_tooltip,
                                   subtotal_row_class=obj_table.subtotal_row_class,
                                   null_as=obj_table.null_as,
                                   drill_text=obj_table.drill_text.get("footer"))


        # Convert all table components to json structure
        head_json = table_head.to_json_structure(self)
        footer_json = table_footer.to_json_structure(self)
        body_json = table_body.to_json_structure(self)

        # Title must be a list
        if not isinstance(obj_table.title, list):
            obj_table.title = [obj_table.title]

        # Set max width

        max_width = obj_table.build_scroll_area(obj_table.max_width)
        max_height = obj_table.build_scroll_area(obj_table.max_height)
        scrollable_area_width = obj_table.build_scroll_area(obj_table.scrollable_area_width)

        scroll = {
            "mobile": {
                "horizontal": {
                    "active": obj_table.horizontal_scrollbar,
                    "width": max_width.get("mobile"),
                    "scrollableAreaWidth": scrollable_area_width.get("mobile"),
                    "freezeColumns": obj_table.freeze_columns
                },
                "vertical": {
                    "active": obj_table.vertical_scrollbar,
                    "height": max_height.get("mobile"),
                    "fixedFooter": obj_table.freeze_footer,
                    "fixedHeader": obj_table.freeze_header
                }
            },
            "desktop": {
                "horizontal": {
                    "active": obj_table.horizontal_scrollbar,
                    "width": max_width.get("desktop"),
                    "scrollableAreaWidth": scrollable_area_width.get("desktop"),
                    "freezeColumns": obj_table.freeze_columns
                },
                "vertical": {
                    "active": obj_table.vertical_scrollbar,
                    "height": max_height.get("desktop"),
                    "fixedFooter": obj_table.freeze_footer,
                    "fixedHeader": obj_table.freeze_header
                }
            }
        }

        pagination = {
            'active': True if obj_table.pagination_size else False,
            'config': {
                'defaultPageSize': obj_table.pagination_size,
                "hideOnSinglePage": obj_table.hide_on_single_page,
                "pageSizeOptions": [
                    "10",
                    "20",
                    "25",
                    "50",
                    "100"
                ],
            }
        }

        drill_json = obj_table._set_drill_down()

        json_content = {
            'objectType': "table",
            'title': obj_table.title,
            'header': head_json,
            'body': body_json,
            'footer': footer_json,
            'drill': drill_json,
            'searchable': obj_table.searchable,
            'searchString': obj_table.search_string,
            'pagination': pagination,
            'framed': obj_table.framed,
            'framedTitle': obj_table.framed_title,
            'stacked': obj_table.stacked,
            'showBorder': obj_table.show_border,
            'showOptionBar': obj_table.show_option_bar,
            'showHighlight': obj_table.show_highlight,
            'striped': obj_table.striped,
            'sortable': obj_table.sortable,
            'scroll': scroll,
            'tabLabel': obj_table.tab_label,
            'class': obj_table.table_class
        }

        return self.remove_json_nones(json_content)

    def web_frame(self, obj_web_frame: ObjWebFrame):

        if obj_web_frame.width is None:
            obj_web_frame.width = ""
        else:
            obj_web_frame.width = str(obj_web_frame.width)

        json_content = OrderedDict(
            {
                "objectType": "webframe",
                "src": obj_web_frame.source,
                "style": {
                    "width": str(obj_web_frame.width),
                    "height": str(obj_web_frame.height)
                },
                "enableFullscreen": obj_web_frame.enable_fullscreen,
                "openFullscreen": obj_web_frame.open_fullscreen,
                'tabLabel': obj_web_frame.tab_label
            }
        )

        return self.remove_json_nones(json_content)

    def plotly_render(self, obj_plotly: ObjPlotly):
        """
        Create the Plotly JSON structure to be read in the FES.
        In this case the function has some peculiarities, for example, if the plotly object has some field of special
        types like ndarray, datetime and etc.. the json's convertion will break because these types objects are not
        serializable. Because of this, before sent the ObjectPlotly to the response frame, the programmer needs to
        transform these fields into normal lists.

        Example:
        --------
        >>> nparray = nparray.tolist()

        :return: A JSON string.
        """
        if obj_plotly.layout is None:
            obj_plotly.layout = go.Layout()

        figure = go.Figure(data=obj_plotly.data, layout=obj_plotly.layout)

        figure_json = figure.to_plotly_json()

        for figure in figure_json["data"]:
            for data in figure:
                if isinstance(figure[data], dict):
                    for key in figure[data]:
                        if isinstance(figure[data][key], np.ndarray):
                            figure[data][key] = figure[data][key].tolist()
                elif isinstance(figure[data], list):
                    for sub_group in figure[data]:
                        if isinstance(sub_group, list):
                            for value in sub_group:
                                if isinstance(sub_group[value], np.ndarray):
                                    sub_group[value] = sub_group[value].tolist()
                if isinstance(figure[data], np.ndarray):
                    figure[data] = figure[data].tolist()

        json_content = {
            'objectType': 'plotly',
            'data': self._dict_to_json(figure_json['data']),
            'layout': self._dict_to_json(figure_json['layout']),
            'stacked': obj_plotly.stacked,
            'displayModeBar': obj_plotly.display_mode_bar,
            'tabLabel': obj_plotly.tab_label
        }

        plotly_json = self._dict_to_json(json_content)

        return self.remove_json_nones(json_content)

    def audio_render(self, obj_audio: ObjAudio):

        source = obj_audio.source
        if 'https://' not in obj_audio.source:
            # From global variable looq
            if os.path.dirname(obj_audio.source) == GlobalCalling.looq.temp_dir:
                source = "/api/tmp/download/" + os.path.basename(obj_audio.source)
            else:
                template_file = os.path.join(GlobalCalling.looq.response_dir() + "/" + obj_audio.source)
                temporary_file = GlobalCalling.looq.temp_file(obj_audio.source)
                shutil.copy(template_file, temporary_file)
                source = "/api/tmp/download/" + os.path.basename(temporary_file)

        json_content = {
            "objectType": "audio",
            "src": source,
            "autoPlay": obj_audio.auto_play,
            'tabLabel': obj_audio.tab_label
        }

        return self.remove_json_nones(json_content)

    def video_render(self, obj_video: ObjVideo):

        source = obj_video.source
        if 'https://' not in obj_video.source:
            # From global variable looq
            if os.path.dirname(obj_video.source) == GlobalCalling.looq.temp_dir:
                source = "/api/tmp/download/" + os.path.basename(obj_video.source)
            else:
                template_file = os.path.join(GlobalCalling.looq.response_dir() + "/" + obj_video.source)
                temporary_file = GlobalCalling.looq.temp_file(obj_video.source)
                shutil.copy(template_file, temporary_file)
                source = "/api/tmp/download/" + os.path.basename(temporary_file)

        json_content = {
            "objectType": "video",
            "src": source,
            "autoPlay": obj_video.auto_play,
            'tabLabel': obj_video.tab_label
        }

        return self.remove_json_nones(json_content)

    def embed_render(self, obj_embed: ObjEmbed):

        json_content = {
            "objectType": "embed",
            "iframe": obj_embed.iframe,
            'tabLabel': obj_embed.tab_label
        }

        return self.remove_json_nones(json_content)

    def obj_form_render(self, obj_form: ObjForm):

        if not isinstance(obj_form.title, list):
            obj_form.title = [obj_form.title]

        json_content = OrderedDict(
            {
                "objectType": "form",
                "title": obj_form.title,
                "method": obj_form.method,
                "action": obj_form.action,
                "filepath": obj_form.filepath,
                "fields": obj_form.fields,
                'tabLabel': obj_form.tab_label
            }
        )

        return self.remove_json_nones(json_content)

    def form_html_render(self, obj_form_html: ObjFormHTML):

        json_content = OrderedDict(
            {
                "objectType": "formHtml",
                "html": obj_form_html.html,
                "content": obj_form_html.content,
                "filepath": obj_form_html.filepath,
                'tabLabel': obj_form_html.tab_label
            }
        )

        return self.remove_json_nones(json_content)

    def image_capture_render(self, obj_image_capture: ObjImageCapture):

        json_content = {
            "objectType": "imageCapture",
            "title": obj_image_capture.title,
            "content": obj_image_capture.content,
            "filepath": obj_image_capture.filepath
        }

        return self.remove_json_nones(json_content)

    def text_render(self, obj_text: ObjText):

        json_content = {
            "class": list(obj_text.obj_class or []),
            "type": "text",
            "style": CssOption.export(obj_text.css_options),
            "text": obj_text.text,
            'tabLabel': obj_text.tab_label
        }

        return self.remove_json_nones(json_content)

    def switch_render(self, obj_switch):
        children_json = [child.to_json_structure(self) for child in obj_switch.children if child.render_condition]

        json_content = {
            "class": list(obj_switch.obj_class or []),
            "type": "switch",
            "orientation": obj_switch.orientation,
            "content": children_json,
            "style": CssOption.export(obj_switch.css_options),
            'tabLabel': obj_switch.tab_label
        }

        return self.remove_json_nones(json_content)

    def tooltip_render(self, obj_tooltip):

        children_json = [child.to_json_structure(self) for child in obj_tooltip.children if child.render_condition]

        json_content = {
            "class": list(obj_tooltip.obj_class or []),
            "type": "tooltip",
            "orientation": obj_tooltip.orientation,
            "text": obj_tooltip.text,
            "content": children_json,
            "style": CssOption.export(obj_tooltip.css_options),
            'tabLabel': obj_tooltip.tab_label
        }

        return self.remove_json_nones(json_content)

    def link_render(self, obj_link):
        children_json = [child.to_json_structure(self) for child in obj_link.children if child.render_condition]

        json_content = {
            "class": list(obj_link.obj_class or []),
            "type": "link",
            "question": obj_link.question,
            "content": children_json,
            "style": CssOption.export(obj_link.css_options),
            'tabLabel': obj_link.tab_label
        }

        return self.remove_json_nones(json_content)

    def row_render(self, obj_row: ObjRow):

        children_json = [child.to_json_structure(self) for child in obj_row.children if child.render_condition]

        json_content = {
            "class": list(obj_row.obj_class or []),
            "type": "row",
            "style": CssOption.export(obj_row.css_options),
            "content": children_json,
            'tabLabel': obj_row.tab_label,
            'config': {}
        }

        return self.remove_json_nones(json_content)

    def column_render(self, obj_column: ObjColumn):

        children_json = [child.to_json_structure(self) for child in obj_column.children if child.render_condition]

        json_content = {
            "class": list(obj_column.obj_class or []),
            "type": "column",
            "style": CssOption.export(obj_column.css_options),
            "content": children_json,
            'tabLabel': obj_column.tab_label,
            'config': {}
        }

        return self.remove_json_nones(json_content)

    def line_render(self, obj_line):
        json_content = {
            "class": list(obj_line.obj_class or []),
            "type": "shape-line",
            "style": CssOption.export(obj_line.css_options),
            'tabLabel': obj_line.tab_label,
        }
        return self.remove_json_nones(json_content)

    def gauge_render(self, obj_gauge):
        json_content = {
            "class": list(obj_gauge.obj_class or []),
            "type": "gauge",
            "values": [t.get("value") for t in obj_gauge.traces],
            "labels": [t.get("label") for t in obj_gauge.traces],
            "min": [t.get("min", 0) for t in obj_gauge.traces],
            "max": [t.get("max", 1) for t in obj_gauge.traces],
            "colors": [t.get("color", "#40da62") for t in obj_gauge.traces],
            "formats": [t.get("format", "percent:0") for t in obj_gauge.traces],
            "animated": obj_gauge.animated,
            "style": CssOption.export(obj_gauge.css_options),
            'tabLabel': obj_gauge.tab_label,
        }
        return self.remove_json_nones(json_content)

    def simple_table_render(self, obj_simple_table: ObjSimpleTable):

        for column in obj_simple_table.data.columns:
            try:
                obj_simple_table.data[column].fillna(obj_simple_table.null_as, inplace=True)
            except TypeError:
                obj_simple_table.data[column].fillna(0, inplace=True)

        head_json = obj_simple_table.build_head_content(obj_simple_table.data, obj_simple_table.metadata)
        body_json = {
            "content": obj_simple_table.build_body_content(obj_simple_table.data)
        }

        json_content = {
            'objectType': "simpleTable",
            'header': head_json,
            'body': body_json
        }

        return self.remove_json_nones(json_content)
