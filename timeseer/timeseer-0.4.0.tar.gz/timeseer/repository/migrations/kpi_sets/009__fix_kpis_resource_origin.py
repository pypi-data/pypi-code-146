import sqlite3

from yoyo import step

__depends__ = {"008__rename_default_kpi_set"}


def rename_default_kpi_set(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute(
        """
            update KPISets set origin = 'default' where origin in ('control loop', 'preset')
        """
    )
    cursor.execute(
        """
            update KPIS set origin = 'default' where origin in ('control loop', 'preset')
        """
    )


steps = [
    step(rename_default_kpi_set),
]
