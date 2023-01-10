import os.path
import os
import re
import subprocess
import tempfile
import shutil
import glob
from jetto_tools.jset import JSET
from jetto_tools.namelist import Namelist
import jetto_tools.lookup
from typing import Dict, Union, List
from pathlib import Path

from .graydata import GrayTemplate

_EXTRA_FILE_PATTERNS = (r'^jetto\.(bnd|ecp?|eqfile|eqrestart|ext?|lhp?|pset|str|sgrid|s?restart|nbip[1-3]?|rfp|fbk2?)$',
                        r'^jetto\.(spec|beamionsource|mhddb|evp|cup|vlp|tep|tip|eqt|eqdsk|cbank|nbicfg|dse)$',
                        r'^jetto_.*\.eqdsk$',
                        r'^ascot\.(endstate.*|h5|accprv|cntl)$',
                        r'^gray(beam)?\.data$',
                        r'^eirene_nbi\.(elemente|neighbors|npco_char)$',
                        r'^(createnl_nominal_ref\.mat|createnl_dyn_out\.mat|createnl_coupling_init\.diag)$',
                        r'^input\.options$',
                        r'^README$',
                        r'^GridSHscalfac\.txt$',
                        r'^TCI_asym\.dat$',
                        r'^imas_jetto_workflow\.cfg$',
                        r'^Ext_HCD_WF_config$')
_EXTRA_FILE_REGEXES = [re.compile(pattern) for pattern in _EXTRA_FILE_PATTERNS]


class TemplateError(Exception):
    """Generic exception used for all errors in the ``template`` module"""
    pass


