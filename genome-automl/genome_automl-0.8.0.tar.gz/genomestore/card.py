from typing import Mapping, List, Tuple, Dict, Any

import json
import logging
import datetime

import io
import base64
import tempfile
import uuid

from .base import BaseRef, CodeRef, DataRef, Segment, ArtifactMeta, BaseMetric


class CardArtifact(ArtifactMeta):

    def __init__(self,

      canonicalName: str = None,
      application: str = None,
      target: str = None,

      pipelineName: str = None,
      pipelineRunId: str = None,
      pipelineStage: str = None,

      code: CodeRef = None,


      versionName: str = None, # version name of the whole config for this model
      specVersionName: str = None, # version name of the code/template for this model

      deployment: str = None, # whole config/spec deployment, which changes even if template is same
      specDeployment: str = None, # template config/spec deployment

      dataRefs: List[DataRef] = None,

      format: str = None, # [json, csv, parquet, avro, ]

      dimension: str = None, # same as an evaluation, cards play to quality dimensions

      cardTarget: BaseRef = None, # what the card is for evaluation, model, data

      artifactBlob: BaseRef = None, # pointer to raw files in storage

      startTime: datetime.datetime = None, #lower time bound of the data contained in this artifact
      endTime: datetime.datetime = None, #upper time bound of the data contained in this artifact

      tags: dict = None,
      context: dict = None):

        self.canonicalName = canonicalName
        self.application = application
        self.target = target

        self.pipelineName = pipelineName
        self.pipelineRunId = pipelineRunId
        self.pipelineStage = pipelineStage

        self.code = code

        self.versionName = versionName
        self.specVersionName = specVersionName

        self.deployment = deployment
        self.specDeployment = specDeployment

        self.dataRefs = dataRefs

        self.format = format
        self.dimension = dimension

        self.cardTarget = cardTarget


        self.artifactBlob = artifactBlob

        self.tags = tags
        self.context = context

        self.id = None # this should be set only when retrieving artifacts from DB, not on instantiation


class HtmlComponent():
    def to_html(self):
        pass


class Card(HtmlComponent):

    def __init__(self, header, content):
        self.header = header
        self.content = content


    def to_html(self):
        return (
                 f"<html>"
                 f"<div class=\"genomeCard\">"
                 f"{self.header.to_html()}"
                 f"{self.content.to_html()}"
                 f"</div>"
                 f"</html>"
               )


class Header(HtmlComponent):

    def __init__(self, title):
        self.header = title

    def to_html(self):
        return f"<h1 class=\"titleCard\">{self.header}</h1>"


class Table(HtmlComponent):

    def __init__(self, rows):
        self.rows = rows or []

    def append(self, row):
        self.rows.append(row)

    def to_html(self):
        return f"<div class=\"tableCard\">{''.join([a.to_html() for a in self.rows])}</div>"


class Row(HtmlComponent):

    def __init__(self, columns:List[HtmlComponent]):
        self.columns = columns or []

    def append(self, col):
        self.columns.append(col)


    def to_html(self):
        import math
        width_percentage = math.floor(100 / max(1, len(self.columns or [])))

        return f"<div class=\"rowCard\">{''.join([a.to_html(width = width_percentage) for a in self.columns])}</div>"



class Column(HtmlComponent):
    def __init__(self, content:HtmlComponent):
        self.content = content

    def to_html(self, width = 100):
        return f"<div class=\"colContentCard\" style=\"width:{width}%;\">{self.content.to_html()}</div>"


class PltImage(HtmlComponent):

    def __init__(self, fig = None):
        self.fig = fig


    def to_html(self):

        from matplotlib import pyplot as plt

        my_string_io_bytes = io.BytesIO()

        fig = self.fig or plt
        fig.savefig(my_string_io_bytes, format='jpg')

        my_string_io_bytes.seek(0)
        base64_jpgData = base64.b64encode(my_string_io_bytes.read())

        return f'<img class="imgCard" src="data:image/jpeg;base64,{base64_jpgData.decode()}" />'


