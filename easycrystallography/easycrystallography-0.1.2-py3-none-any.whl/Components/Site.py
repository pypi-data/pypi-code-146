#  SPDX-FileCopyrightText: 2022 easyCrystallography contributors  <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022 Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>
#
from __future__ import annotations

__author__ = 'github.com/wardsimon'
__version__ = '0.1.0'

from typing import List, Union, ClassVar, TypeVar, Optional, Dict, TYPE_CHECKING

from easyCore import np
from easyCore.Objects.Variable import Descriptor, Parameter
from easyCore.Objects.ObjectClasses import BaseObj
from easyCore.Objects.Groups import BaseCollection
from easyCore.Utils.io.star import StarLoop

from .Lattice import PeriodicLattice
from .Specie import Specie

if TYPE_CHECKING:
    from easyCore.Utils.typing import iF


_SITE_DETAILS = {
    "label": {
        "value": "H",
        "description": "A unique identifier for a particular site in the crystal",
        "url": "https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_label.html",
    },
    "position": {
        "value": 0.0,
        "description": "Atom-site coordinate as fractions of the unit cell length.",
        "url": "https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_fract_.html",
        "fixed": True,
    },
    "occupancy": {
        "value": 1.0,
        "description": "The fraction of the atom type present at this site.",
        "url": "https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_occupancy.html",
        "fixed": True,
    },
}

S = TypeVar("S", bound="Site")


class Site(BaseObj):

    _CIF_CONVERSIONS = [
        ["label", "atom_site_label"],
        ["specie", "atom_site_type_symbol"],
        ["occupancy", "atom_site_occupancy"],
        ["fract_x", "atom_site_fract_x"],
        ["fract_y", "atom_site_fract_y"],
        ["fract_z", "atom_site_fract_z"],
    ]

    label: ClassVar[Descriptor]
    specie: ClassVar[Specie]
    occupancy: ClassVar[Parameter]
    fract_x: ClassVar[Parameter]
    fract_y: ClassVar[Parameter]
    fract_z: ClassVar[Parameter]

    def __init__(
        self,
        label: Optional[Union[str, Descriptor]] = None,
        specie: Optional[Union[str, Specie]] = None,
        occupancy: Optional[Union[float, Parameter]] = None,
        fract_x: Optional[Union[float, Parameter]] = None,
        fract_y: Optional[Union[float, Parameter]] = None,
        fract_z: Optional[Union[float, Parameter]] = None,
        interface: Optional[iF] = None,
        **kwargs,
    ):

        super(Site, self).__init__(
            "site",
            label=Descriptor("label", **_SITE_DETAILS["label"]),
            specie=Specie(_SITE_DETAILS["label"]["value"]),
            occupancy=Parameter("occupancy", **_SITE_DETAILS["occupancy"]),
            fract_x=Parameter("fract_x", **_SITE_DETAILS["position"]),
            fract_y=Parameter("fract_y", **_SITE_DETAILS["position"]),
            fract_z=Parameter("fract_z", **_SITE_DETAILS["position"]),
            **kwargs,
        )
        if label is not None:
            self.label = label
        if specie is not None:
            self.specie = specie
        else:
            if label is not None:
                self.specie = label
        if occupancy is not None:
            self.occupancy = occupancy
        if fract_x is not None:
            self.fract_x = fract_x
        if fract_y is not None:
            self.fract_y = fract_y
        if fract_z is not None:
            self.fract_z = fract_z
        self.interface = interface

    @classmethod
    def default(cls, *args, interface: Optional[iF] = None, **kwargs):
        return cls(*args, **kwargs, interface=interface)

    @classmethod
    def from_pars(
        cls,
        label: str,
        specie: str,
        occupancy: float = _SITE_DETAILS["occupancy"]["value"],
        fract_x: float = _SITE_DETAILS["position"]["value"],
        fract_y: float = _SITE_DETAILS["position"]["value"],
        fract_z: float = _SITE_DETAILS["position"]["value"],
        interface: Optional[iF] = None,
        **kwargs
    ):
        return cls(
            label,
            specie,
            occupancy,
            fract_x,
            fract_y,
            fract_z,
            interface=interface,
            **kwargs
        )

    def __repr__(self) -> str:
        return (
            f"Atom {self.name} ({self.specie.raw_value}) @"
            f" ({self.fract_x.raw_value}, {self.fract_y.raw_value}, {self.fract_z.raw_value})"
        )

    @property
    def name(self) -> str:
        return self.label.raw_value

    @property
    def fract_coords(self) -> np.ndarray:
        """
        Get the current sites fractional co-ordinates as an array

        :return: Array containing fractional co-ordinates
        :rtype: np.ndarray
        """
        return np.array(
            [self.fract_x.raw_value, self.fract_y.raw_value, self.fract_z.raw_value]
        )

    def fract_distance(self, other_site: S) -> float:
        """
        Get the distance between two sites

        :param other_site: Second site
        :param other_site: Second site
        :type other_site: Site
        :return: Distance between 2 sites
        :rtype: float
        """
        return np.linalg.norm(other_site.fract_coords - self.fract_coords)

    @property
    def x(self) -> Parameter:
        return self.fract_x

    @property
    def y(self) -> Parameter:
        return self.fract_y

    @property
    def z(self) -> Parameter:
        return self.fract_z

    @property
    def is_magnetic(self) -> bool:
        return getattr(self.specie, 'spin', None) is not None or hasattr(self, 'msp')


