import pytest
import json
import os.path
import datetime
import copy
from unittest.mock import PropertyMock, patch

import yaml

from jetto_tools.config import RunConfig, RunConfigError, Scan, ScanError
from jetto_tools.jset import JSET, ExtraNamelistItem
from jetto_tools.namelist import Namelist
from jetto_tools.template import Template, TemplateError
from jetto_tools.lookup import to_json
from jetto_tools import __version__


class TestScan:
    """Tests of the Scan class"""

    def test_raises_if_scan_is_not_iterable(self):
        with pytest.raises(ScanError):
            _ = Scan(0)

    def test_raises_if_no_points_in_scan(self):
        with pytest.raises(ScanError):
            _ = Scan([])

    @pytest.mark.parametrize('points', [[1], (1, 2, 3), set(range(10))])
    def test_can_get_length_of_scan(self, points):
        test_scan = Scan(points)

        assert len(test_scan) == len(points)

    def test_can_iterate_through_points(self):
        points = range(10)

        test_scan = Scan(points)

        assert [p for p in test_scan] == [p for p in points]

    def test_can_access_point_by_index(self):
        test_scan = Scan(range(10))

        for i in range(10):
            assert test_scan[i] == i

    def test_raises_if_attempt_to_modify_scan_point(self):
        test_scan = Scan([1])
        with pytest.raises(ScanError):
            test_scan[0] = 0

    def test_raises_if_points_are_not_numeric(self):
        with pytest.raises(ScanError):
            _ = Scan(["foo"])

    def test_can_test_nonidentical_scans_for_equality(self):
        s1 = Scan([0, 1, 2])
        s2 = Scan([0, 1, 2])

        assert s1 == s2

    def test_can_test_nonidentical_scans_for_inequality(self):
        s1 = Scan([0, 1, 2])
        s2 = Scan([0, 1, 3])

        assert s1 != s2


_raw_test_jset = """
!===============================================================================
!                              JETTO SETTINGS FILE
!===============================================================================
*
*File Details
Creation Name                                               : /path/to/jetto.jset
Creation Date                                               : 08/07/2019
Creation Time                                               : 16:43:37
Version                                                     : v060619
*
*Settings
SetUpPanel.exFileName                                       : /path/to/exfile.ex
SetUpPanel.exFilePrvDir                                     : /path/to
SetUpPanel.exFileCatCodeID                                  : jetto
SetUpPanel.exFileCatDateID                                  : dec0417
SetUpPanel.exFileCatMachID                                  : jet
SetUpPanel.exFileCatOwner                                   : fcasson
SetUpPanel.exFileCatSeqNum                                  : 2
SetUpPanel.exFileCatShotID                                  : 92398
SetUpPanel.exFileOldSource                                  : Private
SetUpPanel.exFilePathName                                   : 
SetUpPanel.exFileSource                                     : Private
SetUpPanel.startTime                                        : 100.0
SetUpPanel.endTime                                          : 100.0
SetUpPanel.idsIMASDBShot                                    : 94875
JobProcessingPanel.name                                     : v060619
JobProcessingPanel.numProcessors                            : 2
JobProcessingPanel.runDirNumber                             : testdata
JobProcessingPanel.userid                                   : sim
JobProcessingPanel.wallTime                                 : 2
Panel.ParamName                                             : 0
Panel.EmptyParamName                                        : 
EquilEscoRef.dshEllipticity                                 : 1.5
EquilEscoRefPanel.tvalue.tinterval.numRange                 : 80
EquilEscoRefPanel.tvalue.tinterval.startRange               : 100.0
EquilEscoRefPanel.tvalue.tinterval.endRange                 : 120.0
EquilEscoRefPanel.tvalueOption                              : Interval
EquilibriumPanel.source                                     : ESCO
OutputExtraNamelist.selItems.cell[0][0]                     : BCINTRHON
OutputExtraNamelist.selItems.cell[0][1]                     : 
OutputExtraNamelist.selItems.cell[0][2]                     : 0.7
OutputExtraNamelist.selItems.cell[1][0]                     : IPRAUX
OutputExtraNamelist.selItems.cell[1][1]                     : 
OutputExtraNamelist.selItems.cell[1][2]                     : 2.0
OutputExtraNamelist.selItems.cell[2][0]                     : CURTI
OutputExtraNamelist.selItems.cell[2][1]                     : 
OutputExtraNamelist.selItems.cell[2][2]                     : 0.1
OutputExtraNamelist.selItems.cell[3][0]                     : RCNTREN
OutputExtraNamelist.selItems.cell[3][1]                     : 1 
OutputExtraNamelist.selItems.cell[3][2]                     : 0.1
OutputExtraNamelist.selItems.cell[4][0]                     : RCNTREN
OutputExtraNamelist.selItems.cell[4][1]                     : 2 
OutputExtraNamelist.selItems.cell[4][2]                     : 0.2
OutputExtraNamelist.selItems.columns                        : 3
OutputExtraNamelist.selItems.rows                           : 5
OutputExtraNamelist.select                                  : true
OutputStdPanel.numOfProfileRangeTimes                       : 80
OutputStdPanel.profileFixedTimes[0]                         : 0
OutputStdPanel.profileFixedTimes[1]                         : 1
OutputStdPanel.profileFixedTimes[2]                         : 2
OutputStdPanel.profileFixedTimes[3]                         : 3
OutputStdPanel.profileFixedTimes[4]                         : 4
OutputStdPanel.profileFixedTimes[5]                         : 5
OutputStdPanel.profileFixedTimes[6]                         : 6
OutputStdPanel.profileFixedTimes[7]                         : 7
OutputStdPanel.profileFixedTimes[8]                         : 8
OutputStdPanel.profileFixedTimes[9]                         : 9
OutputStdPanel.profileRangeEnd                              : 120.0
OutputStdPanel.profileRangeStart                            : 100.0
OutputStdPanel.selectProfiles                               : true
SancoOutputExtraNamelist.selItems.cell[0][0]                : FCXMUL
SancoOutputExtraNamelist.selItems.cell[0][1]                : 
SancoOutputExtraNamelist.selItems.cell[0][2]                : 0.0
SancoOutputExtraNamelist.selItems.cell[1][0]                : IFLUS
SancoOutputExtraNamelist.selItems.cell[1][1]                : 
SancoOutputExtraNamelist.selItems.cell[1][2]                : 1
SancoOutputExtraNamelist.selItems.cell[2][0]                : LBLADSS
SancoOutputExtraNamelist.selItems.cell[2][1]                : 1
SancoOutputExtraNamelist.selItems.cell[2][2]                : 6.6
SancoOutputExtraNamelist.selItems.cell[3][0]                : LBLADSS
SancoOutputExtraNamelist.selItems.cell[3][1]                : 2
SancoOutputExtraNamelist.selItems.cell[3][2]                : 7.7
SancoOutputExtraNamelist.selItems.columns                   : 3
SancoOutputExtraNamelist.selItems.rows                      : 4
SancoOutputExtraNamelist.select                             : true
SancoSOLPanel.TemperatureDecayLength                        : 2.0
ImpOptionPanel.select                                       : false
ImpOptionPanel.source                                       : Sanco
AdvancedPanel.catShotID                                     :
AdvancedPanel.catShotID_R                                   :

*
*EOF
"""

_raw_test_namelists = """
================================================================================
                             CODE INPUT NAMELIST FILE
================================================================================

Application                    : JETTO
JAMS Version                   : v060619
Date                           : 08/07/2019
Time                           : 16:43:37
 
JAMS GIT information:-

Current GIT repository         : /home/sim/cmg/jams/v060619/java
Current GIT release tag        : Release-v060619
Current GIT branch             : master
Last commit SHA1-key           : 638c06e07629f5d100da166aac3e2d2da5727631
Repository status              : Clean


--------------------------------------------------------------------------------
 Namelist : NLIST1
--------------------------------------------------------------------------------

 &NLIST1
  BCINTRHON=  0.7      ,
  ELONG    =  1.5      ,
  IRESTR   =  0        ,
  CURTI    =  0.1      ,  0.1      ,
  TBEG     =  100.0      ,
  TMAX     =  100.0      ,
 &END
 
--------------------------------------------------------------------------------
 Namelist : NLIST
--------------------------------------------------------------------------------

 &NLIST
  FIELD_INT=  0      ,
  FIELD_EMPTY=  0      ,
 &END

--------------------------------------------------------------------------------
 Namelist : INESCO
--------------------------------------------------------------------------------

 &INESCO
  IPRAUX=  2.0      ,
  TIMEQU=  100.0      ,  100.0      ,  0.0      ,
  NPULSE=  94875,
 &END

--------------------------------------------------------------------------------
 Namelist : NLIST2
--------------------------------------------------------------------------------
 &NLIST2
  ISYNTHDIAG=  0        ,
  ITOUT    =  1        ,
  KWFRAN   =  0        ,
  KWLH     =  0        ,
  KWMAIN   =  1        ,
  NTINT    =  100      ,
  NTPR     =  78       ,
  TPRINT   =  1.0033445,  1.0133779,  1.0234113,  1.0334449,  1.0434783,
              1.0535117,  1.0635451,  1.0735786,  1.0836121,  1.0936456,
              1.103679 ,  1.1137123,  1.1237458,  1.1337793,  1.1438128,
              1.1538461,  1.1638796,  1.173913 ,  1.1839465,  1.1939799,
 &END

--------------------------------------------------------------------------------
 Namelist : INNBI
--------------------------------------------------------------------------------

 &INNBI
  RCNTREN(1:2)=        0.1,         0.2      ,
  TIMEQU=  100.0      ,  100.0      ,  0.0      ,
 &END
"""

_raw_test_sanco_namelists = """
================================================================================
                             CODE INPUT NAMELIST FILE
================================================================================

Application                    : JETTO
JAMS Version                   : v060619
Date                           : 08/07/2019
Time                           : 16:43:37

JAMS GIT information:-

Current GIT repository         : /home/sim/cmg/jams/v060619/java
Current GIT release tag        : Release-v060619
Current GIT branch             : master
Last commit SHA1-key           : 638c06e07629f5d100da166aac3e2d2da5727631
Repository status              : Clean


--------------------------------------------------------------------------------
 Namelist : JSANC
--------------------------------------------------------------------------------

 &JSANC
  FCXMUL   =  0.0     ,
 &END

--------------------------------------------------------------------------------
 Namelist : KNTROL
--------------------------------------------------------------------------------

 &KNTROL
  IFLUS=  1      ,
 &END

--------------------------------------------------------------------------------
 Namelist : PHYSIC
--------------------------------------------------------------------------------

 &PHYSIC
  TLAM=  2.0      ,
 &END

--------------------------------------------------------------------------------
 Namelist : ADAS
--------------------------------------------------------------------------------

 &ADAS
  LBLADSS=  6     , 7        ,
 &END
"""

_raw_test_lookup = {
    'param': {
        'jset_id': 'Panel.ParamName',
        'nml_id': {
            'namelist': 'NLIST',
            'field': 'FIELD_INT'
        },
        'type': 'int',
        'dimension': 'scalar'
    },
    'bound_ellip': {
        'jset_id': 'EquilEscoRef.dshEllipticity',
        'nml_id': {
            'namelist': 'NLIST1',
            'field': 'ELONG'
        },
        'type': 'real',
        'dimension': 'scalar'
    },
    'bcintrhon': {
        'jset_id': None,
        'nml_id': {
            'namelist': 'NLIST1',
            'field': 'BCINTRHON'
        },
        'type': 'real',
        'dimension': 'scalar'
    },
    'ipraux': {
        'jset_id': None,
        'nml_id': {
            'namelist': 'INESCO',
            'field': 'IPRAUX'
        },
        'type': 'real',
        'dimension': 'scalar'
    },
    'curti': {
        'jset_id': None,
        'nml_id': {
            'namelist': 'NLIST1',
            'field': 'CURTI'
        },
        'type': 'real',
        'dimension': 'scalar'
    },
    'rcntren': {
        'jset_id': None,
        'nml_id': {
            'namelist': 'INNBI',
            'field': 'RCNTREN'
        },
        'type': 'real',
        'dimension': 'vector'
    },
    'shot_in': {
        'jset_id': 'SetUpPanel.idsIMASDBShot',
        'jset_flex_id': [
              'AdvancedPanel.catShotID',
              'AdvancedPanel.catShotID_R'],
        'nml_id': {
              'namelist': 'INESCO',
              'field': 'NPULSE'
        },
        'type': 'int',
        'dimension': 'scalar'
    }
}


