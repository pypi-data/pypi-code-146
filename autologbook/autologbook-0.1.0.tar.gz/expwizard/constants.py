"""
A set of constants to be used for the experiment wizard.
"""
import datetime
from enum import IntEnum, auto


class WizardPage(IntEnum):
    """Enumerator for the wizard pages."""
    PageIntro = auto()
    PageNewExperiment = auto()
    PageCommitNewExperiment = auto()
    PageConclusion = auto()
    PageReviewConfiguration = auto()
    PageSearchExperiment = auto()


# list of fully implemented microscope.
# using the naming convention of the microscopy protocol list.
fully_implemented_microscope = [
    'Quattro',
    'FIB Versa 3D',
    'Vega Tescan',
    'XL40-GB',
    'XL40-Cold'
]

# look up table to convert the microscope names from the protocol list convention to the autologbook convention
microscope_lut = {
    'Quattro': 'Quattro',
    'FIB Versa 3D': 'Versa',
    'XL40-GB': 'XL40-GB',
    'XL40-Cold': 'XL40-Cold',
    'Tecnai-TEM': 'TEM',
    'Vega Tescan': 'Vega'
}

# microscope names according to the microscopy protocol list.
microscope_in_protocol_list = [key for key in microscope_lut.keys()]

# microscope names according to the autologbook convention.
microscope_in_autologbook = list(dict.fromkeys(microscope_lut.values()))

# default settings.
default_settings = {
    'elog_user_name': {
        'value': 'log-robot',
        'typ': str
    },
    'elog_password': {
        'value': 'mTZtK2iFHhwqixkhJV0JkplSqMMu9ykWOhcNY/1WyL7',
        'typ': str
    },
    'elog_hostname': {
        'value': 'https://10.166.16.24',
        'typ': str
    },
    'elog_port': {
        'value': 8080,
        'typ': int
    },
    'elog_use_ssl': {
        'value': True,
        'typ': bool
    },
    'elog_timeout': {
        'value': 10,
        'typ': float
    },
    'protocol_list_logbook': {
        'value': 'Microscopy-Protocol',
        'typ': str
    },
    'quattro_logbook': {
        'value': 'Quattro-Analysis',
        'typ': str
    },
    'quattro_local_folder': {
        'value': 'M:\\',
        'typ': str
    },
    'versa_logbook': {
        'value': 'Versa-Analysis',
        'typ': str
    },
    'versa_local_folder': {
        'value': 'M:\\',
        'typ': str
    },
    'network_folder': {
        'value': f'R:\\A226\\Results\\{datetime.datetime.now():%Y}',
        'typ': str
    },
    'vega_logbook' : {
        'value': 'Vega-Analysis',
        'typ': str
    },
    'vega_local_folder' : {
        'value': 'M:\\',
        'typ': str
    },
    'xl40-GB_logbook' :{
        'value' : 'XL40-GB-Analysis',
        'typ': str
    },
    'xl40-GB_local_folder' : {
        'value': 'M:\\',
        'typ': str
    },
    'xl40-Cold_logbook' :{
        'value' : 'XL40-Cold-Analysis',
        'typ': str
    },
    'xl40-Cold_local_folder' : {
        'value': 'M:\\',
        'typ': str
    }
}
