from lnschema_core.dev.id import base62, pipeline, run


def bfx_pipeline() -> str:
    """Data object: 9 base62."""
    return pipeline()


def bfx_run() -> str:
    """Data object: 20 base62."""
    return run()


def bfxmeta() -> str:
    """Data object: 21 base62."""
    return base62(n_char=21)