@pytest.fixture(scope='function')
def jset():
    return JSET(_raw_test_jset)


@pytest.fixture(scope='function')
def nml():
    return Namelist(_raw_test_namelists)


@pytest.fixture(scope='function')
def sanco_nml():
    return Namelist(_raw_test_sanco_namelists)


@pytest.fixture(scope='function')
def lookup():
    return copy.deepcopy(_raw_test_lookup)


@pytest.fixture()
def lookup_with_sanco():
    sanco_params = {
        'fcxmul': {
            'jset_id': None,
            'nml_id': {
                'namelist': 'JSANC',
                'field': 'FCXMUL'
            },
            'type': 'real',
            'dimension': 'scalar'
        },
        'iflus': {
            'jset_id': None,
            'nml_id': {
                'namelist': 'KNTROL',
                'field': 'IFLUS'
            },
            'type': 'int',
            'dimension': 'scalar'
        },
        'tlam': {
            'jset_id': 'SancoSOLPanel.TemperatureDecayLength',
            'nml_id': {
                'namelist': 'PHYSIC',
                'field': 'TLAM'
            },
            'type': 'real',
            'dimension': 'scalar'
        },
        'lbladss': {
            'jset_id': None,
            'nml_id': {
                'namelist': 'ADAS',
                'field': 'LBLADSS'
            },
            'type': 'real',
            'dimension': 'vector'
        },
    }
    return {**copy.deepcopy(_raw_test_lookup), **sanco_params}


@pytest.fixture
def catalogue_id():
    return 'user/jetto/machine/shot/date/seq-n'


@pytest.fixture(scope='function')
def template(jset, nml, lookup, catalogue_id):
    return Template(jset, nml, lookup, catalogue_id=catalogue_id)


@pytest.fixture()
def sgrid(tmpdir):
    _sgrid = tmpdir.join('jetto.sgrid')
    _sgrid.write('SGRID')

    return _sgrid


@pytest.fixture()
def bnd(tmpdir):
    _bnd = tmpdir.join('jetto.bnd')
    _bnd.write('BND')

    return _bnd


@pytest.fixture()
def eqdsk(tmpdir):
    _eqdsk = tmpdir.join('jetto.eqdsk')
    _eqdsk.write('BND')

    return _eqdsk


@pytest.fixture()
def template_with_extra_files(jset, nml, lookup, sgrid, bnd, eqdsk, tmpdir, catalogue_id):
    return Template(jset, nml, lookup,
                    extra_files=[bnd.strpath, sgrid.strpath, eqdsk.strpath], catalogue_id=catalogue_id)


@pytest.fixture()
def template_with_overriding_exfile(jset, nml, lookup, tmpdir):
    sgrid = tmpdir.join('jetto.sgrid')
    sgrid.write('')

    bnd = tmpdir.join('jetto.bnd')
    bnd.write('')

    _exfile_dir = tmpdir.mkdir('foo')
    _exfile = _exfile_dir.join('jetto.ex')

    return Template(jset, nml, lookup, extra_files=[bnd.strpath, sgrid.strpath, _exfile.strpath])


@pytest.fixture(scope='function')
def exfile(tmpdir):
    f = tmpdir.join('jetto.ex')
    f.write('bar')

    return f


@pytest.fixture(scope='function')
def cataloged_exfile(tmpdir):
    f = tmpdir.mkdir('catalogue').join('jetto.ex')
    f.write('catalogued')

    return f


@pytest.fixture(scope='function')
def config(template, exfile):
    cfg = RunConfig(template)
    cfg.exfile = exfile.strpath

    return cfg


@pytest.fixture(scope='function')
def config_with_extra_files(template_with_extra_files, exfile):
    cfg = RunConfig(template_with_extra_files)
    cfg.exfile = exfile.strpath

    return cfg


@pytest.fixture()
def config_with_sanco(jset, nml, lookup_with_sanco, sanco_nml, exfile):
    jset['ImpOptionPanel.select'] = True

    template = Template(jset, nml, lookup_with_sanco, sanco_nml)

    cfg = RunConfig(template)
    cfg.exfile = exfile.strpath

    return cfg


class TestConfigFiles:
    def test_can_retrieve_exfile(self, config, exfile):
        assert config.exfile == exfile.strpath

    def test_can_set_exfile(self, config):
        config.exfile = '/path/to/other/exfile.ex'

        assert config.exfile == '/path/to/other/exfile.ex'

    def test_exfile_provided_in_extra_files_has_precedence(self, jset, nml, lookup, tmpdir):
        _exfile = tmpdir.join('jetto.ex')
        _exfile.write('')

        _template = Template(jset, nml, lookup, extra_files=[_exfile.strpath])
        config = RunConfig(_template)

        assert config.exfile == _exfile.strpath


class TestConfigLoadModule:
    def test_can_retrieve_binary(self, config):
        assert config.binary == 'v060619'

    def test_can_set_binary(self, config):
        config.binary = 'v010203'

        assert config.binary == 'v010203'

    def test_can_retrieve_userid(self, config):
        assert config.userid == 'sim'

    def test_can_set_userid(self, config):
        config.userid = 'foo'

        assert config.userid == 'foo'


class TestConfigProcessors:
    """Test that we can set and retrieve the number of processors"""
    def test_can_retrieve(self, config):
        assert config.processors == 2

    def test_can_set(self, config):
        config.processors = 4

        assert config.processors == 4

    @pytest.mark.parametrize('processors', [-1, 0])
    def test_raises_if_processors_set_is_invalid_int(self, config, processors):
        with pytest.raises(RunConfigError):
            config.processors = processors

    @pytest.mark.parametrize('processors', ['foo', None])
    def test_raises_if_processors_set_is_invalid_type(self, config, processors):
        with pytest.raises(RunConfigError):
            config.processors = processors


class TestConfigWalltime:
    """Test that we can get the PROMINENCE walltime"""
    def test_can_retrieve(self, config):
        assert config.walltime == 2

    def test_can_set(self, config):
        config.walltime = 3

        assert config.walltime == 3

    def test_raises_if_walltime_invalid_type(self, config):
        with pytest.raises(RunConfigError):
            config.walltime = 'foo'

    def test_raises_if_walltime_invalid_value(self, config):
        with pytest.raises(RunConfigError):
            config.walltime = -1


class TestConfigTimeRange:
    """Test that we can get and retrieve the start and end times"""

    @pytest.fixture(params=['start_time', 'end_time'], ids=['Start', 'End'])
    def time(self, request):
        return request.param

    def test_can_retrieve_time(self, config, time):
        assert getattr(config, time) == 100.0

    def test_can_set_time(self, config, time):
        setattr(config, time, 200.0)

        assert getattr(config, time) == 200.0

    def test_int_time_converted_to_float(self, config, time):
        setattr(config, time, 1)

        assert isinstance(getattr(config, time), float)

    @pytest.mark.parametrize('invalid_time', [-1, 'foo', None], ids=['Negative', 'String', 'None'])
    def test_raises_if_time_invalid(self, config, time, invalid_time):
        with pytest.raises(RunConfigError):
            setattr(config, time, invalid_time)

    @pytest.fixture(params=['esco_timesteps', 'profile_timesteps'], ids=['ESCO', 'Profile'])
    def timesteps(self, request):
        return request.param

    def test_can_retrieve_timesteps(self, config, timesteps):
        assert getattr(config, timesteps) == 80

    def test_can_set_timesteps(self, config, timesteps):
        setattr(config, timesteps, 81)

        assert getattr(config, timesteps) == 81

    @pytest.mark.parametrize('invalid_timestep', [-1, 0, 1.0, 'foo', None],
                             ids=['Negative', 'Zero', 'Float', 'String', None])
    def test_raises_if_esco_timesteps_invalid(self, config, invalid_timestep):
        with pytest.raises(RunConfigError):
            config.esco_timesteps = invalid_timestep

    @pytest.mark.parametrize('invalid_timestep', [-1, 1.0, 'foo', None],
                             ids=['Negative', 'Float', 'String', None])
    def test_raises_if_profile_timesteps_invalid(self, config, invalid_timestep):
        with pytest.raises(RunConfigError):
            config.profile_timesteps = invalid_timestep


class TestConfigParameters:
    """Test that we can get and set the values of parameters in the configuration"""
    def test_raises_if_parameter_does_not_exist(self, config):
        with pytest.raises(RunConfigError):
            _ = config['nonexistent_param']

    def test_gets_expected_value_of_parameter(self, config):
        assert config['param'] == 0

    def test_raises_if_set_parameter_does_not_exist(self, config):
        with pytest.raises(RunConfigError):
            config['nonexistent_param'] = 0

    def test_can_set_parameter_to_new_value(self, config):
        config['param'] = 1

        assert config['param'] == 1

    def test_raises_if_int_is_set_from_incompatible_real(self, config):
        with pytest.raises(RunConfigError):
            config['param'] = 1.5

    def test_can_set_int_from_compatible_real(self, config):
        config['param'] = 2.0

        assert config['param'] == 2

    def test_raises_if_set_int_from_other_type(self, config):
        with pytest.raises(RunConfigError):
            config['param'] = 'string'

    def test_cannot_set_param_to_none(self, config):
        with pytest.raises(RunConfigError):
            config['param'] = None

    def test_cannot_set_param_to_non_numeric_type(self, config):
        with pytest.raises(RunConfigError):
            config['param'] = 'foo'

    def test_can_set_real_param_from_int(self, config):
        config['bound_ellip'] = 1

        assert config['bound_ellip'] == 1.0

    def test_raises_if_set_real_from_other_type(self, config):
        with pytest.raises(RunConfigError):
            config['bound_ellip'] = 'string'

    def test_can_get_value_of_extra_namelist_parameter(self, config):
        assert config['bcintrhon'] == 0.7

    def test_can_set_value_of_extra_namelist_parameter(self, config):
        config['ipraux'] = 2.1

        assert config['ipraux'] == 2.1

    def test_can_get_value_of_extra_namelist_array(self, config):
        assert config['rcntren'] == [0.1, 0.2]

    def test_can_set_value_of_extra_namelist_array(self, config):
        config['rcntren'] = [0.3, 0.4]

        assert config['rcntren'] == [0.3, 0.4]

    def test_can_get_value_of_sanco_extra_namelist_parameter(self, config_with_sanco):
        assert config_with_sanco['iflus'] == 1

    def test_can_set_value_of_sanco_extra_namelist_parameter(self, config_with_sanco):
        config_with_sanco['iflus'] = 2

        assert config_with_sanco['iflus'] == 2

    def test_can_get_value_of_sanco_extra_namelist_array(self, config_with_sanco):
        assert config_with_sanco['lbladss'] == [6.6, 7.7]

    def test_can_set_value_of_extra_namelist_array(self, config_with_sanco):
        config_with_sanco['lbladss'] = [7.7, 8.8]

        assert config_with_sanco['lbladss'] == [7.7, 8.8]

    def test_can_iterate_over_parameters(self, config, lookup):
        assert set(p for p in config) == set(p for p in lookup)

    def test_can_check_if_parameter_exists(self, config):
        assert 'bound_ellip' in config

    def test_can_check_if_parameter_does_not_exist(self, config):
        assert 'foo' not in config

    def test_jset_int_is_converted_to_float_if_required(self, jset, nml, lookup):
        lookup['bound_ellip']['type'] = 'real'
        jset['EquilEscoRef.dshEllipticity'] = 1

        config = RunConfig(Template(jset, nml, lookup))

        assert config['bound_ellip'] == 1.0 and isinstance(config['bound_ellip'], float)

    def test_jset_float_is_converted_to_int_if_required(self, jset, nml, lookup):
        lookup['bound_ellip']['type'] = 'int'
        jset['EquilEscoRef.dshEllipticity'] = 1.0

        config = RunConfig(Template(jset, nml, lookup))

        assert config['bound_ellip'] == 1 and isinstance(config['bound_ellip'], int)

    def test_raises_if_initial_value_cannot_be_converted(self, jset, nml, lookup):
        lookup['bound_ellip']['type'] = 'int'
        jset['EquilEscoRef.dshEllipticity'] = 1.5

        with pytest.raises(RunConfigError):
            _ = RunConfig(Template(jset, nml, lookup))

    def test_raises_if_parameter_is_none(self, jset, nml, lookup):
        jset['EquilEscoRef.dshEllipticity'] = None

        with pytest.raises(RunConfigError):
            _ = RunConfig(Template(jset, nml, lookup))

    def test_raises_if_jetto_parameter_vector_when_scalar_expected(self, jset, nml, lookup):
        lookup['rcntren']['dimension'] = 'scalar'

        with pytest.raises(RunConfigError):
            _ = RunConfig(Template(jset, nml, lookup))

    def test_raises_if_jetto_parameter_scalar_when_vector_expected(self, jset, nml, lookup):
        lookup['bcintrhon']['dimension'] = 'vector'

        with pytest.raises(RunConfigError):
            _ = RunConfig(Template(jset, nml, lookup))

    def test_raises_if_sanco_parameter_vector_when_scalar_expected(self, jset, nml, lookup_with_sanco, sanco_nml):
        lookup_with_sanco['lbladss']['dimension'] = 'scalar'

        with pytest.raises(RunConfigError):
            _ = RunConfig(Template(jset, nml, lookup_with_sanco, sanco_namelist=sanco_nml))

    def test_raises_if_sanco_parameter_scalar_when_vector_expected(self, jset, nml, lookup_with_sanco, sanco_nml):
        lookup_with_sanco['fcxmul']['dimension'] = 'vector'

        with pytest.raises(RunConfigError):
            _ = RunConfig(Template(jset, nml, lookup_with_sanco, sanco_namelist=sanco_nml))

    def test_raises_if_jetto_vector_has_wrong_type(self, jset, nml, lookup):
        lookup['rcntren']['type'] = 'int'

        with pytest.raises(RunConfigError):
            _ = RunConfig(Template(jset, nml, lookup))

    def test_raises_if_sanco_vector_has_wrong_type(self, jset, nml, lookup_with_sanco, sanco_nml):
        lookup_with_sanco['lbladss']['type'] = 'int'

        with pytest.raises(RunConfigError):
            _ = RunConfig(Template(jset, nml, lookup_with_sanco, sanco_namelist=sanco_nml))

    def test_raises_if_set_jetto_vector_to_wrong_type(self, config):
        with pytest.raises(RunConfigError):
            config['rcntren'] = ['foo', 'bar']

    def test_jetto_vector_converted_to_expected_type(self, config):
        config['rcntren'] = [1, 2]

        assert config['rcntren'] == [1.0, 2.0]

    def test_raises_if_set_sanco_vector_to_wrong_type(self, config_with_sanco):
        with pytest.raises(RunConfigError):
            config_with_sanco['lbladss'] = ['foo', 'bar']

    def test_sanco_vector_converted_to_expected_type(self, config_with_sanco):
        config_with_sanco['lbladss'] = [1, 2]

        assert config_with_sanco['lbladss'] == [1.0, 2.0]


