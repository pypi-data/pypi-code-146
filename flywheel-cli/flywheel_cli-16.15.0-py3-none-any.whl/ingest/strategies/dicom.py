"""Provides the DicomImporter class."""
# pylint: disable=R0903
from ... import util
from ..template import create_scanner_node
from .abstract import Strategy


class DicomStrategy(Strategy):
    """Strategy to ingest dicom files"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.config.subject:
            util.set_nested_attr(self.context, "subject.label", self.config.subject)
        if self.config.session:
            util.set_nested_attr(self.context, "session.label", self.config.session)

    def initialize(self):
        """Initialize the importer."""
        self.add_template_node(create_scanner_node("dicom"))
