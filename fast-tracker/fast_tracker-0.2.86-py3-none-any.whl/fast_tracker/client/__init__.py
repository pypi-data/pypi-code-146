#!/usr/local/bin python3
# -*- coding: utf-8 -*-

"""
    created by FAST-DEV 2021/4/6
"""


class ServiceManagementClient(object):
    def send_instance_props(self):
        raise NotImplementedError()

    def send_heart_beat(self):
        raise NotImplementedError()


class TraceSegmentReportService(object):
    def report(self, generator):
        raise NotImplementedError()