class TestConfigSerialisation:
    def serialisation_field(self, config: RunConfig, field: str):
        serialisation = config.serialise()
        decoded_serialisation = json.loads(serialisation)

        return decoded_serialisation[field]

    def test_intial_exfile(self, config, exfile):
        assert self.serialisation_field(config, 'files')['jetto.ex'] == exfile.strpath

    def test_updated_exfile(self, config):
        config.exfile = '/path/to/other/exfile.ex'

        assert self.serialisation_field(config, 'files')['jetto.ex'] == '/path/to/other/exfile.ex'

    def test_extra_files(self, template_with_extra_files):
        _config = RunConfig(template_with_extra_files)

        assert self.serialisation_field(_config, 'files') \
               == {**template_with_extra_files.extra_files, **{'jetto.ex': template_with_extra_files.jset.exfile}}

    def test_extra_files_with_overiding_exfile(self, template_with_overriding_exfile):
        _config = RunConfig(template_with_overriding_exfile)

        assert self.serialisation_field(_config, 'files') == template_with_overriding_exfile.extra_files

    def test_path_is_expanded(self, config):
        config.exfile = './jetto.ex'

        assert self.serialisation_field(config, 'files')['jetto.ex'] == os.path.abspath('./jetto.ex')

    def test_initial_binary(self, config):
        assert self.serialisation_field(config, 'loadmodule')['binary'] == 'v060619'

    def test_updated_binary(self, config):
        config.binary = 'v010203'

        assert self.serialisation_field(config, 'loadmodule')['binary'] == 'v010203'

    def test_initial_userid(self, config):
        assert self.serialisation_field(config, 'loadmodule')['userid'] == 'sim'

    def test_updated_userid(self, config):
        config.userid = 'foo'

        assert self.serialisation_field(config, 'loadmodule')['userid'] == 'foo'

    def test_initial_processors(self, config):
        assert self.serialisation_field(config, 'processors') == 2

    def test_updated_processors(self, config):
        config.processors = 4

        assert self.serialisation_field(config, 'processors') == 4

    def test_initial_walltime(self, config):
        assert self.serialisation_field(config, 'walltime') == 2

    def test_updated_walltime(self, config):
        config.walltime = 4

        assert self.serialisation_field(config, 'walltime') == 4

    @pytest.mark.parametrize('time', ['start_time', 'end_time'], ids=['Start', 'End'])
    def test_time_range(self, config, time):
        setattr(config, time, 75.0)

        assert self.serialisation_field(config, time) == 75.0

    @pytest.mark.parametrize('timesteps', ['esco_timesteps', 'profile_timesteps'], ids=['ESCO', 'Profile'])
    def test_timestep(self, config, timesteps):
        setattr(config, timesteps, 20)

        assert self.serialisation_field(config, timesteps) == 20

    def test_parameters_in_lookup_are_present(self, config):
        assert self.serialisation_field(config, 'parameters') == {'param': 0,
                                                                  'bound_ellip': 1.5,
                                                                  'bcintrhon': 0.7,
                                                                  'ipraux': 2.0,
                                                                  'curti': 0.1,
                                                                  'rcntren': [0.1, 0.2],
                                                                  'shot_in': 94875 }

    def test_parameters_in_lookup_with_sanco_are_present(self, config_with_sanco):
        assert self.serialisation_field(config_with_sanco, 'parameters') == {'param': 0,
                                                                             'bound_ellip': 1.5,
                                                                             'bcintrhon': 0.7,
                                                                             'ipraux': 2.0,
                                                                             'iflus': 1,
                                                                             'fcxmul': 0.0,
                                                                             'tlam': 2.0,
                                                                             'curti': 0.1,
                                                                             'rcntren': [0.1, 0.2],
                                                                             'shot_in': 94875,
                                                                             'lbladss': [6.6, 7.7]}

    def test_updated_parameter(self, config):
        config['param'] = 1

        assert self.serialisation_field(config, 'parameters')['param'] == 1

    def test_int_scan(self, config):
        config['param'] = Scan([0, 1, 2])

        assert self.serialisation_field(config, 'parameters')['param'] == {'__class__': 'Scan',
                                                                           '__value__': [0, 1, 2]}

    def test_real_scan(self, config):
        config['bound_ellip'] = Scan([0.0, 1.1, 2.2])

        assert self.serialisation_field(config, 'parameters')['bound_ellip'] == {'__class__': 'Scan',
                                                                                 '__value__': [0.0, 1.1, 2.2]}

    def test_extra_scan(self, config):
        config['bcintrhon'] = Scan([0.7, 0.75, 0.8, 0.85])

        assert self.serialisation_field(config, 'parameters')['bcintrhon'] == {'__class__': 'Scan',
                                                                               '__value__': [0.7, 0.75, 0.8, 0.85]}

    def test_sanco_scan(self, config_with_sanco):
        config_with_sanco['iflus'] = Scan([0, 1])

        assert self.serialisation_field(config_with_sanco, 'parameters')['iflus'] == {'__class__': 'Scan',
                                                                                      '__value__': [0, 1]}

    def test_multiple_scans(self, config):
        config['bound_ellip'] = Scan([0.0, 1.1, 2.2])
        config['bcintrhon'] = Scan([0.7, 0.75, 0.8, 0.85])

        assert self.serialisation_field(config, 'parameters')['bound_ellip'] \
               == {'__class__': 'Scan', '__value__': [0.0, 1.1, 2.2]} and \
               self.serialisation_field(config, 'parameters')['bcintrhon'] \
               == {'__class__': 'Scan', '__value__': [0.7, 0.75, 0.8, 0.85]}

    def test_coupled_scans_pair(self, config):
        config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]), 'bcintrhon': Scan([0.7, 0.75, 0.8])})

        assert self.serialisation_field(config, 'parameters')['bound_ellip'] == {'__class__': '_CoupledScan',
                                                                                 '__value__': [0.0, 1.1, 2.2],
                                                                                 '__coupled_with__': ['bcintrhon']} \
               and self.serialisation_field(config, 'parameters')['bcintrhon'] == {'__class__': '_CoupledScan',
                                                                                   '__value__': [0.7, 0.75, 0.8],
                                                                                   '__coupled_with__': ['bound_ellip']}

    def test_coupled_scans_triple(self, config):
        config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]),
                                    'bcintrhon': Scan([0.7, 0.75, 0.8]),
                                    'ipraux': Scan([0, 1, 2])})

        serialisation = self.serialisation_field(config, 'parameters')

        assert sorted(['bound_ellip', 'ipraux']) == sorted(serialisation['bcintrhon']['__coupled_with__'])

    def test_scan_readback(self, config):
        config['param'] = Scan([0, 1, 2])
        serialisation_out = config.serialise()

        serialisation_in = json.loads(serialisation_out, object_hook=Scan.from_json)

        param = serialisation_in['parameters']['param']
        assert isinstance(param, Scan) and list(param) == [0, 1, 2]


class TestConfigScan:
    """Test that we can configure scans over suitable parameters"""
    def test_can_scan_over_int_parameter(self, config):
        config['param'] = Scan([0, 1, 2])

    def test_can_scan_over_real_parameter(self, config):
        config['bound_ellip'] = Scan([0.0, 1.1, 2.2])

    def test_can_retrieve_scan(self, config):
        s = Scan(range(10))

        config['param'] = s

        assert config['param'] == s

    def test_raises_if_scan_over_int_param_contains_incompatible_floats(self, config):
        with pytest.raises(RunConfigError):
            config['param'] = Scan([1.1])

    def test_can_scan_real_parameter_over_ints(self, config):
        config['bound_ellip'] = Scan([0, 1, 2])

    def test_scan_values_for_int_param_are_converted(self, config):
        config['param'] = Scan([1.0, 2.0, 3.0])

        assert config['param'] == Scan([1, 2, 3])

    def test_scan_values_for_real_param_are_converted(self, config):
        config['bound_ellip'] = Scan([1, 2, 3])

        assert config['bound_ellip'] == Scan([1.0, 2.0, 3.0])

    def test_scan_dimension_points_limit(self, config):
        with pytest.raises(RunConfigError):
            config['param'] = Scan(range(200))

    def test_scan_dimension_limit(self, config):
        config['param'] = Scan([1, 2])
        config['ipraux'] = Scan([1, 2])
        config['bcintrhon'] = Scan([1, 2])

        with pytest.raises(RunConfigError):
            config['bound_ellip'] = Scan([1, 2])

    def test_scan_total_points_limit(self, config):
        config['param'] = Scan(range(100))

        with pytest.raises(RunConfigError):
            config['bcintrhon'] = Scan(range(6))

    def test_coupled_scan_within_points_limit(self, config):
        config.create_coupled_scan({'ipraux': Scan(range(20)), 'bcintrhon': Scan(range(20))})

        config['param'] = Scan(range(20))

    def test_can_replace_scan_without_triggering_limit(self, config):
        """Regression test to catch the fact that the code wasn't smart enough to realise that a scan was being
        replaced when computing the number of points in the scan"""
        config['bound_ellip'] = Scan(range(100))
        config['ipraux'] = Scan(range(5))

        config['ipraux'] = Scan(range(5))


