"""
repository for GB OCR status.
Uses the DrsDbContext and the drs models.
Focus on GB processing tracking
"""
import argparse
from datetime import datetime
from collections import namedtuple
from pathlib import Path

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.future import select

# Just use everything
from log_ocr.models.drs import *

# Claims to work, https://pydoc.dev/sqlalchemy/latest/sqlalchemy.dialects.mysql.dml.Insert.html
# but doesn't
from sqlalchemy.dialects.mysql.dml import insert

from log_ocr.DrsContextBase import DrsDbContextBase


class GbOcrContext(DrsDbContextBase):
    """
    Context which just holds some adds/updates for specific tables
    """

    def add_metadata_upload(self, work_name: str, metadata_upload_date: datetime, upload_result: int):
        """
        Adds a metadata upload record
        :type work_name: str
        :param work_name: the BDRC work name
        :type metadata_upload_date: datetime
        :param metadata_upload_date:
        :param upload_result: return code from upload
        """

        w = self.get_or_create_work(work_name)
        self.session.add(
            GbMetadata(work_id=w.workId, upload_time=metadata_upload_date,
                       upload_result=upload_result))
        self.session.flush()
        self.session.commit()

    def add_content_activity(self, work_rid: str, image_group_label: str, activity: str,
                             start_time: datetime, activity_rc: int, log_data: str = ''):
        """
        :param work_rid: Work containing image group
        :param image_group_label: entity to track
        :param activity: activity type (freeform)
        :param start_time: time of activity start
        :param activity_rc: if 0 , success
        :param log_data: user defined data
        :return:
        """
        v: Volumes = self.get_or_create_volume(work_name=work_rid, volume_name=image_group_label)
        self.session.add(
            GbContent(volume_id=v.volumeId, step_time=start_time, job_step=activity, step_rc=activity_rc,
                      gb_log=log_data))
        self.session.flush()
        self.session.commit()

    def add_content_state(self, work_rid: str, image_group_label: str, key_date: datetime, state: str, log: str):
        """
        Reflects changes in state of works on GRIN pages. Does NOT reflect activity, such as downloads
        :param work_rid: Work Name
        :param image_group_label: Image group label
        :param state: which page is sending this
        :param log: json string of other page data (no format)
        :return:
        """
        v: Volumes = self.get_or_create_volume(work_name=work_rid, volume_name=image_group_label)
        # Nice, but not needed
        # stmt = select(GbState).where(and_(GbState.volume_id == v.volumeId, GbState.job_state == state))
        # hasany = self.drs_session.execute(stmt)
        # for gb_track in hasany.scalars():
        #     print(f"{gb_track.volume_id}  {gb_track.job_state}")
        try:

            # is it a time thing?
            exec_date: str = key_date.strftime("%")
            # Sigh - on duplicate key update doesnt work for composite keys in SQLAlchemy.
            # This doesn't work either:
            #   File "/Users/jimk/dev/ao-google-books/venv/lib/python3.9/site-packages/sqlalchemy/engine/base.py", line 1548, in _execute_clauseelement
            #     keys = sorted(distilled_params[0])
            # TypeError: '<' not supported between instances of 'str' and 'int'
            # regardless if ON DUPLICATE KEY UPDATE or not
            # self.drs_session.execute(
            #     # ON DUPLICATE KEY UPDATE (gb_log) Values (?)...., log
            #     f"INSERT INTO {GbState.__table__} (volume_id, job_state, state_date, gb_log) VALUES (?, ?, ?, ?) ;",
            #    (_v, state, key_date.strftime("%y/%m/%dT%H:%M:%S"), log)
            # )
            # self.drs_session.execute(
            #     # ...., log
            #     f"INSERT INTO {GbState.__table__} (volume_id, job_state, state_date, gb_log) VALUES (?, ?, ?, ?) ON DUPLICATE KEY UPDATE (gb_log) Values (?);",
            #    (_v, state, key_date.strftime("%y/%m/%dT%H:%M:%S"), log, log)
            # )
            # self.drs_session.commit()
            ins = insert(GbState).values(volume_id=v.volumeId, job_state=state, gb_log=log, state_date=key_date)
            ins.on_duplicate_key_update(gb_log=ins.inserted.gb_log)
            self.session.execute(ins)
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            pass

    def add_download(self, work_name: str, volume_label: str, download_path: Path, download_object: str):
        """
        Adds a download record
        :param work_name:
        :param volume_label:
        :param download_path:
        :param download_object:
        :return:
        """
        vol: Volumes = self.get_or_create_volume(work_name, volume_label)
        down_record = GbDownload(
            volume=vol,
            download_time=datetime.now(),
            download_path=str(download_path),
            download_object_name=download_object)
        self.session.add(down_record)
        self.session.commit()


def import_track_from_activity_log(log: Path, activity: str):
    """
    Creates records for
    :param log: Path to input log file
    :param activity:
    :return:
    """
    pass


if __name__ == '__main__':
    """
    This is a stub test
    To run, enter the VPN and mount RS2://processing. Or use the default (See ~/.bashrc ) 
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("log_file", help="tracking log to read", type=argparse.FileType('r'))

    args = ap.parse_args(['/Volumes/Processing/logs/google-books-logs/transfer-activity.log'])

    # each line is
    # log_entry_date:result:operation:operand:operation_type{content|metadata}
    Row = namedtuple('GbLogRow', ('entry_dtm', 'operation', 'result', 'operand', 'op_class'))

    with GbOcrContext as gb_t:
        for line in args.log_file.readlines():
            fields = line.strip().split(':')
            _row = Row._make(fields)
            start_time: datetime = datetime.strptime(_row.entry_dtm, '%m-%d-%Y %H-%M-%S')
            result: int = 0 if _row.result == 'success' else 1
            if (_row.op_class == 'metadata'):
                gb_t.add_metadata_upload(_row.operand,
                                         start_time,
                                         result)