class BokehComponent(HtmlComponent):

    def __init__(self, fig = None):
        self.fig = fig

    def to_html(self):
        from bokeh.embed import components
        script, div = components(self.fig)

        width = (self.fig.width + 5) if getattr(self.fig, "width", None) else None
        height = (self.fig.height + 20) if getattr(self.fig, "height", None) else None
        sizing = "" if not width else f"style=\"width:{width}px;height:{height}px;border:0px;\""

        all_container = f"<div class=\"bokehComponent\">";

        html_container = f"<script src=\"https://cdn.bokeh.org/bokeh/release/bokeh-3.0.1.min.js\" crossorigin=\"anonymous\"></script>";
        html_container += script.replace("'", "`");
        html_container += div;

        all_container += f"<iframe {sizing} srcdoc='{html_container}'></iframe>";
        all_container += "</div>"

        return all_container


class EvidentlyComponent(HtmlComponent):

    def __init__(self, report = None, reference_data=None, current_data=None):
        self.report = report
        self.reference = reference_data
        self.current = current_data


    def to_html(self):

        self.report.run(reference_data=self.reference, current_data=self.current)

        tmpdir = tempfile.mkdtemp()
        file_report_path = tmpdir + "/report_file.html"

        self.report.save_html(file_report_path)

        file_obj = open(file_report_path, 'r')
        raw_html = file_obj.read()
        file_obj.close()

        component_iframe_id = str(uuid.uuid4())

        raw_html = raw_html.replace("format('woff2');", "format(\"woff2\");")
        raw_html = raw_html.replace("'Material Icons'", "\"Material Icons\"")
        #bug in evidtly
        raw_html += "</html>"

        base64_html_data = base64.b64encode(raw_html.encode('utf-8'))



        width = None
        height = 1000
        sizing = f"style=\"width:{100}%;min-height:{height}px;border:0px\"" if not width else f"style=\"width:{width}px;height:{height}px;\""

        all_container = f"<div class=\"evdlyComponent\">";


        # encode content as base64 so we do not have parsing problems because of enclosing quotes;
        # then use createObjectURL from javascript to circimvent brwoser size limits
        all_container += ("<iframe onload=\"(e)=>{console.log('onload evdtly iframe:', e); e.target.style.height=(e.target.contentDocument.body.scrollHeight + 245) + 'px';}\" "
                         f"id=\"evdtlComponent_{component_iframe_id}\" {sizing} "
                         f"src=\"about:blank()\"></iframe>");

        all_container += (f"<script type='text/javascript'>\n"
            "function dataURLtoBlob(dataurl) {\n"
            "    console.log('called dataUrl with length:', dataurl.length);\n"
            "    var mime = \"text/html\","
            "        bstr = atob(dataurl), n = bstr.length, u8arr = new Uint8Array(n);\n"
            "    while(n--){\n"
            "        u8arr[n] = bstr.charCodeAt(n);\n"
            "    }\n"
            "    return new Blob([u8arr], {type:mime});\n"
            "}\n"
            f"var evdtlyComp_data_uri = \"{base64_html_data.decode('utf-8')}\";\n"
            f"var iframeBlob = dataURLtoBlob(evdtlyComp_data_uri);\n"
            f"var temp_url = URL.createObjectURL(iframeBlob);\n"
            f"console.log('called createObjectURL with result length:', temp_url.length);\n"
            f"document.getElementById(\"evdtlComponent_{component_iframe_id}\").src = temp_url;\n"
            f"</script>"
        )
        all_container += "</div>"

        return all_container



class Markdown(HtmlComponent):
    def __init__(self, content):
        self.content = content

    def to_html(self):
        import markdown
        return f"<div class=\"markdownCard\">{markdown.markdown(self.content)}</div>"



class ArtifactComponent(HtmlComponent):

    def __init__(self, artifact: ArtifactMeta = None):
        self.artifact = artifact

    def to_html(self):
        meta = self.artifact.get_meta()
        return (f"<div class=\"artifactComponent\">"
        f"<div class=\"artifactType\">{type(self.artifact).__name__}</div>"
        f"{self._prop_html(meta)}"
        f"</div>")


    def _prop_html(self, val: Any):
        result = ""
        if type(val) in [dict, list]:
            val_iterable = val.items() if type(val) == dict else enumerate(val)
            for k, v in val_iterable:
                result += (f"<div class=\"artifactKV\">"
                       f"<div class=\"artifactK\">{str(k)}</div>"
                       f"{self._prop_html(v)}"
                       f"</div>")

        elif type(val) in [int, float, bool, str]:
            result = f"<div class=\"artifactV\">{str(val)}</div>"

        return result





class InnerHtml(HtmlComponent):
    def __init__(self, content):
        self.content = content

    def to_html(self):
        return f"<div class=\"innerHtmlCard\">{self.content}</div>"
