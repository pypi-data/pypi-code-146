# -*- coding: utf-8 -*-
import os
import numpy

from .procedure import Procedure


class ParseSequenceMixin(object):
    def parse_sequences(self):
        """
        Parse MIB sequences
        """

        # the CSF table describes the top level of the sequence hierarchy, i.e. it defines the sequence itself

        csf_dtype = numpy.dtype(
            [
                ('SQNAME', 'U8'),
                ('DESC', 'U24'),
                ('DESC2', 'U64'),
                (
                    'IFTT',
                    'U1',
                ),  # Flag identifying whether or not the sequence contains execution
                # time-tagged commands
                (
                    'NFPARS',
                    'U64',
                ),  # Number of formal parameters of this sequence
                ('ELEMS', 'U64'),  # Number of elements in this sequence
                (
                    'CRITICAL',
                    'U1',
                ),  # Flag identifying the sequence 'criticality'
                (
                    'PLAN',
                    'U1',
                ),  # Flag identifying the sources which are allowed to reference
                # directly this sequence and use it in a planning file
                (
                    'EXEC',
                    'U1',
                ),  # Flag controlling whether this sequence can be loaded onto
                # SCOS-2000 manual stacks stand-alone
                (
                    'SUBSYS',
                    'U64',
                ),  # Identifier of the subsystem which the sequence belongs to
                ('TIME', 'U17'),  # Time when sequence was generated
                (
                    'DOCNAME',
                    'U32',
                ),  # Document name from which it was generated (Procedure name)
                ('ISSUE', 'U10'),  # Issue number of document described above
                ('DATE', 'U17'),  # Issue date of document described above
                (
                    'DEFSET',
                    'U8',
                ),  # Name of the default parameter value set for the sequence
                (
                    'SUBSCHEDID',
                    'U64',
                ),  # Identifier of the default on-board sub-schedule to be used when
                # loading this sequence as execution time-tagged
            ]
        )

        csf_table = self.from_table(
            os.path.join(self.dir_path, 'csf.dat'),
            dtype=csf_dtype,
            regex_dict={'SQNAME': '^(ANEF|AIW[CFV])[0-9]{3}[A-Z]$'},
        )

        # the CSS table contains an entry for each element in the sequence
        # an element can either be a sequence or command, or it can be a formal parameter of the current sequence

        css_dtype = numpy.dtype(
            [
                (
                    'SQNAME',
                    'U8',
                ),  # Name of the sequence which the element belongs to
                (
                    'COMM',
                    'U32',
                ),  # Additional comment to be associated with the sequence element
                ('ENTRY', int),  # Entry number for the sequence element
                (
                    'TYPE',
                    'U1',
                ),  # Flag identifying the element type (C: Command, T: Textual comment)
                (
                    'ELEMID',
                    'U8',
                ),  # Element (identifier) for the current entry within the sequence
                (
                    'NPARS',
                    int,
                ),  # Number of editable parameters this element has
                (
                    'MANDISP',
                    'U1',
                ),  # Flag controlling whether the command requires explicit manual
                # dispatch in a manual stack
                (
                    'RELTYPE',
                    'U1',
                ),  # Flag controlling how the field CSS_RELTIME has to be used to
                # calculate the command release time-tag or the nested sequence
                # release start time
                (
                    'RELTIME',
                    'U8',
                ),  # This field contains the delta release time-tag for the sequence
                # element
                (
                    'EXTIME',
                    'U17',
                ),  # This field contains the delta execution time-tag for the sequence
                # element
                (
                    'PREVREL',
                    'U1',
                ),  # Flag controlling how the field CSS_EXTIME has to be used to
                # calculate the command execution time-tag or the nested sequence
                # execution start time
                (
                    'GROUP',
                    'U1',
                ),  # This field defines the grouping condition for the sequence element
                (
                    'BLOCK',
                    'U1',
                ),  # This field defines the blocking condition for the sequence element
                ('ILSCOPE', 'U1'),
                # Flag identifying the type of the interlock associated to this sequence element
                ('ILSTAGE', 'U1'),
                # The type of verification stage to which an interlock associated to this
                # sequence element waits on
                ('DYNPTV', 'U1'),
                # Flag controlling whether the dynamic PTV checks shall be overridden for this sequence element
                ('STAPTV', 'U1'),
                # Flag controlling whether the static (TM based) PTV check shall be overridden for this sequence element
                ('CEV', 'U1'),
                # Flag controlling whether the CEV checks shall be disabled for this sequence element
            ]
        )

        css_table = self.from_table(
            os.path.join(self.dir_path, 'css.dat'),
            dtype=css_dtype,
            regex_dict={'SQNAME': '^(ANEF|AIW[CFV])[0-9]{3}[A-Z]$'},
        )

        # the SDF table defines the values of the editable element parameters.

        sdf_dtype = numpy.dtype(
            [
                (
                    'SQNAME',
                    'U8',
                ),  # Name of the sequence which the parameter belongs to
                (
                    'ENTRY',
                    int,
                ),  # Entry number of the sequence element to which this parameter belongs
                (
                    'ELEMID',
                    'U8',
                ),  # Name of the sequence element to which this parameter belongs
                ('POS', int),
                # If the sequence element is a command, then this field specifies the bit offset of the parameter in the command
                (
                    'PNAME',
                    'U8',
                ),  # Element parameter name i.e. name of the editable command parameter
                ('FTYPE', 'U1'),
                # Flag controlling whether the parameter value can be modified after loading the sequence on the stack or if it should be considered as fixed
                ('VTYPE', 'U1'),
                # Flag identifying the source of the element parameter value and how to interpret the SDF_VALUE field
                (
                    'VALUE',
                    'U17',
                ),  # This field contains the value for the element parameter
                ('VALSET', 'U8'),
                # Name of the parameter value set (PSV_PVSID) which will be used to provide the value
                ('REPPOS', 'int'),  # Command parameter repeated position
            ]
        )

        sdf_table = self.from_table(
            os.path.join(self.dir_path, 'sdf.dat'),
            dtype=sdf_dtype,
            regex_dict={'SQNAME': '^(ANEF|AIW[CFV])[0-9]{3}[A-Z]$'},
        )

        # the CSP defines the formal parameters associated with the current sequence

        csp_dtype = numpy.dtype(
            [
                (
                    'SQNAME',
                    'U8',
                ),  # Name of the sequence which formal parameter belongs to
                ('FPNAME', 'U8'),  # Name of this formal parameter
                (
                    'FPNUM',
                    int,
                ),  # Unique number of the formal parameter within the sequence
                (
                    'DESCR',
                    'U24',
                ),  # Textual description of the formal parameter
                ('PTC', int),  # Parameter Type Code
                ('PFC', int),  # Parameter Format Code
                ('DISPFMT', 'U1'),
                # Flag controlling the input and display format of the engineering values for calibrated parameters and for time parameters
                ('RADIX', 'U1'),
                # This is the default radix that the raw representation of the parameter if it is unsigned integer
                (
                    'TYPE',
                    'U1',
                ),  # Flag identifying the type of the formal parameter
                ('VTYPE', 'U1'),
                # Flag identifying the representation used to express the formal parameter default value
                (
                    'DEFVAL',
                    'U17',
                ),  # This field contains the default value for this formal parameter
                ('CATEG', 'U1'),
                # Flag identifying the type of calibration or special processing associated to the parameter
                ('PRFREF', 'U10'),
                # This field contains the name of an existing parameter range set to which the parameter will be associated
                ('CCAREF', 'U10'),
                # This field contains the name of an existing numeric calibration curve to which the parameter will be associated
                ('PAFREF', 'U10'),
                # This field contains the name of an existing textual calibration definition to which the parameter will be associated
                ('UNIT', 'U4'),  # Engineering unit mnemonic
            ]
        )

        csp_table = self.from_table(
            os.path.join(self.dir_path, 'csp.dat'), dtype=csp_dtype,
        )

        # filter tables to keep only RPW sequences and return tables

        # filter tables to keep only RPW sequences and create the procedure list
        return Procedure.create_from_MIB(
            csf_table, css_table, sdf_table, csp_table,
        )
