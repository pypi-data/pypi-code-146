import sqlite3

from datetime import datetime, timezone

from yoyo import step

__depends__ = {"038__data_service_view_evaluation"}


def _populate_evaluations_from_views(connection: sqlite3.Connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        select id, last_evaluation_date from DataServiceViews
    """
    )
    view_evaluation_dates = list(cursor)
    for view_id, evaluation_date in view_evaluation_dates:
        if evaluation_date is None:
            evaluation_date = datetime.now(tz=timezone.utc)

        cursor.execute(
            """
            select count(*) from DataServiceViewEvaluations where data_service_view_id = ?
        """,
            [view_id],
        )
        (count,) = cursor.fetchone()
        if count == 0:
            cursor.execute(
                """
                insert into DataServiceViewEvaluations (data_service_view_id, evaluation_date) values (?, ?)
            """,
                [view_id, evaluation_date],
            )


steps = [
    step(_populate_evaluations_from_views),
]
