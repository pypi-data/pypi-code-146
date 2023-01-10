# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2022 Comet ML INC
#  This file can not be copied and/or distributed without
#  the express permission of Comet ML Inc.
# *******************************************************

import sys

from metaflow.plugins.cards import card_decorator

from . import comet_decorator, single_card_list

COMET_SKIP_DECORATOR = "comet_skip"


class CometFlow:
    def __init__(self, workspace=None, project_name=None):
        self._workspace = workspace
        self._project_name = project_name
        command_line = " ".join(sys.argv)
        self._card_on_command_line = "--with card" in command_line

    def __call__(self, flow_spec_class):
        for method in self._get_methods(flow_spec_class):
            if self._card_on_command_line:
                self._decorate_with_card(method)
            self._decorate_with_comet(method)
        return flow_spec_class

    def _decorate_with_card(self, method):
        method.decorators = single_card_list.SingleCardList(method.decorators)
        method.decorators.append(card_decorator.CardDecorator())

    def _get_methods(self, cls):
        return [
            getattr(cls, name) for name in cls.__dict__ if callable(getattr(cls, name))
        ]

    def _decorate_with_comet(self, method):
        decorator = comet_decorator.CometDecorator(
            workspace=self._workspace, comet_project=self._project_name
        )
        if COMET_SKIP_DECORATOR in method.decorators:
            decorator.skip = True
            method.decorators.remove(COMET_SKIP_DECORATOR)
        method.decorators.append(decorator)


def comet_skip(metaflow_step):
    metaflow_step.decorators.append(COMET_SKIP_DECORATOR)
    return metaflow_step


def comet_flow(func=None, **kwargs):
    if func is None:
        return CometFlow(**kwargs)
    return CometFlow().__call__(func)
