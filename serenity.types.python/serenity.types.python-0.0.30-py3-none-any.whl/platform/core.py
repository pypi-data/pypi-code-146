from typing import List

from serenity_types.utils.serialization import CamelModel


class LookupRow(CamelModel):
    """
    A single mapping from a server-side enum to supporting metadata for Serenity UX.
    """

    key: str
    """
    The name of the enum in code, e.g. FOO_BAR.
    """

    display_name: str
    """
    A human-readable short name for the name, e.g. Foobarity.
    """

    tooltip: str
    """
    A human-readable description of this particular key suitable for tooltips, e.g. “A statistical measure of
    fundamental foobariosity; may be purple.”
    """


class LookupTable(CamelModel):
    """
    A simple collection of enum metadata to be used by the Serenity front-end to map API codes to human-readable
    strings, tooltips, etc..
    """

    table_name: str
    """
    Short code for the lookup table, e.g. ASSET_CLASSES.
    """

    rows: List[LookupRow]
    """
    All rows in this particular lookup table.
    """
