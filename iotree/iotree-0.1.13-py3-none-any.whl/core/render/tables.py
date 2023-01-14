import rich
from typing import Any, Dict, List, Optional, Union


from iotree.utils.paths import (
    package_dir, base_dir, config_dir, safe_config_load
)

symbols, themes, user_infos, local_config = safe_config_load()

def treeThemeToTable(theme: Union[str, Dict[str, Any]] = "default"):
    """Convert a theme fit for a tree to one for a rich.table.Table object."""
    if isinstance(theme, str):
        theme = themes[theme]
    table_theme = {
        "header": theme["node"][0],
        "rows": theme["node"][1:3],
    }
    return table_theme

def recordFormatting(record: Dict[str, Any], columns: List[str]) -> Dict[str, Any]:
    """Add empty column values to a partial record + convert values to strings.
    
    Also orders the columns in the same order as the columns list."""
    lrow = []
    for col in columns:
        if col not in record.keys():
            lrow.append("")
        else:
            lrow.append(str(record[col]))
    return lrow

def tableFromRecords(
    records: List[Dict[str, Any]],
    title: Optional[str] = "Table of records",
    theme: Optional[str] = None,
    ) -> rich.table.Table:
    theme = treeThemeToTable(theme)
    tab = rich.table.Table(
        title=title,
        header_style=theme["header"],
        box=rich.box.ROUNDED,
        row_styles=theme["rows"]
        )
    columns = list(records[0].keys())
    for col in columns:
        tab.add_column(col, justify="center")
    for record in records:
        tab.add_row(*recordFormatting(record, columns))
    return tab