class PeriodicSite(Site):
    def __init__(
        self,
        lattice: PeriodicLattice,
        label: Descriptor,
        specie: Specie,
        occupancy: Parameter,
        fract_x: Parameter,
        fract_y: Parameter,
        fract_z: Parameter,
        interface: Optional[iF] = None,
        **kwargs,
    ):
        super(PeriodicSite, self).__init__(
            label, specie, occupancy, fract_x, fract_y, fract_z, interface, **kwargs
        )
        self.lattice = lattice

    @staticmethod
    def _from_site_kwargs(lattice: PeriodicLattice, site: S) -> Dict[str, float]:
        return {
            "lattice": lattice,
            "label": site.label,
            "specie": site.specie,
            "occupancy": site.occupancy,
            "fract_x": site.fract_x,
            "fract_y": site.fract_y,
            "fract_z": site.fract_z,
            "interface": site.interface,
        }

    @classmethod
    def from_site(cls, lattice: PeriodicLattice, site: S) -> S:
        kwargs = cls._from_site_kwargs(lattice, site)
        return cls(**kwargs)

    def get_orbit(self) -> np.ndarray:
        """
        Generate all orbits for a given fractional position.

        """
        sym_op = self.lattice.spacegroup._sg_data.get_orbit
        return sym_op(self.fract_coords)

    @property
    def cart_coords(self) -> np.ndarray:
        """
        Get the atomic position in Cartesian form.
        :return:
        :rtype:
        """
        return self.lattice.get_cartesian_coords(self.fract_coords)


