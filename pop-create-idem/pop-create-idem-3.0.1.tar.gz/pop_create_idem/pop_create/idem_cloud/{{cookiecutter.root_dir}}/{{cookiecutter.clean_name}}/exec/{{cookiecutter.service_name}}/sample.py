# This will put our "list_" function on the hub as "list"
# Func alias works around function names that shadow builtin python names
__func_alias__ = {"list_": "list"}


async def list_(hub, ctx):
    """Return a list of items"""
    return {
        "comment": "sample list",
        "ret": [],
        "status": True,
    }


async def get(hub, ctx, name: str):
    """Return a single named item"""
    return {
        "comment": "sample get",
        "ret": name,
        "status": True,
    }


async def create(hub, ctx, name: str, **kwargs):
    """Create an item with this name and these attributes"""
    return {
        "comment": "sample create",
        "ret": name,
        "status": True,
    }


async def delete(hub, ctx, name: str):
    """Delete the item with this name"""
    return {
        "comment": "sample delete",
        "ret": name,
        "status": True,
    }
