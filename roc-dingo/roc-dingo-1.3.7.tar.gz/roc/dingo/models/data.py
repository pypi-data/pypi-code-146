#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Reference documentation: ROC-GEN-SYS-NTT-00038-LES

"""
Database model for:
    - sbm_log,
    - lfr_kcoeff_dump
    - bia_sweep_log,
    - efecs_events
    - event_log
    - solohk_param
    - process_queue
tables.
"""

from poppy.core.db.non_null_column import NonNullColumn

from poppy.core.db.base import Base
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.dialects.postgresql import (
    BIGINT,
    BOOLEAN,
    FLOAT,
    ENUM,
    SMALLINT,
    TIMESTAMP,
    JSONB,
)

__all__ = [
    'SbmLog',
    'BiaSweepLog',
    'LfrKcoeffDump',
    'EventLog',
    'SoloHkParam',
    'ProcessQueue',
    'EfecsEvents',
    'HfrTimeLog',
    'Event'
]

# Create enumeration for sbm_log.status column
SBM_STATUS_LIST = ['Available', 'Requested',
                   'Downlinked', 'Deleted', 'Missed', 'Unknown']
sbm_status_enum = ENUM(
    *SBM_STATUS_LIST,
    name='sbm_status_type',
    # schema='pipeline',
)


class SbmLog(Base):
    """
    Class representation of the table for sbm_log table in the ROC database.
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    sbm_type = NonNullColumn(
        SMALLINT(),
        descr='Type of SBM event (1=SBM1 or 2=SBM2)')
    cuc_time = NonNullColumn(
        String(1024),
        descr='SBM event occurrence on-board time in CCSDS CUC'
              'format "coarse:fine".')
    obt_time = NonNullColumn(
        TIMESTAMP(),
        descr='SBM event occurrence on-board time in SQL timestamp format')
    utc_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='SBM event occurrence UTC time in SQL timestamp format')
    utc_time_is_predictive = NonNullColumn(
        BOOLEAN,
        nullable=True,
        descr='Flag to indicate if UTC time is predictive (True)'
              'or definitive (False)')
    sbm_qf = NonNullColumn(
        FLOAT(),
        descr='SBM detection quality factor')
    sbm_algo = NonNullColumn(
        SMALLINT(),
        descr='SBM detection algorithm status')
    sbm_algo_param = NonNullColumn(
        JSONB(),
        nullable=True,
        descr='List of SBM algo parameters (JSON format)')
    retrieved_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Local date/time at which the SBM event science data'
              'has been retrieved.')
    selected = NonNullColumn(
        BOOLEAN,
        nullable=True,
        descr='True if SBM event is selected')
    status = NonNullColumn(
        sbm_status_enum,
        descr='Status of the sbm event.'
              f'Possible values are: {SBM_STATUS_LIST}')
    insert_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Database insertion local time.')
    __tablename__ = 'sbm_log'
    __table_args__ = (
        UniqueConstraint('cuc_time', 'sbm_type'),
        {
            'schema': 'pipeline',
        }
    )


class BiaSweepLog(Base):
    """
    Class representation of the table for bia_sweep_log table
    in the ROC database.
    """
    id = NonNullColumn(BIGINT(), primary_key=True)
    sweep_step = NonNullColumn(
        String(16),
        descr='Step of the Bias sweep'
              '(TM_DPU_EVENT_PR_BIA_SWEEP.PA_DPU_BIA_SWEEP_PR_CODE values)')
    utc_time = NonNullColumn(
        TIMESTAMP(),
        descr='Sweep step UTC time')
    cuc_time = NonNullColumn(
        String(1024),
        descr='Sweep step on-board time in CCSDS CUC format "coarse:fine".')
    utc_time_is_predictive = NonNullColumn(
        BOOLEAN, nullable=True,
        descr='Flag to indicate if UTC time is predictive (True)'
              'or definitive (False)')
    insert_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Database insertion local time.')

    __tablename__ = 'bia_sweep_log'
    __table_args__ = (
        UniqueConstraint('sweep_step', 'utc_time'),
        {
            'schema': 'pipeline',
        }
    )


class LfrKcoeffDump(Base):
    """
    Class representation of the table for lfr_kcoeff_dump table
    in the ROC database.
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    utc_time = NonNullColumn(
        TIMESTAMP(),
        descr='TM_LFR_KCOEFFICIENTS_DUMP packet creation time (UTC)')
    cuc_time = NonNullColumn(
        String(1024),
        descr='Packet creation on-board time in CCSDS CUC'
              'format "coarse:fine".')
    utc_time_is_predictive = NonNullColumn(
        BOOLEAN,
        nullable=True,
        descr='Flag to indicate if UTC time is predictive (True)'
              'or definitive (False)')
    kcoeff_pkt_cnt = NonNullColumn(
        SMALLINT(),
        descr='Total count of packets for LFR inter calibration factors dump.'
              '(PA_LFR_KCOEFF_PKT_CNT)')
    kcoeff_pkt_nr = NonNullColumn(
        SMALLINT(),
        descr='Number of the packet for LFR inter calibration factors dump.'
              '(PA_LFR_KCOEFF_PKT_NR)')
    kcoeff_blk_nr = NonNullColumn(
        SMALLINT(),
        descr='Number of block LFR_KCOEFFICENT_PARAMETERS in the packet'
              '(PA_LFR_KCOEFF_BLK_NR)')
    kcoeff_values = NonNullColumn(
        JSONB(),
        descr='32 values of the Kcoeff for the current list of frequencies'
              '(json format)')
    insert_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Database insertion local time.')

    __tablename__ = 'lfr_kcoeff_dump'
    __table_args__ = (
        UniqueConstraint('utc_time', 'kcoeff_pkt_nr'),
        {
            'schema': 'pipeline',
        }
    )