class TestConfigCoupledScan:
    """Test that we can configure coupled scans over multiple parameters"""

    def test_raises_if_less_than_two_params(self, config):
        with pytest.raises(ScanError):
            config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2])})

    def test_raises_if_value_is_not_scan(self, config):
        with pytest.raises(RunConfigError):
            config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]), 'bcintrhon': [0.7, 0.75, 0.8]})

    def test_raises_if_scans_different_length(self, config):
        with pytest.raises(ScanError):
            config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]),
                                        'bcintrhon': Scan([0.7, 0.75, 0.8, 0.85])})

    def test_raises_if_parameter_does_not_exist_in_lookup(self, config):
        with pytest.raises(RunConfigError):
            config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1]), 'nonexistent_param': Scan([0.7, 0.75])})

    def test_raises_if_parameter_already_in_coupled_scan(self, config):
        config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]), 'bcintrhon': Scan([0.7, 0.75, 0.8])})

        with pytest.raises(RunConfigError):
            config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]), 'ipraux': Scan([0.7, 0.75, 0.8])})

    def test_raises_if_user_sets_coupled_parameter_to_value(self, config):
        config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]), 'bcintrhon': Scan([0.7, 0.75, 0.8])})

        with pytest.raises(RunConfigError):
            config['bound_ellip'] = 0.0

    def test_raises_if_user_sets_coupled_parameter_to_scan(self, config):
        config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]), 'bcintrhon': Scan([0.7, 0.75, 0.8])})

        with pytest.raises(RunConfigError):
            config['bound_ellip'] = Scan([0.0, 1.1, 2.2])


@pytest.fixture(scope='function')
def export_dir(tmpdir):
    dir = tmpdir.mkdir('export')

    return dir


@pytest.fixture(scope='function')
def rundir(export_dir):
    return export_dir.basename


class TestConfigExportTemplateFiles:
    """Test that the expected files are created in the exported _template directory"""

    @pytest.mark.parametrize('file', ['_template/jetto.jset',
                                      '_template/jetto.in',
                                      '_template/lookup.json'
                                      ])
    def test_creates_expected_file_in_template_directory(self, config, export_dir, file):
        path = export_dir.strpath

        config.export(path)

        assert os.path.isfile(os.path.join(path, file))

    def test_does_not_create_sanco_namelist_file_in_template_directory(self, config, export_dir):
        path = export_dir.strpath

        config.export(path)

        assert not os.path.isfile(os.path.join(path, '_template/jetto.sin'))

    def test_creates_sanco_namelist_file_in_template_directory(self, config_with_sanco, export_dir):
        path = export_dir.strpath

        config_with_sanco.export(path)

        assert os.path.isfile(os.path.join(path, '_template/jetto.sin'))

    def test_creates_extra_files_in_template_directory(self, config_with_extra_files, export_dir):
        path = export_dir.strpath

        config_with_extra_files.export(path)

        assert os.path.isfile(os.path.join(path, '_template/jetto.sgrid')) and \
               os.path.isfile(os.path.join(path, '_template/jetto.bnd'))

    def test_template_extra_files_have_expected_contents(self, config_with_extra_files, export_dir):
        path = export_dir.strpath

        config_with_extra_files.export(path)

        with open(os.path.join(path, '_template/jetto.sgrid')) as f:
            expected_sgrid_contents = f.read()

        with open(os.path.join(path, '_template/jetto.bnd')) as f:
            expected_bnd_contents = f.read()

        assert expected_sgrid_contents == 'SGRID' and expected_bnd_contents == 'BND'


class TestConfigExportFiles:
    """Tests that each expected file is in the export directory"""

    def test_creates_export_directory_if_it_does_not_exist(self, config, export_dir):
        path = export_dir.strpath

        export_dir.remove()
        assert os.path.isdir(path) is False
        config.export(path)

        assert os.path.isdir(path)

    def test_creates_export_directory_recursively_if_it_does_not_exist(self, config, tmpdir):
        path = os.path.join(tmpdir.strpath, 'path/to/nested/export/dir')

        config.export(path)

        assert os.path.isdir(path)

    @pytest.mark.parametrize('file', ['jetto.jset',
                                      'jetto.in',
                                      'jetto.ex',
                                      'serialisation.json',
                                      ])
    def test_creates_expected_file_in_export_directory(self, config, export_dir, file):
        path = export_dir.strpath

        config.export(path)

        assert os.path.isfile(os.path.join(path, file))

    def test_does_not_create_sanco_file_in_export_directory_if_disabled(self, config, export_dir):
        path = export_dir.strpath

        config.export(path)

        assert not os.path.isfile(os.path.join(path, 'jetto.sin'))

    def test_creates_sanco_file_in_export_directory_if_enabled(self, config_with_sanco, export_dir):
        path = export_dir.strpath

        config_with_sanco.export(path)

        assert os.path.isfile(os.path.join(path, 'jetto.sin'))

    def test_raises_if_exfile_does_not_exist(self, config, export_dir):
        config.exfile = '/foo/bar'

        with pytest.raises(RunConfigError):
            config.export(export_dir.strpath)

    def test_raises_if_extra_file_does_not_exist(self, template_with_extra_files, exfile, sgrid, export_dir):
        sgrid.remove()

        _config = RunConfig(template_with_extra_files)
        _config.exfile = exfile.strpath

        with pytest.raises(RunConfigError):
            _config.export(export_dir.strpath)

    def test_creates_extra_files(self, template_with_extra_files, exfile, sgrid, bnd, eqdsk, export_dir):
        _config = RunConfig(template_with_extra_files)
        _config.exfile = exfile.strpath

        _config.export(export_dir.strpath)

        assert os.path.isfile(os.path.join(export_dir.strpath, 'jetto.sgrid')) and \
               os.path.isfile(os.path.join(export_dir.strpath, 'jetto.bnd')) and \
               os.path.isfile(os.path.join(export_dir.strpath, 'jetto.eqdsk'))

    def test_export_returns_export_directory(self, config, export_dir):
        ret = config.export(export_dir.strpath)

        assert ret == [os.path.abspath(export_dir.strpath)]


class TestConfigExportFilesContents:
    """Test that the contents of default exported files are as we expect"""

    def test_serialisation(self, config, export_dir):
        path = export_dir.strpath

        config.export(path)

        with open(export_dir.join('serialisation.json'), 'r') as f:
            actual_serialisation = json.loads(f.read())

        expected_serialisation = json.loads(config.serialise())
        expected_serialisation['name'] = 'export'
        expected_serialisation['index'] = 0

    def test_jset(self, config, export_dir):
        path = export_dir.strpath

        with patch('jetto_tools.jset.JSET.__str__') as patched_str:
            patched_str.return_value = 'foo'

            config.export(path)

        with open(export_dir.join('jetto.jset'), 'r') as f:
            assert f.read() == 'foo'

    def test_namelist(self, config, export_dir):
        path = export_dir.strpath

        with patch('jetto_tools.namelist.Namelist.__str__') as patched_str:
            patched_str.return_value = 'foo'

            config.export(path)

        with open(export_dir.join('jetto.in'), 'r') as f:
            assert f.read() == 'foo'

    def test_sanco_namelist(self, config_with_sanco, export_dir):
        path = export_dir.strpath

        with patch('jetto_tools.namelist.Namelist.__str__') as patched_str:
            patched_str.return_value = 'foo'

            config_with_sanco.export(path)

        with open(export_dir.join('jetto.sin'), 'r') as f:
            assert f.read() == 'foo'

    def test_exfile(self, config, export_dir, exfile):
        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.ex'), 'r') as f:
            assert f.read() == exfile.read()

    def test_extra_files(self, template_with_extra_files, exfile, sgrid, bnd, export_dir):
        _config = RunConfig(template_with_extra_files)
        _config.exfile = exfile.strpath

        _config.export(export_dir.strpath)

        with open(os.path.join(export_dir.strpath, 'jetto.sgrid')) as f:
            actual_contents = f.read()

            assert actual_contents == 'SGRID'