class Atoms(BaseCollection):

    _SITE_CLASS = Site

    def __init__(self, name: str, *args, interface: Optional[iF] = None, **kwargs):
        if not isinstance(name, str):
            raise TypeError("A `name` for this collection must be given in string form")
        super(Atoms, self).__init__(name, *args, **kwargs)
        self.interface = interface
        self._kwargs._stack_enabled = True

    def __repr__(self) -> str:
        return f"Collection of {len(self)} sites."

    def __getitem__(
        self, idx: Union[int, slice]
    ) -> Union[Parameter, Descriptor, BaseObj, "BaseCollection"]:
        if isinstance(idx, str) and idx in self.atom_labels:
            idx = self.atom_labels.index(idx)
        return super(Atoms, self).__getitem__(idx)

    def __delitem__(self, key: Union[int, str]):
        if isinstance(key, str) and key in self.atom_labels:
            key = self.atom_labels.index(key)
        return super(Atoms, self).__delitem__(key)

    def append(self, item: S):
        if not issubclass(type(item), Site):
            raise TypeError("Item must be a Site")
        if item.label.raw_value in self.atom_labels:
            raise AttributeError(
                f"An atom of name {item.label.raw_value} already exists."
            )
        super(Atoms, self).append(item)

    @property
    def atom_labels(self) -> List[str]:
        return [atom.label.raw_value for atom in self]

    @property
    def atom_species(self) -> List[str]:
        return [atom.specie.raw_value for atom in self]

    @property
    def atom_occupancies(self) -> np.ndarray:
        return np.array([atom.occupancy.raw_value for atom in self])

    def to_star(self) -> List[StarLoop]:
        adps = [hasattr(item, "adp") for item in self]
        has_adp = any(adps)
        main_loop = StarLoop(self, exclude=["adp", "msp"])
        if not has_adp:
            return [main_loop]
        add_loops = []
        adp_types = [item.adp.adp_type.raw_value for item in self]
        if all(adp_types):
            if adp_types[0] in ["Uiso", "Biso"]:
                main_loop = main_loop.join(
                    StarLoop.from_StarSections(
                        [getattr(item, "adp").to_star(item.label) for item in self]
                    ),
                    "label",
                )
            else:
                entries = []
                for item in self:
                    entries.append(item.adp.to_star(item.label))
                add_loops.append(StarLoop.from_StarSections(entries))
        else:
            raise NotImplementedError("Multiple types of ADP are not supported")
        has_msp = any([hasattr(item, "msp") for item in self])
        if has_msp:
            entries = []
            for item in self:
                if hasattr(item, "msp"):
                    entries.append(item.msp.to_star(item.label))
            add_loops.append(StarLoop.from_StarSections(entries))
        loops = [main_loop, *add_loops]
        return loops

    @classmethod
    def from_string(cls, in_string: str):
        s = StarLoop.from_string(in_string, [name[0] for name in cls._SITE_CLASS._CIF_CONVERSIONS])
        return s.to_class(cls, cls._SITE_CLASS)


A = TypeVar("A", bound=Atoms)


class PeriodicAtoms(Atoms):

    _SITE_CLASS = PeriodicSite

    def __init__(self, name: str, *args,
                 lattice: Optional[PeriodicLattice] = None,
                 interface: Optional[iF] = None, **kwargs):
        args = list(args)
        if lattice is None:
            for item in args:
                if hasattr(item, "lattice"):
                    lattice = item.lattice
                    break
        if lattice is None:
            raise AttributeError
        for idx, item in enumerate(args):
            if issubclass(type(item), Site):
                args[idx] = self._SITE_CLASS.from_site(lattice, item)
        super(PeriodicAtoms, self).__init__(name, *args, **kwargs, interface=interface)
        self.lattice = lattice

    @classmethod
    def from_atoms(cls, lattice: PeriodicLattice, atoms: Atoms) -> A:
        return cls(atoms.name, *atoms, lattice=lattice, interface=atoms.interface)

    def __repr__(self) -> str:
        return f"Collection of {len(self)} periodic sites."

    def append(self, item: S):
        if not issubclass(item.__class__, Site):
            raise TypeError("Item must be a Site or periodic site")
        if item.label.raw_value in self.atom_labels:
            raise AttributeError(
                f"An atom of name {item.label.raw_value} already exists."
            )
        # if isinstance(item, Site):
        item = self._SITE_CLASS.from_site(self.lattice, item)
        super(PeriodicAtoms, self).append(item)

    def get_orbits(self, magnetic_only: bool = False):
        orbit_dict = {}
        for item in self:
            if magnetic_only and not item.is_magnetic:
                continue
            orbit_dict[item.label.raw_value] = item.get_orbit()
        return orbit_dict
