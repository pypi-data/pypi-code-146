#  SPDX-FileCopyrightText: 2022 easyCrystallography contributors  <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022 Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>
#

from __future__ import annotations

__author__ = 'github.com/wardsimon'
__version__ = '0.1.0'

from typing import List, Tuple, Union, ClassVar, TypeVar, Optional, TYPE_CHECKING

from easyCore import np
from easyCore.Utils.io.star import StarEntry, StarSection, StarLoop
from easyCore.Objects.ObjectClasses import BaseObj, Descriptor, Parameter
from easyCore.Utils.classTools import addProp, removeProp
from abc import abstractmethod

if TYPE_CHECKING:
    from easyCore.Utils.typing import iF

_ANIO_DETAILS = {
    'adp_type': {
        'description': "A standard code used to describe the type of atomic displacement parameters used for the site.",
        'url':         'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_adp_type.html',
        'value':       'Uani'
    },
    'Uani':     {
        'description': 'Isotropic atomic displacement parameter, or equivalent isotropic atomic  displacement '
                       'parameter, U(equiv), in angstroms squared, calculated from anisotropic atomic displacement  '
                       'parameters.',
        'url':         'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_U_.html',
        'value':       0.0,
        'units':       'angstrom^2',
        'fixed':       True,
    },
    'Uiso':     {
        'description': 'The standard anisotropic atomic displacement components in angstroms squared which appear in '
                       'the structure-factor term.',
        'url':         'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_U_iso_or_equiv.html',
        'value':       0.0,
        'min':         0,
        'max':         np.inf,
        'units':       'angstrom^2',
        'fixed':       True,
    },
    'Bani':     {
        'description': 'The standard anisotropic atomic displacement components in angstroms squared which appear in '
                       'the structure-factor term.',
        'url':         'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_aniso_B_.html',
        'value':       0.0,
        'units':       'angstrom^2',
        'fixed':       True,
    },
    'Biso':     {
        'description': 'Isotropic atomic displacement parameter, or equivalent isotropic atomic displacement '
                       'parameter, B(equiv), in angstroms squared, calculated from anisotropic displacement '
                       'components.',
        'url':         'https://www.iucr.org/__data/iucr/cifdic_html/1/cif_core.dic/Iatom_site_B_iso_or_equiv.html',
        'value':       0.0,
        'min':         0,
        'max':         np.inf,
        'units':       'angstrom^2',
        'fixed':       True,
    }
}


class AdpBase(BaseObj):

    def __init__(self, *args, **kwargs):
        super(AdpBase, self).__init__(*args, **kwargs)

    @property
    def matrix(self) -> np.ndarray:
        matrix = np.zeros([3, 3])
        pars = self.get_parameters()
        if len(pars) == 1:
            np.fill_diagonal(matrix, pars[0].raw_value)
        elif len(pars) == 6:
            matrix[0, 0] = pars[0].raw_value
            matrix[0, 1] = pars[1].raw_value
            matrix[0, 2] = pars[2].raw_value
            matrix[1, 1] = pars[3].raw_value
            matrix[1, 2] = pars[4].raw_value
            matrix[2, 2] = pars[5].raw_value
        return matrix

    @abstractmethod
    def default(cls, interface: Optional[iF] = None):
        pass

    @abstractmethod
    def from_pars(cls, interface: Optional[iF] = None, **kwargs):
        pass


class Anisotropic(AdpBase):

    U_11: ClassVar[Parameter]
    U_12: ClassVar[Parameter]
    U_13: ClassVar[Parameter]
    U_22: ClassVar[Parameter]
    U_23: ClassVar[Parameter]
    U_33: ClassVar[Parameter]

    def __init__(self,
                 U_11: Optional[Union[Parameter, float]] = None, U_12: Optional[Union[Parameter, float]] = None,
                 U_13: Optional[Union[Parameter, float]] = None, U_22: Optional[Union[Parameter, float]] = None,
                 U_23: Optional[Union[Parameter, float]] = None, U_33: Optional[Union[Parameter, float]] = None,
                 interface: Optional[iF] = None):
        super(Anisotropic, self).__init__('anisoU',
                                          U_11=Parameter('U_11', **_ANIO_DETAILS['Uani']), U_12=Parameter('U_12', **_ANIO_DETAILS['Uani']),
                                          U_13=Parameter('U_13', **_ANIO_DETAILS['Uani']), U_22=Parameter('U_22', **_ANIO_DETAILS['Uani']),
                                          U_23=Parameter('U_23', **_ANIO_DETAILS['Uani']), U_33=Parameter('U_33', **_ANIO_DETAILS['Uani']))
        if U_11 is not None:
            self.U_11 = U_11
        if U_12 is not None:
            self.U_12 = U_12
        if U_13 is not None:
            self.U_13 = U_13
        if U_22 is not None:
            self.U_22 = U_22
        if U_23 is not None:
            self.U_23 = U_23
        if U_33 is not None:
            self.U_33 = U_33
        self.interface = interface

    @classmethod
    def default(cls, interface: Optional[iF] = None):
        return cls(interface=interface)

    @classmethod
    def from_pars(cls,
                  U_11: Optional[float] = None, U_12: Optional[float] = None,
                  U_13: Optional[float] = None, U_22: Optional[float] = None,
                  U_23: Optional[float] = None, U_33: Optional[float] = None,
                  interface: Optional[iF] = None):
        return cls(U_11, U_12, U_13, U_22, U_23, U_33, interface)


