"""Utility functions for interacting with GAIuS"""
import warnings

def create_gdf(strings=None, vectors=None, emotives=None, metadata=None):
    """Create GDF using supplied list of strings, vectors, emotives, and/or metadata

    Args:
        strings (list, optional): Used to provide symbols as string data to GAIuS. Defaults to None.
        vectors (list, optional): Used to input vector data to GAIuS. Defaults to None.
        emotives (dict, optional): Used to provide emotional data to GAIuS. Defaults to None.
        metadata (dict, optional): Used to provide miscellaneous data to GAIuS. Defaults to None.

    Returns:
        GDF: A dictionary representing the GDF
        
    .. warning::
        If fields provided are not of the type expected, a warning will be raised, but the GDF will still
        be made with the improper format
    """
    gdf = {
        "vectors": [] if vectors is None else vectors,
        "strings": [] if strings is None else strings,
        "emotives": {} if emotives is None else emotives,
        "metadata": {} if metadata is None else metadata
    }
    
    if not isinstance(gdf['vectors'], list):
        warnings.warn(UserWarning(f"vectors field is of type {type(gdf['vectors'])}, expected list"))
    if not isinstance(gdf['strings'], list):
        warnings.warn(UserWarning(f"strings field is of type {type(gdf['strings'])}, expected list"))
    if not isinstance(gdf['emotives'], dict):
        warnings.warn(UserWarning(f"emotives field is of type {type(gdf['emotives'])}, expected dict"))
    if not isinstance(gdf['metadata'], dict):
        warnings.warn(UserWarning(f"metadata field is of type {type(gdf['metadata'])}, expected dict"))
    
    return gdf