class TestConfigExportJSETContents:
    """Test that the exported JSET is updated as expected"""

    def test_name_is_set_to_export_path(self, config, export_dir):
        path = export_dir.strpath
        jset_path = export_dir.join('jetto.jset')

        config.export(path)

        with open(jset_path) as f:
            jset = JSET(f.read())

        assert jset.cname == jset_path.strpath

    @pytest.mark.skip()
    def test_date_is_set_to_current_date(self, config, export_dir):
        """This test could fail if it occurred exactly on the roll-over between days"""
        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset.cdate == datetime.date.today()

    @pytest.mark.skip()
    def test_time_is_set_to_current_time(self, config, export_dir):
        """This test checks for approximate equality of times, to avoid occasional failures at second roll-overs. The
        test could fail if it occurred exactly on the roll-over between days"""
        config.export(export_dir.strpath)

        now = datetime.datetime.now()
        lower_limit = datetime.time(hour=now.hour, minute=now.minute, second=now.second)
        now_plus_1 = now + datetime.timedelta(seconds=1)
        upper_limit = datetime.time(hour=now_plus_1.hour, minute=now_plus_1.minute, second=now_plus_1.second)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset.ctime >= lower_limit and jset.ctime <= upper_limit

    def test_version_is_set_to_jetto_tools_version(self, config, export_dir, jset):
        original_version = jset.version
        path = export_dir.strpath
        jset_path = export_dir.join('jetto.jset')

        config.export(path)

        with open(jset_path) as f:
            new_jset = JSET(f.read())

        assert new_jset.version == ' + '.join([original_version, 'Python API', __version__])

    def test_binary_is_set(self, config, export_dir):
        config.binary = 'v543210'

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset.binary == config.binary

    def test_userid_is_set(self, config, export_dir):
        config.userid = 'foo'

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset.userid == config.userid

    def test_original_exfile_is_set(self, config, export_dir, exfile):
        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['SetUpPanel.exFileName'] == config.exfile and \
               jset['SetUpPanel.exFilePrvDir'] == os.path.dirname(config.exfile) and \
               jset['SetUpPanel.exFileSource'] == 'Private'

    def test_new_exfile_is_set(self, config, export_dir, tmpdir):
        new_exfile = tmpdir.join('myfile.ex')
        new_exfile.write('foo')

        config.exfile = new_exfile.strpath
        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['SetUpPanel.exFileName'] == config.exfile and \
               jset['SetUpPanel.exFilePrvDir'] == os.path.dirname(config.exfile) and \
               jset['SetUpPanel.exFileSource'] == 'Private'

    def test_original_processors_is_set(self, config, export_dir):
        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['JobProcessingPanel.numProcessors'] == config.processors

    @pytest.mark.parametrize('key', ['SetUpPanel.startTime',
                                     'EquilEscoRefPanel.tvalue.tinterval.startRange',
                                     'OutputStdPanel.profileRangeStart'],
                             ids=['Setup', 'ESCO', 'Profiles'])
    def test_start_times_are_set(self, config, export_dir, key):
        config.start_time = 50.0

        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset[key] == 50.0

    @pytest.mark.parametrize('key', ['SetUpPanel.startTime',
                                     'EquilEscoRefPanel.tvalue.tinterval.startRange',
                                     'OutputStdPanel.profileRangeStart'],
                             ids=['Setup', 'ESCO', 'Profiles'])
    def test_start_times_are_not_set(self, config, export_dir, jset, key):
        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            new_jset = JSET(f.read())

        assert jset[key] == new_jset[key]

    @pytest.mark.parametrize('key', ['SetUpPanel.endTime',
                                     'EquilEscoRefPanel.tvalue.tinterval.endRange',
                                     'OutputStdPanel.profileRangeEnd'],
                             ids=['Setup', 'ESCO', 'Profiles'])
    def test_end_times_are_set(self, config, export_dir, key):
        config.end_time = 50.0

        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset[key] == 50.0

    @pytest.mark.parametrize('key', ['SetUpPanel.endTime',
                                     'EquilEscoRefPanel.tvalue.tinterval.endRange',
                                     'OutputStdPanel.profileRangeEnd'],
                             ids=['Setup', 'ESCO', 'Profiles'])
    def test_end_times_are_not_set(self, config, export_dir, jset, key):
        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            new_jset = JSET(f.read())

        assert jset[key] == new_jset[key]

    def test_esco_timesteps_is_set(self, config, export_dir):
        config.esco_timesteps = 15

        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['EquilEscoRefPanel.tvalue.tinterval.numRange'] == 15

    def test_profile_timesteps_is_set(self, config, export_dir):
        config.profile_timesteps = 15

        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['OutputStdPanel.numOfProfileRangeTimes'] == 15

    def test_new_processors_is_set(self, config, export_dir):
        config.processors = 4

        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['JobProcessingPanel.numProcessors'] == config.processors

    def test_original_walltime_is_set(self, config, export_dir):
        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['JobProcessingPanel.wallTime'] == config.walltime

    def test_new_walltime_is_set(self, config, export_dir):
        config.walltime = 4

        config.export((export_dir.strpath))
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['JobProcessingPanel.wallTime'] == config.walltime

    def test_cataloged_exfile_is_left_unchanged(self, jset, nml, lookup, export_dir, cataloged_exfile):
        jset['SetUpPanel.exFileSource'] = 'Cataloged'
        template = Template(jset, nml, lookup)

        with patch('jetto_tools.jset.JSET.exfile', new_callable=PropertyMock) as mock_exfile:
            mock_exfile.return_value = cataloged_exfile.strpath
            config = RunConfig(template)

            config.export(export_dir.strpath)
            with open(export_dir.join('jetto.jset')) as f:
                new_jset = JSET(f.read())

            assert new_jset['SetUpPanel.exFileSource'] == 'Cataloged'

    def test_cataloged_exfile_not_replaced_by_extra_file(self, jset, nml, lookup, export_dir, exfile, cataloged_exfile):
        jset['SetUpPanel.exFileSource'] = 'Cataloged'
        template = Template(jset, nml, lookup, extra_files=[exfile.strpath])

        config = RunConfig(template)
        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            new_jset = JSET(f.read())

        assert new_jset['SetUpPanel.exFileSource'] == 'Cataloged'

    def test_non_extra_parameter_value_is_set(self, config, export_dir):
        config['param'] = 1

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['Panel.ParamName'] == 1

    def test_extra_namelist_scalar_parameter_value_is_set(self, config, export_dir):
        config['bcintrhon'] = 3.14

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset.extras['BCINTRHON'] == ExtraNamelistItem(3.14)

    @pytest.mark.parametrize('active', [None, True, False])
    def test_extra_namelist_parameter_retains_its_active_status(self, config, export_dir, active):
        config._template.jset.extras['BCINTRHON'].active = active
        config['bcintrhon'] = 3.14

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset.extras['BCINTRHON'].active is active

    def test_extra_namelist_vector_parameter_value_is_set(self, config, export_dir):
        config['rcntren'] = [1.1, 2.2]

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset.extras['RCNTREN'] == ExtraNamelistItem([1.1, 2.2], 1)

    def test_rundir_is_set_for_single_point(self, config, export_dir):
        config.export(export_dir.strpath, rundir='foo')
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset.rundir == 'foo'

    @pytest.mark.parametrize('time', ['start_time', 'end_time'])
    @pytest.mark.parametrize('jset_id', [*(f'OutputStdPanel.profileFixedTimes[{i}]' for i in range(10))])
    def test_output_profiles_settings_are_retained(self, config, export_dir, jset, jset_id, time):
        original_value = jset[jset_id]

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            new_jset = JSET(f.read())

        assert new_jset[jset_id] == original_value

    @pytest.mark.parametrize('time', ['start_time', 'end_time'])
    @pytest.mark.parametrize('jset_id', [*(f'OutputStdPanel.profileFixedTimes[{i}]' for i in range(10))])
    def test_output_profiles_settings_are_cleared_if_time_changed(self, config, export_dir, jset_id, time):
        setattr(config, time, getattr(config, time) - 1)

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset[jset_id] is None

    def test_jset_flex_ids_are_set(self, config, export_dir):
        config['shot_in'] = 42

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.jset')) as f:
            jset = JSET(f.read())

        assert jset['SetUpPanel.idsIMASDBShot'] == 42
        assert jset['AdvancedPanel.catShotID'] == 42
        assert jset['AdvancedPanel.catShotID_R'] == 42


