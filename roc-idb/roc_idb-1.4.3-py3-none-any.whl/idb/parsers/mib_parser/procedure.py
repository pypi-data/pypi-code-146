# -*- coding: utf-8 -*-
import re

representation_map = {
    'E': 'Eng',
    'H': 'Hex',
    'D': 'Def',
    'R': 'Dec',
    'F': 'FP',
    'S': 'FP-like',
}


def parse_time_tag(time_tag):
    time_pattern = re.compile('([0-9]{2})\.([0-9]{2})\.([0-9]{2})')

    if time_tag == '':
        value = None
    elif time_pattern.match(str(time_tag)) is not None:
        hour, minute, second = time_tag.split('.')
        value = int(second) + int(minute) * 60 + int(hour) * 3600
    else:
        raise Exception('Invalid time tag field')

    return value


def seconds_to_hours_minutes_seconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


class Procedure(object):
    """Procedure class"""

    @staticmethod
    def create_from_MIB(csf_table, css_table, sdf_table, csp_table):
        """
        Create a procedure list from the MIB tables

        :param csf_table: the CSF table describes the top level of the sequence hierarchy (the sequence itself)
        :param css_table: the CSS table contains an entry for each element in the sequence
        :param sdf_table: the SDF table defines the values of the editable element parameters
        :param csp_table: the CSP defines the formal parameters associated with the current sequence
        :return: procedure list
        """

        # parse the formal parameters
        formal_parameters = {}

        for formal_parameter in csp_table:
            if formal_parameter['VTYPE'] == 'R':
                if formal_parameter['RADIX'] == 'H':
                    representation = 'Hex'
                else:
                    representation = 'Dec'
            else:
                representation = representation_map.get(
                    formal_parameter['VTYPE'], None
                )

            formal_parameters[formal_parameter['FPNAME']] = {
                'value': formal_parameter['DEFVAL'],
                'representation': representation,
                'fp_data': formal_parameter,
            }

        # parse the parameters and merge fp data if any
        parameters = {}

        for parameter in sdf_table:
            key = f'{parameter["SQNAME"]}-{parameter["ENTRY"]}-{parameter["ELEMID"]}'

            # if it's a FP
            if parameter['VTYPE'] == 'F':
                fp_name = parameter['VALUE']
                formal_parameter = formal_parameters[fp_name]

                value = formal_parameter['value']
                representation = formal_parameter['representation']

                if representation == 'Hex' and value.startswith('0x'):
                    value = value[2:]

                parameters.setdefault(key, []).append(
                    {
                        'position': int(parameter['POS']),
                        'representation': representation,
                        'value': value,
                        'is_formal_parameter': True,
                        'srdb_id': parameter['PNAME'],
                        'fp_name': fp_name,
                    }
                )
            # if the VTYPE is S
            # the value is stored in the csp table (like the fp)
            # we treat the parameter as if it were a formal parameter
            elif parameter['VTYPE'] == 'S':
                # get the fp like identifier
                fp_like_name = parameter['PNAME']

                # get the data
                formal_parameter_like_data = formal_parameters[fp_like_name]

                value = formal_parameter_like_data['value']
                representation = formal_parameter_like_data['representation']

                if representation == 'Hex' and value.startswith('0x'):
                    value = value[2:]

                parameters.setdefault(key, []).append(
                    {
                        'position': int(parameter['POS']),
                        'representation': representation,
                        'value': value,
                        'is_formal_parameter': False,
                        'srdb_id': parameter['PNAME'],
                    }
                )
            else:
                representation = representation_map.get(
                    parameter['VTYPE'], None
                )

                value = parameter['VALUE']

                if representation == 'Hex' and value.startswith('0x'):
                    value = value[2:]

                parameters.setdefault(key, []).append(
                    {
                        'position': int(parameter['POS']),
                        'value': value,
                        'representation': representation,
                        'is_formal_parameter': False,
                        'srdb_id': parameter['PNAME'],
                    }
                )

        # parse the statements and merge parameters data if any
        statements = {}

        for statement in css_table:
            sequence_name = statement['SQNAME']
            key = f'{statement["SQNAME"]}-{statement["ENTRY"]}-{statement["ELEMID"]}'
            statements.setdefault(sequence_name, []).append(
                {
                    'srdb_id': statement['ELEMID'],
                    'deltatime': statement['RELTIME'],
                    'comment': statement['COMM'],
                    'position': int(statement['ENTRY']),
                    # get parameters if any
                    'parameters': parameters.get(key, []),
                }
            )

        # create the dictionary of procedures and sequences
        procedure_data = {}

        # populate the dict with sequences data
        for sequence in csf_table:
            procedure = procedure_data.setdefault(sequence['DOCNAME'], {})
            sequence_name = sequence['SQNAME']

            procedure[sequence_name] = {
                'statements': statements[sequence_name],
                'description': sequence['DESC'],
            }

        return procedure_data

    @staticmethod
    def as_xls_data(sequence_data, tc_duration_table):

        stmt_header = [
            'Stmt_nr',
            'Step_nr',
            'Stmt_type',
            'Stmt_id',
            'Blk_flag',
            'Time_tag',
            'info',
            'Param_val_int_tm',
            'Param_val_tm',
            'Proforma',
            'Packet',
            'Manual_Dispatch',
        ]

        cmd_params_header = [
            'Cmd_nr',
            'Param_name',
            'Param_val_int',
            'Param_val',
            'FP_def_val_int',
            'FP_def_val',
        ]

        tlm_values_header = [
            'TLM_nr',
            'val_relation',
            'param_val_int',
            'param_val',
        ]

        pkt_params_header = [
            'Pkt_nr',
            'Param_name',
            'Param_val_int',
            'Param_val',
        ]

        info_header = [
            'Procedure Title',
            'Objective',
            'Summary of Constraints',
            'Mode at start',
            'Intermediate Mode (if any)',
            'Mode at end',
            'Procedure Duration',
            'Short Sequence Description',
            'Long Sequence Description',
        ]

        stmt = {'header': stmt_header, 'rows': []}
        cmd = {'header': cmd_params_header, 'rows': []}

        # initialize the sequence duration
        duration = 0
        for statement in sequence_data['statements']:

            statement_data = {
                'Stmt_nr': statement['position'],
                'Step_nr': statement['position'],
                'Stmt_type': 'CMD',
                'Stmt_id': statement['srdb_id'],
                'Blk_flag': '',
                'Time_tag': statement['deltatime'].replace(':', '.'),
                'info': statement['comment'],
                'Param_val_int_tm': '',
                'Param_val_tm': '',
                'Proforma': '',
                'Packet': '',
                'Manual_Dispatch': 'Y',
            }

            stmt['rows'].append(statement_data)

            # increment the total duration
            duration += parse_time_tag(statement['deltatime'])

            for parameter in statement['parameters']:
                if parameter['is_formal_parameter']:
                    parameter_data = {
                        'Cmd_nr': statement['position'],
                        'Param_name': parameter['srdb_id'],
                        'Param_val_int': 'FP',
                        'Param_val': parameter['fp_name'],
                        'FP_def_val_int': parameter['representation'],
                        'FP_def_val': parameter['value'],
                    }
                else:
                    parameter_data = {
                        'Cmd_nr': statement['position'],
                        'Param_name': parameter['srdb_id'],
                        'Param_val_int': parameter['representation'],
                        'Param_val': parameter['value'],
                    }
                cmd['rows'].append(parameter_data)

        # get the last TC duration
        last_tc_duration = tc_duration_table.get(
            stmt['rows'][-1]['Stmt_id'], {'duration': 1}
        )['duration']

        # add the last TC duration
        duration += last_tc_duration

        description = sequence_data['description']

        h, m, s = seconds_to_hours_minutes_seconds(duration)

        info = {
            'header': info_header,
            'rows': [
                {
                    'Procedure Title': description,
                    'Objective': description,
                    'Summary of Constraints': description,
                    'Mode at start': '',
                    'Intermediate Mode (if any)': '',
                    'Mode at end': '',
                    'Procedure Duration': f'{h}:{m:02d}:{s:02d}',
                    'Short Sequence Description': description,
                    'Long Sequence Description': description,
                }
            ],
        }

        # there are no tml nor pkt data in the MIB
        tlm = {'header': tlm_values_header, 'rows': []}
        pkt = {'header': pkt_params_header, 'rows': []}

        # return the data by sheet
        return {
            'STMT': stmt,
            'CMD Params': cmd,
            'TLM Values': tlm,
            'PKT Params': pkt,
            'Info': info,
        }

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