class Template:
    """Class representing a template for a JETTO run"""
    def __init__(self, jset: JSET, namelist: Namelist, lookup: Dict, sanco_namelist=None,
                 extra_files=[], catalogue_id=None):
        """Initialise a JETTO template

        Validates the template files according to a set of checks.

        :param jset: Template JSET
        :type jset: JSET
        :param namelist: Template JETTO namelist
        :type namelist: Namelist
        :param lookup: Template lookup map
        :type lookup: Dict
        :param sanco_namelist: Template SANCO namelist
        :type sanco_namelist: Namelist
        :param extra_files: Paths to extra (non-core) template files
        :type extra_files: List[str]
        :param catalogue_id: Catalogue identifier (if the template came from the catalogue)
        :type catalogue_id: str
        :raise: TemplateError if any of the checks fail
        """
        try:
            jetto_tools.lookup.validate(lookup)
        except jetto_tools.lookup.ValidationError as err:
            raise TemplateError(str(err))

        if jset.impurities and jset.sanco and sanco_namelist is None:
            raise TemplateError('SANCO configured as impurities source but SANCO namelist file not provided')

        for name, param in lookup.items():
            if Template.is_regular_param(param):
                Template.validate_regular_param(name, param, jset, namelist, sanco_namelist)
            else:
                Template.validate_extra_namelist_param(name, param, jset, namelist, sanco_namelist)

        self._files = Template.transform_extra_files(extra_files)

        self._jset = jset
        self._namelist = namelist
        self._lookup = lookup
        self._sanco_namelist = sanco_namelist
        self._catalogue_id = catalogue_id

    @classmethod
    def transform_extra_files(cls, extra_files: List[str]) -> Dict[str, str]:
        """Transform the extra file list into a dictionary

        Transforms extra file list into a dictionary where keys are the file names and values are the file paths

        :param extra_files: List of extra file paths
        :type extra files: List[str]
        :return: Extra file dictionary
        :rtype: Dict[str, str]
        :raise: TemplateError if any of the files are not recognised as valid extra file names
        """
        d = dict()
        for path in extra_files:
            name = cls.validate_extra_file(path)
            if not name:
                raise TemplateError(f'Invalid extra file {path}')
            d[name] = path

        return d

    @classmethod
    def validate_extra_file(cls, path: str) -> Union[None, str]:
        """Validate an extra file path

        Checks that the file name matches one of the allowed extra file names

        :param path: Path to the extra file
        :type path: str
        :return: File name if it is an allowed extra file; otherwise None
        :rtype: Union[None, str]
        """
        name = os.path.basename(path)
        for regex in _EXTRA_FILE_REGEXES:
            match = regex.fullmatch(name)
            if match:
                return match.group(0)

        return None

    @classmethod
    def is_regular_param(cls, param: Dict) -> bool:
        """Check if a parameter is a regular parameter

        A parameter is regular if its 'jset_id' is not None

        :param param: Parameter specification
        :type param: Dict
        :return: True if the parameter is regular; otherwise false
        :rtype: bool
        """
        return param['jset_id'] is not None

    @classmethod
    def extract_jset_ids(cls, param: Dict) -> List[str]:
        """Extract jset_ids, as they can be zero, one or many per parameter
        
        Returns a tuple with those lists and the dimension

        jset_ids, namelist_ids, fields, dimension = extract_all_fields(param)

        :param param: Parameter specification
        :type param: Dict
        """

        jset_ids = []
        if 'jset_id' in param.keys():
            jset_ids.append(param['jset_id'])
        if 'jset_flex_id' in param.keys():
            jset_ids += param['jset_flex_id']

        return jset_ids

    @classmethod
    def validate_regular_param(cls, name: str, param: Dict, jset, namelist: jetto_tools.namelist.Namelist,
                               sanco_namelist: Union[None, jetto_tools.namelist.Namelist]):
        """Validate a regular parameter

        Assumes that 'jset_id' is not None. Checks that the parameter exists in the general JSET settings (i.e. not in
        one of the extra namelists), and that it exists in one of the JETTO or SANCO namelist files.

        :param name: Parameter name
        :type name: str
        :param param: Parameter specification
        :type param: Dict
        :jset: JSET file
        :type jset: jetto_tools.jset.JSET
        :namelist: JETTO namelist file
        :type namelist: jetto_tools.namelist.Namelist
        :param sanco_namelist: SANCO namelist file
        :type sanco_namelist: Union[None, jetto_tools.namelist.Namelist]
        :raise: TemplateError if any of the checks fail
        """
        jset_ids = Template.extract_jset_ids(param)
        dimension = param['dimension']

        if dimension == 'vector':
            raise TemplateError(f'Vector parameter {name} not supported outside of extra namelists')
        for jset_id in jset_ids:
            if jset_id not in jset:
                raise TemplateError(f'jset_id {jset_id} not found in template JSET')

        if 'nml_id' not in param:
            return

        namelist_id = param['nml_id']['namelist']
        field = param['nml_id']['field']

        if not namelist.exists(namelist_id, field):
            if sanco_namelist is None or not sanco_namelist.exists(namelist_id, field):
                raise TemplateError(f'Parameter {name} not found in template namelist(s)')

    @classmethod
    def validate_extra_namelist_param(cls, name: str, param: Dict, jset, namelist: jetto_tools.namelist.Namelist,
                                      sanco_namelist: Union[None, jetto_tools.namelist.Namelist]):
        """Validate a parameter from one of the JSET extra namelists

        Assumes that 'jset_id' is None. Checks that the parameter exists in one of extra namelists (JETTO or SANCO),
        and that it is also found in the corresponding namelist file

        :param name: Parameter name
        :type name: str
        :param param: Parameter specification
        :type param: Dict
        :jset: JSET file
        :type jset: jetto_tools.jset.JSET
        :namelist: JETTO namelist file
        :type namelist: jetto_tools.namelist.Namelist
        :param sanco_namelist: SANCO namelist file
        :type sanco_namelist: Union[None, jetto_tools.namelist.Namelist]
        :raise: TemplateError if any of the checks fail
        """
        field = param['nml_id']['field']

        if field not in jset.extras and field not in jset.sanco_extras:
            raise TemplateError(f'Extra namelist parameter {name} not found'
                                ' in JETTO/SANCO extra namelists')

        data_type = {'int': int, 'real': float, 'str': str}[param['type']]
        dimension = param['dimension']
        if field in jset.extras:
            cls.validate_extra_namelist_param_details(field, jset.extras, namelist, data_type, 'JETTO')
        else:
            cls.validate_extra_namelist_param_details(field, jset.sanco_extras, sanco_namelist, data_type, 'SANCO')

    @classmethod
    def validate_extra_namelist_param_details(cls, field: str, extras: jetto_tools.jset.ExtraNamelists,
                                              namelist: jetto_tools.namelist.Namelist, data_type, file: str):
        """Validate the details of a  parameter from an extra namelists file

        Checks that:
        - The parameter exists in the appropriate namelist file (JETTO or SANCO)

        :param field: Namelist identifier
        :type name: str
        :param extras: Extra namelists object in the which the parameter exists
        :type extras: jetto_tools.jset.ExtraNamelists
        :param namelist: Namelist file in which the parameter should exist
        :type namelist: jetto_tools.namelist.Namelist
        :param data_type: Expected data type, based on the lookup file
        :type data_type: int or float
        :param file: Namelist in which the parameter exists ('JETTO' or 'SANCO')
        :type file: str
        :raise: TemplateError if any of the checks fail
        """
        if namelist is None or namelist.namelist_lookup(field) is None:
            raise TemplateError(f'{file} extra namelist param {field} not found in {file} namelist file')

    @property
    def jset(self) -> JSET:
        """Get the template's JSET

        :return: The JSET
        :rtype: JSET
        """
        return self._jset

    @property
    def namelist(self) -> Namelist:
        """Get the template's JETTO namelist

        :return: The JETTO namelist
        :rtype: Namelist
        """
        return self._namelist

    @property
    def lookup(self) -> Dict:
        """Get the template's lookup

        :return: The lookup
        :rtype: Dict
        """
        return self._lookup

    @property
    def sanco_namelist(self) -> Union[None, Namelist]:
        """Get the template's SANCO namelist

        :return: The SANCO namelist, or None if the template doesn't have one
        :rtype: Union[None, Namelist]
        """
        return self._sanco_namelist

    @property
    def extra_files(self) -> Dict[str, str]:
        """Get the extra template files

        Extra files are those which may appear in the JETTO template, but are not the core JSET, namelists or lookup
        files. Examples include the EQDSK files (.eqdsk), SGRID (.sgrid) etc. Files are returned as a dictionary, where
        the key is the file name, and the value is the full path to the file (including the name).

        :return: Dictionary of paths to the extra files
        :rtype: Dict[str, str]
        """
        return self._files

    @property
    def gray(self):
        try:
            gray = self._gray
        except AttributeError:
            try:
                path = self._files.get('graybeam.data')
                if not path:
                    raise TemplateError('template does not contain graybeam.data file')

                self._gray = GrayTemplate.parse_file(path)
            except Exception as err:
                # cache so we don't load the file every time
                self._gray = None
                self._gray_error = err

                # reraise exception
                raise

            return self._gray

        # there was an issue loading the data last time, raise the
        # original exception
        if gray is None:
            raise self._gray_error

        return gray

    @property
    def catalogue_id(self) -> bool:
        """Get the catalogue identifier

        Indicates whether or not the template was loaded from the catalogue

        :return: Catalogue id
        :rtype: str
        """
        return self._catalogue_id