class TestConfigExportNamelistContents:
    @pytest.mark.skip()
    def test_date_is_set_to_current_date(self, config, export_dir):
        """This test could fail if it occurred exactly on the roll-over between days"""
        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.date == datetime.date.today()

    @pytest.mark.skip()
    def test_time_is_set_to_current_time(self, config, export_dir):
        """This test checks for approximate equality of times, to avoid occasional failures at second roll-overs. The
        test could fail if it occurred exactly on the roll-over between days"""
        config.export(export_dir.strpath)

        now = datetime.datetime.now()
        lower_limit = datetime.time(hour=now.hour, minute=now.minute, second=now.second)
        now_plus_1 = now + datetime.timedelta(seconds=1)
        upper_limit = datetime.time(hour=now_plus_1.hour, minute=now_plus_1.minute, second=now_plus_1.second)
        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.time >= lower_limit and namelist.time <= upper_limit

    def test_version_is_set_to_jettotools_version(self, config, export_dir):
        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.version == __version__

    @pytest.mark.parametrize('property', ['repo', 'tag', 'branch', 'sha', 'status'])
    def test_git_header_fields_are_set_to_not_applicable(self, config, export_dir, property):
        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert getattr(namelist, property) == 'n/a'

    def test_regular_parameter_value_is_set(self, config, export_dir):
        config['param'] = 1

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('NLIST', 'FIELD_INT') == 1

    def test_array_parameter_value_is_set(self, config, export_dir):
        config['curti'] = 1.0

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('NLIST1', 'CURTI') == [1.0, 1.0]

    @pytest.mark.parametrize('active', [None, True])
    def test_extra_namelist_parameter_value_is_set(self, config, export_dir, active):
        config._template.jset.extras['BCINTRHON'].active = active
        config['bcintrhon'] = 3.14

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('NLIST1', 'BCINTRHON') == 3.14

    def test_extra_namelist_parameter_value_is_not_set_if_inactive(self, config, export_dir):
        config._template.jset.extras['BCINTRHON'].active = False
        original_value = config['bcintrhon']
        config['bcintrhon'] = 3.14

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('NLIST1', 'BCINTRHON') == original_value

    @pytest.mark.parametrize('active', [None, True])
    def test_extra_namelist_parameter_vector_value_is_set(self, config, export_dir, active):
        config._template.jset.extras['RCNTREN'].active = active
        config['rcntren'] = [1.1, 2.2]

        config.export(export_dir.strpath)
        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('INNBI', 'RCNTREN') == [1.1, 2.2]

    def test_sanco_regular_param_is_set(self, config_with_sanco, export_dir):
        config_with_sanco['tlam'] = 2.5

        config_with_sanco.export(export_dir.strpath)
        with open(export_dir.join('jetto.sin')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('PHYSIC', 'TLAM') == 2.5

    @pytest.mark.parametrize('active', [None, True])
    def test_sanco_extra_namelist_param_is_set(self, config_with_sanco, export_dir, active):
        config_with_sanco._template.jset.sanco_extras['FCXMUL'].active = active
        config_with_sanco['fcxmul'] = 1.1

        config_with_sanco.export(export_dir.strpath)
        with open(export_dir.join('jetto.sin')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('JSANC', 'FCXMUL') == 1.1

    def test_sanco_extra_namelist_param_is_not_set_if_inactive(self, config_with_sanco, export_dir  ):
        config_with_sanco._template.jset.sanco_extras['FCXMUL'].active = False
        original_value = config_with_sanco['fcxmul']
        config_with_sanco['fcxmul'] = 1.1

        config_with_sanco.export(export_dir.strpath)
        with open(export_dir.join('jetto.sin')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('JSANC', 'FCXMUL') == original_value

    @pytest.mark.parametrize('restart, irestr', [(True, 1), (False, 0)])
    def test_restart_parameter_has_expected_value(self, jset, nml, lookup, exfile, export_dir, restart, irestr):
        jset.restart = restart
        template_ = Template(jset, nml, lookup)
        config_ = RunConfig(template_)
        config_.exfile = exfile.strpath

        config_.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST1', 'IRESTR') == irestr

    @pytest.mark.parametrize('property, field', [('start_time', 'TBEG'), ('end_time', 'TMAX')], ids=['Start', 'End'])
    def test_time_range_is_set(self, config, export_dir, property, field):
        setattr(config, property, 10.0)

        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST1', field) == 10.0

    @pytest.mark.parametrize('start, end, timesteps, expected',
                             [(0.0, 1.0, 3, [0.0, 1.0, 0.5]),
                              (0.0, 1.0, 2, [0.0, 1.0, 1.0])],
                             ids=['0', '1'])
    def test_esco_output_profile_time_range_is_set(self, config, export_dir, start, end, timesteps, expected):
        config.start_time = start
        config.end_time = end
        config.esco_timesteps = timesteps

        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('INESCO', 'TIMEQU') == expected

    def test_exception_raised_if_esco_time_range_is_discrete(self, template, exfile, export_dir):
        template.jset['EquilEscoRefPanel.tvalueOption'] = 'Discrete'
        config = RunConfig(template)
        config.exfile = exfile.strpath

        with pytest.raises(RunConfigError):
            config.export(export_dir.strpath)

    def test_no_change_applied_if_profiles_not_selected(self, template, exfile, export_dir):
        template.jset['OutputStdPanel.selectProfiles'] = False
        config = RunConfig(template)
        config.exfile = exfile.strpath
        original_tprint = template.namelist.get_field('NLIST2', 'TPRINT')

        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST2', 'TPRINT') == original_tprint

    def test_ntpr_set_to_zero_if_profiles_not_selected(self, template, exfile, export_dir):
        template.jset['OutputStdPanel.selectProfiles'] = False
        config = RunConfig(template)
        config.exfile = exfile.strpath
        original_tprint = template.namelist.get_field('NLIST2', 'TPRINT')

        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST2', 'NTPR') == 0

    @pytest.mark.parametrize(
        'start, end, timesteps, expected', [
            # (0.0, 1.0, 2, []), # currently fails in f90nml/namelist.py
            (0.0, 1.0, 3, [0.5]),
            (0.0, 1.0, 5, [0.25, 0.5, 0.75]),
            (0.0, 1.0, 6, [0.2, 0.4, 0.6, 0.8]),
        ], ids=['3', '5', '6'])
    def test_profile_output_time_range_is_set(self, config, export_dir, start, end, timesteps, expected):
        config.start_time = start
        config.end_time = end
        config.profile_timesteps = timesteps

        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('NLIST2', 'NTPR') == len(expected)
        assert namelist.get_array('NLIST2', 'TPRINT') == pytest.approx(expected)

    def test_esco_timestep_width_set_to_default_value_if_1_timestep(self, config, export_dir):
        config.esco_timesteps = 1

        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())
        interval = namelist.get_field('INESCO', 'TIMEQU')[2]
        assert isinstance(interval, float) and interval == 1.0e30

    def test_output_profile_times_unchanged(self, config, nml, export_dir):
        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            new_nml = Namelist(f.read())

        assert new_nml.get_field('NLIST2', 'NTPR') == nml.get_field('NLIST2', 'NTPR')
        assert new_nml.get_array('NLIST2', 'TPRINT') == nml.get_field('NLIST2', 'TPRINT')

    def test_can_export_with_non_esco_equilibrium(self, template, export_dir, exfile):
        template.jset['EquilibriumPanel.source'] = 'CBANK'
        # Note that f90nml has inconsistent support for case-insensitivity
        # Getting an item is case-insensitive; deletion of an item is not. This behaviour has varied
        # between f90nml versions (deletion is case-insensitive in 1.2 and 1.4, but not in 1.3)
        del template.namelist._namelists['inesco']['timequ']
        local_config = RunConfig(template)
        local_config.exfile = exfile.strpath

        local_config.export(export_dir.strpath)

    def test_namelist_is_identical_if_unmodified(self, config, export_dir, nml):
        config.export(export_dir.strpath)

        with open(export_dir.join('jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist == nml


class TestConfigExportTemplateContents:
    """Test that the original template files are written out on export"""

    def test_lookup(self, config, export_dir, lookup):
        config.export(export_dir.strpath)

        with open(export_dir.join('_template/lookup.json')) as f:
            exported_lookup = json.loads(f.read())

        assert exported_lookup == lookup

    @pytest.mark.skip
    def test_jset(self, config, export_dir, jset):
        """Need rigorous notion of comparing JSETs to implement this test"""
        original_jset = copy.deepcopy(jset)

        config.export(export_dir.strpath)

        with open(export_dir.join('_template/jetto.jset')) as f:
            exported_jset = JSET(f.read())

        assert original_jset.__eq__(exported_jset)

    @pytest.mark.skip
    def test_namelist(self, config, export_dir, nml):
        """Need rigorous notion of comparing namelists to implement this test"""
        pass


class TestConfigExportLabels:
    @pytest.fixture
    def rundir(self, export_dir):
        return export_dir.basename

    def test_label_file_is_created(self, config, export_dir, rundir):
        config.export(export_dir.strpath, rundir)

        assert os.path.isfile(export_dir / 'labels.yaml')

    def test_scan_label_is_rundir(self, config, export_dir, rundir):
        config.export(export_dir.strpath, rundir)

        with open(export_dir / 'labels.yaml') as f:
            labels = yaml.safe_load(f)

        assert labels['scan-label'] == rundir

    @pytest.mark.skip
    def test_scan_label_blank_if_no_rundir(self, config, export_dir):
        config.export(export_dir.strpath)

        with open(export_dir / 'labels.yaml') as f:
            labels = yaml.safe_load(f)

        assert labels['scan-label'] == ''

    def test_point_index_is_zero(self, config, export_dir, rundir):
        config.export(export_dir.strpath, rundir)

        with open(export_dir / 'labels.yaml') as f:
            labels = yaml.safe_load(f)

        assert labels['point-index'] == 0

    def test_catalogue_id_is_set(self, config, export_dir, rundir, catalogue_id):
        config.export(export_dir.strpath, rundir)

        with open(export_dir / 'labels.yaml') as f:
            labels = yaml.safe_load(f)

        assert labels['template'] == catalogue_id


class TestConfigExportFiles1DScan:
    """Test that a 1D scan results in the files we expect"""

    @pytest.fixture()
    def scan_config_1d(self, config_with_extra_files):
        config_with_extra_files['param'] = Scan(range(3))

        return config_with_extra_files

    @pytest.fixture(params=range(3))
    def point(self, request, export_dir):
        idx = request.param
        return idx, export_dir / f'point_{idx:03d}'

    def test_point_directories_are_created(self, scan_config_1d, export_dir, point):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path)

        assert all([os.path.isdir(os.path.join(path, 'point_{:03d}'.format(i))) for i in range(3)])

    def test_export_returns_point_directories(self, scan_config_1d, export_dir):
        ret = scan_config_1d.export(export_dir.strpath)

        assert ret == [os.path.abspath(export_dir.join('point_{:03d}'.format(i))) for i in range(3)]

    def test_point_directories_are_used_if_they_already_exist(self, scan_config_1d, export_dir, point):
        idx, point_dir = point
        path = export_dir.strpath

        export_dir.mkdir('point_000')
        export_dir.mkdir('point_001')
        export_dir.mkdir('point_002')

        scan_config_1d.export(path)

    def test_top_level_serialisation_is_created_in_export_directory(self, scan_config_1d, export_dir):
        path = export_dir.strpath

        scan_config_1d.export(path)

        assert os.path.isfile(os.path.join(path, 'serialisation.json'))

    def test_top_level_serialisation_has_expected_contents(self, scan_config_1d, export_dir):
        path = export_dir.strpath

        scan_config_1d.export(path)

        with open(os.path.join(path, 'serialisation.json')) as f:
            assert f.read() == scan_config_1d.serialise()

    def test_top_level_labels_is_created_in_export_directory(self, scan_config_1d, export_dir):
        path = export_dir.strpath

        scan_config_1d.export(path)

        assert os.path.isfile(os.path.join(path, 'labels.yaml'))

    def test_top_level_labels_has_expected_contents(self, scan_config_1d, export_dir, rundir, template):
        path = export_dir.strpath

        scan_config_1d.export(path, rundir)
        with open(export_dir / 'labels.yaml') as f:
            labels = yaml.safe_load(f)

        assert labels == {'scan-label': export_dir.basename, 'template': template.catalogue_id}

    @pytest.mark.parametrize('file', ['jetto.jset',
                                      'jetto.in',
                                      'jetto.ex',
                                      'serialisation.json',
                                      'jetto.bnd',
                                      'jetto.sgrid'])
    def test_point_directory_contains_expected_files(self, scan_config_1d, export_dir, point, file):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path)

        assert os.path.isfile(os.path.join(point_dir, file))

    def test_point_directory_contains_template_dir(self, scan_config_1d, export_dir, point):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path)

        assert os.path.isdir(os.path.join(point_dir, '_template'))

    def test_point_template_is_symlink_to_scan_template(self, scan_config_1d, export_dir, point):
        idx, point_dir = point
        path = export_dir.strpath
        real_template_path = os.path.join(export_dir.strpath, '_template')
        sym_template_path = os.path.join(point_dir, '_template')

        scan_config_1d.export(path)

        assert os.path.realpath(sym_template_path) == real_template_path

    def test_point_jset_contains_expected_value(self, scan_config_1d, export_dir, point):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset['Panel.ParamName'] == idx

    def test_point_jset_contains_expected_rundir_value(self, scan_config_1d, export_dir, point):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path, rundir='foo')

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset.rundir == os.path.join('foo', os.path.relpath(point_dir, path))

    def test_point_namelist_contains_expected_value(self, scan_config_1d, export_dir, point):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST', 'FIELD_INT') == idx

    def test_point_serialisation_contains_expected_contents(self, scan_config_1d, export_dir, point):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path)

        with open(os.path.join(point_dir, 'serialisation.json')) as f:
            actual_serialisation = json.loads(f.read())
        expected_serialisation = json.loads(scan_config_1d.serialise())
        expected_serialisation['name'] = 'export'
        expected_serialisation['index'] = idx
        expected_serialisation['parameters']['param'] = idx

        assert expected_serialisation == actual_serialisation

    def test_point_labels_contains_expected_contents(self, scan_config_1d, export_dir, point, rundir, template):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path)

        with open(os.path.join(point_dir, 'labels.yaml')) as f:
            labels = yaml.safe_load(f)

        assert labels == {'scan-label': rundir,
                          'point-index': idx,
                          'template': template.catalogue_id,
                          'scan-param-param': idx}

    def test_point_extra_files_contain_expected_contents(self, scan_config_1d, export_dir, point,
                                                         sgrid, bnd, exfile):
        idx, point_dir = point
        path = export_dir.strpath

        scan_config_1d.export(path)

        with open(os.path.join(point_dir, 'jetto.sgrid')) as f:
            actual_sgrid_contents = f.read()
        with open(sgrid.strpath) as f:
            expected_sgrid_contents = f.read()

        with open(os.path.join(point_dir, 'jetto.bnd')) as f:
            actual_bnd_contents = f.read()
        with open(bnd.strpath) as f:
            expected_bnd_contents = f.read()

        with open(os.path.join(point_dir, 'jetto.ex')) as f:
            actual_ex_contents = f.read()
        with open(exfile.strpath) as f:
            expected_ex_contents = f.read()

        assert actual_sgrid_contents == expected_sgrid_contents and \
               actual_bnd_contents == expected_bnd_contents and \
               actual_ex_contents == expected_ex_contents

    @pytest.fixture()
    def scan_1d_over_extra_namelist(self, config):
        config['bcintrhon'] = Scan([1.1, 2.2, 3.3])

        return config

    @pytest.fixture(params=enumerate([1.1, 2.2, 3.3]))
    def extra_point(self, request, export_dir):
        idx = request.param[0]
        return idx, request.param[1], export_dir / f'point_{idx:03d}'

    def test_point_jset_contains_expected_value_extra_namelist(self, scan_1d_over_extra_namelist, export_dir,
                                                               extra_point):
        idx, p, point_dir = extra_point
        path = export_dir.strpath

        scan_1d_over_extra_namelist.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset.extras['BCINTRHON'].as_dict() == {None: p}

    def test_point_namelist_contains_expected_value_extra_namelist(self, scan_1d_over_extra_namelist, export_dir,
                                                                   extra_point):
        idx, p, point_dir = extra_point
        path = export_dir.strpath

        scan_1d_over_extra_namelist.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('NLIST1', 'BCINTRHON') == p

    @pytest.fixture()
    def scan_1d_over_extra_namelist_vector(self, config):
        config['rcntren'] = Scan([[1.1, 2.2], [3.3, 4.4]])

        return config

    @pytest.fixture(params=enumerate([[1.1, 2.2], [3.3, 4.4]]))
    def extra_namelist_vector_point(self, request, export_dir):
        idx = request.param[0]
        return idx, request.param[1], export_dir / f'point_{idx:03d}'

    def test_point_jset_contains_expected_value_extra_namelist_vector(self, scan_1d_over_extra_namelist_vector,
                                                                      export_dir, extra_namelist_vector_point):
        idx, p, point_dir = extra_namelist_vector_point
        path = export_dir.strpath

        scan_1d_over_extra_namelist_vector.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset.extras['RCNTREN'].as_list() == p

    def test_point_namelist_contains_expected_value_extra_namelist_vector(self, scan_1d_over_extra_namelist_vector,
                                                                          export_dir, extra_namelist_vector_point):
        idx, p, point_dir = extra_namelist_vector_point
        path = export_dir.strpath

        scan_1d_over_extra_namelist_vector.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())

        assert namelist.get_field('INNBI', 'RCNTREN') == p


