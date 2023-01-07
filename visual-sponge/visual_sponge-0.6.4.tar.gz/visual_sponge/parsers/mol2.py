from pathlib import Path

from . import Parser
from .. import Model, mda
from ..utils import guess_element

class MOL2Parser(Parser, formats="mol2"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        u = mda.Universe(m, topology_format="MOL2", **kwargs)
        atoms = [{"elem": atom.element or guess_element(atom.name),
                  "x": float(atom.position[0]),
                  "y": float(atom.position[1]),
                  "z": float(atom.position[2]),
                  "bonds":[],
                  "atom": atom.name,
                  "resi": int(atom.resid),
                  "resn": atom.resname} for atom in u.atoms]
        for bond in u.bonds:
            i, j = [ int(atom.id) - 1 for atom in bond.atoms]
            atoms[i]["bonds"].append(j)
        model = Model(name=Path(m).stem, u=u)
        model.traj_files.append((m, "MOL2"))
        return atoms, model

    @staticmethod
    def Traj_Parse(traj):
        return "MOL2"
