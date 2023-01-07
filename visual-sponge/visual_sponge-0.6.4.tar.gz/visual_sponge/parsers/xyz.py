from pathlib import Path

from . import Parser
from .. import Model, mda
from ..utils import guess_bonds, guess_element


class XYZParser(Parser, formats="xyz"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        u = mda.Universe(m, topology_format="XYZ", **kwargs)
        atoms = [{"elem": guess_element(atom.element),
                  "atom": atom.element,
                  "x": float(atom.position[0]),
                  "y": float(atom.position[1]),
                  "z": float(atom.position[2]),
                  "bonds":[]} for atom in u.atoms]
        guess_bonds(u, atoms, 1.6)
        model = Model(name=Path(m).stem, u=u)
        model.traj_files.append((m, "XYZ"))
        return atoms, model

    @staticmethod
    def Traj_Parse(traj):
        return "XYZ"
