import sqlite3

from yoyo import step

__depends__ = {"023__series_sets"}


def update_tables(db: sqlite3.Connection):
    cursor = db.cursor()
    view_evaluation_ids = _get_last_evaluation_per_view(cursor)
    _update_favorite_kpi_scores(cursor, view_evaluation_ids)
    _update_scores(cursor, view_evaluation_ids)
    _update_bad_actors(cursor, view_evaluation_ids)
    _update_subscores(cursor, view_evaluation_ids)
    _update_excel_exports(cursor, view_evaluation_ids)
    _update_bad_actor_kpi_score(cursor, view_evaluation_ids)
    _update_statistics(cursor, view_evaluation_ids)


def _get_last_evaluation_per_view(cursor: sqlite3.Cursor) -> list[int]:
    cursor.execute(
        """
            select id, data_service_view_id, max(evaluation_date) from DataServiceViewEvaluations
            group by data_service_view_id

        """
    )
    results = cursor.fetchall()
    cursor.executemany(
        """
            update DataServiceViews set last_evaluation_date = ? where id = ?
        """,
        [
            [evaluation_date, data_service_view_id]
            for _, data_service_view_id, evaluation_date in results
        ],
    )
    return [view_evaluation_id for view_evaluation_id, _, _ in results]


def _update_scores(cursor: sqlite3.Cursor, view_evaluation_ids: list[int]):
    cursor.execute(
        """
        CREATE TABLE new_Scores(
            id integer primary key autoincrement,
            data_service_view_id integer not null,
            series_id text,
            score_name text not null,
            score real not null,
            kpi_name text,

            foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
        )
    """
    )
    cursor.execute(
        f"""
            insert into new_Scores
            (id, data_service_view_id, series_id, score_name, score, kpi_name)
            select
                id,
                (select data_service_view_id from DataServiceViewEvaluations
                    where id = data_service_view_evaluation_id
                    order by evaluation_date asc
                    limit 1),
                series_id,
                score_name,
                score,
                kpi_name
            from Scores
            where data_service_view_evaluation_id in ({",".join(["?"] * len(view_evaluation_ids))})
        """,
        view_evaluation_ids,
    )
    cursor.execute(
        """
            drop table Scores;
        """
    )
    cursor.execute(
        """
            alter table new_Scores rename to Scores;
        """
    )


def _update_favorite_kpi_scores(cursor: sqlite3.Cursor, view_evaluation_ids: list[int]):
    cursor.execute(
        """
        CREATE TABLE new_FavoriteKPIScores(
            id integer primary key autoincrement,
            data_service_view_id integer not null,
            name integer not null,
            score real,

            unique(data_service_view_id, name, score),
            foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
        )
    """
    )
    cursor.execute(
        f"""
            insert into new_FavoriteKPIScores (id, data_service_view_id, name, score)
            select
                id,
                (select data_service_view_id from DataServiceViewEvaluations
                    where id = data_service_view_evaluation_id
                    order by evaluation_date asc
                    limit 1),
                name,
                score
            from FavoriteKPIScores
            where data_service_view_evaluation_id in ({",".join(["?"] * len(view_evaluation_ids))})
        """,
        view_evaluation_ids,
    )
    cursor.execute(
        """
            drop table FavoriteKPIScores;
        """
    )
    cursor.execute(
        """
            alter table new_FavoriteKPIScores rename to FavoriteKPIScores;
        """
    )


def _update_bad_actors(cursor: sqlite3.Cursor, view_evaluation_ids: list[int]):
    cursor.execute(
        """
        CREATE TABLE new_DataServiceBadActorScores(
            id integer primary key autoincrement,
            data_service_view_id integer not null,
            series_id text,
            start_date datetime not null,
            end_date datetime not null,
            state text not null,
            score real not null,

            foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
        )
    """
    )
    cursor.execute(
        f"""
            insert into new_DataServiceBadActorScores
            (id, data_service_view_id, series_id, start_date, end_date, state, score)
            select
                id,
                (select data_service_view_id from DataServiceViewEvaluations
                    where id = data_service_view_evaluation_id
                    order by evaluation_date asc
                    limit 1),
                series_id,
                start_date,
                end_date,
                state,
                score
            from DataServiceBadActorScore
            where data_service_view_evaluation_id in ({",".join(["?"] * len(view_evaluation_ids))})
        """,
        view_evaluation_ids,
    )
    cursor.execute(
        """
            drop table DataServiceBadActorScore;
        """
    )
    cursor.execute(
        """
            alter table new_DataServiceBadActorScores rename to DataServiceBadActorScores;
        """
    )


