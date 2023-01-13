import sqlite3

from yoyo import step
from timeseer import ResourceOrigin

from timeseer.kpi_sets import DefaultKPISet

__depends__ = {"007__change_to_kpi_set"}


def rename_default_kpi_set(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute(
        """
            update KPISets set name = ?, origin = ?
            where name = 'default' and origin = 'default'
        """,
        [DefaultKPISet.DEFAULT.value, ResourceOrigin.DEFAULT.value],
    )


steps = [
    step(rename_default_kpi_set),
]
