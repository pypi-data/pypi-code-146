from txp.web.resources.resources_management import ImageManagement
import streamlit as st
import dataclasses
import json

@dataclasses.dataclass
class ConditionReport:
    """A class to handle the asset condition report"""
    def __post_init__(self):
        self.conditions_mapping = {
            "OPTIMAL": self._optimal_condition,
            "GOOD": self._good_condition,
            "UNDEFINED": self._critical_condition,
            "OPERATIONAL": self._operational_condition,
            "CRITICAL": self._critical_condition,
        }

    @property
    def _critical_condition(self):
        return self._image_html_and_text("unstable_condition.jpg", "Mala", width=30)

    @property
    def _operational_condition(self):
        return self._image_html_and_text("operational_condition.jpg", "Operativa", width=30)

    @property
    def _optimal_condition(self):
        return self._image_html_and_text("optimal_condition.jpg", "Óptima", width=30)

    @property
    def _good_condition(self):
        return self._image_html_and_text("good_condition.jpg", "Buena", width=30)

    def _image_html(self, file_name, responsive=False, width=60):
        """
        returns an image html tag from a file_name
        """
        if responsive:
            resources = ImageManagement(file_name)
            html_responsive_resource = resources.get_local_html_responsive_resource(width)
            return html_responsive_resource
        else:
            resources = ImageManagement(file_name)
            html_resource = resources.get_local_html_resource(width)
            return html_resource

    def _image_html_and_text(self, file_name, text, width=60):
        """
        returns an image html tag from a file_name and includes the possibility of add text
        """
        img = self._image_html(file_name, width=width)
        return img + f"""<br>{text}"""


@dataclasses.dataclass
class EventReport:
    """A class to handle the event type report"""
    def __init__(self):
        self.events_mapping = self._built_report_to_events()

    @property
    def _detrimental(self):
        return self._image_html_and_text("detrimental_event.gif", "Perjudicial", width=30)

    @property
    def _inofensive(self):
        return self._image_html_and_text("inofensive_events.gif", "Inofensivo", width=30)

    def _image_html(self, file_name, responsive=False, width=60):
        """
        returns an image html tag from a file_name
        """
        if responsive:
            resources = ImageManagement(file_name)
            html_responsive_resource = resources.get_local_html_responsive_resource(width)
            return html_responsive_resource
        else:
            resources = ImageManagement(file_name)
            html_resource = resources.get_local_html_resource(width)
            return html_resource

    def _image_html_and_text(self, file_name, text, width=60):
        """
        returns an image html tag from a file_name and includes the possibility of add text
        """
        img = self._image_html(file_name, width=width)
        return img + f"""<br>{text}"""

    def _built_report_to_events(self):
        report = {}
        declarative_events= json.loads(st.secrets['event_type_report'])
        for event, value in declarative_events.items():
            if value == 'inofensive':
                report[event]=self._inofensive
            else:
                report[event]=self._detrimental
        return report
