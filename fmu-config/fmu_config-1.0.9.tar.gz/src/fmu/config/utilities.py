"""Module with some simple functions, e.g. for parsing for YAML into RMS
"""

# for ordered dicts!
from fmu.config import oyaml as yaml


def yaml_load(filename, safe=True, tool=None):
    """Load as YAML file, return a dictionary of type OrderedDict which is the config.

    Returning an ordered dictionary is a main feature of this loader. It makes it much
    easier to compare the dictionaries returned.

    Args:
        filename (str): Name of file (YAML formatted)
        safe (bool): If True (default), then use `safe_load`
        tool (str): Refers to a particular main section in the config.
            Default is None, which measn 'all'.

    Example::
        >>> import fmu.config.utilities as utils
        >>> cfg = utils.yaml_load('somefile.yml')

    """

    with open(filename, "r", encoding="utf-8") as stream:
        if safe:
            cfg = yaml.safe_load(stream)
        else:
            cfg = yaml.load(stream)

    if tool is not None:
        try:
            newcfg = cfg[tool]
            cfg = newcfg
        except Exception as exc:  # pylint: disable=broad-except
            print("Cannot import: {}".format(exc))
            return None

    return cfg


def compare_yaml_files(file1, file2):
    """Compare two YAML files and return True if they are equal

    Args:
        file1 (str): Path to file1
        file2 (str): Path to file2
    """

    cfg1 = yaml_load(file1)
    cfg2 = yaml_load(file2)

    cfg1txt = yaml.dump(cfg1)
    cfg2txt = yaml.dump(cfg2)

    if cfg1txt == cfg2txt:
        return True

    return False


def compare_text_files(file1, file2, comments="//"):
    """Compare two text files, e.g. IPL and return True if they are equal

    Lines starting with comments indicator will be discarded

    Args:
        file1 (str): Path to file1
        file2 (str): Path to file2
        comments (str): How comment lines are indicated, e.g. "//" for IPL
    """

    text1 = ""
    text2 = ""

    with open(file1, "r", encoding="utf-8") as fil1:
        for line in fil1:
            if not line.startswith(comments):
                text1 += line

    with open(file2, "r", encoding="utf-8") as fil2:
        for line in fil2:
            if not line.startswith(comments):
                text2 += line

    if text1 == text2:
        return True

    return False
