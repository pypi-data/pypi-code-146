from pathlib import Path

import Xponge.analysis.md_analysis as xmda

from . import Parser
from .. import Model, mda


class XpongeResidueParser(Parser, formats="xponge_residue"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        u = mda.Universe(m, topology_format=xmda.XpongeResidueReader, **kwargs)
        atoms = [{"elem": atom.element,
                  "atom": atom.name,
                  "resi": int(atom.resid),
                  "resn": atom.resname,
                  "x": float(atom.position[0]),
                  "y": float(atom.position[1]),
                  "z": float(atom.position[2]),
                  "bonds":[]} for atom in u.atoms]
        for bond in u.bonds:
            i, j = [ int(atom.id) - 1 for atom in bond.atoms]
            atoms[i]["bonds"].append(j)
        model = Model(name=m.name, u=u)
        return atoms, model

class XpongeMoleculeParser(Parser, formats="xponge_molecule"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        u = mda.Universe(m, topology_format=xmda.XpongeMoleculeReader, **kwargs)
        atoms = [{"elem": atom.element,
                  "atom": atom.name,
                  "resi": int(atom.resid),
                  "resn": atom.resname,
                  "x": float(atom.position[0]),
                  "y": float(atom.position[1]),
                  "z": float(atom.position[2]),
                  "bonds":[]} for atom in u.atoms]
        for bond in u.bonds:
            i, j = [ int(atom.id) - 1 for atom in bond.atoms]
            atoms[i]["bonds"].append(j)

        model = Model(name=m.name, u=u)
        return atoms, model

class SpongeInputParser(Parser, formats="sponge_mass"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        if m.endswith("_mass.txt"):
            m = m.replace("_mass.txt", "")
        u = mda.Universe(m,
                         topology_format=xmda.SpongeInputReader,
                         format=xmda.SpongeNoneReader,
                         **kwargs)
        atoms = [{"elem": atom.element,
                  "atom": atom.name,
                  "resi": int(atom.resid),
                  "bonds":[]} for atom in u.atoms]
        for bond in u.bonds:
            i, j = [ int(atom.id) - 1 for atom in bond.atoms]
            atoms[i]["bonds"].append(j)
        model = Model(name=Path(m).stem, u=u)
        return atoms, model

class SpongeTrajectoryParser(Parser, formats="dat"):
    @staticmethod
    def Traj_Parse(traj):
        path = Path(traj)
        if path.name == "mdcrd.dat":
            box = path.with_name("mdbox.txt")
        else:
            box = path.with_suffix(".box")
        return xmda.SpongeTrajectoryReader.with_arguments(box=str(box))

class SpongeCoordinateParser(Parser, formats="sponge_coordinate"):
    @staticmethod
    def Traj_Parse(traj):
        return xmda.SpongeCoordinateReader

class H5MDParser(Parser, formats="h5md"):
    @staticmethod
    def Traj_Parse(traj):
        return "h5md"
