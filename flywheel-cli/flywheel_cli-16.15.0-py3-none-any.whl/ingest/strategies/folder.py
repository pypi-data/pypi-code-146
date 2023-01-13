"""Provides FolderImporter class."""
# pylint: disable=R0903
import re

from ..template import StringMatchNode
from .abstract import Strategy


class FolderStrategy(Strategy):
    """Strategy to ingest a folder"""

    def initialize(self):
        """Initialize the strategy."""
        for _ in range(self.config.root_dirs):
            self.add_template_node(StringMatchNode(re.compile(".*")))

        if not self.config.group:
            self.add_template_node(StringMatchNode("group"))

        if not self.config.project:
            self.add_template_node(StringMatchNode("project"))

        if not self.config.no_subjects:
            self.add_template_node(StringMatchNode("subject"))

        if not self.config.no_sessions:
            self.add_template_node(StringMatchNode("session"))

        if self.config.pack_acquisitions:
            self.add_template_node(
                StringMatchNode(
                    "acquisition", packfile_type=self.config.pack_acquisitions
                )
            )
        else:
            self.add_template_node(StringMatchNode("acquisition"))
            self.add_template_node(
                StringMatchNode(re.compile(self.config.dicom), packfile_type="dicom")
            )