def _update_subscores(cursor: sqlite3.Cursor, view_evaluation_ids: list[int]):
    cursor.execute(
        """
        CREATE TABLE new_Subscores(
            id integer primary key autoincrement,
            data_service_view_id integer not null,
            series_id text,
            subscore_name text not null,
            subscore_result real not null, kpi_name text,

            foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
        )
    """
    )
    cursor.execute(
        f"""
            insert into new_Subscores
            (id, data_service_view_id, series_id, subscore_name, subscore_result)
            select
                id,
                (select data_service_view_id from DataServiceViewEvaluations
                    where id = data_service_view_evaluation_id
                    order by evaluation_date asc
                    limit 1),
                series_id,
                subscore_name,
                subscore_result
            from Subscores
            where data_service_view_evaluation_id in ({",".join(["?"] * len(view_evaluation_ids))})
        """,
        view_evaluation_ids,
    )
    cursor.execute(
        """
            drop table Subscores;
        """
    )
    cursor.execute(
        """
            alter table new_Subscores rename to Subscores;
        """
    )


def _update_excel_exports(cursor: sqlite3.Cursor, view_evaluation_ids: list[int]):
    cursor.execute(
        """
        CREATE TABLE new_ExcelExports(
            id integer primary key autoincrement,
            data_service_view_id integer not null,
            series_id text not null,
            filename text,
            file blob,
            date datetime,
            type text,
            start_date datetime,
            end_date datetime,

            foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
        )
    """
    )
    cursor.execute(
        f"""
            insert into new_ExcelExports
            (id, data_service_view_id, series_id, filename, file, date, type, start_date, end_date)
            select
                id,
                (select data_service_view_id from DataServiceViewEvaluations
                    where id = view_evaluation_id
                    order by evaluation_date asc
                    limit 1),
                series_id,
                filename,
                file,
                date,
                type,
                start_date,
                end_date
            from ExcelExports
            where view_evaluation_id in ({",".join(["?"] * len(view_evaluation_ids))})
        """,
        view_evaluation_ids,
    )
    cursor.execute(
        """
            drop table ExcelExports;
        """
    )
    cursor.execute(
        """
            alter table new_ExcelExports rename to ExcelExports;
        """
    )


def _update_bad_actor_kpi_score(cursor: sqlite3.Cursor, view_evaluation_ids: list[int]):
    cursor.execute(
        """
        CREATE TABLE new_DataServiceBadActorKPIScore(
            id integer primary key autoincrement,
            data_service_view_id integer not null,
            series_id text not null,
            start_date datetime not null,
            end_date datetime not null,
            kpi_name text not null,
            state text not null,
            score real not null,

            foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
        )
    """
    )
    cursor.execute(
        f"""
            insert into new_DataServiceBadActorKPIScore
            (id, data_service_view_id, series_id, start_date, end_date, kpi_name, state, score)
            select
                id,
                (select data_service_view_id from DataServiceViewEvaluations
                    where id = data_service_view_evaluation_id
                    order by evaluation_date asc
                    limit 1),
                series_id,
                start_date,
                end_date,
                kpi_name,
                state,
                score
            from DataServiceBadActorKPIScore
            where data_service_view_evaluation_id in ({",".join(["?"] * len(view_evaluation_ids))})
        """,
        view_evaluation_ids,
    )
    cursor.execute(
        """
            drop table DataServiceBadActorKPIScore;
        """
    )
    cursor.execute(
        """
            alter table new_DataServiceBadActorKPIScore rename to DataServiceBadActorKPIScore;
        """
    )


def _update_statistics(cursor: sqlite3.Cursor, view_evaluation_ids: list[int]):
    cursor.execute(
        """
        CREATE TABLE new_Statistics(
            id integer primary key autoincrement,
            data_service_view_id integer not null,
            name text not null,
            type text not null,
            value text not null,

            foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
        )
    """
    )
    cursor.execute(
        f"""
            insert into new_Statistics
            (id, data_service_view_id, name, type, value)
            select
                id,
                (select data_service_view_id from DataServiceViewEvaluations
                    where id = data_service_view_evaluation_id
                    order by evaluation_date asc
                    limit 1),
                name,
                type,
                value
            from Statistics
            where data_service_view_evaluation_id in ({",".join(["?"] * len(view_evaluation_ids))})
        """,
        view_evaluation_ids,
    )
    cursor.execute(
        """
            drop table Statistics;
        """
    )
    cursor.execute(
        """
            alter table new_Statistics rename to Statistics;
        """
    )


steps = [
    step(update_tables),
]
