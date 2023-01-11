""" """
import zipfile
import tarfile
import pathlib

from .solver_log_parser import get_regex_result, HybridMIPSolverParser, HybridQUBOSolverParser, HybridParser


def get_packed_file_type(instance: pathlib.Path) -> str:
    """ determine file type of file in archive <instance>
        handles: .zip, .tar.gz
    """

    # TODO: account for more than one file in archive ?
    if zipfile.is_zipfile(instance):
        with zipfile.ZipFile(instance, "r") as zipf:
            filename = zipf.infolist()[0].filename

    else:
        try:
            tarf = tarfile.open(instance, "r|gz")
            filename = tarf.getmembers()[0].name
        except IOError:
            # not a tar.gz file
            pass

    file_ext = '.' + filename.split('.')[-1]
    return file_ext


def get_solver_type_ext(instance: pathlib.Path) -> str:
    """ determine solver type from file extension"""
    file_ext = instance.suffix

    unpacked_ext = {".lp": "LP",
                    ".mps": "MPS",
                    ".qubo": "QUBO"
                    }

    packed_ext = [".zip",
                  ".gz"
                  ]

    if file_ext in packed_ext:
        file_ext = get_packed_file_type(instance)

    if file_ext in unpacked_ext:
        solvertype = unpacked_ext[file_ext]

    else:
        raise ValueError("Unknown file type")
    return solvertype


def get_solver_type(log: str) -> str:
    """  get solver type from solver log """

    if get_regex_result(r"Quantagonia HybridSolver.\n", log):
        isHybridMIP = bool(get_regex_result(r"Solution sta", log))
        isHybridQUBO = bool(get_regex_result(r"solver results", log))
        isHybridSolver = bool(get_regex_result(r"Model   status(\s).*: ", log))

    else:
        raise ValueError("error parsing solver log")
    types = ["HybridMIP", "HybridQUBO", "Hybrid"]
    types_found = [isHybridMIP, isHybridQUBO, isHybridSolver]

    pos = [i for i, x in enumerate(types_found) if x]

    if not any(types) or len(pos) == 0:
        raise ValueError("unable to determine solver type")

    return types[pos[0]]


def Factory(log: str, instance: pathlib.Path, solver_override: str = None):
    """  """

    solvertype = get_solver_type(log)
    parsers = {
        "HybridMIP": HybridMIPSolverParser,
        "HybridQUBO": HybridQUBOSolverParser,
        "Hybrid": HybridParser
    }
    return parsers[solvertype](log, instance)