class TestConfigExportFiles2DScan:
    """Test that a 2-dimensional scan results in the files we expect"""

    @pytest.fixture()
    def scan_config_2d(self, config):
        config['param'] = Scan([0, 1])
        config['bcintrhon'] = Scan([1.1, 2.2])

        return config

    @pytest.fixture(params=[(i, 'point_{:03d}'.format(i)) for i in range(4)])
    def point(self, request, export_dir):
        return request.param[0], os.path.join(export_dir.strpath, request.param[1])

    def test_point_directories_are_created(self, scan_config_2d, export_dir):
        path = export_dir.strpath

        scan_config_2d.export(path)

        assert all([os.path.isdir(os.path.join(path, 'point_{:03d}'.format(i))) for i in range(4)])

    def test_export_returns_point_directories(self, scan_config_2d, export_dir):
        ret = scan_config_2d.export(export_dir.strpath)

        assert ret == [os.path.abspath(export_dir.join('point_{:03d}'.format(i))) for i in range(4)]

    def test_top_level_serialisation_is_created_in_export_directory(self, scan_config_2d, export_dir):
        path = export_dir.strpath

        scan_config_2d.export(path)

        assert os.path.isfile(os.path.join(path, 'serialisation.json'))

    def test_top_level_serialisation_has_expected_contents(self, scan_config_2d, export_dir):
        path = export_dir.strpath

        scan_config_2d.export(path)

        with open(os.path.join(path, 'serialisation.json')) as f:
            assert f.read() == scan_config_2d.serialise()

    def test_top_level_labels_is_created_in_export_directory(self, scan_config_2d, export_dir):
        path = export_dir.strpath

        scan_config_2d.export(path)

        assert os.path.isfile(os.path.join(path, 'labels.yaml'))

    def test_top_level_labels_has_expected_contents(self, scan_config_2d, export_dir, rundir, template):
        path = export_dir.strpath

        scan_config_2d.export(path, rundir)
        with open(export_dir / 'labels.yaml') as f:
            labels = yaml.safe_load(f)

        assert labels == {'scan-label': export_dir.basename, 'template': template.catalogue_id}

    @pytest.fixture(params=enumerate([(0, 1.1), (0, 2.2), (1, 1.1), (1, 2.2)]))
    def nd_point(self, request, export_dir):
        idx = request.param[0]
        params = request.param[1]
        return idx, params, export_dir / f'point_{idx:03d}'

    @pytest.mark.parametrize('file', ['jetto.jset',
                                      'jetto.in',
                                      'jetto.ex',
                                      'serialisation.json'])
    def test_point_directory_contains_expected_files(self, scan_config_2d, export_dir, nd_point, file):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_2d.export(path)

        assert os.path.isfile(os.path.join(point_dir, file))

    def test_point_jset_contains_expected_value(self, scan_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_2d.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset['Panel.ParamName'] == p[0] and jset.extras['BCINTRHON'].as_dict() == {None: p[1]}

    def test_point_namelist_contains_expected_value(self, scan_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_2d.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST', 'FIELD_INT') == p[0] and namelist.get_field('NLIST1', 'BCINTRHON') == p[1]

    def test_point_serialisation_contains_expected_contents(self, scan_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_2d.export(path)

        with open(os.path.join(point_dir, 'serialisation.json')) as f:
            actual_serialisation = json.loads(f.read())
        expected_serialisation = json.loads(scan_config_2d.serialise())
        expected_serialisation['name'] = 'export'
        expected_serialisation['index'] = idx
        expected_serialisation['parameters']['param'] = p[0]
        expected_serialisation['parameters']['bcintrhon'] = p[1]

        assert expected_serialisation == actual_serialisation

    def test_point_labels_contains_expected_contents(self, scan_config_2d, export_dir, nd_point, rundir, template):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_2d.export(path)

        with open(os.path.join(point_dir, 'labels.yaml')) as f:
            labels = yaml.safe_load(f)

        assert labels == {'scan-label': rundir,
                          'point-index': idx,
                          'template': template.catalogue_id,
                          'scan-param-param': p[0],
                          'scan-param-bcintrhon': p[1]}


class TestConfigExportFiles3DScan:
    """Test that a 3-dimensional scan results in the files we expect"""

    @pytest.fixture()
    def scan_config_3d(self, config_with_sanco):
        config_with_sanco['param'] = Scan([0, 1])
        config_with_sanco['bcintrhon'] = Scan([1.1, 2.2])
        config_with_sanco['fcxmul'] = Scan([3.3, 4.4])

        return config_with_sanco

    @pytest.fixture(params=[(i, 'point_{:03d}'.format(i)) for i in range(8)])
    def point(self, request, export_dir):
        return request.param[0], os.path.join(export_dir.strpath, request.param[1])

    def test_point_directories_are_created(self, scan_config_3d, export_dir):
        path = export_dir.strpath

        scan_config_3d.export(path)

        assert all([os.path.isdir(os.path.join(path, 'point_{:03d}'.format(i))) for i in range(8)])

    def test_export_returns_point_directories(self, scan_config_3d, export_dir):
        ret = scan_config_3d.export(export_dir.strpath)

        assert ret == [os.path.abspath(export_dir.join('point_{:03d}'.format(i))) for i in range(8)]

    def test_top_level_serialisation_is_created_in_export_directory(self, scan_config_3d, export_dir):
        path = export_dir.strpath

        scan_config_3d.export(path)

        assert os.path.isfile(os.path.join(path, 'serialisation.json'))

    def test_top_level_serialisation_has_expected_contents(self, scan_config_3d, export_dir):
        path = export_dir.strpath

        scan_config_3d.export(path)

        with open(os.path.join(path, 'serialisation.json')) as f:
            assert f.read() == scan_config_3d.serialise()

    @pytest.fixture(params=enumerate([
        (0, 1.1, 3.3), (0, 1.1, 4.4), (0, 2.2, 3.3), (0, 2.2, 4.4),
        (1, 1.1, 3.3), (1, 1.1, 4.4), (1, 2.2, 3.3), (1, 2.2, 4.4),
    ]))
    def nd_point(self, request, export_dir):
        idx = request.param[0]
        params = request.param[1]
        return idx, params, export_dir / f'point_{idx:03d}'

    @pytest.mark.parametrize('file', ['jetto.jset',
                                      'jetto.in',
                                      'jetto.sin',
                                      'jetto.ex',
                                      'serialisation.json'])
    def test_point_directory_contains_expected_files(self, scan_config_3d, export_dir, nd_point, file):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_3d.export(path)

        assert os.path.isfile(os.path.join(point_dir, file))

    def test_point_jset_contains_expected_value(self, scan_config_3d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_3d.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset['Panel.ParamName'] == p[0] and \
               jset.extras['BCINTRHON'].as_dict() == {None: p[1]} and \
               jset.sanco_extras['FCXMUL'].as_dict() == {None: p[2]}

    def test_point_namelist_contains_expected_value(self, scan_config_3d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_3d.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())
        with open(os.path.join(point_dir, 'jetto.sin')) as f:
            sanco_namelist = Namelist(f.read())

        assert namelist.get_field('NLIST', 'FIELD_INT') == p[0] and \
               namelist.get_field('NLIST1', 'BCINTRHON') == p[1] and \
               sanco_namelist.get_field('JSANC', 'FCXMUL') == p[2]

    def test_point_serialisation_contains_expected_contents(self, scan_config_3d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        scan_config_3d.export(path)

        with open(os.path.join(point_dir, 'serialisation.json')) as f:
            actual_serialisation = json.loads(f.read())
        expected_serialisation = json.loads(scan_config_3d.serialise())
        expected_serialisation['name'] = 'export'
        expected_serialisation['index'] = idx
        expected_serialisation['parameters']['param'] = p[0]
        expected_serialisation['parameters']['bcintrhon'] = p[1]
        expected_serialisation['parameters']['fcxmul'] = p[2]

        assert expected_serialisation == actual_serialisation


class TestConfigExportFilesCoupledScanOnly1D:
    @pytest.fixture()
    def coupled_scan_only_config_1d(self, config):
        config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]), 'bcintrhon': Scan([0.7, 0.75, 0.8])})
        return config

    @pytest.fixture(params=[(i, 'point_{:03d}'.format(i)) for i in range(3)])
    def point(self, request, export_dir):
        return request.param[0], os.path.join(export_dir.strpath, request.param[1])

    def test_point_directories_are_created(self, coupled_scan_only_config_1d, export_dir, point):
        p, point_dir = point
        path = export_dir.strpath

        coupled_scan_only_config_1d.export(path)

        assert all([os.path.isdir(os.path.join(path, 'point_{:03d}'.format(i))) for i in range(3)])

    def test_export_returns_point_directories(self, coupled_scan_only_config_1d, export_dir):
        ret = coupled_scan_only_config_1d.export(export_dir.strpath)

        assert ret == [os.path.abspath(export_dir.join('point_{:03d}'.format(i))) for i in range(3)]

    def test_top_level_serialisation_is_created_in_export_directory(self, coupled_scan_only_config_1d, export_dir):
        path = export_dir.strpath

        coupled_scan_only_config_1d.export(path)

        assert os.path.isfile(os.path.join(path, 'serialisation.json'))

    def test_top_level_serialisation_has_expected_contents(self, coupled_scan_only_config_1d, export_dir):
        path = export_dir.strpath

        coupled_scan_only_config_1d.export(path)

        with open(os.path.join(path, 'serialisation.json')) as f:
            assert f.read() == coupled_scan_only_config_1d.serialise()

    @pytest.fixture(params=enumerate([(0.0, 0.7), (1.1, 0.75), (2.2, 0.8)]))
    def nd_point(self, request, export_dir):
        idx = request.param[0]
        params = request.param[1]
        return idx, params, export_dir / f'point_{idx:03d}'

    @pytest.mark.parametrize('file', ['jetto.jset',
                                      'jetto.in',
                                      'jetto.ex',
                                      'serialisation.json'])
    def test_point_directory_contains_expected_files(self, coupled_scan_only_config_1d, export_dir, nd_point, file):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        coupled_scan_only_config_1d.export(path)

        assert os.path.isfile(os.path.join(point_dir, file))

    def test_point_jset_contains_expected_value(self, coupled_scan_only_config_1d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        coupled_scan_only_config_1d.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset['EquilEscoRef.dshEllipticity'] == p[0] and jset.extras['BCINTRHON'].as_dict() == {None: p[1]}

    def test_point_namelist_contains_expected_value(self, coupled_scan_only_config_1d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        coupled_scan_only_config_1d.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST1', 'ELONG') == p[0] and namelist.get_field('NLIST1', 'BCINTRHON') == p[1]

    def test_point_serialisation_contains_expected_contents(self, coupled_scan_only_config_1d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        coupled_scan_only_config_1d.export(path)

        with open(os.path.join(point_dir, 'serialisation.json')) as f:
            actual_serialisation = json.loads(f.read())
        expected_serialisation = json.loads(coupled_scan_only_config_1d.serialise())
        expected_serialisation['name'] = 'export'
        expected_serialisation['index'] = idx
        expected_serialisation['parameters']['bound_ellip'] = p[0]
        expected_serialisation['parameters']['bcintrhon'] = p[1]

        assert expected_serialisation == actual_serialisation


class TestConfigExportFilesCoupledScanOnly2D:
    @pytest.fixture()
    def coupled_scan_only_config_2d(self, config_with_sanco):
        config_with_sanco.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]),
                                               'bcintrhon': Scan([0.7, 0.75, 0.8])})
        config_with_sanco.create_coupled_scan({'param': Scan([0, 1]), 'ipraux': Scan([0.5, 0.6]),
                                               'fcxmul': Scan([0.3, 0.4])})
        return config_with_sanco

    @pytest.fixture(params=[(i, 'point_{:03d}'.format(i)) for i in range(6)])
    def point(self, request, export_dir):
        return request.param[0], os.path.join(export_dir.strpath, request.param[1])

    def test_point_directories_are_created(self, coupled_scan_only_config_2d, export_dir, point):
        p, point_dir = point
        path = export_dir.strpath

        coupled_scan_only_config_2d.export(path)

        assert all([os.path.isdir(os.path.join(path, 'point_{:03d}'.format(i))) for i in range(6)])

    def test_export_returns_point_directories(self, coupled_scan_only_config_2d, export_dir):
        ret = coupled_scan_only_config_2d.export(export_dir.strpath)

        assert ret == [os.path.abspath(export_dir.join('point_{:03d}'.format(i))) for i in range(6)]

    def test_top_level_serialisation_is_created_in_export_directory(self, coupled_scan_only_config_2d, export_dir):
        path = export_dir.strpath

        coupled_scan_only_config_2d.export(path)

        assert os.path.isfile(os.path.join(path, 'serialisation.json'))

    def test_top_level_serialisation_has_expected_contents(self, coupled_scan_only_config_2d, export_dir):
        path = export_dir.strpath

        coupled_scan_only_config_2d.export(path)

        with open(os.path.join(path, 'serialisation.json')) as f:
            assert f.read() == coupled_scan_only_config_2d.serialise()

    @pytest.fixture(params=enumerate([
        (0.0, 0.7, 0, 0.5, 0.3), (1.1, 0.75, 0, 0.5, 0.3), (2.2, 0.8, 0, 0.5, 0.3),
        (0.0, 0.7, 1, 0.6, 0.4), (1.1, 0.75, 1, 0.6, 0.4), (2.2, 0.8, 1, 0.6, 0.4),
    ]))
    def nd_point(self, request, export_dir):
        idx = request.param[0]
        params = request.param[1]
        return idx, params, export_dir / f'point_{idx:03d}'

    @pytest.mark.parametrize('file', ['jetto.jset',
                                      'jetto.in',
                                      'jetto.sin',
                                      'jetto.ex',
                                      'serialisation.json'])
    def test_point_directory_contains_expected_files(self, coupled_scan_only_config_2d, export_dir, nd_point, file):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        coupled_scan_only_config_2d.export(path)

        assert os.path.isfile(os.path.join(point_dir, file))

    def test_point_jset_contains_expected_value(self, coupled_scan_only_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        coupled_scan_only_config_2d.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset['EquilEscoRef.dshEllipticity'] == p[0] and jset.extras['BCINTRHON'].as_dict() == {None: p[1]} and \
            jset['Panel.ParamName'] == p[2] and jset.extras['IPRAUX'].as_dict() == {None: p[3]} and \
            jset.sanco_extras['FCXMUL'].as_dict() == {None: p[4]}

    def test_point_namelist_contains_expected_value(self, coupled_scan_only_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        coupled_scan_only_config_2d.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())
        with open(os.path.join(point_dir, 'jetto.sin')) as f:
            sanco_namelist = Namelist(f.read())
        assert namelist.get_field('NLIST1', 'ELONG') == p[0] and namelist.get_field('NLIST1', 'BCINTRHON') == p[1] and \
            namelist.get_field('NLIST', 'FIELD_INT') == p[2] and namelist.get_field('INESCO', 'IPRAUX') == p[3] and \
            sanco_namelist.get_field('JSANC', 'FCXMUL') == p[4]

    def test_point_serialisation_contains_expected_contents(self, coupled_scan_only_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        coupled_scan_only_config_2d.export(path)

        with open(os.path.join(point_dir, 'serialisation.json')) as f:
            actual_serialisation = json.loads(f.read())
        expected_serialisation = json.loads(coupled_scan_only_config_2d.serialise())
        expected_serialisation['name'] = 'export'
        expected_serialisation['index'] = idx
        expected_serialisation['parameters']['bound_ellip'] = p[0]
        expected_serialisation['parameters']['bcintrhon'] = p[1]
        expected_serialisation['parameters']['param'] = p[2]
        expected_serialisation['parameters']['ipraux'] = p[3]
        expected_serialisation['parameters']['fcxmul'] = p[4]

        assert expected_serialisation == actual_serialisation


class TestConfigExportFilesCoupledScan1DWithRegularScan:
    @pytest.fixture()
    def mixed_scans_config_1d(self, config):
        config['param'] = Scan([0, 1, 2])
        config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]),
                                    'bcintrhon': Scan([0.7, 0.75, 0.8]),
                                    'ipraux': Scan([0.3, 0.4, 0.5])})
        return config

    @pytest.fixture(params=[(i, 'point_{:03d}'.format(i)) for i in range(9)])
    def point(self, request, export_dir):
        return request.param[0], os.path.join(export_dir.strpath, request.param[1])

    def test_point_directories_are_created(self, mixed_scans_config_1d, export_dir, point):
        p, point_dir = point
        path = export_dir.strpath

        mixed_scans_config_1d.export(path)

        assert all([os.path.isdir(os.path.join(path, 'point_{:03d}'.format(i))) for i in range(9)])

    def test_export_returns_point_directories(self, mixed_scans_config_1d, export_dir):
        ret = mixed_scans_config_1d.export(export_dir.strpath)

        assert ret == [os.path.abspath(export_dir.join('point_{:03d}'.format(i))) for i in range(9)]

    def test_top_level_serialisation_is_created_in_export_directory(self, mixed_scans_config_1d, export_dir):
        path = export_dir.strpath

        mixed_scans_config_1d.export(path)

        assert os.path.isfile(os.path.join(path, 'serialisation.json'))

    def test_top_level_serialisation_has_expected_contents(self, mixed_scans_config_1d, export_dir):
        path = export_dir.strpath

        mixed_scans_config_1d.export(path)

        with open(os.path.join(path, 'serialisation.json')) as f:
            assert f.read() == mixed_scans_config_1d.serialise()

    @pytest.fixture(params=enumerate([
        (0, 0.0, 0.7, 0.3), (0, 1.1, 0.75, 0.4), (0, 2.2, 0.8, 0.5),
        (1, 0.0, 0.7, 0.3), (1, 1.1, 0.75, 0.4), (1, 2.2, 0.8, 0.5),
        (2, 0.0, 0.7, 0.3), (2, 1.1, 0.75, 0.4), (2, 2.2, 0.8, 0.5),
    ]))
    def nd_point(self, request, export_dir):
        idx = request.param[0]
        params = request.param[1]
        return idx, params, export_dir / f'point_{idx:03d}'

    @pytest.mark.parametrize('file', ['jetto.jset',
                                      'jetto.in',
                                      'jetto.ex',
                                      'serialisation.json'])
    def test_point_directory_contains_expected_files(self, mixed_scans_config_1d, export_dir, nd_point, file):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        mixed_scans_config_1d.export(path)

        assert os.path.isfile(os.path.join(point_dir, file))

    def test_point_jset_contains_expected_value(self, mixed_scans_config_1d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        mixed_scans_config_1d.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset['Panel.ParamName'] == p[0] and \
               jset['EquilEscoRef.dshEllipticity'] == p[1] and \
               jset.extras['BCINTRHON'].as_dict() == {None: p[2]} and \
               jset.extras['IPRAUX'].as_dict() == {None: p[3]}

    def test_point_namelist_contains_expected_value(self, mixed_scans_config_1d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        mixed_scans_config_1d.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST', 'FIELD_INT') == p[0] and \
               namelist.get_field('NLIST1', 'ELONG') == p[1] and \
               namelist.get_field('NLIST1', 'BCINTRHON') == p[2] and \
               namelist.get_field('INESCO', 'IPRAUX') == p[3]

    def test_point_serialisation_contains_expected_contents(self, mixed_scans_config_1d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        mixed_scans_config_1d.export(path)

        with open(os.path.join(point_dir, 'serialisation.json')) as f:
            actual_serialisation = json.loads(f.read())
        expected_serialisation = json.loads(mixed_scans_config_1d.serialise())
        expected_serialisation['name'] = 'export'
        expected_serialisation['index'] = idx
        expected_serialisation['parameters']['param'] = p[0]
        expected_serialisation['parameters']['bound_ellip'] = p[1]
        expected_serialisation['parameters']['bcintrhon'] = p[2]
        expected_serialisation['parameters']['ipraux'] = p[3]

        assert expected_serialisation == actual_serialisation


class TestConfigExportFilesCoupledScan2DWithRegularScan:
    @pytest.fixture()
    def mixed_scans_config_2d(self, config):
        config['param'] = Scan([0, 1, 2])
        config.create_coupled_scan({'bound_ellip': Scan([0.0, 1.1, 2.2]),
                                    'bcintrhon': Scan([0.7, 0.75, 0.8]),
                                    'ipraux': Scan([0.3, 0.4, 0.5])})
        config.create_coupled_scan({'curti': Scan([1.9, 2.8]),
                                    'rcntren': Scan([[2.5, 3.0], [2.6, 3.1]])})
        return config

    @pytest.fixture(params=[(i, 'point_{:03d}'.format(i)) for i in range(18)])
    def point(self, request, export_dir):
        return request.param[0], os.path.join(export_dir.strpath, request.param[1])

    def test_point_directories_are_created(self, mixed_scans_config_2d, export_dir, point):
        p, point_dir = point
        path = export_dir.strpath

        mixed_scans_config_2d.export(path)

        assert all([os.path.isdir(os.path.join(path, 'point_{:03d}'.format(i))) for i in range(18)])

    def test_export_returns_point_directories(self, mixed_scans_config_2d, export_dir):
        ret = mixed_scans_config_2d.export(export_dir.strpath)

        assert ret == [export_dir / f'point_{i:03d}' for i in range(18)]

    def test_top_level_serialisation_is_created_in_export_directory(self, mixed_scans_config_2d, export_dir):
        path = export_dir.strpath

        mixed_scans_config_2d.export(path)

        assert os.path.isfile(os.path.join(path, 'serialisation.json'))

    def test_top_level_serialisation_has_expected_contents(self, mixed_scans_config_2d, export_dir):
        path = export_dir.strpath

        mixed_scans_config_2d.export(path)

        with open(os.path.join(path, 'serialisation.json')) as f:
            assert f.read() == mixed_scans_config_2d.serialise()

    @pytest.fixture(params=enumerate([
        (0, 0.0, 0.7, 0.3, 1.9, [2.5, 3.0]), (0, 0.0, 0.7, 0.3, 2.8, [2.6, 3.1]),
        (0, 1.1, 0.75, 0.4, 1.9, [2.5, 3.0]), (0, 1.1, 0.75, 0.4, 2.8, [2.6, 3.1]),
        (0, 2.2, 0.8, 0.5, 1.9, [2.5, 3.0]), (0, 2.2, 0.8, 0.5, 2.8, [2.6, 3.1]),

        (1, 0.0, 0.7, 0.3, 1.9, [2.5, 3.0]), (1, 0.0, 0.7, 0.3, 2.8, [2.6, 3.1]),
        (1, 1.1, 0.75, 0.4, 1.9, [2.5, 3.0]), (1, 1.1, 0.75, 0.4, 2.8, [2.6, 3.1]),
        (1, 2.2, 0.8, 0.5, 1.9, [2.5, 3.0]), (1, 2.2, 0.8, 0.5, 2.8, [2.6, 3.1]),

        (2, 0.0, 0.7, 0.3, 1.9, [2.5, 3.0]), (2, 0.0, 0.7, 0.3, 2.8, [2.6, 3.1]),
        (2, 1.1, 0.75, 0.4, 1.9, [2.5, 3.0]), (2, 1.1, 0.75, 0.4, 2.8, [2.6, 3.1]),
        (2, 2.2, 0.8, 0.5, 1.9, [2.5, 3.0]), (2, 2.2, 0.8, 0.5, 2.8, [2.6, 3.1])
    ]))
    def nd_point(self, request, export_dir):
        idx = request.param[0]
        params = request.param[1]
        return idx, params, export_dir / f'point_{idx:03d}'

    @pytest.mark.parametrize('file', ['jetto.jset',
                                      'jetto.in',
                                      'jetto.ex',
                                      'serialisation.json'])
    def test_point_directory_contains_expected_files(self, mixed_scans_config_2d, export_dir, nd_point, file):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        mixed_scans_config_2d.export(path)

        assert os.path.isfile(os.path.join(point_dir, file))

    def test_point_jset_contains_expected_value(self, mixed_scans_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        mixed_scans_config_2d.export(path)

        with open(os.path.join(point_dir, 'jetto.jset')) as f:
            jset = JSET(f.read())
        assert jset['Panel.ParamName'] == p[0] and jset['EquilEscoRef.dshEllipticity'] == p[1] and \
               jset.extras['BCINTRHON'].as_dict() == {None: p[2]} and \
               jset.extras['IPRAUX'].as_dict() == {None: p[3]} and \
               jset.extras['CURTI'].as_dict() == {None: p[4]} and \
               jset.extras['RCNTREN'].as_dict() == dict(enumerate(p[5], start=1))

    def test_point_namelist_contains_expected_value(self, mixed_scans_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        mixed_scans_config_2d.export(path)

        with open(os.path.join(point_dir, 'jetto.in')) as f:
            namelist = Namelist(f.read())
        assert namelist.get_field('NLIST', 'FIELD_INT') == p[0] and \
               namelist.get_field('NLIST1', 'ELONG') == p[1] and \
               namelist.get_field('NLIST1', 'BCINTRHON') == p[2] and \
               namelist.get_field('INESCO', 'IPRAUX') == p[3] and \
               namelist.get_field('NLIST1', 'CURTI') == [p[4], p[4]] and \
               namelist.get_field('INNBI', 'RCNTREN') == p[5]

    def test_point_serialisation_contains_expected_contents(self, mixed_scans_config_2d, export_dir, nd_point):
        idx, p, point_dir = nd_point
        path = export_dir.strpath

        mixed_scans_config_2d.export(path)

        with open(os.path.join(point_dir, 'serialisation.json')) as f:
            actual_serialisation = json.loads(f.read())
        expected_serialisation = json.loads(mixed_scans_config_2d.serialise())
        expected_serialisation['name'] = 'export'
        expected_serialisation['index'] = idx
        expected_serialisation['parameters']['param'] = p[0]
        expected_serialisation['parameters']['bound_ellip'] = p[1]
        expected_serialisation['parameters']['bcintrhon'] = p[2]
        expected_serialisation['parameters']['ipraux'] = p[3]
        expected_serialisation['parameters']['curti'] = p[4]
        expected_serialisation['parameters']['rcntren'] = p[5]

        assert expected_serialisation == actual_serialisation
