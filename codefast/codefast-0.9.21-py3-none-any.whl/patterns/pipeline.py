#!/usr/bin/env python
""" rss feed
"""
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod

from codefast import logger as cf
from codefast.exception import get_exception_str


class Component(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.print_log = True

    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    def exec(self, *args, **kwargs):
        class_name = self.__class__.__name__
        file_name = self.__class__.__module__.split('.')[-1]
        if self.print_log:
            cf.info('pipeline starts exec [{}], args {}, kwargs {}'.format(
                file_name + "." + class_name, args, kwargs))
        results = self.process(*args, **kwargs)
        if self.print_log:
            cf.info('pipeline finish exec [{}], results: {}'.format(
                class_name, results))
        return results


class Pipeline(object):
    def __init__(self, components: List[Component] = None):
        self.components = components if components else []
        self.source_input = None

    def add(self, component: Component):
        self.components.append(component)
        return self

    def set_source_input(self, source_input):
        self.source_input = source_input
        return self

    def process(self, args=None):
        results = self.source_input
        if not results:
            results = args
        try:
            for c in self.components:
                if results is not None:
                    results = c.exec(results)
                else:
                    results = c.exec()
        except Exception as e:
            cf.error(get_exception_str(e))
        return results
