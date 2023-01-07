from .. import MACROS, Xponge

def VERSION():
    """
        This function shows the version of Visual Sponge and Xponge
    """
    return f"""Visual Sponge{MACROS.localization(' Version')}: {MACROS.VERSION}
Xponge{MACROS.localization(' Version')}: {Xponge.__version__}"""
