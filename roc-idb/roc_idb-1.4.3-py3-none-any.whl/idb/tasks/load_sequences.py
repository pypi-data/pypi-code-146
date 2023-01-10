#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from poppy.core.conf import settings
from poppy.core.db.connector import Connector
from poppy.core.db.handlers import create, get_or_create, get_update_or_create
from poppy.core.logger import logger
from poppy.core.target import PyObjectTarget
from poppy.core.task import Task
from roc.idb.parsers.mib_parser.procedure import parse_time_tag

__all__ = ['LoadSequencesTask']

try:
    MUSIC_DATABASE = settings.MUSIC_DATABASE
except AttributeError:
    logger.warning('MUSIC_DATABASE is not defined in pipeline settings')
    MUSIC_DATABASE = '___MUSIC_DATABASE_NOT_DEFINED___'


def create_telecommand(
    session,
    *,
    position,
    sequence_id,
    srdb_id,
    comment,
    duration,
    parameters_data,
):
    """
    Create a telecommand and associated parameters in the database

    :param position:
    :param sequence_id:
    :param srdb_id:
    :param comment:
    :param duration:
    :param parameters_data:
    :return: the telecommand instance
    """

    from roc.idb.models.music.figaro import Telecommand, TelecommandParameter

    # create the telecommand
    telecommand = create(
        session,
        Telecommand,
        position=position,
        sequence_id=sequence_id,
        srdb_id=srdb_id,
        comment=comment,
        duration=duration,
        manual_dispatch=True,
    )

    for param_idx, parameter_data in enumerate(parameters_data):
        create(
            session,
            TelecommandParameter,
            position=param_idx,
            statement_id=telecommand.id_telecommand,
            is_formal_parameter=parameter_data['is_formal_parameter'],
            representation=parameter_data['representation'],
            srdb_id=parameter_data['srdb_id'],
            value=parameter_data['value'],
        )

    return telecommand


@PyObjectTarget.input('sequences')
@PyObjectTarget.input('tc_duration_table')
@PyObjectTarget.input('sequence_description_table')
@PyObjectTarget.input('rpw_states')
@PyObjectTarget.input('idb_version')
@PyObjectTarget.input('idb_source')
@Task.as_task(plugin_name='roc.idb', name='idb_load_sequences')
@Connector.if_connected(MUSIC_DATABASE)
def LoadSequencesTask(self):
    from roc.idb.models.music.figaro import (
        Procedure,
        Sequence,
        StepSeparator,
        Telecommand,
        TelecommandParameter,
        TelecommandDuration,
        RpwStateDescription,
    )
    from sqlalchemy.ext.declarative import DeferredReflection

    # get the meb connector and get the database
    connector = Connector.manager[settings.MUSIC_DATABASE]
    database = connector.get_database()

    # create music tables reflection and mappings
    DeferredReflection.prepare(database.engine)

    # ensure database is connected
    database.connectDatabase()

    # get a database session
    session = database.session_factory()

    sequences_data_dict = self.inputs['sequences'].value
    tc_duration_table = self.inputs['tc_duration_table'].value
    sequence_description_table = self.inputs[
        'sequence_description_table'
    ].value
    rpw_states = self.inputs['rpw_states'].value

    # load RPW modes and config
    get_update_or_create(
        session,
        RpwStateDescription,
        idb_version=self.inputs['idb_version'].value,
        idb_source='MIB',
        update_fields=rpw_states,
    )

    # load the tc durations in the database
    for srdb_id in tc_duration_table:
        get_update_or_create(
            session,
            TelecommandDuration,
            srdb_id=srdb_id,
            update_fields=tc_duration_table[srdb_id],
        )

    # load the sequences in the database
    for procedure_name in sequences_data_dict:

        # get or create the procedure
        procedure = get_or_create(session, Procedure, name=procedure_name,)

        for sequence_name, sequence_data in sequences_data_dict[
            procedure_name
        ].items():

            # get and update the existing sequence
            # or create a new one

            if sequence_name in sequence_description_table:
                sequence_descriptions = sequence_description_table[
                    sequence_name
                ]
            else:
                sequence_descriptions = {
                    'long_description': sequence_data['description'],
                    'description': sequence_data['description'],
                }

            sequence = get_update_or_create(
                session,
                Sequence,
                name=sequence_name,
                update_fields={
                    'procedure_id': procedure.id_procedure,
                    'idb_source': 'MIB',
                    'idb_version': self.inputs['idb_version'].value,
                    **sequence_descriptions,
                },
            )

            # delete existing statements with associated parameters
            tc_query = session.query(Telecommand).filter_by(
                sequence_id=sequence.id_sequence
            )
            for telecommand in tc_query:
                session.query(TelecommandParameter).filter_by(
                    statement_id=telecommand.id_telecommand
                ).delete()
                session.delete(telecommand)

            session.query(StepSeparator).filter_by(
                sequence_id=sequence.id_sequence
            ).delete()
            session.commit()

            # create new statements
            for statement_idx, statement_data in enumerate(
                sequence_data['statements'][:-1]
            ):

                # get the srdb_id
                srdb_id = statement_data['srdb_id']

                # compute durations
                duration = parse_time_tag(
                    sequence_data['statements'][statement_idx + 1]['deltatime']
                )
                min_duration = tc_duration_table.get(srdb_id, {'duration': 1})[
                    'duration'
                ]

                # compare the MIB duration with the min one (from the tc duration table)
                if duration < min_duration:
                    logger.warning(
                        f"Statement duration for statement '{sequence_name}:{srdb_id}' is lower than the "
                        f"value of the tc duration table ('{duration}' < '{min_duration}'). Maybe a "
                        f'spacecraft sequence ? Overriding MIB value'
                    )
                    statement_duration = min_duration
                else:
                    statement_duration = duration

                # create the telecommand
                create_telecommand(
                    session,
                    position=statement_idx * 2,
                    sequence_id=sequence.id_sequence,
                    srdb_id=statement_data['srdb_id'],
                    comment=statement_data['comment'],
                    duration=statement_duration,
                    parameters_data=statement_data['parameters'],
                )

                # create the step separator
                create(
                    session,
                    StepSeparator,
                    position=statement_idx * 2 + 1,
                    sequence_id=sequence.id_sequence,
                )

            # handle last the last TC
            statement_idx = len(sequence_data['statements']) - 1
            statement_data = sequence_data['statements'][statement_idx]

            # get the last TC duration
            last_tc_duration = tc_duration_table.get(
                statement_data['srdb_id'], {'duration': 1}
            )['duration']

            create_telecommand(
                session,
                position=statement_idx * 2,
                sequence_id=sequence.id_sequence,
                srdb_id=statement_data['srdb_id'],
                comment=statement_data['comment'],
                duration=last_tc_duration,
                parameters_data=statement_data['parameters'],
            )