class Isotropic(AdpBase):

    Uiso: ClassVar[Parameter]

    def __init__(self, Uiso: Optional[Union[Parameter, float]] = None, interface: Optional[iF] = None):
        super(Isotropic, self).__init__('Uiso',
                                        Uiso=Parameter('Uiso', **_ANIO_DETAILS['Uiso']))
        if Uiso is not None:
            self.Uiso = Uiso
        self.interface = interface

    @classmethod
    def default(cls, interface: Optional[iF] = None):
        return cls(interface=interface)

    @classmethod
    def from_pars(cls, Uiso: Optional[float] = None, interface: Optional[iF] = None):
        return cls(Uiso, interface=interface)


class AnisotropicBij(AdpBase):

    B_11: ClassVar[Parameter]
    B_12: ClassVar[Parameter]
    B_13: ClassVar[Parameter]
    B_22: ClassVar[Parameter]
    B_23: ClassVar[Parameter]
    B_33: ClassVar[Parameter]

    def __init__(self,
                 B_11: Optional[Union[Parameter, float]] = None, B_12: Optional[Union[Parameter, float]] = None,
                 B_13: Optional[Union[Parameter, float]] = None, B_22: Optional[Union[Parameter, float]] = None,
                 B_23: Optional[Union[Parameter, float]] = None, B_33: Optional[Union[Parameter, float]] = None,
                 interface: Optional[iF] = None):
        super(AnisotropicBij, self).__init__('anisoB',
                                             **{name: Parameter(name, **_ANIO_DETAILS['Bani']) for name in
                                              ['B_11', 'B_12', 'B_13',
                                               'B_22', 'B_23', 'B_33']
                                                })
        if B_11 is not None:
            self.B_11 = B_11
        if B_12 is not None:
            self.B_12 = B_12
        if B_13 is not None:
            self.B_13 = B_13
        if B_22 is not None:
            self.B_22 = B_22
        if B_23 is not None:
            self.B_23 = B_23
        if B_33 is not None:
            self.B_33 = B_33
        self.interface = interface

    @classmethod
    def default(cls, interface: Optional[iF] = None):
        return cls(interface=interface)

    @classmethod
    def from_pars(cls,
                  B_11: Optional[float] = None, B_12: Optional[float] = None,
                  B_13: Optional[float] = None, B_22: Optional[float] = None,
                  B_23: Optional[float] = None, B_33: Optional[float] = None,
                  interface: Optional[iF] = None):
        return cls(B_11, B_12, B_13, B_22, B_23, B_33, interface)


class IsotropicB(AdpBase):

    Biso: ClassVar[Parameter]

    def __init__(self, Biso: Optional[Union[Parameter, float]] = None, interface: Optional[iF] = None):
        super(IsotropicB, self).__init__('Biso',
                                         Biso=Parameter('Biso', **_ANIO_DETAILS['Biso']))
        if Biso is not None:
            self.Biso = Biso
        self.interface = interface

    @classmethod
    def default(cls, interface: Optional[iF] = None):
        return cls(interface=interface)

    @classmethod
    def from_pars(cls, Biso: Optional[float] = None, interface: Optional[iF] = None):
        return cls(Biso, interface=interface)


_AVAILABLE_ISO_TYPES = {
    'Uani': Anisotropic,
    'Uiso': Isotropic,
    # 'Uovl': 'Overall',
    # 'Umpe': 'MultipoleExpansion',
    'Bani': AnisotropicBij,
    'Biso': IsotropicB,
    # 'Bovl': 'OverallB'
}

if TYPE_CHECKING:
    AB = TypeVar('AB', bound=AdpBase)