class EventLog(Base):
    """
    Class representation of the table for event_log table in the ROC database.
    """
    id = NonNullColumn(BIGINT(), primary_key=True)
    start_time = NonNullColumn(
        TIMESTAMP(),
        descr='Event UTC start time')
    end_time = NonNullColumn(
        TIMESTAMP(),
        descr='Event UTC end time')
    description = NonNullColumn(
        JSONB(),
        descr='Description of event')
    label = NonNullColumn(
        String(),
        descr='Label of event')
    is_predictive = NonNullColumn(
        BOOLEAN,
        nullable=True,
        descr='Flag to indicate if event is predictive (True)'
              'or definitive (False)')
    insert_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Database insertion local time.')

    __tablename__ = 'event_log'
    __table_args__ = (
        UniqueConstraint('start_time', 'end_time', 'label', 'description'),
        {
            'schema': 'pipeline',
        }
    )


class SoloHkParam(Base):
    """
    Class representation of the table solo_hk_param in the ROC database.
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    name = NonNullColumn(
        String(16),
        descr='Parameter name (SRDB ID)')
    utc_time = NonNullColumn(
        TIMESTAMP(),
        descr='ParamSampleListElement.TimeStampAsciiA XML tag value')
    description = NonNullColumn(
        String(),
        descr='ParamSampleListElement.Description XML tag value')
    unit = NonNullColumn(
        String(),
        descr='ParamSampleListElement.Unit XML tag value')
    eng_value = NonNullColumn(
        String(),
        descr='ParamSampleListElement.EngineeringValue XML tag value')
    raw_value = NonNullColumn(
        String(),
        descr='ParamSampleListElement.RawValue XML tag value')
    sha = NonNullColumn(
        String(),
        descr='SHA of the element. Computed from'
              '(name, time_stamp, raw_value)')

    __tablename__ = 'solo_hk_param'
    __table_args__ = (
        UniqueConstraint('sha'),
        {
            'schema': 'pipeline',
        }
    )


class ProcessQueue(Base):
    """
    Class representation of the table process_queue in the ROC database.
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    dataset_id = NonNullColumn(
        String(512),
        descr='Dataset ID in the ROC database')
    start_time = NonNullColumn(
        TIMESTAMP(),
        descr='Start time of data')
    end_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='End time of data')
    version = NonNullColumn(
        String(16),
        nullable=True,
        descr='Data version of the file')
    file = NonNullColumn(
        String(),
        nullable=True,
        descr='Dataset file name'
    )
    insert_time = NonNullColumn(
        TIMESTAMP(),
        nullable=True,
        descr='Database insertion local time.')

    __tablename__ = 'process_queue'
    __table_args__ = (
        {
            'schema': 'pipeline',
        }
    )


