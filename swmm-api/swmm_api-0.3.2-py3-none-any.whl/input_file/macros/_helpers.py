from ..section_labels import STORAGE, OUTFALLS, OUTLETS, PUMPS, XSECTIONS


def get_used_curves(inp):
    """
    Get the used curves from the sections [STORAGE, OUTFALLS, OUTLETS, PUMPS and XSECTIONS].

    Args:
        inp (swmm_api.SwmmInput): inp-file data

    Returns:
        set[str]: set of names of used curves
    """
    used_curves = set()
    for section in [STORAGE, OUTFALLS, OUTLETS, PUMPS, XSECTIONS]:
        if section in inp:
            for name in inp[section]:
                if isinstance(inp[section][name].curve_name, str):
                    if (section == PUMPS) and (inp[section][name].curve_name == '*'):
                        continue
                    used_curves.add(inp[section][name].curve_name)
    return used_curves
