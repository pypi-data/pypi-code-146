"""Module to read, update and write JETTO settings (JSET) files."""

from __future__ import annotations

import datetime
import pathlib
import re
import itertools
import cerberus
import os.path
from typing import Tuple, Union, Iterator, Dict, List, Optional
from collections import OrderedDict

from jetto_tools._utils import is_int, is_float, is_bool, to_bool, is_numeric, to_numeric
import jetto_tools.common as common


_HEADER = """!===============================================================================
!                              JETTO SETTINGS FILE
!==============================================================================="""
_SECTION_MARKER = '*'
_EOF = 'EOF'
_SECTIONS = ['File Details', 'Settings', 'EOF']
_DETAILS = ['Creation Name', 'Creation Date', 'Creation Time', 'Version']

_SECTION_REGEX = r"""
         \*             # Match a section marker
         \s+            # Match any amount of whitespace (inc. newline) 
         \*             # Match another section marker
         ([\w ]+)       # Match any number of words and spaces - record in group as the section name
         \s*            # Match any amount of whitespace (inc. newline)
         """
_SECTION_PATTERN = re.compile(_SECTION_REGEX, re.VERBOSE)

_LINE_REGEX = r"""
    ^                           # Match start of the string
    (?P<name>[\S ]+?)           # Match any number of non-whitespace characters and spaces - record as parameter 'name'
    \s+                         # Match any amount of whitespace
    \:                          # Match the dividing colon
    \s*                         # Match any amount of whitespace
    (?P<value>[\S\s]*?)         # Match any whitespace and non-whitespace characters - record as parameter 'value'
    \s*                         # Match zero or more whitespace
    $                           # Match end of string
"""
_LINE_PATTERN = re.compile(_LINE_REGEX, re.VERBOSE)

_DEFAULT_DATE = datetime.date(year=1970, month=1, day=1)
_DEFAULT_TIME = datetime.time(hour=0, minute=0, second=0)

_VERSION_REGEX = r"""
    ^                           # Match start of the string
    v                           # Match leading 'v'
    (?P<day>\d\d)               # Match two digits of day
    (?P<month>\d\d)             # Match two digits of month
    (?P<year>\d\d)              # Match two digits of year
    .*                          # Match any other characters
    $                           # Match end of the string
"""
_VERSION_PATTERN = re.compile(_VERSION_REGEX, re.ASCII | re.VERBOSE)


def read(path: pathlib.Path):
    """Read a JSET file

    Reads the contents of the provided file, and constructs a `JSET` object from them

    :Example:

    >>> from jetto_tools.jset import read
    >>> from pathlib import Path
    >>> j = jset.read(Path('/path/to/jetto.jset'))

    :param path: Path to the JSET file to read
    :type path: pathlib.Path
    :return: JSET object
    :rtype: JSET
    """
    with open(path, 'r', encoding='utf-8') as f:
        return JSET(f.read())


def write(jset, path: pathlib.Path):
    """Write a JSET file

    Sets the 'File Details' section of the JSET, and writes the JSET out to the specified path.

    - The 'Creation Name' field is set to the value of path
    - The 'Creation Date' field is set to the current date
    - The Creation Time' field is set to the current time

    :param jset: JSET object to write out
    :type jset: JSET
    :param path: Path to write the JSET to
    :type path: pathlib.Path
    """
    jset.cname = str(path)
    now = datetime.datetime.now()
    jset.cdate = now.date()
    jset.ctime = now.time()
    jset.version = ''
    with open(path, 'w') as f:
        f.write(str(jset))


class JSETError(Exception):
    """Generic exception used for all errors in the ``JSET`` module"""
    pass


