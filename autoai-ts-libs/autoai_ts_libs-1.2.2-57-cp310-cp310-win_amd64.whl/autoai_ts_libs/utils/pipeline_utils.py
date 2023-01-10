################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R
# (c) Copyright IBM Corp. 2019, 2022. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

from autoai_ts_libs.utils.constants import PIPELINE_INFO, SYNTHESIZED_ANOMALY


class PipelineUtils:
    @staticmethod
    def get_pipeline_info_by_name(cls, name):
        pipeline = None
        for obj in PIPELINE_INFO:
            if obj["name"] == name:
                pipeline = obj
                break

        return pipeline

    @staticmethod
    def get_pipeline_name_list(cls):
        pipelines = []
        for obj in PIPELINE_INFO:
            pipelines.append(obj["name"])

        return pipelines

    @staticmethod
    def get_synthesized_anomaly_name(cls, anomaly_pattern, anomaly_type):
        for anomaly in SYNTHESIZED_ANOMALY:
            if (
                anomaly["pattern"] == anomaly_pattern
                and anomaly["type"] == anomaly_type
            ):
                return anomaly["name"]

        return None
