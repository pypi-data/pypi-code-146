from typing import List
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class AssetSectorMapping(CamelModel):
    """
    A single entry in a particular sectory taxonomy mapping a single asset to a sector path.
    """

    asset_id: UUID
    """
    Unique ID for this asset in the Asset Master.
    """

    taxonomy_id: UUID
    """
    Unique ID for the sector taxonomy.
    """

    sector_levels: List[str]
    """
    Fully-qualified sector level to the asset, e.g. something like [”Foo Sector”, “Bar Sub-sector”, “Baz Industry”].
    """


class SectorTaxonomy(CamelModel):
    """
    A single sector taxonomy (hierarchy) known to the system.
    """

    taxonomy_id: UUID
    """
    Unique ID for the sector taxonomy.
    """

    display_name: str
    """
    Short descriptive name, e.g. DATS
    """

    sector_levels: List[str]
    """
    List of names of level types supported, e.g. [”Sector”, “Sub-sector”, “Industry”] or [”Sector”, “Sub-sector”].
    """
