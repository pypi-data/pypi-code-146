#!/usr/bin/env python


class Property(object):
    JOB_ID = "jobId"
    TERMINATED = "terminated"
    RUN_FOLDER = "runFolder"
    SITE_ID = "siteId"
    INSTRUMENT_TYPE = "instrumentType"
    VERSION = "version"
    PRODUCT = "product"
    SAMPLE_REFERENCE = "uploadSampleReference"
    EXPECTED_UPLOAD_TIME = "expectedUploadTime"


class Type(object):
    UPLOAD_DATA = "UploadData"
    UPLOAD_MANIFEST = "UploadManifest"
    UPLOAD_SENTINEL = "UploadSentinel"
    UPLOAD_JOB = "UPLOAD"
    BAM = "bam"
    FASTQ = "fastq"
    CSV = "csv"
    PDF = "pdf"
    XLSX = "xlsx"
    WESQCREPORT = "WESQcReport"
    AB1 = "ab1"
    FSA = "fsa"
    METADATA = "metadata"
    BCL = "bcl"


class State(object):
    RUNNING = "running"
    WAITING = "waiting_on_input"
    TERMINATED = "terminated"
    DONE = "done"
    OPEN = "open"
    CLOSING = "closing"
    CLOSED = "closed"
