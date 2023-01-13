import sqlite3

from yoyo import step

__depends__ = {"037__calculated_statistics"}


def rename_old_table(db: sqlite3.Connection):
    cursor = db.cursor()
    _rename_old_table(cursor)


def _rename_old_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        select count(*) from sqlite_master where type='table' AND name='DataServiceViewEvaluations';
    """
    )
    if cursor.fetchone()[0] == 0:
        return

    cursor.execute(
        """
        alter table DataServiceViewEvaluations rename to to_remove_DataServiceViewEvaluations;
    """
    )


def create_table(db: sqlite3.Connection):
    cursor = db.cursor()
    _create_table(cursor)


def _create_table(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        CREATE TABLE DataServiceViewEvaluations (
            id integer primary key autoincrement,
            data_service_view_id integer not null,
            evaluation_date datetime not null,

            foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
        );
    """
    )
    cursor.execute(
        """
        create index DataServiceViewEvaluations_idx_data_service_view_id
        on DataServiceViewEvaluations(data_service_view_id);
    """
    )


steps = [
    step(rename_old_table),
    step(create_table),
]