def from_files(jset_path: str, jetto_namelist_path: str, lookup_path: str,
               sanco_namelist_path=None, extra_files=[], catalogue_id=None) -> Template:
    """Load a template from individual files

    For each of the provided files (JSET, JETTO namelist, and lookup), this function checks if the file exists, and then
    loads the corresponding ``JSET``, ``Ǹamelist`` and lookup objects. If the path to a SANCO namelist file is supplied,
    the same approach is applied. All of the loaded files are passed to a Template instance, which is then returned.

    If any extra file paths are supplied, they are checked to see if they exist, but the files are not loaded: these
    file paths are then passed directly to the Template instance (converted to absolute paths if necessary).

    Before returning the created template, the ``set_backwards_compatibility`` function is called on the template's
    ``JSET`` object. This is to match the behaviour of JAMS when it loads a JSET file (see
    ``JettoProcessSettings.postReadSettings`` in the JAMS source code).

    :param jset_path: Path to the JSET file
    :type jset_path: str
    :param jetto_namelist_path: Path to the JETTO namelist file
    :type jetto_namelist_path: str
    :param lookup_path: Path to the lookup file
    :type lookup_path: str
    :param sanco_namelist_path: Path to the SANCO namelist file
    :type sanco_namelist_path: str
    :param extra_files: Paths to any extra template files
    :type extra_files: List[str]
    :param catalogue_id: Catalogue identifier (if the files came from the catalogue)
    :type catalogue_id: str
    :return: The template
    :rtype: Template
    :raise: TemplateError if any of the supplied file paths do not exist
    """
    if not os.path.isfile(jset_path):
        raise TemplateError(f'JSET file not found at "{jset_path}"')
    with open(jset_path) as f:
        jset = JSET(f.read())

    if catalogue_id is None and jset.restart:
        # see https://git.ccfe.ac.uk/jintrac/jetto-pythontools/-/merge_requests/68
        # for more explanation
        raise TemplateError(
            'For reasons of provenance please use the catalogue for restarted cases'
        )

    if not os.path.isfile(jetto_namelist_path):
        raise TemplateError(f'JETTO namelist file not found at "{jetto_namelist_path}"')
    with open(jetto_namelist_path) as f:
        jetto_namelist = Namelist(f.read())

    if not os.path.isfile(lookup_path):
        raise TemplateError(f'Lookup file not found at "{lookup_path}"')
    with open(jetto_namelist_path) as f:
        lookup = jetto_tools.lookup.from_file(Path(lookup_path))

    if sanco_namelist_path:
        if not os.path.isfile(sanco_namelist_path):
            raise TemplateError(f'SANCO namelist file not found at "{sanco_namelist_path}"')
        with open(sanco_namelist_path) as f:
            sanco_namelist = Namelist(f.read())
    else:
        sanco_namelist = None

    for file in extra_files:
        if not os.path.isfile(file):
            raise TemplateError(f'Extra file not found at {file}')
    abs_files = [os.path.abspath(file) for file in extra_files]

    t = Template(jset, jetto_namelist, lookup, sanco_namelist, abs_files, catalogue_id=catalogue_id)
    if t.jset.version_as_date is not None:
        t.jset.set_backwards_compatibility()

    return t