class JSET:
    """Class representing a JETTO settings (JSET) file

    Initialise from a JSET file:

    .. highlight:: python

    >>> from jetto_tools.jset import JSET
    >>> with open("jetto.jset") as f:
    >>>   jset = JSET(f.read())

    Retrieve details as properties

    .. highlight:: python

    >>> jset.cname
    '/work/fcasson/jetto/runs/runtestdata5i/jetto.jset'
    >>> jset.cdate
    datetime.date(2019, 7, 8)
    >>> jset.ctime
    datetime.time(16, 43, 37)
    >>> jset.version
    'v060619'

    Retrieve settings by identifier:

    .. highlight:: python

    >>> jset['AdvancedPanel.catCodeID']
    'jetto'

    Update settings via identifier:

    .. highlight:: python

    >>> jset['BallooningL1RefPanel.DurationFallTime']
    0.0002
    >>> jset['BallooningL1RefPanel.DurationFallTime'] = 0.001
    >>> jset['BallooningL1RefPanel.DurationFallTime']
    0.001

    Check presence of setting:

    .. highlight:: python

    >>> 'BallooningL1RefPanel.DurationFallTime' in jset
    True

    Write back to string:

    .. highlight:: python

    >>> print(str(jset))
    !===============================================================================
    !                              JETTO SETTINGS FILE
    !===============================================================================
    *
    *File Details
    Creation Name                                               : /work/fcasson/jetto/runs/runtestdata5i/jetto.jset
    Creation Date                                               : 08/07/2019
    Creation Time                                               : 16:43:37
    Version                                                     : v060619
    *
    *Settings
    AdvancedPanel.catCodeID                                     : jetto
    ...

    """
    def __init__(self, s: str):
        """Initialise a JSET from file contents

        :param s: JSET file contents
        :type s: str
        :raise: JSETError if the file does not contain the expected sections
        """
        self._sections, self._contents = JSET._parse_sections(s)
        if self._sections != _SECTIONS:
            raise JSETError('JSET must contain File Details, Settings and EOF sections, in that order')

        self._details = JSET._parse_details(self._contents['File Details'])

        all_settings = JSET._parse_settings(self._contents['Settings'])
        self._extras = JSET._parse_jetto_extras(all_settings)
        self._sanco_extras = JSET._parse_sanco_extras(all_settings)
        self._settings = JSET._remove_extra_namelist_settings(all_settings)
        self._exfile = JSET._retrieve_exfile(self._settings)

    def __str__(self):
        """Generate a string representation of the JSET

        Formats the contents of the JSET as a string suitable for writing to a JSET file. The lines in the Settings
        section are sorted in lexicographic order, following the JAMS convention.

        :return: JSET as a string
        :rtype: str
        """
        non_extra_settings_lines = \
            ['{:60}: {}'.format(name, JSET._detypify(value)) for name, value in
             self._settings.items()]

        jetto_extra_settings_lines = \
            ['{:60}: {}'.format(name, JSET._detypify(value)) for name, value in
             self._extras.as_jset_settings().items()]

        sanco_extra_settings_lines = \
            ['{:60}: {}'.format(name, JSET._detypify(value)) for name, value in
             self._sanco_extras.as_jset_settings().items()]

        settings_lines = sorted(non_extra_settings_lines +
                                jetto_extra_settings_lines +
                                sanco_extra_settings_lines)

        details = '\n'.join(['{:60}: {}'.format(name, JSET._detypify(value)) for name, value in
                             self._details.items()])
        settings = '\n'.join(settings_lines)

        return '\n'.join([_HEADER,
                          _SECTION_MARKER,
                          _SECTION_MARKER + 'File Details',
                          details,
                          _SECTION_MARKER,
                          _SECTION_MARKER + 'Settings',
                          settings,
                          _SECTION_MARKER,
                          _SECTION_MARKER + 'EOF',
                          ''
                          ])

    def get(self, setting: str, default):
        """Safely retrieve the value of a setting

        :param setting: Setting identifier
        :return: The parameter value, or ``default`` if it doesn't exist
        """
        return self._settings.get(setting, default)

    def __getitem__(self, setting: str) -> Union[None, int, float, bool, str]:
        """Retrieve the value of the given JSET setting

        :param setting: Setting identifier
        :return: The parameter value
        :raise: JSETError if the setting does not exist in the JSET
        """
        if setting not in self._settings:
            raise JSETError('Setting {} does not exist in the JSET'.format(setting))

        return self._settings[setting]

    def __setitem__(self, setting: str, value: Union[None, int, float, bool, str]):
        """Set the value of a given JSET setting

        :param setting: Setting identifier
        :param value: Setting value
        :raise: JSETError if the setting does not exist in the JSET
        """
        if setting not in self._settings:
            raise JSETError('Setting {} does not exist in the JSET'.format(setting))

        self._settings[setting] = value

    def __contains__(self, setting: str) -> bool:
        """Check if a parameter exists in the settings

        :param setting: Setting identifier
        :return: True if the parameter is in the settings; otherwise False
        :rtype: bool
        """
        return setting in self._settings

    def __delitem__(self, setting):
        """Raise an exception if someone tries to delete a setting

        :param setting: Setting identifier
        :raises: JSETError
        """
        raise JSETError('Cannot delete setting from JSET')

    @property
    def cname(self) -> str:
        """Return the file Creation Name

        Returns the contents of the 'Creation Name' field in the File Details section

        :return: The name
        :rtype: str
        """
        return self._details['Creation Name']

    @cname.setter
    def cname(self, cname: str):
        """Set the file Creation Name

        Sets the contents of the 'Creation Name' field in the File Details section

        :param cname: The name
        :type cname: str
        """
        self._details['Creation Name'] = cname

    @property
    def cdate(self) -> datetime.date:
        """Return the file Creation Date

        Returns the contents of the 'Creation Date' field in the File Details section

        :return: The date
        :rtype: datetime.date
        """
        return self._details['Creation Date']

    @cdate.setter
    def cdate(self, cdate: datetime.date):
        """Set the file Creation Date

        Sets the contents of the 'Creation Date' field in the File Details section

        :param cdate: The name
        :type cdate: datetime.date
        """
        self._details['Creation Date'] = cdate

    @property
    def ctime(self) -> datetime.time:
        """Return the file Creation Time

        Returns the contents of the 'Creation Time' field in the File Details section

        :return: The time
        :rtype: datetime.time
        """
        return self._details['Creation Time']

    @ctime.setter
    def ctime(self, ctime: datetime.time):
        """Set the file Creation Time

        Sets the contents of the 'Creation Time' field in the File Details section

        :param ctime: The time
        :type ctime: datetime.time
        """
        self._details['Creation Time'] = ctime

    @property
    def version(self) -> str:
        """Return the file Version

        Returns the contents of the 'Version' field in the File Details section

        :return: The version
        :rtype: str
        """
        return self._details['Version']

    @version.setter
    def version(self, version: str):
        """Set the file Version

        Sets the contents of the 'Version' field in the File Details section

        :param version: The version
        :type version: str
        """
        self._details['Version'] = version

    @property
    def version_as_date(self) -> Union[None, datetime.date]:
        """Return the file Version as a date

        Returns the contents of the 'Version' field in the File Details section. Assumes that the version string starts
        with the format ``vddmmyy`` (but it can have other characters appended).

        :return: The version, or None if the version could not be parsed
        :rtype: datetime.date or None
        """
        match = _VERSION_PATTERN.fullmatch(self.version)
        if not match:
            return None

        day = int(match.group('day'))
        month = int(match.group('month'))
        year = int(match.group('year')) + 2000

        return datetime.date(year=year, month=month, day=day)

    @property
    def extras(self) -> ExtraNamelists:
        """Return the JETTO extra namelists

        :return: The extra namelists
        :rtype: ExtraNamelists
        """
        return self._extras

    @property
    def sanco_extras(self):
        """Return the SANCO extra namelists

        :return: The extra namelists
        :rtype: ExtraNamelists
        """
        return self._sanco_extras

    @property
    def exfile(self):
        """Retrieve the ex-file path

        :return: The path to the configured ex-file
        :rtype: str
        """
        return JSET._retrieve_exfile(self._settings)

    @exfile.setter
    def exfile(self, exfile: str):
        """Set the exfile

        Only setting of a private source for the exfile is supported. Cataloged sources are not.

        :param exfile: Path to the exfile
        :type exfile: str
        """
        self._settings['SetUpPanel.exFileName'] = exfile
        self._settings['SetUpPanel.exFilePrvDir'] = os.path.dirname(exfile)
        self._settings['SetUpPanel.exFileSource'] = 'Private'

    def make_graybeamfile_private(self, path: str):
        self._settings['ECRHPanel.GRAYBeamFileName'] = path
        self._settings['ECRHPanel.GRAYBeamPrvDir'] = os.path.dirname(path)
        self._settings['ECRHPanel.GRAYBeamSource'] = 'Private'

    @property
    def binary(self):
        """Return the JETTO version

        Returns the contents of the 'JobProcessingPanel.name' field in the Settings section

        :return: The version
        :rtype: str
        """
        return self._settings['JobProcessingPanel.name']

    @binary.setter
    def binary(self, value: str):
        """Set the JETTO version

        Sets the contents of the 'JobProcessingPanel.name' field in the Settings section

        :param value: JETTO version
        :type value: str
        """
        self._settings['JobProcessingPanel.name'] = value

    @property
    def userid(self):
        """Return the JETTO userid

        Returns the contents of the 'JobProcessingPanel.userid' field in the Settings section

        :return: The userid
        :rtype: str
        """
        return self._settings['JobProcessingPanel.userid']

    @userid.setter
    def userid(self, value: str):
        """Set the JETTO userid

        Sets the contents of the 'JobProcessingPanel.userid' field in the Settings section

        :param value: JETTO userid
        :type value: str
        """
        self._settings['JobProcessingPanel.userid'] = value

    @property
    def processors(self):
        """Return the number of processors used

        Returns the contents of the 'JobProcessingPanel.numProcessors' field in the Settings section

        :return: The number of processors
        :rtype: int
        """
        return self._settings['JobProcessingPanel.numProcessors']

    @processors.setter
    def processors(self, value: int):
        """Set the number of processors used

        Sets the contents of the 'JobProcessingPanel.numProcessors' field in the Settings section

        :param value: Number of processors
        :type value: int
        """
        self._settings['JobProcessingPanel.numProcessors'] = value

    @property
    def impurities(self):
        """Get the impurities select flag

        Returns the contents of the 'ImpOptionPanel.select' field in the Settings section

        :return: The select flag
        :rtype: bool
        """
        return self._settings['ImpOptionPanel.select']

    @impurities.setter
    def impurities(self, value: bool):
        """Set the impurities select flag

        Sets the contents of the 'ImpOptionPanel.select' field in the Settings section

        :param value: The new value of the select flag
        :type value: bool
        """
        self._settings['ImpOptionPanel.select'] = value

    @property
    def sanco(self) -> bool:
        """Check if sanco is set as the impurities source

        Returns whether or not the the contents of the 'ImpOptionPanel.source' field in the Setting section are 'Sanco'

        :return: True if the impurities source is sanco; otherwise False
        :rtype: bool
        """
        return self._settings['ImpOptionPanel.source'] == 'Sanco'

    @sanco.setter
    def sanco(self, value):
        """Raise an exception if the user attempts to modify the sanco flag"""
        raise JSETError('Sanco impurities source flag is read-only')

    @property
    def restart(self):
        """Get the restart flag

        Returns the value of the 'AdvancedPanel.selReadRestart' field in the Settings section, or False
        if the field doesn't exist

        :return: The restart flag
        :rtype: Bool
        """
        return self._settings.get('AdvancedPanel.selReadRestart', False)

    @restart.setter
    def restart(self, value: bool):
        """Set the restart flag

        Sets the contents of the 'AdvancedPanel.selReadRestart' field in the Settings section. If the field doesn't
        exist, it is added to the JSET.

        :param value: Restart flag
        :type value: bool
        :raise: JSETError if value is not boolean
        """
        if not isinstance(value, bool):
            raise JSETError(f'Invalid value {value} for restart flag')

        self._settings['AdvancedPanel.selReadRestart'] = value

    @property
    def continue_(self):
        """Get the continue flag

        Returns the value of the 'AdvancedPanel.selReadContinue' field in the Settings section, or False
        if the field doesn't exist

        :return: The continue flag
        :rtype: Bool
        """
        return self._settings.get('AdvancedPanel.selReadContinue', False)

    @continue_.setter
    def continue_(self, value: bool):
        """Set the continue

        Sets the contents of the 'AdvancedPanel.selReadContinue' field in the Settings section. If the field doesn't
        exist, it is added to the JSET.

        :param value: Continue flag
        :type value: bool
        :raise: JSETError if value is not boolean
        """
        if not isinstance(value, bool):
            raise JSETError(f'Invalid value {value} for continue flag')

        self._settings['AdvancedPanel.selReadContinue'] = value

    @property
    def repeat(self):
        """Get the repeat flag

        Returns the value of the 'AdvancedPanel.selReadRepeat' field in the Settings section, or False
        if the field doesn't exist

        :return: The repeat flag
        :rtype: Bool
        """
        return self._settings.get('AdvancedPanel.selReadRepeat', False)

    @repeat.setter
    def repeat(self, value: bool):
        """Set the repeat flag

        Sets the contents of the 'AdvancedPanel.selReadRepeat' field in the Settings section. If the field doesn't
        exist, it is added to the JSET.

        :param value: Repeat flag
        :type value: bool
        :raise: JSETError if value is not boolean
        """
        if not isinstance(value, bool):
            raise JSETError(f'Invalid value {value} for repeat flag')

        self._settings['AdvancedPanel.selReadRepeat'] = value

    @property
    def rundir(self):
        """Get the run directory

        Returns the contents of the 'JobProcessingPanel.runDirNumber' field in the Settings section

        :return: The run directory
        :rtype: str
        """
        return self._settings['JobProcessingPanel.runDirNumber']

    @rundir.setter
    def rundir(self, value: str):
        """Set the run directory

        Sets the contents of the 'JobProcessingPanel.runDirNumber' field in the Settings section

        :param value: The new value of the run directory
        :type value: str
        """
        self._settings['JobProcessingPanel.runDirNumber'] = value

    @property
    def walltime(self):
        """Get the walltime

        Returns the contents of the 'JobProcessingPanel.wallTime' field in the Settings section. If the field does not
        exist, returns None.

        :return: The walltime
        :rtype: Union[int, None]
        """
        return self._settings.get('JobProcessingPanel.wallTime', None)

    @walltime.setter
    def walltime(self, value: float):
        """Set the walltime

        Sets the contents of the 'JobProcessingPanel.wallTime' field in the Settings section

        :param value: The new value of the walltime
        :type value: float

        """
        self._settings['JobProcessingPanel.wallTime'] = value

    def set_catalogued_files(self, owner: str, code: str, machine: str, shot: int, date: str, seq: int):
        """Set the file sources for the catalogued case

        This function attempts to replicate the behaviour of the ``JettoProcessSettings.postReadSettings`` function in
        JAMS, which executes on loading a catalogued case. For each file in the JSET, it lists the file source as
        catalogued, and adjusts each of the relevant JSET parameters accordingly.

        For some files, this action is always performed on load. For others, additional logical checks are required to
        determine if the adjustment needs to be performed. For example, the SANCO files are only adjusted if
        impurities are enabled and if SANCO is set as the impurities source.

        :param owner: Catalogue owner
        :type owner: str
        :param code: Code identifier
        :type code: str
        :param machine: Machine identifier
        :type machine: str
        :param shot: Shot number
        :type shot: int
        :param date: Date identifier
        :type date: str
        :param seq: Sequence number
        :type seq: int
        """
        args = (owner, code, machine, shot, date, seq)

        self._set_restart_catalogued(*args)
        self._set_catalogued_file('SetUpPanel', 'exFile', *args, file_postfix=False)
        self._set_catalogued_file('LHPanel', 'FRTC', *args)
        self._set_catalogued_file('EquilCreateNLRefPanel', 'Create', *args)
        self._set_catalogued_file('EquilCreateNLRefPanel', 'CreateNominalRef', *args)
        self._set_catalogued_file('EquilEqdskRefPanel', 'eqdskFile', *args)
        self._set_catalogued_file('EquilCbankRefPanel', 'cbankFile', *args)
        self._set_catalogued_file('ECRHPanel', 'GRAY', *args)
        self._set_catalogued_gray_beam_file(*args)

        equil_source = self.get('EquilibriumPanel.source', '')
        equil_bound_source = self.get('EquilEscoRefPanel.boundSource', '')
        if equil_source == 'ESCO' and equil_bound_source in ('EQDSK directly', 'EQDSK using FLUSH'):
            self._set_catalogued_file('EquilEscoRefPanel', 'eqdskFile', *args, file_postfix=False)

        if equil_source == 'ESCO' and equil_bound_source == 'Boundary File':
            self._set_catalogued_file('EquilEscoRefPanel', 'bndFile', *args, file_postfix=False)

        wf_select = self.get('ExternalWFPanel.select', False)
        if wf_select is True:
            self._set_catalogued_file('ExternalWFPanel', 'CfgFile', *args, file_postfix=False)

        nbi_select = self.get('NBIPanel.select', False)
        nbi_source = self.get('NBIPanel.source', '')
        nbi_ascot_source = self.get('NBIAscotRef.source', '')
        if nbi_select is True and nbi_source == 'Ascot' and nbi_ascot_source == 'From File':
            self._set_catalogued_file('NBIAscotRef', 'config', *args)

        catpath = JSET._get_catalogue_path(*args)
        transport_file_select = self.get('SancoTransportPanel.transportFileSelect', False)
        if self.impurities and self.sanco and transport_file_select:
            self._set_catalogued_file('SancoTransportPanel', 'transport', *args,
                                      file_postfix=True, file_name=os.path.join(catpath, 'jetto.str'))

        grid_file_select = self.get('SancoOtherPanel.selReadGridFile', False)
        if self.impurities and self.sanco and grid_file_select:
            self._set_catalogued_file('SancoOtherPanel', 'gridFile', *args,
                                      file_postfix=False, file_name=os.path.join(catpath, 'jetto.sgrid'))

    def set_restart_flags(self, continue_: bool):
        """Set the JSET restart flags

        Sets the contents of the AdvancedPanel in the JSET based on the continuation status. The following rules are
        applied:

        - If it's a continuation case, `selReadRestart` is set True, `selReadContinue` is set True and `selReadRepeat`
          is set False
        - It it's not a continuation case, and `selReadRestart` is True, then `selReadContinue` is set False and
          `selReadRepeat` is set True
        - It it's not a continuation case, and `selReadRestart` is False, then no change is applied

        :param continue_: Continuation case status
        :type continue_: bool
        """
        if continue_:
            self.restart = True
            self.continue_ = True
            self.repeat = False
        else:
            if self.restart:
                self.continue_ = False
                self.repeat = True

    def set_time_config(self, time_config: common.TimeConfig):
        """Set the JSET's time configuration

        Given a time configuration, updates the corresponding fields in the JSET to match the configuration

        :param time_config: Time configuration
        :type time_config: jetto_tools.common.TimeConfig
        """
        self._settings['SetUpPanel.startTime'] = time_config.start_time
        self._settings['EquilEscoRefPanel.tvalue.tinterval.startRange'] = time_config.start_time
        self._settings['OutputStdPanel.profileRangeStart'] = time_config.start_time
        self._settings['SetUpPanel.endTime'] = time_config.end_time
        self._settings['EquilEscoRefPanel.tvalue.tinterval.endRange'] = time_config.end_time
        self._settings['OutputStdPanel.profileRangeEnd'] = time_config.end_time
        self._settings['EquilEscoRefPanel.tvalue.tinterval.numRange'] = time_config.n_esco_times
        self._settings['OutputStdPanel.numOfProfileRangeTimes'] = time_config.n_output_profile_times

    def get_time_config(self) -> common.TimeConfig:
        """Get the JSET's time configuration

        Extracts the time fields from the JSET, and returns them as a time configuration object

        :return: JSET time configuration
        :rtype: common.TimeConfig
        """
        return common.TimeConfig(**{
            'start_time': self._settings['SetUpPanel.startTime'],
            'end_time': self._settings['SetUpPanel.endTime'],
            'n_esco_times': self._settings['EquilEscoRefPanel.tvalue.tinterval.numRange'],
            'n_output_profile_times': self._settings['OutputStdPanel.numOfProfileRangeTimes']
        })

    def reset_fixed_output_profiles_times(self):
        """Reset the array of fixed output profiles times

        Convenience function which clears all of the fixed profile times from OutputStdPanel
        """
        profile_times = (setting for setting in self._settings
                         if setting.startswith('OutputStdPanel.profileFixedTimes'))
        for setting in profile_times:
            self._settings[setting] = None

    def apply_bp_coilset(self, coilset: Dict):
        """Update the JSET with a new BLUEPRINT coilset

        Takes a BLUEPRINT coilset and adds its contents to the extrat namelists of the JSET. If any of the relevant
        variables already exist in the JSET, they will be overwritten. The coil width and height dimensions are
        doubled with respect to the ``dx`` and ``dz`` dimensions provided in the coilset.

        No validation of the contents of the coilset is done. All coils in the coilset will be included, in the same
        order as they appear when iterating over the dictionary, *except* for any coils which have zero current.

        If the extra namelist parameter ``PFCIPLINNUM`` is present in the JSET, this function will additionally populate
        the ``PFCIPLIN`` variable with constant time polygons for each of the coils.

        :param coilset: Coilset read from a BLUEPRINT ``coilset.json`` file
        :type coilset: Dict
        """
        filtered_coilset = {k: v for k, v in coilset.items() if v['current'] != 0.0}

        self._extras['PFCNUM'] = ExtraNamelistItem(len(filtered_coilset))
        self._extras['PFCRCEN'] = ExtraNamelistItem([filtered_coilset[coil]['x'] for coil in filtered_coilset], 1)
        self._extras['PFCZCEN'] = ExtraNamelistItem([filtered_coilset[coil]['z'] for coil in filtered_coilset], 1)
        self._extras['PFCRWID'] = ExtraNamelistItem([filtered_coilset[coil]['dx'] * 2 for coil in filtered_coilset], 1)
        self._extras['PFCZWID'] = ExtraNamelistItem([filtered_coilset[coil]['dz'] * 2 for coil in filtered_coilset], 1)

        if 'PFCIPLINNUM' in self._extras:
            coil_items = {}
            for icoil, coil in enumerate(filtered_coilset):
                for time in range(1, self._extras['PFCIPLINNUM'][None] + 1):
                    coil_items[(time, icoil + 1)] = \
                        ExtraNamelistItem(filtered_coilset[coil]['current'], (time, icoil + 1))

            first_index = next(iter(coil_items))
            combined_coil_items = coil_items[first_index]
            del coil_items[first_index]

            for item in coil_items.values():
                combined_coil_items.combine(item)

            self._extras['PFCIPLIN'] = combined_coil_items

    def _set_restart_catalogued(self, owner: str, code: str, machine: str, shot: int, date: str, seq: int):
        """Set the restart parameters for a catalogued case

        Sets the advanced panel parameters ('AdvancedPanel....') in the JSET, based on the arguments supplied. If this
        is a continuation case (i.e. the 'AdvancedPanel.selReadContinue' is set to 'true', then the existing catalogue
        parameters are saved in the '_R' parameters in the advanced panel section. This replicates the corresponding
        JAMS behaviour on loading a catalogued run.

        :param owner: Catalogue owner
        :type owner: str
        :param code: Code identifier
        :type code: str
        :param machine: Machine identifier
        :type machine: str
        :param shot: Shot number
        :type shot: int
        :param date: Date identifier
        :type date: str
        :param seq: Sequence number
        :type seq: int
        """
        if self['AdvancedPanel.selReadContinue']:
            self['AdvancedPanel.catOwner_R'] = self['AdvancedPanel.catOwner']
            self['AdvancedPanel.catCodeID_R'] = self['AdvancedPanel.catCodeID']
            self['AdvancedPanel.catMachID_R'] = self['AdvancedPanel.catMachID']
            self['AdvancedPanel.catShotID_R'] = self['AdvancedPanel.catShotID']
            self['AdvancedPanel.catDateID_R'] = self['AdvancedPanel.catDateID']
            self['AdvancedPanel.catSeqNum_R'] = self['AdvancedPanel.catSeqNum']

        self['AdvancedPanel.catOwner'] = owner
        self['AdvancedPanel.catCodeID'] = code
        self['AdvancedPanel.catMachID'] = machine
        self['AdvancedPanel.catShotID'] = shot
        self['AdvancedPanel.catDateID'] = date
        self['AdvancedPanel.catSeqNum'] = seq

    def _set_catalogued_file(self, panel: str, prefix: str, owner: str, code: str, machine: str, shot: int, date: str,
                             seq: int, file_postfix=True, file_name=''):
        """Set a file to be sourced from the catalogue

        Sets the JSET settings associated with a particular file (defined by its panel name and file prefix) to indicate
        that the file is sourced from a catalogued case. JAMS uses a standardised set of JSET parameters for each file,
        one each for the catalogue source, owner, code, machine, shot, date and sequence.

        Unfortunately, JAMS is not entirely consistent in its naming convention, with the result that the file name
        parameter sometimes (e.g. for Equilibrium EQDSK or CBank files) has an additional ``File`` inserted in the JSET
        identifier. The ``file_postfix`` flag indicates to this function whether or not such an additional ``File``
        string needs to be inserted.

        Additionally, for some files is is desirable to include the path to the catalogued file in the file name
        setting. This is handled via the ``file_name`` parameter.

        :param panel: JAMS panel identifier for the file
        :type panel: str
        :prefix: JAMS file prefix identifier
        :type prefix: str
        :param owner: Catalogue owner
        :type owner: str
        :param code: Code identifier
        :type code: str
        :param machine: Machine identifier
        :type machine: str
        :param shot: Shot number
        :type shot: int
        :param date: Date identifier
        :type date: str
        :param seq: Sequence number
        :type seq: int
        :param file_postfix: Indicates whether or not to modify the JSET id for the file name
        :type file_postfix: bool
        :param file_name: Path to the catalogued file (if desired, otherwise blank)
        :type file_name: str
        """
        full_prefix = f'{panel}.{prefix}'

        self._set_or_update_item(f'{full_prefix}Source', 'Cataloged')
        self._set_or_update_item(f'{full_prefix}CatOwner', owner)
        self._set_or_update_item(f'{full_prefix}CatCodeID', code)
        self._set_or_update_item(f'{full_prefix}CatMachID', machine)
        self._set_or_update_item(f'{full_prefix}CatShotID', shot)
        self._set_or_update_item(f'{full_prefix}CatDateID', date)
        self._set_or_update_item(f'{full_prefix}CatSeqNum', seq)
        self._set_or_update_item(f'{full_prefix}PrvDir', '')
        if file_postfix is True:
            self._set_or_update_item(f'{full_prefix}FileName', file_name)
        else:
            self._set_or_update_item(f'{full_prefix}Name', file_name)

    def _set_catalogued_gray_beam_file(self, owner: str, code: str, machine: str, shot: int, date: str, seq: int):
        """Set the ECRH GRAY beam file to be sourced from the catalogue

        Requires a separate implementation from the other files, as JAMS uses inconsistent naming for the JSET settings
        that identify the characteristics of the GRAY Beam file. Ordinarily, the owner, code etc. would have settings
        ``GRAYBeamCatOwner`` and so forth, but this only applies to the source, previous directory and file name
        settings. The remaining settings omit the ``Beam``, and thus overlap with the regular GRAY file in the ECRH
        panel.

        :param owner: Catalogue owner
        :type owner: str
        :param code: Code identifier
        :type code: str
        :param machine: Machine identifier
        :type machine: str
        :param shot: Shot number
        :type shot: int
        :param date: Date identifier
        :type date: str
        :param seq: Sequence number
        :type seq: int
        """
        full_prefix = f'ECRHPanel.GRAY'

        self._set_or_update_item(f'{full_prefix}BeamSource', 'Cataloged')
        self._set_or_update_item(f'{full_prefix}CatOwner', owner)
        self._set_or_update_item(f'{full_prefix}CatCodeID', code)
        self._set_or_update_item(f'{full_prefix}CatMachID', machine)
        self._set_or_update_item(f'{full_prefix}CatShotID', shot)
        self._set_or_update_item(f'{full_prefix}CatDateID', date)
        self._set_or_update_item(f'{full_prefix}CatSeqNum', seq)
        self._set_or_update_item(f'{full_prefix}BeamPrvDir', '')
        self._set_or_update_item(f'{full_prefix}BeamFileName', '')

    def set_backwards_compatibility(self):
        """Make backwards compatibility changes
        
        If the version is less than or equal to a threshold date (2010-10-26) and the current usage is set as 
        'Interpretive' in the equations panel, a number of settings must be changed for backwards compatibility. This 
        is consistent with the JAMS behaviour implemented in ``JettoProcessSettings.postReadSettings``.
        """
        if self.version_as_date <= datetime.date(year=2010, month=10, day=26) \
                and self['EquationsPanel.current.usage'] == 'Interpretive':
            self['BoundCondPanel.faradayOption'] = 'Current (amps)'
            self['BoundCondPanel.current'] = 'From PPF'

    @classmethod
    def _retrieve_exfile(cls, settings: Dict) -> str:
        """Extract the exfile path from the settings

        Extracts the exfile path from the parsed settings section of the JSET. If the SetUpPanel.exFileSource is
        'Private', the path is given by the setting SetUpPanel.exFileName. If it is 'Cataloged', the source is given
        by the concatentation of the catalogue path fields from the setup panel drop-down menus.

        :param settings: Parsed settings
        :type settings: dict
        :return: The exfile path
        :rtype: str
        :raise JSETError if the exFileSource is not either 'Private' or 'Cataloged'
        """
        source = settings['SetUpPanel.exFileSource']

        if source == 'Private':
            return settings['SetUpPanel.exFileName']
        elif source == 'Cataloged':
            owner = settings['SetUpPanel.exFileCatOwner']
            code = settings['SetUpPanel.exFileCatCodeID']
            date = settings['SetUpPanel.exFileCatDateID']
            machine = settings['SetUpPanel.exFileCatMachID']
            seq = settings['SetUpPanel.exFileCatSeqNum']
            shot = settings['SetUpPanel.exFileCatShotID']
            return os.path.join(cls._get_catalogue_path(owner, code, machine, shot, date, seq), 'jetto.ex')
        else:
            raise JSETError(f"Exfile source {source} is unrecognised")

    @classmethod
    def _get_catalogue_path(cls, owner: str, code: str, machine: str, shot: int, date: str, seq: int):
        """Get the path to a catalogue directory

        Assumes that the catalogue directory is located at
        /u/<owner>/cmg/catalog/<code>/<machine>/<shot>/<date>/seq#<seq>. Does not reference any environment variable
        modifying the location of the user home directory.

        :param owner: Catalogue owner
        :type owner: str
        :param code: Code identifier
        :type code: str
        :param machine: Machine identifier
        :type machine: str
        :param shot: Shot number
        :type shot: int
        :param date: Date identifier
        :type date: str
        :param seq: Sequence number
        :type seq: int
        """
        return f'/u/{owner}/cmg/catalog/{code}/{machine}/{shot}/{date}/seq#{seq}'

    @classmethod
    def _parse_sections(cls, s: str) -> Tuple[List, Dict]:
        """Parse the Sections of a JSET file

        Extracts the section names and contents from a JSET file. A section name is delimited by the section header,
        made up of the section marker and newlines i.e.

        *
        * Section Name

        The contents of each section are also extracted, as a single string containing all of the lines following the
        section header, until the start of the next section header. Note that EOF section in a well-formed file
        typically has no content. The file header (any line starting with '!'), and any blank lines are discarded.

        :param s: JSET file contents
        :type s: str
        :return: Dictionary mapping section name to section contents e.g.
         {'File Details', : 'Creation Name ...', 'Settings' : 'AdvancedPanel...', 'EOF' : ''}
        :rtype: dict
        """

        # Remove the header lines and any blank lines
        s = '\n'.join([line for line in s.split('\n') if not (line.startswith('!') or line.strip() == '')])

        section_names = _SECTION_PATTERN.findall(s)
        section_contents = _SECTION_PATTERN.split(s)
        # Remove the leading empty string produced by split()
        section_contents.remove('')
        # Fiddly bit of code. re.split() returns all of the file including the sections (because of group in the regex)
        # so we need to remove the section names manually in order to cleanly separate the two
        for section in section_names:
            section_contents.remove(section)

        section_contents_map = {name: contents for (name, contents) in zip(section_names, section_contents)}

        return (section_names, section_contents_map)

    @classmethod
    def _parse_details(cls, s: str) -> Dict[str, Union[str, datetime.date, datetime.time]]:
        """Parse the File Details section of a JSET file

        Extracts the Creation Name, Creation Date, Creation Time and Version fields from the File Details section. The
        fields are returned as values in a dictionary, where the keys are 'Creation Name' etc. The creation date and
        time values are transformed into datetime.date and datetime.time objects before being returned.

        :param s: Contents of the File Details section, excluding the section header
        :type s: str
        :return: Dictionary with File Details parameter names as keys, and parameter values as values
        :raise: JSETError if the expected fields are not found, or if the date or time parameters cannot be decoded
        """
        parsed_lines = [JSET._parse_line(line) for line in s.split('\n') if line]
        details = {name: value for (name, value) in parsed_lines}

        for name in details:
            if name not in _DETAILS:
                raise JSETError('Unexpected field "{}" in File Details section'.format(name))
        for name in _DETAILS:
            if name not in details:
                raise JSETError('Missing field "{}" in File Details section'.format(name))

        _cdate = details['Creation Date']
        _ctime = details['Creation Time']
        if _cdate == '':
            cdate = _DEFAULT_DATE
        else:
            try:
                cdate = datetime.datetime.strptime(_cdate, '%d/%m/%Y').date()
            except ValueError:
                raise JSETError('Cannot parse {} as a valid date'.format(_cdate))
        details['Creation Date'] = cdate
        if _ctime == '':
            ctime = _DEFAULT_TIME
        else:
            try:
                ctime = datetime.datetime.strptime(_ctime, '%H:%M:%S').time()
            except ValueError:
                raise JSETError('Cannot parse {} as a valid date'.format(_ctime))
        details['Creation Time'] = ctime

        return details

    @classmethod
    def _parse_settings(cls, s: str) -> Dict[str, Union[None, int, float, bool, str]]:
        """Parse the Settings section of a JSET file

        Extracts a dictionary of name: value pairs from the settings section of a JSET file.

        :param s: Contents of the settings section, excluding the section header
        :type s: str
        :return: Dictionary mapping parameter name(s) to typed values
        """
        parsed_lines = [JSET._parse_line(line) for line in s.split('\n') if line]

        return {name: JSET._typify(value) for (name, value) in parsed_lines}

    @classmethod
    def _parse_line(cls, s: str) -> Tuple[str, str]:
        """Parse a line of content from a JSET section

        Extracts the parameter name (everything prior to the colon, excluding trailing whitespace) and parameter value
        (everything following the colon, excluding leading and trailing whitespace).

        :param s: The line to be parsed
        :type s: str
        :return: Tuple of two strings. The first string is the parameter name; the second is the parameter value
        :raise: JSETError if the line cannot be parsed

        :Example:

            >>> _parse_line('Creation Name                     : /path/to/file/.jset')
            ('Creation Name', '/path/to/file.jset')

        """
        match = _LINE_PATTERN.search(s)
        if match is None:
            raise JSETError('Unable to parse file line "{}"'.format(s))

        return match.group('name'), match.group('value')

    @classmethod
    def _parse_jetto_extras(cls, settings: Dict) -> ExtraNamelists:
        """Extract the JETTO extra namelists from the settings

        :settings: The contents of the Settings section of the JSET
        :type settings: dict
        :return: The extra namelist object
        :rtype: ExtraNamelists
        :raise: JSETError if the extra namelists cannot be parsed
        """
        return cls._parse_extras(settings, prefix='')

    @classmethod
    def _parse_sanco_extras(cls, settings: Dict) -> ExtraNamelists:
        """Extract the SANCO extra namelists from the settings

        :settings: The contents of the Settings section of the JSET
        :type settings: dict
        :return: The extra namelist object
        :rtype: ExtraNamelists
        """
        return cls._parse_extras(settings, prefix='Sanco')

    @classmethod
    def _parse_extras(cls, settings: Dict, prefix) -> ExtraNamelists:
        """Extract the select set of extra namelist settings from the JSET settings

        Filters the settings section of the JSET for all settings beginning with '<prefix>OutputExtraNamelist', and
        creates an ExtraNamelists object from them

        :settings: The contents of the Settings section of the JSET
        :type settings: dict
        :prefix: The extra namelist prefix ('' for JETTO, 'Sanco' for SANCO)
        :type prefix: str
        :return: The extra namelist object
        :rtype: ExtraNamelists
        :raise: JSETError if the extra namelists cannot be parsed
        """
        raw_extras = {k: v for k, v in settings.items() if k.startswith(f'{prefix}OutputExtraNamelist')}

        try:
            extras = ExtraNamelists(raw_extras, prefix)
        except ExtraNamelistsError as err:
            raise JSETError(str(err))

        return extras

    @classmethod
    def _remove_extra_namelist_settings(cls, settings: Dict) -> Dict:
        """Remove the extra namelists settings from the Settings section

        Removes all settings whose keys start with 'OutputExtraNamelist' or 'SancoOutputExtraNamelist'.

        :param settings: original contents of the Settings section
        :type settings: dict
        :return: Filtered settings section
        :rtype: dict
        """
        return {k: v for k, v in settings.items() if not (k.startswith('OutputExtraNamelist') or
                                                          k.startswith('SancoOutputExtraNamelist'))}

    @classmethod
    def _typify(cls, s: str) -> Union[None, int, float, bool, str]:
        """Convert a JSET parameter value string into a typed variable

        Empty strings are converted to None, numeric types are converted to integers if possible, or floats if not. The
        strings 'true' and 'false' are converted to the corresponding boolean values. If none of the above apply, the
        string is returned unmodified.

        :param s: JSET parameter value
        :type s: str
        :return: Typed parameter
        :rtype: One of None, int, float, bool or string
        """
        if s == '':
            return None
        elif is_int(s):
            return int(s)
        elif is_float(s):
            return float(s)
        elif is_bool(s):
            return to_bool(s)
        else:
            return s

    @classmethod
    def _detypify(cls, value: Union[None, int, float, bool, str]) -> str:
        """Convert JSET typed parameter value into a string

        Essentially the inverse of _typify. None values are converted to empty strings, ints and floats are
        converted in the standard way using the str() built-in. Booleans are converted into 'true' or 'false'. Strings
        are unmodified.

        :param value: JSET parameter value
        :type value: None, int, float, bool or str
        :return: String corresponding to the parameter
        :rtype: str
        """
        if value is None:
            return ''
        elif isinstance(value, bool):
            return 'true' if value else 'false'
        elif isinstance(value, float):
            return str(value)
        elif isinstance(value, int):
            return str(value)
        elif isinstance(value, datetime.date):
            return value.strftime('%d/%m/%Y')
        elif isinstance(value, datetime.time):
            return value.strftime('%H:%M:%S')
        else:
            return value

    def _set_or_update_item(self, setting: str, value: Union[None, int, float, bool, str]):
        """Set or update the value of a given JSET setting

        Updates the value of a JSET setting, or adds it if it doesn't exist. Differs from the public interface provided
        by ``__setitem__``, which does not allow addition of new items. This internal work-around is necessary to allow
        addition of catalogued file settings which my not exist in older catalogued JSETs

        :param setting: Setting identifier
        :param value: Setting value
        """
        self._settings[setting] = value


