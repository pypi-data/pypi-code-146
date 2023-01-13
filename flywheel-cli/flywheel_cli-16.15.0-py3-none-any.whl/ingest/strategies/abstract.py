"""Provides AbstractIngestStrategy class."""
from abc import ABC, abstractmethod

from ... import util


class Strategy(ABC):
    """Abstract ingest strategy class"""

    def __init__(self, config, context=None):
        self.root_node = None
        self._last_added_node = None
        self.config = config
        self.context = context or {}

    @abstractmethod
    def initialize(self):
        """Initialize the strategy"""

    def add_template_node(self, next_node):
        """Append next_node to the last node that was added (or set the root node)

        Arguments:
            next_node (ImportTemplateNode): The node to append
        """
        last = self._last_added_node
        if last:
            if not hasattr(last, "set_next"):
                raise ValueError(f"Cannot add node - invalid node type: {type(last)}")

            last.set_next(next_node)
        else:
            self.root_node = next_node

        self._last_added_node = next_node

    def initial_context(self):
        """Creates the initial context for import.

        Returns:
            dict: The initial context
        """
        context = {}

        if self.context:
            for key, value in self.context.items():
                util.set_nested_attr(context, key, value)

        if self.config.group:
            util.set_nested_attr(context, "group._id", self.config.group)

        if self.config.project:
            # TODO: Check for <id:xyz> syntax
            util.set_nested_attr(context, "project.label", self.config.project)

        return context