def from_directory(path: str, catalogue_id=None) -> Template:
    """Load a template from a directory

    Assumes that the template directory contains at least the mandatory template files (``jetto.jset``, ``jetto.in``
    and ``lookup.json``), and passes their paths to the ``from_files`` function. If a SANCO namelist file
    (``jetto.sin``) exists, its path is also passed to ``from_files``. For any other files in the template directory,
    if they are one of the allowed extra files (see ``/u/sim/cmg/configs/retrieve/jetto`` on the JET cluster file
    system for the full list), the extra file paths are also passed to the ``from_files`` function.

    :param path: Path to the template directory
    :type path: str
    :param catalogue_id: Catalogue identifier (if the directory came from the catalogue)
    :type catalogue_id: str
    :return: The template
    :rtype: Template
    :raise: TemplateError if the directory does not exist, or if any of the mandatory template files do not exist
    """
    if not os.path.isdir(path):
        raise TemplateError(f'Template directory "{path}" not found')

    jset_path = os.path.join(path, 'jetto.jset')
    jetto_namelist_path = os.path.join(path, 'jetto.in')
    lookup_path = os.path.join(path, 'lookup.json')

    sanco_namelist_path = os.path.join(path, 'jetto.sin')
    if not os.path.isfile(sanco_namelist_path):
        sanco_namelist_path = None

    all_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    extra_files = [os.path.join(path, file) for file in all_files
                   if any([regex.match(file) for regex in _EXTRA_FILE_REGEXES])]

    return from_files(jset_path, jetto_namelist_path, lookup_path, sanco_namelist_path,
                      extra_files=extra_files, catalogue_id=catalogue_id)