class ExtraNamelistsError(Exception):
    """Generic exception used for all errors in the ``ExtraNamelist`` class"""
    pass


class ExtraNamelistsTraits:
    """Helper class for handling extra namelist items

    Decoding and handling of extra namelists requires a large number of constants, each of which is parametrised
    by the required prefix for the collection of extra namelists we are dealing with (either JETTO or SANCO). This
    class simplifies the process of geenrating all of the necessary constants by expressing each constant as an
    attribute of the class. The supported attributes are:

    - prefix: The extra namelist prefix e.g. OutputExtraNamelist
    - select: The prefix for the select flag e.g. OutputExtraNamelist.select
    - rows: The rows prefix e.g. OutputExtraNamelist.selItems.rows
    - columns: The columns prefix e.g. OutputExtraNamelist.selItems.columns
    - cell: The cell prefix e.g.OutputExtraNamelist.selItems.cell
    - extra_namelist_selitem_pattern: Compiled regex matching a cell name e.g.OutputExtraNamelist.selItems.cell[0][0]
    - extra_namelist_header_params: Tuple of the non-cell prefixes
    - validator: Validation schema for the extra namelists dictionary
    """
    def __init__(self, prefix=''):
        """Initialise the traits

        :param prefix: Extra namelists prefix
        :type prefix: str
        :raise:
        """
        self.prefix = f'{prefix}OutputExtraNamelist'
        self.select = f'{self.prefix}.select'
        self.rows = f'{self.prefix}.selItems.rows'
        self.columns = f'{self.prefix}.selItems.columns'
        self.cell = f'{self.prefix}.selItems.cell'

        selitem_regex = fr"""
        ^                                                 # Match start of the string
        {self.cell}\[(?P<row>\d+)\]\[(?P<column>\d+)\]    # Match item name - record row and column
        $                                                 # Match end of string
        """
        self.extra_namelist_selitem_pattern = re.compile(selitem_regex, re.VERBOSE)

        self.extra_namelist_header_params = (self.select, self.columns, self.rows)

        extra_namelist_validation_schema = {
            self.select: {
                'type': 'boolean',
                'empty': False,
                'required': True
            },
            self.columns: {
                'type': 'integer',
                'empty': False,
                'required': True,
                'allowed': [3, 4]
            },
            self.rows: {
                'type': 'integer',
                'empty': False,
                'required': True,
                'min': 0
            }
        }
        self.validator = cerberus.Validator(extra_namelist_validation_schema)
        self.validator.allow_unknown = True


