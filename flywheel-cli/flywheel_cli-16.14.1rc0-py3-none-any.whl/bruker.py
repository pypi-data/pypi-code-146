"""Bruker operations module"""
import logging

from flywheel_migration import bruker

from .util import set_nested_attr

log = logging.getLogger(__name__)


def extract_bruker_metadata_fn(filename, keys):
    """Create a function that will open filename and extract bruker parameters.

    Arguments:
        filename (str): The name of the file to open (e.g. subject)
        keys (dict): The mapping of src_key to dst where dst is a key or a function
            that returns a key and a value, given an input value.

    Returns:
        function: The function that will extract bruker params as metadata
    """

    def extract_metadata(_, context, walker, path):
        file_path = walker.combine(path, filename)
        log.debug(f"Attempting to import params from: {file_path}")

        try:
            with walker.open(file_path, mode="r", encoding="utf-8") as file_obj:
                params = bruker.parse_bruker_params(file_obj)

                paravision_version = params.get("PARAVISION_version", "").split(".")[0]
                if context.get("packfile", None) and paravision_version:
                    context["packfile"] = f"pv{paravision_version}"

            for src_key, dst_key in keys.items():
                if src_key in params:
                    value = params[src_key]
                    if callable(dst_key):
                        ret = dst_key(value, path=file_path, context=context)
                        if ret:
                            dst_key, value = ret
                        else:
                            dst_key = None

                    if dst_key:
                        set_nested_attr(context, dst_key, value)
        except FileNotFoundError:
            log.info(f"No param file located at: {file_path}")
        except IOError as exc:
            log.error(f"Unable to process params file {file_path}: {exc}")

    return extract_metadata


if __name__ == "__main__":
    # pylint: disable=invalid-name
    import argparse

    parser = argparse.ArgumentParser(
        description="Read and print bruker parameters file"
    )
    parser.add_argument("path", help="The path to the file to read")

    args = parser.parse_args()

    with open(args.path, "r", encoding="utf-8") as f:
        parse_result = bruker.parse_bruker_params(f)

    for result_key, result_value in parse_result.items():
        print(f"{result_key} = {result_value}")