class AtomicDisplacement(BaseObj):

    adp_type: ClassVar[Descriptor]
    adp_class: ClassVar[AB]

    def __init__(self, adp_type: Optional[Union[Descriptor, str]] = None, interface: Optional[iF] = None, **kwargs):
        if adp_type is None:
            adp_type = 'Uiso'
        if isinstance(adp_type, str):
            adp_type = Descriptor('adp_type', adp_type)
        adp_class_name = adp_type.raw_value
        if adp_class_name in _AVAILABLE_ISO_TYPES.keys():
            adp_class = _AVAILABLE_ISO_TYPES[adp_class_name]
            if "adp_class" in kwargs.keys():
                adp = kwargs.pop("adp_class")
            else:
                adp = adp_class(**kwargs, interface=interface)
        else:
            raise AttributeError(f"{adp_class_name} is not a valid adp type")
        super(AtomicDisplacement, self).__init__('adp',
                                                 adp_type=adp_type,
                                                 adp_class=adp)
        for par in adp.get_parameters():
            addProp(self, par.name, fget=self.__a_getter(par.name), fset=self.__a_setter(par.name))
        self.interface = interface

    def switch_type(self, adp_string: str, **kwargs):
        if adp_string in _AVAILABLE_ISO_TYPES.keys():
            adp_class = _AVAILABLE_ISO_TYPES[adp_string]
            if kwargs:
                adp = adp_class(**kwargs, interface=self.interface)
            else:
                adp = adp_class(interface=self.interface)
        else:
            raise AttributeError(f"{adp_string} is not a valid adp type")
        for par in self.adp_class.get_parameters():
            removeProp(self, par.name)
        self.adp_class = adp_class
        self.adp_type = adp
        for par in adp.get_parameters():
            addProp(self, par.name, fget=self.__a_getter(par.name), fset=self.__a_setter(par.name))

    @classmethod
    def from_pars(cls, adp_type: str, interface: Optional[iF] = None, **kwargs):
        return cls(adp_type, **kwargs, interface=interface)

    @classmethod
    def default(cls, interface: Optional[iF] = None):
        return cls(interface=interface)

    @classmethod
    def from_string(cls, in_string: Union[str, StarLoop]) -> Tuple[List[str], List['AtomicDisplacement']]:
        # We assume the in_string is a loop
        from easyCrystallography.Components.Site import Site
        if isinstance(in_string, StarLoop):
            loop = in_string
        else:
            loop = StarLoop.from_string(in_string)
        sections = loop.to_StarSections()
        atom_labels = []
        adp = []
        for section in sections:
            entries = section.to_StarEntries()
            site_name_idx = section.labels.index(Site._CIF_CONVERSIONS[0][1])
            atom_labels.append(entries[site_name_idx].value)
            adp_type_idx = section.labels.index(cls._CIF_CONVERSIONS[0][1])
            adp_type = entries[adp_type_idx].value
            if adp_type not in _AVAILABLE_ISO_TYPES.keys():
                raise AttributeError(f"{adp_type} is not a valid adp type")
            adp_class = _AVAILABLE_ISO_TYPES[adp_type]
            pars = [par[1] for par in adp_class._CIF_CONVERSIONS]
            par_dict = {}
            idx_list = []
            name_list = []
            for idx, par in enumerate(pars):
                idx_list.append(section.labels.index(par))
                name_list.append(adp_class._CIF_CONVERSIONS[idx][0])
                par_dict[name_list[-1]] = entries[idx_list[-1]].value
            obj = cls.from_pars(adp_type, **par_dict)
            for idx2, idx in enumerate(idx_list):
                if hasattr(entries[idx], 'fixed') and entries[idx].fixed is not None:
                    entry = getattr(obj, name_list[idx2])
                    entry.fixed = entries[idx].fixed
                if hasattr(entries[idx], 'error') and entries[idx].error is not None:
                    entry = getattr(obj, name_list[idx2])
                    entry.error = entries[idx].error
            adp.append(obj)
        return atom_labels, adp

    @property
    def available_types(self) -> List[str]:
        return [name for name in _AVAILABLE_ISO_TYPES.keys()]

    def to_star(self, atom_label: Descriptor) -> StarEntry:
        s = [StarEntry(atom_label, 'label'),
             StarEntry(self.adp_type),
             *[StarEntry(par) for par in self.adp_class.get_parameters()]
             ]
        return StarSection.from_StarEntries(s)

    @staticmethod
    def __a_getter(key: str):

        def getter(obj):
            return obj.adp_class._kwargs[key]

        return getter

    @staticmethod
    def __a_setter(key):
        def setter(obj, value):
            obj.adp_class._kwargs[key].value = value

        return setter