class ExtraNamelistItem:
    """Class representing a single item within the extra namelists section of a JSET

    A single item is the value or values comprising an item with a common namelist identifier e.g. IPRAUX
    """
    def __init__(self, value: Union[int, float, str, bool, List[int], List[float], List[str], List[bool]],
                 index=None, active: Optional[bool] = None):
        """Initialise an extra namelist item

        An item can be a scalar (i.e. have a single value) or a vector, where there are multiple values with different
        (not necessarily contiguous) indices, or an array, where there are multiples values with different (not
        necessarily contiguous) indices. In any case, the value(s) must be numeric (i.e. integers or floats),
        strings or booleans.

        Internally, the contents of an item are represented as a dictionary, where the key is the index of a value
        within the item. A vector or array item can have multiple values, each with its own index. A scalar item has a
        single value, with an index of None.

        An item can optionally have an active status: this corresponds to the "Active" column in the JAMS extra
        namelists tab.

        :param value: Value of the item
        :type value: Int, float, string or bool, or list thereof
        :param index: Index of the item (defaults to None for scalar item)
        :type index: Integer, or None if it is a scalar item
        :param active: Active status of the item
        :type active: Optional[bool]
        :raise: ExtraNamelistsError if the item's index or value are invalid
        """
        if index is None:
            if ExtraNamelistItem._validate_scalar_value(value):
                self._scalar = True
                self._array = False
                self._dict = {index: value}
                self._type = type(value)
            else:
                raise ExtraNamelistsError(f'Invalid value {value} for scalar parameter')
        elif isinstance(index, int):
            if ExtraNamelistItem._validate_vector_index(index):
                self._scalar = False
                self._array = False
                if ExtraNamelistItem._validate_scalar_value(value):
                    self._dict = {index: value}
                    self._type = type(value)
                elif ExtraNamelistItem._validate_vector_value(value):
                    self._dict = {(k + index): v for k, v in enumerate(value)}
                    self._type = type(value[0])
                else:
                    raise ExtraNamelistsError(f'Invalid value {value} for vector parameter')
            else:
                raise ExtraNamelistsError(f'Invalid index {index} for vector parameter')
        else:
            if ExtraNamelistItem._validate_array_index(index):
                self._scalar = False
                self._array = True
                if ExtraNamelistItem._validate_scalar_value(value):
                    self._dict = {index: value}
                    self._type = type(value)
                else:
                    raise ExtraNamelistsError(f'Invalid value {value} for array parameter')
            else:
                raise ExtraNamelistsError(f'Invalid index {index} for array parameter')

        self._active = active

    @property
    def active(self) -> Optional[bool]:
        """Get the item's active status"""
        return self._active

    @active.setter
    def active(self, v: Union[None, True, False]):
        """Set the item's active status"""
        self._active = v

    @staticmethod
    def _validate_array_index(index) -> bool:
        """Check if the index is valid

        Valid indices are pairs of positive integers (for array items).

        :param index: Index to check
        :return: True if the index is valid, otherwise false
        :rtype: bool
        """
        return len(index) == 2 and \
               all(isinstance(i, int) for i in index) and \
               all(i >= 1 for i in index)

    @staticmethod
    def _validate_vector_index(index) -> bool:
        """Check if the index is valid

        Valid indices are positive integers (for vector items).

        :param index: Index to check
        :return: True if the index is valid, otherwise false
        :rtype: bool
        """
        return isinstance(index, int) and index >= 1

    @classmethod
    def _validate_scalar_value(cls, value) -> bool:
        """Check if a scalar item value is valid

        For a scalar item, only a single numeric (int or float), string or boolean value is valid.

        :param value: Value being checked
        :return: True if the value is valid; otherwise False
        :rtype: bool
        """
        return isinstance(value, int) or isinstance(value, float) or isinstance(value, str) or isinstance(value, bool)

    @classmethod
    def _validate_vector_value(cls, value) -> bool:
        """Check if a vector item value is valid

        For a vector item, a value is valid is it is a valid scalar item value, or an iterable thereof. Iterables of
        zero length are not allowed, and all elements of an iterable must be the same type

        :param value: Value being checked
        :return: True if the value is valid; otherwise False
        :rtype: bool
        """
        try:
            iterator = iter(value)
        except TypeError:
            return cls._validate_scalar_value(value)
        else:
            return len(value) > 0 and \
                   all(cls._validate_scalar_value(v) for v in value) and \
                   all(isinstance(v, type(value[0])) for v in value)

    def is_scalar(self):
        """Check if the item is a scalar

        :return: True if the item is a scalar; otherwise False
        :rtype: bool
        """
        return self._scalar

    def is_vector(self):
        """Check is item is a vector

        :return: True if the item is a vector; otherwise False
        :rtype: bool
        """
        return not self.is_scalar() and not self.is_array()

    def is_array(self):
        """Check if the item is an array

        :return: True if the item is an array; otherwise False
        :rtype: bool
        """
        return self._array

    def is_contiguous(self) -> bool:
        """Check if a vector or array item has contiguous indices

        Checks that there are no missing indices in the item. Only applies to vector or array items. Indices are assumed
        to start from 1 for vectors. For arrays, they are assumed to start from (1, 1).

        :return: True if the item is contiguous; false if any indices are missing
        :rtype: bool
        :raise: ExtraNamelistsError if the item is a scalar
        """
        if self.is_scalar():
            raise ExtraNamelistsError('Function "is_contiguous" not applicable to scalar items')

        if self.is_array():
            max_i, max_j = max(i for i, _ in self._dict.keys()), max(j for _, j in self._dict.keys())
            indices = itertools.product(range(1, max_i + 1), range(1, max_j + 1))
        else:
            indices = range(1, len(self._dict) + 1)

        return all(index in self._dict for index in indices)

    def type(self):
        """Return the item's type

        """
        return self._type

    def as_dict(self) -> Dict:
        """Gets a dictionary representation of the item

        For a scalar item, the dictionary representation has a single item with key None. For a vector item, there is
        one key per index. Note that the returned value is a *copy* of the contents of the item, to prevent modification
        of the item itself via this function.

        :return: Dictionary representation of the item
        :rtype: dict
        """
        return dict(self._dict)

    def as_list(self) -> List:
        """Gets a list representation of the item

        For extra namelist items containing a vector, returns a list in which each element appears in order of it index
        in the item. Only applies to vector items which have contiguous indices. Calling this function on any other kind
        of extra namelist item will raise an error

        :return: List representation of item
        :rtype: List
        :raise: ExtraNamelistsError if the item is scalar, array, or if it is not contiguous
        """
        if self.is_scalar() or self.is_array():
            raise ExtraNamelistsError('Function "as_list" not applicable to scalar/array items')

        if not self.is_contiguous():
            raise ExtraNamelistsError('Cannot express vector item with non-contiguous indices as a list')

        return [self._dict[v] for v in range(1, len(self._dict) + 1)]

    def combine(self, other: ExtraNamelistItem):
        """Combine this item's contents with those of another

        Checks to see that both items are indexed (i.e. not scalar) and that there is not overlap between their
        respective indices. If so, then the two dictionaries are combined in the calling item.

        The two items' being combined must have matching values of their active states. If the values don't match, an
        exception is raised. If they do, the combined item will have the same active status as the original items.

        :param other: Item to combine contents from
        :type other: ExtraNamelistItem
        :raise: ExtraNamelistsError if either one of the items is scalar, or if there are overlapping indices in the
                combination, or if the active states of the two items differ
        """
        if self._scalar or other.is_scalar():
            raise ExtraNamelistsError('Cannot combine scalar extra namelist item(s)')

        if self.is_array() and other.is_vector() or self.is_vector() and other.is_array():
            raise ExtraNamelistsError('Cannot combine array and vector extra namelist item(s)')

        if any([index in self._dict for index in other.as_dict()]):
            raise ExtraNamelistsError('Overlap in indices between combined extra namelist items')

        if self._active is not other.active:
            raise ExtraNamelistsError('Active status differs in combined extra namelist items')

        self._dict = {**self._dict, **other.as_dict()}

    def __getitem__(self, index: Union[None, int, Tuple[int]]) -> Union[int, float, bool, str]:
        """Get the value at a particular index

        Only applicable to vector or array items: using this function on a scalar item raises an exception

        :param index: Index of the value
        :type index: int
        :raise: ExtraNamelistsError if the item is scalar, or if the index does not exist
        """
        if index not in self._dict:
            raise ExtraNamelistsError(f'Invalid index {index} for item')

        return self._dict[index]

    def __setitem__(self, index: Union[None, int], value: Union[int, float, bool, str]):
        """Set the value of a particular index

        Sets the value of the item for a particular index. Index can be any positive integer, pair of positive integers,
        or None for scalar items, and can overwrite existing indices. Value can be any of the allowed types, but must be
        of the same type as the item.

        :param index: Index of the value
        :type index: int
        :param value: Value at the index
        :type value: Same as that of the item
        :raise: ExtraNamelistsError if the type of the value does not match the item, or if the index is invalid for
                the item
        """
        if not isinstance(value, self._type):
            raise ExtraNamelistsError(f'Invalid type {type(value)}: expected {self._type}')

        if index is None:
            if not self._scalar:
                raise ExtraNamelistsError(f'Invalid index {index} for scalar parameter')
            else:
                self._dict[index] = value
        else:
            if self._array and ExtraNamelistItem._validate_array_index(index):
                self._dict[index] = value
            elif ExtraNamelistItem._validate_vector_index(index):
                self._dict[index] = value
            else:
                raise ExtraNamelistsError(f'Invalid index {index} for vector/array parameter')

    def __eq__(self, other: ExtraNamelistItem) -> bool:
        """Check if two extra namelist items have the same contents

        :param other: Item to check against
        :type other: _ExtraNamelistItem
        :return: True if the two items have the same contents; otherwise False
        :rtype: bool
        """
        return self._dict == other.as_dict() and self._active is other.active

    def __ne__(self, other: ExtraNamelistItem) -> bool:
        """Check if two extra namelist items do not have the same contents

        :param other: Item to check against
        :type other: _ExtraNamelistItem
        :return: False if the two items have the same contents; otherwise True
        :rtype: bool
        """
        return not self == other


