"""Useful functions for interacting with GAIuS"""

def create_gdf(strings=None, vectors=None, emotives=None):
    """
    Create GDF using supplied list of strings, vectors, and/or emotives
    """
    gdf = {
        "vectors": [] if vectors is None else vectors,
        "strings": [] if strings is None else strings,
        "emotives": {} if emotives is None else emotives
    }
    return gdf