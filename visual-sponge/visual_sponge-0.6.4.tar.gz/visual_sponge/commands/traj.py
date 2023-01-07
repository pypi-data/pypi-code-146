from pathlib import Path

from .. import MACROS, Model, ChainReader
from ..parsers import Parser

def TRAJ(traj, format_=None, m=None, append=False, **kwargs):
    if m is None:
        m = Model.WORKING
        if m is None:
            raise ValueError("Model not provided")
    elif isinstance(m, int):
        m = Model.models[m]
    if format_ is None:
        if isinstance(traj, str):
            path = Path(traj)
            suffix = path.suffix[1:]
            if suffix != "txt":
                format_ = suffix
            elif traj.endswith("_coordinate.txt"):
                format_ = "sponge_coordinate"
            else:
                raise NotImplementedError
        else:
            raise TypeError
    parser = Parser(format_)
    reader = parser.Traj_Parse(traj)
    if reader:
        reader = (traj, reader)
    else:
        reader = traj
    if not append:
        m.traj_files = [reader]
    else:
        m.traj_files.append(reader)
    print(m.traj_files)
    m.u.trajectory = ChainReader(m.traj_files, n_atoms=m.u.trajectory.n_atoms, **kwargs)
    MACROS.CMD = [{"cmd": "TRAJ", "mid":Model.WORKING.id},
                  {"cmd": "DEFAULT", "mid":Model.WORKING.id}]
    return m