class ExtraNamelists:
    """Class representing the extra namelist items within a JSET"""
    def __init__(self, raw: Dict, prefix=''):
        """Validate the raw extra namelist contents and initialise each item

        :param raw: Contents of the extra namelists section from the JSET dictionary
        :type raw: dict
        :param prefix: Prefix for the extra namelist items ('' for JETTO items, 'Sanco' for SANCO items)
        :type prefix: str
        :raise: ExtraNamelistsError if the validation fails
        """
        traits = ExtraNamelistsTraits(prefix)

        ExtraNamelists._validate(raw, traits)

        self._selected = raw[traits.select]
        if self._selected:
            self._items = ExtraNamelists._parse_items(raw, raw[traits.rows], traits)
        else:
            self._items = {}

        self._raw = raw
        self._prefix = prefix
        self._traits = traits
        self._columns = self._raw[self._traits.columns]

    @property
    def prefix(self) -> str:
        """Return the extra namelists prefix

        :return: The prefix
        :rtype: str
        """
        return self._prefix

    @classmethod
    def _validate(cls, raw: Dict, traits: ExtraNamelistsTraits):
        """Validate the contents of the extra namelists section

        Validation consists of checking that the expected fields are present (e.g. 'select', 'rows', 'columns'), have
        the expected types and values, and that each of the items fields are well formed.

        :param raw: Contents of the extra namelists section from the JSET dictionary
        :type raw: dict
        :param traits: Extra namelist traits
        :type traits: ExtraNamelistsTraits
        :raise: ExtraNamelistsError if any of the validation checks fail
        """
        if not traits.validator.validate(raw):
            raise ExtraNamelistsError(f'Schema validation of extra namelists section failed'
                                      f' (Cerberus feedback : "{traits.validator.errors}")')

        for k in raw:
            if k not in traits.extra_namelist_header_params:
                m = traits.extra_namelist_selitem_pattern.fullmatch(k)
                if not m:
                    raise ExtraNamelistsError(f"Item {k} does not have the expected format")
                if m.group('column') == '0' and not isinstance(raw[k], str):
                    raise ExtraNamelistsError(f"Parameter {m.group('row')} has no name set")
                if m.group('column') == '2' and raw[k] is None:
                    raise ExtraNamelistsError(f"Parameter {m.group('row')} has no value set")
                if m.group('column') == '3' and raw[traits.columns] == 3:
                    raise ExtraNamelistsError(f"Parameter {m.group('row')} has active flag but number of columns is 3")

    @classmethod
    def _parse_items(cls, raw: Dict, nitems: int, traits: ExtraNamelistsTraits) -> Dict:
        """Parse the items in the extra namelists section

        Each item in the extra namelists section is split across three entries in the JSET dict: one entry for the
        namelist field name, one entry for the index (if any), and one entry for the value(s). This function goes
        through the raw JSET dictionary and builds an ``ExtraNamelistItem`` for each item. The number of items to expect
        is provided as an argument to the function.

        If an item appears more than once in the raw dictionary, then the resulting individual extra namelist items
        are combined in the returned dictionary (assuming the two items have disjoint indices).

        :param raw: Contents of the extra namelists section from the JSET dictionary
        :type raw: dict
        :param nitems: Number of items to expect (corresponds to the field 'OutputExtraNamelist.rows' in the JSET)
        :type nitems: int
        :param traits: Extra namelist traits
        :type traits: ExtraNamelistsTraits
        :raise: ExtraNamelistsError if any expected key is not present, or if parsing of the values into an item fails
        """
        items = {}
        for row in range(nitems):
            for column in range(3):
                if f'{traits.cell}[{row}][{column}]' not in raw:
                    raise ExtraNamelistsError("Parameter {} missing column {}".format(row, column))

            name = raw[f'{traits.cell}[{row}][0]']
            index = raw[f'{traits.cell}[{row}][1]']
            value = raw[f'{traits.cell}[{row}][2]']
            active = raw.get(f'{traits.cell}[{row}][3]', None)

            if isinstance(value, str):
                value = ExtraNamelists._parse_string_value(value, index)
            if isinstance(index, str):
                index = ExtraNamelists._parse_string_index(index)

            if name in items:
                items[name].combine(ExtraNamelistItem(value, index, active=active))
            else:
                items[name] = ExtraNamelistItem(value, index, active=active)

        return items

    @classmethod
    def _parse_string_value(cls, s: str, index: Union[None, int]) -> Union[str, List]:
        """Deal with the case where an indexed item has a string value

        JAMS extra namelists items can be plain strings, or vectors of other types (including strings). JAMS allows the
        user to enter a comma-separated list of values for extra namelist items which are indexed. For example, to set
        an array item in a namelist to have the value 1 at index 1 and 2 at index 2, the user can set the index column
        in JAMS to 1, and the value column to '1, 2'. This function takes the string value and splits it into an array
        of values of the appropriate types.

        Conversion proceeds in a similar way to the general manner in which the ``JSET`` class handles type conversion.
        The conversion attempts will be int, then float, then string, then boolean. An additional wrinkle is that JAMS
        encodes boolean values differently in the extra namelist sections of the file, from those in other sections of
        file. In other sections, boolean values are encoded as the strings 'true' and 'false'. In the extra namelist
        sections, they are encoded as the strings 'T' and 'F' (case-insensitive). Plain strings are stripped of their
        leading and trailing quotes (single or double).

        :param s: Raw string
        :type value: str
        :param index: Index of the item
        :type index: None or integer
        :return: Stripped string, or split array of scalar values
        :rtype: String or list
        :raise: ExtraNamelistsError if the string cannot be parsed
        """
        if index is None:
            value = cls._typify(s)
        else:
            split_values = cls._split_string_vector_value(s)
            value = [cls._typify(v) for v in split_values]

        return value

    @classmethod
    def _parse_string_index(cls, s: str) -> Tuple[int, int]:
        """Deal with the case where an indexed item has a string index

        String indices are assumed to be for arrays, where the index consist of a tuple of two integers

        :param s: Raw string
        :type value: str
        :return: Pair of integers
        :rtype: Tuple
        :raise: ExtraNamelistsError if the string cannot be parsed
        """
        try:
            indices = tuple(int(i) for i in s.split(','))
        except ValueError:
            raise ExtraNamelistsError(f'Unable to parse string {s} into array index')

        return indices

    @classmethod
    def _split_string_vector_value(cls, value: str) -> List[str]:
        """Split a string encoding a vector of values

        Splitting is performed based on commas being the delimiter. The individual strings are trimmed of leading and
        trailing whitespace. If the initial string to be split has no comma delimiters, it is returned as the only
        element of the list, with leading and trailing whitespace removed

        :param value: Raw string
        :type value: str
        :return: Split list of strings
        :rtype: List[str]
        """
        return [v.strip() for v in value.split(',')]

    @classmethod
    def _typify(cls, s: str) -> Union[int, float, bool, str]:
        """Convert a string encoding a JSET extra namelists parameter value into a typed variable

        The rules for doing this conversion are complicated, but the following is believed to reproduce how JAMS
        behaves when dealing with extra namelist items encoded as strings. The rules are applied in this order:

        - If the string converts to a numeric value (int or float), it is converted as such
        - If the string starts and ends with single or double quotes, it is treated as a single scalar string value,
          stripped of its quotes
        - If the string is T or F (case-insensitive) then it is the corresponding boolean value

        :param s: Extra namelists parameter value
        :type s: str
        :return: Typed parameter
        :rtype: One of int, float, bool or string
        :raise: ExtraNamelistsError if none of the conversions apply
        """
        if is_int(s):
            return int(s)
        elif is_float(s):
            return float(s)
        elif s.startswith('"') and s.endswith('"'):
            return s.strip('"')
        elif s.startswith("'") and s.endswith("'"):
            return s.strip("'")
        elif s.upper() in ('T', 'F'):
            return {'T': True, 'F': False}[s.upper()]
        else:
            raise ExtraNamelistsError(f'Value type for {s} is not valid')

    @classmethod
    def _detypify(cls, value: Union[int, float, bool, str]) -> Union[int, float, str]:
        """Convert extra namelists typed parameter value into a string

        Essentially the inverse of _typify. Ints and floats are left as they are, as they will be converted by the
        top-level JSET conversion to string. Booleans are converted into 'T' or 'F'. Strings are unmodified, but have
        leading and trailing single quotes applied to them, matching JAMS formatting in the JSET file.

        :param value: Extra namelists parameter value
        :type value: Union[int, float, bool, str]
        :return: String corresponding to the parameter
        :rtype: str
        :raise: ExtraNamelistsError if none of the conversion rules apply to the value
        """
        if isinstance(value, bool):
            return 'T' if value else 'F'
        elif isinstance(value, int) or isinstance(value, float):
            return value
        elif isinstance(value, str):
            return f"'{value}'"
        else:
            raise ExtraNamelistsError(f'Value type for {value} is not valid')

    def __len__(self):
        """Return the number of extra namelist items present

        Immediately after reading in the extra namelists from raw, this function will return the value of the 'rows'
        field in the extra namelists section of the JSET (unless the 'select' field is false, in which case it will
        return zero). If the user adds or removes any item from the extra namelists, this function will return an
        updated value accordingly.

        :return: Number of items
        :rtype: int
        """
        return len(self._items)

    def __getitem__(self, key):
        """Get an extra namelist item

        :param key: Name of the item
        :type key: str
        :raise: ExtraNamelistsError if the item does not exist
        """
        if key not in self._items:
            raise ExtraNamelistsError('Parameter {} does not exist'.format(key))

        return self._items[key]

    def __setitem__(self, key: str, item: ExtraNamelistItem):
        """Add/modify an extra namelist item

        If the item exists, it will simply be overwritten with the new object. If not, it will be added to the internal
        dictionary. An item can only be replaced with another item of the same dimension (scalar or vector) and type
        as the original item.

        Note that if the extra namelist 'select' flag was set to false in the original JSET, the addition of
        a new item will automatically switch it to true.

        :param key: Name of the item
        :type key: str
        :param value: Extra namelist item
        :type item: ExtraNamelistItem
        """
        if key in self._items:
            self._update_existing_item(key, item)
        else:
            self._items[key] = item

        self._selected = True

    def _update_existing_item(self, key: str, item: ExtraNamelistItem):
        """Update an existing extra namelist item

        Checks that the new item has the same type and dimension as the existing item,. If it does, the existing item is
         replaced by the new item.

        :param key: Name of the item
        :type key: str
        :param item: Extra namelist item
        :type item: ExtraNamelistItem
        :raise: ExtraNamelistsError if the new item has a different dimension or type to the existing item
        """
        existing_scalar = self._items[key].is_scalar()
        existing_type = self._items[key].type()

        if item.is_scalar() == existing_scalar and item.type() == existing_type:
            self._items[key] = item
        else:
            raise ExtraNamelistsError(f'Cannot update existing namelist item {key} to different type or dimension')

    def __delitem__(self, key: str):
        """Remove an item from the extra namelists

        :param key: Name of the item
        :type param: str
        :raise: ExtraNamelistsError if the item does not exist
        """
        if key not in self._items:
            raise ExtraNamelistsError('Parameter {} does not exist'.format(key))

        del self._items[key]

    def __contains__(self, key: str) -> bool:
        """Check if an item exists in the extra namelists

        :param key: Name of the item
        :type param: str
        :return: True if the item exists, otherwise false
        :rtype: bool
        """
        if key not in self._items:
            return False

        return True

    def as_jset_settings(self):
        """Export the extra namelists as raw JSET settings

        The extra namelists are initialised from the raw JSET settings, which are expressed as a simple dictionary of
        key-value pairs. This function reverses the process, converting the extra namelists back into a JSET-compatible
        dictionary, with appropriate key values where the cell[][] array has the expected row and column values. An
        important point is that, although this class supports reading in extra namelists which are specified as an array
        of values starting at a certin index, the conversion back splits arrays into individual values, one value per
        index in the item. For example, given the following raw JSET dictionary:

            "OutputExtraNamelist.selItems.cell[0][0]": "ITRDOWNSC",
            "OutputExtraNamelist.selItems.cell[0][1]": 1,
            "OutputExtraNamelist.selItems.cell[0][2]": '4,5',

        The corresponding output would be:

            "OutputExtraNamelist.selItems.cell[0][0]": "ITRDOWNSC",
            "OutputExtraNamelist.selItems.cell[0][1]": 1,
            "OutputExtraNamelist.selItems.cell[0][2]": 4,
            "OutputExtraNamelist.selItems.cell[1][0]": "ITRDOWNSC",
            "OutputExtraNamelist.selItems.cell[1][1]": 2,
            "OutputExtraNamelist.selItems.cell[1][2]": 5,

        Additionally, any array indices (which are expressed as tuples), are converted back into strings.

        :return: Extra namelists section of the JSET settings
        :rtype: dict
        """
        d = {}
        d[self._traits.select] = self._selected
        if any(item.active is not None for item in self._items.values()) or self._columns == 4:
            d[self._traits.columns] = 4
        else:
            d[self._traits.columns] = 3

        row = 0
        for name in self._items:
            item_dict = self._items[name].as_dict()
            for index in item_dict:
                if isinstance(index, tuple):
                    converted_index = ','.join(str(i) for i in index)
                else:
                    converted_index = index

                prefix = f'{self._traits.cell}[{row}]'
                d[f'{prefix}[0]'] = name
                d[f'{prefix}[1]'] = converted_index
                d[f'{prefix}[2]'] = ExtraNamelists._detypify(item_dict[index])
                if self._items[name].active is not None:
                    d[f'{prefix}[3]'] = self._items[name].active
                row += 1

        d[self._traits.rows] = row

        return d
