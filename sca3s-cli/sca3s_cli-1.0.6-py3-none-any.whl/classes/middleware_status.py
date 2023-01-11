# Copyright (C) 2018 SCARV project <info@scarv.org>
#
# Use of this source code is restricted per the MIT license, a copy of which
# can be found at https://opensource.org/licenses/MIT (or should be included
# as LICENSE.txt within the associated archive or repository).

import enum
import re

# status modes
MODE_SUCCESS = 0x0
MODE_FAILURE = 0x1
MODE_PENDING = 0x2

# status domain separators
DOMAIN_GENERIC = 0x0
DOMAIN_BE = 0x1
DOMAIN_FE = 0x2


class MWStatus(enum.IntEnum):
    def encode(mode, domain, value):
        return ((mode & 0x3) << 30) | ((domain & 0x3) << 28) | ((value & 0xFFFF) << 0)

    @staticmethod
    def build(value):
        try:  # B10 Integer
            return MWStatus(int(value))
        except ValueError:  # B16 Integer
            return MWStatus(int(value, 16))

    @staticmethod
    def dict(status: enum.IntEnum, data=None) -> dict:
        if data is None:
            return {
                'status': status.hex()
            }
        data['status'] = status.hex()
        return data

    # status values: generic
    SUCCESS = encode(MODE_SUCCESS, DOMAIN_GENERIC, 0x0000)
    # status values: generic, job related
    PENDING_JOB_EXECUTION = encode(MODE_PENDING, DOMAIN_GENERIC, 0x0100)
    PENDING_JOB_COMPLETION = encode(MODE_PENDING, DOMAIN_GENERIC, 0x0101)
    # status values:  back-end
    FAILURE_BE_JOB_PROLOGUE = encode(MODE_FAILURE, DOMAIN_BE, 0x0000)
    FAILURE_BE_JOB_PROCESS = encode(MODE_FAILURE, DOMAIN_BE, 0x0001)
    FAILURE_BE_JOB_EPILOGUE = encode(MODE_FAILURE, DOMAIN_BE, 0x0002)
    # status values: front-end, job/contest-related
    FAILURE_FE_JOB_NOT_FOUND = encode(MODE_FAILURE, DOMAIN_FE, 0x0000)
    FAILURE_FE_JOB_INVALID = encode(MODE_FAILURE, DOMAIN_FE, 0x0001)
    FAILURE_FE_CONTEST_NOT_FOUND = encode(MODE_FAILURE, DOMAIN_FE, 0x0002)
    # status values: front-end, API-related
    FAILURE_FE_API_QUEUE_EMPTY = encode(MODE_FAILURE, DOMAIN_FE, 0x0100)
    FAILURE_FE_API_QUEUE_FULL = encode(MODE_FAILURE, DOMAIN_FE, 0x0101)
    FAILURE_FE_API_INVALID_TOKEN = encode(MODE_FAILURE, DOMAIN_FE, 0x0102)
    FAILURE_FE_API_SCHEMA_MISMATCH = encode(MODE_FAILURE, DOMAIN_FE, 0x0103)
    # status values: front-end, User-related
    FAILURE_FE_USER_NOT_FOUND = encode(MODE_FAILURE, DOMAIN_FE, 0x0200)
    FAILURE_FE_USER_NO_CREDITS = encode(MODE_FAILURE, DOMAIN_FE, 0x0201)
    FAILURE_FE_USER_NOT_AUTHORIZED = encode(MODE_FAILURE, DOMAIN_FE, 0x0202)
    # status values: front-end, GitHub-related
    FAILURE_FE_GITHUB_UNACTIONABLE_EVENT = encode(MODE_FAILURE, DOMAIN_FE, 0x0300)
    FAILURE_FE_GITHUB_NO_CONFIG_FILE = encode(MODE_FAILURE, DOMAIN_FE, 0x0301)
    FAILURE_FE_GITHUB_INSTALLATION_TOKEN = encode(MODE_FAILURE, DOMAIN_FE, 0x0302)

    def is_success(self):
        return ((self.value >> 30) & 0x3) == MODE_SUCCESS

    def is_failure(self):
        return ((self.value >> 30) & 0x3) == MODE_FAILURE

    def is_pending(self):
        return ((self.value >> 30) & 0x3) == MODE_PENDING

    def describe(self):
        if (self.value == self.SUCCESS):
            t = 'success'

        elif (self.value == self.PENDING_JOB_EXECUTION):
            t = 'Job pending execution'
        elif (self.value == self.PENDING_JOB_COMPLETION):
            t = 'Job pending completion'
        elif (self.value == self.FAILURE_BE_JOB_PROLOGUE):
            t = 'Job failed during processing prologue (before processing, e.g. allocation of resources)'
        elif (self.value == self.FAILURE_BE_JOB_PROCESS):
            t = 'Job failed during processing'
        elif (self.value == self.FAILURE_BE_JOB_EPILOGUE):
            t = 'Job failed during processing epilogue (after  processing, e.g. deallocation of resources)'
        elif (self.value == self.FAILURE_FE_JOB_UNKNOWN):
            t = 'Job suffered an unknown failure on the frontend'
        elif (self.value == self.FAILURE_FE_JOB_INVALID):
            t = 'Job is invalid'
        elif (self.value == self.FAILURE_FE_API_QUEUE_EMPTY):
            t = 'The queue is empty and the job cannot be retrieved'
        elif (self.value == self.FAILURE_FE_API_QUEUE_FULL):
            t = 'The queue is full and the job cannot be submitted'
        elif (self.value == self.FAILURE_FE_AWS_AUTH):
            t = 'AWS authentication failed'
        elif (self.value == self.FAILURE_FE_AWS_URL):
            t = 'AWS storage URL generation failed'

        return re.sub(r'\s\s+', ' ', t)

    def hex(self):
        return "0x{0:08X}".format(self.value)

    def __repr__(self):
        return (self.name) + ' : ' + ('<' + '{0:08X}'.format(self.value) + '>')
