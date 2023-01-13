from typing import Any, Dict, List

import sqlalchemy.engine.row


def sql_rows_to_json(rows: List[sqlalchemy.engine.row.Row]) -> Dict[str, Any]:
    if not rows:
        return {}
    keys = [key for key in rows[0].keys()]
    json_rows = []
    for row in rows:
        json_rows.append({key: row[key] for key in keys})
    return json_rows
