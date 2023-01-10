import re
from typing import Any
from typing import Dict
from typing import List
from typing import Set

KEYWORDS = ["include"]


async def apply(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
    cfn: str,
    resolved: Set[str],
) -> List[str]:
    """
    Parse through the includes and download not-yet-resolved includes

    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    :param cfn: The cache file name, or the location of sls within the given sources
    :param resolved: a set of refs that have already been resolved
    """
    # Maintain unresolved as a list to keep the sls file order. This order is used during param override.
    unresolved = []
    include = state.pop("include", [])

    if not isinstance(include, List):
        hub.idem.RUNS[name]["errors"].append(
            f"Include Declaration in SLS {sls_ref} is not formed as a list but as a {type(include)}"
        )
        return unresolved

    # Handle relative includes
    for inc_sls in include:
        # If the inc_sls starts with a dot then it is a relative include
        if inc_sls.startswith("."):
            match = re.match(r"^(\.+)(.*)$", inc_sls)

            # "levels" indicates the number of parents that need to be considered relative to the resolved source
            levels, inc_ref = match.groups()

            # The number of "."s indicates how many parents of the sls_ref we need to remove
            level_count = len(levels)

            # Transform the relative ref into an absolute ref
            p_comps = sls_ref.split(".")
            if level_count > len(p_comps):
                hub.idem.RUNS[name]["errors"].append(
                    f'Attempted relative include of "{inc_sls}" within SLS {sls_ref} goes beyond top level package'
                )
                continue
            inc_sls = ".".join(p_comps[:-level_count] + [inc_ref])

        # Make sure unresolved contains a unique set of sls files' reference
        if inc_sls not in resolved and inc_sls not in unresolved:
            unresolved.append(inc_sls)

    return unresolved
