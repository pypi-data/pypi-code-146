import sqlite3

from yoyo import step

__depends__ = {"023__series_sets"}

RELATIVE_DATES = {
    "Last 60 minutes": "Most recent results (60 minutes)",
    "Last 24 hours": "Most recent results (24 hours)",
    "Yesterday": "Most recent results (24 hours)",
    "Last 7 days": "Most recent results (7 days)",
    "Last 30 days": "Most recent results (30 days)",
    "Last 3 months": "Most recent results (30 days)",
    "Last 12 months": "Most recent results (30 days)",
    "Last week": "Most recent results (7 days)",
    "Last month": "Most recent results (30 days)",
    "Last quarter": "Most recent results (30 days)",
    "Last year": "Most recent results (30 days)",
}


def update_tables(db: sqlite3.Connection):
    cursor = db.cursor()
    _update_relative_scores(cursor)


def _update_relative_scores(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        select id, relative_date from DataServices where relative_date is not NULL
    """
    )
    cursor.executemany(
        """
            update DataServices set relative_date = ?
                where id = ?
        """,
        [
            [RELATIVE_DATES[relative_date], db_id]
            for db_id, relative_date in cursor.fetchall()
        ],
    )


steps = [
    step(update_tables),
]
