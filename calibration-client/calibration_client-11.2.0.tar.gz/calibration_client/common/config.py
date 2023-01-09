"""Project Configuration variables"""

##########################################################################
#
# APPLICATION MODULES
#
##########################################################################
DETECTOR = 'detector'
DETECTOR_TYPE = 'detector_type'
PHYSICAL_DETECTOR_UNIT = 'physical_detector_unit'
PARAMETER = 'parameter'
CONDITION = 'condition'
CALIBRATION = 'calibration'
CALIBRATION_CONSTANT = 'calibration_constant'
CALIBRATION_CONSTANT_VERSION = 'calibration_constant_version'
REPORT = 'report'

##########################################################################
#
# API PAGINATION
#
##########################################################################
DEF_PAGE = 1
DEF_PAGE_SIZE = 100

##########################################################################
#
# OAUTH2_XFEL_CLIENT (defaults)
#
##########################################################################
DEF_MAX_RETRIES = 3
DEF_TIMEOUT = 12
DEF_SSL_VERIFY = True

##########################################################################
#
# ACTIONS
#
##########################################################################
CREATE = 'CREATE'
DELETE = 'DELETE'
UPDATE = 'UPDATE'
GET = 'GET'
SET = 'SET'
