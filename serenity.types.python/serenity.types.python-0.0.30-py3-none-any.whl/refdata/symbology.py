from serenity_types.utils.serialization import CamelModel


class SymbolAuthority(CamelModel):
    """
    An authoritative source for asset symbols.
    """

    short_name: str
    """
    Short name for the authority or symbology; used in enums.
    """

    description: str
    """
    Human-readable description of this authority or symbology.
    """


class XRefSymbol(CamelModel):
    """
    A simple that can be used for cross-referencing a Serenity asset ID to another,
    external source's symbols.
    """

    authority: str
    """
    The short name for the owning authority.
    """

    symbol: str
    """
    The corresponding symbol.
    """
