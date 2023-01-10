#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import datetime
import os

import xlwt
from poppy.core.target import PyObjectTarget
from poppy.core.task import Task
from roc.idb.parsers.mib_parser.procedure import Procedure

__all__ = ['ExportSequencesTask']


def create_csv_from_dict(filepath, data):
    # create directories if needed
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # create the csv file
    with open(filepath, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, data['header'])
        csv_writer.writeheader()
        for row in data['rows']:
            csv_writer.writerow(row)


def create_sequence_csv(filepath, data):
    # loop over the sheets
    for key in ['STMT', 'CMD Params', 'TLM Values', 'PKT Params', 'Info']:
        create_csv_from_dict(os.path.join(filepath, key + '.csv'), data[key])


def create_xls_sheet(workbook, sheet_name, data):
    header = data['header']

    # create the sheet
    sheet = workbook.add_sheet(sheet_name)
    # populate the header
    for index, entry in enumerate(header):
        sheet.write(0, index, entry)

    # populate the rest of the sheet with the given data
    for row_idx, row in enumerate(data['rows']):
        for col_index, col_name in enumerate(header):
            entry = row.get(col_name)

            # handle case where style is bundled with the value
            if isinstance(entry, tuple):
                value, style = entry
                sheet.write(row_idx + 1, col_index, value, style)
            else:
                sheet.write(row_idx + 1, col_index, entry)


def create_sequence_xls(filepath, data):
    workbook = xlwt.Workbook()

    # loop over the sheets
    for key in ['STMT', 'CMD Params', 'TLM Values', 'PKT Params', 'Info']:
        create_xls_sheet(workbook, key, data[key])

    workbook.save(filepath)


def render_xls_time(time_str, format='h:mm:ss'):
    h, m, s = map(int, time_str.split(':'))
    time_format = xlwt.XFStyle()
    time_format.num_format_str = format
    return (datetime.time(h, m, s), time_format)


@PyObjectTarget.input('sequences')
@PyObjectTarget.input('tc_duration_table')
@Task.as_task(plugin_name='roc.idb', name='idb_export_sequences')
def ExportSequencesTask(self):
    args = self.pipeline.args

    if args.seq_dir_path is None:
        output_path = os.path.join(self.pipeline.output, 'mib_sequences')
    else:
        output_path = args.seq_dir_path

    sequences_data = self.inputs['sequences'].value
    tc_duration_table = self.inputs['tc_duration_table'].value

    # create the csv files
    for procedure_name in sequences_data:
        for sequence_name in sequences_data[procedure_name]:
            xls_data = Procedure.as_xls_data(
                sequences_data[procedure_name][sequence_name],
                tc_duration_table,
            )
            create_sequence_csv(
                os.path.join(output_path, procedure_name, sequence_name),
                xls_data,
            )

            # update the total duration value to be compatible with the xls renderer
            xls_data['Info']['rows'][0][
                'Procedure Duration'
            ] = render_xls_time(
                xls_data['Info']['rows'][0]['Procedure Duration']
            )

            create_sequence_xls(
                os.path.join(
                    output_path, procedure_name, sequence_name + '.xls'
                ),
                xls_data,
            )
