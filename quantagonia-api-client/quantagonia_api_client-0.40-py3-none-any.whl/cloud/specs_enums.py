from enum import Enum


class SpecsEndpoints(str, Enum):
    checkjob = "/checkjob"
    getcurstatus = "/getcurstatus"
    getcursolution = "/getcursolution"
    getcurlog = "/getcurlog"
    getresults = "/getresults"
    interruptjob = "/job"
    job = "/job"
    s3 = "/s3"


class JobStatus(str, Enum):
    finished = "FINISHED"
    terminated = "TERMINATED"
    error = "ERROR"
    running = "RUNNING"
    created = "CREATED"
    timeout = "TIMEOUT"
    success = "SUCCESS"