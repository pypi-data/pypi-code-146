from pathlib import Path
from importlib import import_module

import Xponge.analysis.md_analysis as xmda

from .. import Model, mda
from ..utils import guess_element, guess_bonds

__all__ = ["Parser", "DefaultParser"]

class Parser():
    formats = {}
    def __init_subclass__(cls, formats):
        if isinstance(formats, str):
            Parser.formats[formats] = cls
        else:
            Parser.formats.update({}.fromkeys(formats, cls))

    def __new__(cls, format_):
        return cls.formats.get(format_, cls.formats["default"])

class DefaultParser(Parser, formats="default"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        u = mda.Universe(m, **kwargs)
        try:
            u.trajectory
        except AttributeError:
            u = mda.Universe(m, m, format=xmda.SpongeNoneReader, **kwargs)
        atoms = [{"bonds":[]} for atom in u.atoms]
        if hasattr(u.atoms, "positions"):
            for i, atom in enumerate(u.atoms):
                atoms[i]["x"] = float(atom.position[0])
                atoms[i]["y"] = float(atom.position[1])
                atoms[i]["z"] = float(atom.position[2])
        if hasattr(u.atoms, "names") and hasattr(u.atoms, "elements"):
            for i, atom in enumerate(u.atoms):
                atoms[i]["atom"] = atom.name
                atoms[i]["elem"] = atom.element
        elif not hasattr(u.atoms, "names") and hasattr(u.atoms, "elements"):
            for i, atom in enumerate(u.atoms):
                atoms[i]["atom"] = atom.element
                atoms[i]["elem"] = guess_element(atom.element)
        elif hasattr(u.atoms, "names") and not hasattr(u.atoms, "elements"):
            for i, atom in enumerate(u.atoms):
                atoms[i]["atom"] = atom.name
                atoms[i]["elem"] = guess_element(atom.name)
        else:
            raise AttributeError("No atom names or elements found for the model")
        if hasattr(u.atoms, "resids"):
            for i, atom in enumerate(u.atoms):
                atoms[i]["resi"] = int(atom.resid)
        if hasattr(u.atoms, "resnames"):
            for i, atom in enumerate(u.atoms):
                atoms[i]["resn"] = atom.resname
        if hasattr(u, "bonds"):
            id2index = {atomi.id : i for i, atomi in enumerate(u.atoms)}
            for bond in u.bonds:
                i, j = [ id2index[atom.id] for atom in bond.atoms]
                atoms[i]["bonds"].append(j)
        elif hasattr(u.atoms, "positions"):
            guess_bonds(u, atoms, 1.6)
        model = Model(name=Path(m).stem, u=u)
        if hasattr(u.atoms, "positions"):
            model.traj_files.append(m)
        return atoms, model

    @staticmethod
    def Traj_Parse(traj):
        pass

for file in Path(__file__).parent.rglob("*.py"):
    module_name = file.stem
    if module_name != "__init__":
        module = import_module(f"{__name__}.{module_name}")
