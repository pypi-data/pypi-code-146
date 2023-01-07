from pathlib import Path

from .. import MACROS, Model, Xponge
from ..parsers import Parser

def MODEL(m, format_=None, **kwargs):
    if format_ is None:
        if isinstance(m, str):
            path = Path(m)
            suffix = path.suffix
            if suffix != ".txt":
                format_ = suffix[1:]
            elif "_" in str(path.stem) and str(path.stem).split("_")[-1] == "mass":
                format_ = "sponge_mass"
            else:
                raise NotImplementedError
        elif isinstance(m, (Xponge.ResidueType, Xponge.Residue)):
            format_ = "xponge_residue"
        elif isinstance(m, Xponge.Molecule):
            format_ = "xponge_molecule"
        else:
            raise TypeError(f"type of {m} {type(m)} is not a valid input")
    parser = Parser(format_)
    atoms, model = parser.Model_Parse(m, **kwargs)
    Model.WORKING = model
    MACROS.CMD = [{"cmd":"MODEL", "atoms": atoms, "name": model.name},
                  {"cmd":"DEFAULT", "mid":Model.WORKING.id}]
    return model
