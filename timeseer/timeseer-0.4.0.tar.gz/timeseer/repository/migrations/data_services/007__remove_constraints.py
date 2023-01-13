import sqlite3

from yoyo import step

__depends__ = {"006__contribution_evaluations"}


def migrate_data_service_not_null_constraints(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute("pragma schema_version")
    (schema_version,) = cursor.fetchone()
    cursor.execute("pragma writable_schema = ON")
    cursor.execute(
        """
        update sqlite_master
        set sql = 'create table DataServiceBadActorScore(
    id integer primary key autoincrement,
    data_service_view_evaluation_id integer not null,
    series_id text,
    start_date datetime not null,
    end_date datetime not null,
    state text not null,
    score real not null,

    foreign key (data_service_view_evaluation_id) references DataServiceViewEvaluations(id) on delete cascade
)'
        where type = 'table' and name = 'DataServiceBadActorScore'
    """
    )
    cursor.execute(
        """
        update sqlite_master
        set sql = 'CREATE TABLE Scores(
    id integer primary key autoincrement,
    data_service_view_evaluation_id integer not null,
    series_id text,
    score_name text not null,
    score float not null,

    foreign key (data_service_view_evaluation_id) references DataServiceViewEvaluations(id) on delete cascade
)'
        where type = 'table' and name = 'Scores'
    """
    )
    cursor.execute(f"pragma schema_version = {schema_version + 1}")
    cursor.execute("pragma writable_schema = OFF")


steps = [
    step(migrate_data_service_not_null_constraints),
]
