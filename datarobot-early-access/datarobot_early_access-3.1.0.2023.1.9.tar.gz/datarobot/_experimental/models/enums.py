#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from datarobot.enums import enum

UnsupervisedTypeEnum = enum(ANOMALY="anomaly", CLUSTERING="clustering")


class DocumentTextExtractionMethod:
    OCR = "TESSERACT_OCR"
    EMBEDDED = "DOCUMENT_TEXT_EXTRACTOR"

    ALL = [OCR, EMBEDDED]
