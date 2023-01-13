import sqlite3


from yoyo import step

__depends__ = {"039__populate_data_service_view_evaluation"}

__disable_foreign_keys__ = True


def _drop_last_evaluation_date(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.executescript(
        """
create table DataServiceViews_new (
    id integer primary key autoincrement,
    data_service_id integer not null,
    series_set_name text not null,
    removed integer not null default 0,

    unique(data_service_id, series_set_name),
    foreign key (data_service_id) references DataServices(id) on delete cascade
);

insert into DataServiceViews_new
select id, data_service_id, series_set_name, removed
from DataServiceViews;

drop table DataServiceViews;
alter table DataServiceViews_new rename to DataServiceViews;

create index DataServiceViews_idx_data_service_id on DataServiceViews(data_service_id);
    """
    )


steps = [
    step(_drop_last_evaluation_date),
]