class EfecsEvents(Base):
    """
    Class representation of the table efecs_events in the ROC database.
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    name = NonNullColumn(
        String(),
        descr='EFECS event name')
    utc_time = NonNullColumn(
        TIMESTAMP(),
        descr='EFECS event time')
    attributes = NonNullColumn(
        JSONB(),
        descr='EFECS event attributes (in JSON format)',
        nullable=True)
    ltp_count = NonNullColumn(
        SMALLINT(),
        descr='LTP counter')
    gen_time = NonNullColumn(
        TIMESTAMP(),
        descr='EFECS generation time')

    __tablename__ = 'efecs_events'
    __table_args__ = (
        UniqueConstraint('name', 'utc_time'),
        {
            'schema': 'pipeline',
        }
    )


class HfrTimeLog(Base):
    """
    Class representation of the table hfr_time_log in the ROC database.
    See https://gitlab.obspm.fr/ROC/RCS/THR_CALBAR/-/issues/76 for details
    about why this table is needed
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    acq_time = NonNullColumn(
        TIMESTAMP(),
        descr='HFR TM PA_THR_ACQUISITION_TIME human readable time',
    )
    coarse_time = NonNullColumn(
        BIGINT(),
        descr='HFR TM PA_THR_ACQUISITION_TIME, coarse part')
    fine_time = NonNullColumn(
        BIGINT(),
        descr='HFR TM PA_THR_ACQUISITION_TIME, fine part')
    mode = NonNullColumn(
        SMALLINT(),
        descr='HFR mode (0=NORMAL, 1=BURST)',
    )
    delta_time1 = NonNullColumn(
        JSONB(),
        descr='Values of delta_time for HF1 for each TM '
              'for the current PA_THR_ACQUISITION_TIME value. '
              'Keywords are packet creation times (coarse * 100000 + fine)',
        nullable=True
    )
    delta_time2 = NonNullColumn(
        JSONB(),
        descr='Values of delta_time for HF2 for each TM '
              'for the current PA_THR_ACQUISITION_TIME value. '
              'Keywords are packet creation times (coarse * 100000 + fine)',
        nullable=True
    )

    __tablename__ = 'hfr_time_log'
    __table_args__ = (
        UniqueConstraint('coarse_time', 'fine_time', 'mode'),
        {
            'schema': 'pipeline',
        }
    )


# Create enumeration for event.origin column
EVENT_ORIGIN_LIST = ['SOLO', 'RPW']
event_origin_enum = ENUM(
    *EVENT_ORIGIN_LIST,
    name='event_origin_enum',
    # schema='pipeline',
)


class Event(Base):
    """
    Class listing the different events for RPW
    """

    id = NonNullColumn(BIGINT(), primary_key=True)
    label = NonNullColumn(
        String(),
        descr='Event label'
    )
    is_tracked = NonNullColumn(
        BOOLEAN, default=True,
        descr='True if event has to be tracked'
    )
    is_anomaly = NonNullColumn(
        BOOLEAN, default=True,
        descr='True if event is an anomaly'
    )
    origin = NonNullColumn(
        event_origin_enum,
        descr='Origin of the event.'
              f'Possible values are: {EVENT_ORIGIN_LIST}'
    )

    __tablename__ = 'events'
    __table_args__ = (
        UniqueConstraint('label'),
        {
            'schema': 'pipeline',
        }
    )
