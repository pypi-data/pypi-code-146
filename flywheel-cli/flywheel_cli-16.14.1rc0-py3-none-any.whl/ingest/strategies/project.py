"""Project Strategy"""

import re

from ..template import StringMatchNode
from .abstract import Strategy


class ProjectStrategy(Strategy):
    """ProjectStrategy class"""

    def initialize(self):
        """Initialize the strategy."""

        self.add_template_node(StringMatchNode(re.compile(".*")))  # skip project name
        # skip subjects delimiter
        self.add_template_node(StringMatchNode(re.compile("SUBJECTS")))

        self.add_template_node(StringMatchNode("subject"))

        # skip sessions delimiter
        self.add_template_node(StringMatchNode(re.compile("SESSIONS")))

        self.add_template_node(StringMatchNode("session"))

        # skip acquisitions delimiter
        self.add_template_node(StringMatchNode(re.compile("ACQUISITIONS")))

        self.add_template_node(StringMatchNode("acquisition"))

        # skip files delimiter
        self.add_template_node(StringMatchNode(re.compile("FILES")))