def from_catalogue(owner: str, machine: str, shot: int, date: str, seq: int, lookup: str,
                   continue_run=False, retrieval_dir='.retrieval') -> Template:
    """Load a template from the catalogue

    Uses the ``retrieve`` script to copy the files from a catalogued JETTO run into ``retrieval_dir``. The
    ``from_directory`` function is then called to create the returned template. Because of the dependence on the
    ``retrieve`` script, this function should only be used in an environment in which the script exists i.e. the JET
    analysis clusters.

    Since the load is from the catalogue, prior to returning the template created by the call to ``from_directory``,
    the function ``set_catalogued_files`` is called on the template's ``JSET``. This configures the JETTO files' sources
    in the JSET as being catalogued. In addition, ``set_advanced_flags`` is called, which applies
    continuation/restart-based changes to the JSET ``AdvancedPanel`` settings.

    Unlike the case in using ``from_directory`` to load a template, the lookup file will generally not be found in the
    catalogue source directory. As a result, the user must supply the path to the lookup file separately, via the
    ``lookup`` parameter, from where it will be copied into the same temporary directory used by the ``retrieve``
    script.

    :param owner: Catalogue owner (e.g. ``sim``)
    :type owner: str
    :param machine: Machine (e.g. ``'jet'``)
    :type machine: str
    :param shot: Shot identifier (e.g. 92398)
    :type shot: int
    :param date: Date identifier (e.g. ``dec1318``)
    :type date: str
    :param seq: Sequence number
    :type seq: int
    :param lookup: Path to template lookup file
    :type lookup: str
    :param continue_run: Flag indicating that the continue switch (``-c``) should be passed to the call to ``retrieve``
    :type continue_run: bool
    :param retrieval_dir: Directory to use to retrieve the catalogued files (defaults to ``.retrieval`` in the cwd)
    :type retrieval_dir: str
    :return: Template loaded from the retrieved catalogue files
    :rtype: Template
    :raise: TemplateError if the retrieve script call fails, or if the catalogue files cannot be loaded
    """
    retrieve_args = [f'-m{machine}', f'-o{owner}', '-Cjetto']

    if continue_run is True:
        retrieve_args.append('-c')

    retrieve_args.extend([f'{shot}', f'{date}', f'{seq}'])

    if not os.path.isdir(retrieval_dir):
        os.mkdir(retrieval_dir)
    for f in glob.glob(os.path.join(retrieval_dir, '*')):
        os.remove(f)

    retrieve_cmd = ['retrieve'] + retrieve_args
    call = subprocess.run(retrieve_cmd, encoding='utf-8', cwd=retrieval_dir, capture_output=True)
    if call.returncode != 0:
        raise TemplateError(f'Call to retrieve script failed '
                            f'(return code: {call.returncode}, stdout: "{call.stdout}", stderr: "{call.stderr}")')

    if not os.path.isfile(lookup):
        raise TemplateError(f'Lookup file not found at path "{lookup}"')
    shutil.copyfile(lookup, os.path.join(retrieval_dir, 'lookup.json'))

    catalogue_id = f'{owner}/jetto/{machine}/{shot}/{date}/seq-{seq}'
    template = from_directory(retrieval_dir, catalogue_id=catalogue_id)

    template.jset.set_catalogued_files(owner, 'jetto', machine, shot, date, seq)
    template.jset.set_restart_flags(continue_run)

    return template
