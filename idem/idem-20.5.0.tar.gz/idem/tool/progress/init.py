import copy
from typing import Iterable


def create(hub, iterable: Iterable, **kwargs) -> Iterable:
    """
    Create a progress bar that updates as the iterable is iterated.
    """
    # Only show this progress bar if the "--progress" flag was set
    enabled = hub.OPT.get("idem", {}).get("progress", False)
    if not enabled:
        return iterable

    progress_plugin = hub.OPT.get("idem", {}).get("progress_plugin", "tqdm")

    if not hasattr(hub.tool.progress, progress_plugin):
        hub.log.trace(f"No progress bar plugin '{progress_plugin}' is loaded")
        return iterable

    # Add other options to the progress bar from config
    progress_opts = copy.copy(hub.OPT.get("idem", {}).get("progress_options", {}))
    if not isinstance(progress_opts, dict):
        hub.log.debug(
            f"'hub.OPT.idem.progress_options' is not a dictionary: {type(progress_opts)}"
        )
        progress_opts = {}

    # Merge config options with explicitly passed options
    progress_opts.update(kwargs)

    progress_bar = hub.tool.progress[progress_plugin].create(
        iterable,
        **progress_opts,
    )

    return progress_bar


def update(hub, progress_bar: Iterable, **kwargs):
    """
    Update the progress bar through the progress plugin
    """
    # Only show this progress bar if the "--progress" flag was set
    enabled = hub.OPT.get("idem", {}).get("progress", False)
    if not enabled:
        return

    progress_plugin = hub.OPT.get("idem", {}).get("progress_plugin", "tqdm")

    if not hasattr(hub.tool.progress, progress_plugin):
        hub.log.trace(f"No progress bar plugin '{progress_plugin}' is loaded")
        return

    hub.tool.progress[progress_plugin].update(
        progress_bar,
        **kwargs,
    )
