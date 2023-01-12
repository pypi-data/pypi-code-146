#  SPDX-FileCopyrightText: 2022 easyCrystallography contributors  <crystallography@easyscience.software>
#  SPDX-License-Identifier: BSD-3-Clause
#  © 2022 Contributors to the easyCore project <https://github.com/easyScience/easyCrystallography>
#

__author__ = 'github.com/wardsimon'
__version__ = '0.1.0'

from typing import List, Tuple, Union, ClassVar, Optional, Type

from easyCore import np
from easyCore.Utils.io.star import StarEntry, StarSection, StarLoop
from easyCore.Objects.ObjectClasses import BaseObj, Descriptor, Parameter
from easyCore.Utils.classTools import addProp, removeProp
from abc import abstractmethod

_ANIO_DETAILS = {
    'msp_type': {
        'description': "A standard code used to describe the type of magnetic susceptibility parameters used for the "
                       "site.",
        'value':       'Uani'
    },
    'Cani':     {
        'description': 'The standard anisotropic magnetic susceptibility components in inverse teslas which appear in '
                       'the structure-factor term.',
        'value':       0.0,
        'max':         np.inf,
        'units':       'T^-1',
        'fixed':       True,
    },
    'Ciso':     {
        'description': 'Isotropic magnetic susceptibility parameter, or equivalent isotropic magnetic susceptibility '
                       'parameter, C(equiv), in inverted teslas, calculated from anisotropic susceptibility '
                       'components.',
        'value':       0.0,
        'max':         np.inf,
        'units':       'T^-1',
        'fixed':       True,
    },
}


class MSPBase(BaseObj):

    def __init__(self, *args, **kwargs):
        super(MSPBase, self).__init__(*args, **kwargs)

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
    def default(cls, interface=None):
        pass

    @abstractmethod
    def from_pars(cls, interface=None, **kwargs):
        pass


class Cani(MSPBase):
    chi_11: ClassVar[Parameter]
    chi_12: ClassVar[Parameter]
    chi_13: ClassVar[Parameter]
    chi_22: ClassVar[Parameter]
    chi_23: ClassVar[Parameter]
    chi_33: ClassVar[Parameter]

    def __init__(self,
                 chi_11: Optional[Union[Parameter, float]] = None,
                 chi_12: Optional[Union[Parameter, float]] = None,
                 chi_13: Optional[Union[Parameter, float]] = None,
                 chi_22: Optional[Union[Parameter, float]] = None,
                 chi_23: Optional[Union[Parameter, float]] = None,
                 chi_33: Optional[Union[Parameter, float]] = None,
                 interface=None):

        super(Cani, self).__init__('Cani',
                                   chi_11=Parameter('chi_11', **_ANIO_DETAILS['Cani']),
                                   chi_12=Parameter('chi_12', **_ANIO_DETAILS['Cani']),
                                   chi_13=Parameter('chi_13', **_ANIO_DETAILS['Cani']),
                                   chi_22=Parameter('chi_22', **_ANIO_DETAILS['Cani']),
                                   chi_23=Parameter('chi_23', **_ANIO_DETAILS['Cani']),
                                   chi_33=Parameter('chi_33', **_ANIO_DETAILS['Cani']),
                                   )
        if chi_11 is not None:
            self.chi_11 = chi_11
        if chi_12 is not None:
            self.chi_12 = chi_12
        if chi_13 is not None:
            self.chi_13 = chi_13
        if chi_22 is not None:
            self.chi_22 = chi_22
        if chi_23 is not None:
            self.chi_23 = chi_23
        if chi_33 is not None:
            self.chi_33 = chi_33
        self.interface = interface

    @classmethod
    def default(cls, interface=None):
        return cls(interface=interface)

    @classmethod
    def from_pars(cls,
                  chi_11: Optional[float] = None,
                  chi_12: Optional[float] = None,
                  chi_13: Optional[float] = None,
                  chi_22: Optional[float] = None,
                  chi_23: Optional[float] = None,
                  chi_33: Optional[float] = None,
                  interface=None):
        #                  interface: Optional[iF] = None):
        return cls(chi_11=chi_11, chi_12=chi_12, chi_13=chi_13, chi_22=chi_22,
                   chi_23=chi_23, chi_33=chi_33, interface=interface)


class Ciso(MSPBase):
    chi: ClassVar[Parameter]

    def __init__(self, chi: Optional[Union[Parameter, float]] = None, interface=None):
        super(Ciso, self).__init__('Ciso',
                                   chi=Parameter('chi', **_ANIO_DETAILS['Ciso']))
        if chi is not None:
            self.chi = chi
        self.interface = interface

    @classmethod
    def default(cls, interface=None):
        return cls(interface=interface)

    @classmethod
    def from_pars(cls, chi: Optional[float] = None, interface=None):
        return cls(chi=chi, interface=interface)


_AVAILABLE_ISO_TYPES = {
    'Cani': Cani,
    'Ciso': Ciso,
}


class MagneticSusceptibility(BaseObj):
    msp_type: ClassVar[Descriptor]
    msp_class: ClassVar[Type[MSPBase]]

    def __init__(self, msp_type: Union[Descriptor, str], interface: Optional = None, **kwargs):
        if isinstance(msp_type, str):
            msp_type = Descriptor('msp_type', msp_type)
        msp_class_name = msp_type.raw_value
        if msp_class_name in _AVAILABLE_ISO_TYPES.keys():
            msp_class = _AVAILABLE_ISO_TYPES[msp_class_name]
            if "msp_class" in kwargs:
                msp = kwargs.pop("msp_class")
            else:
                msp = msp_class(**kwargs, interface=interface)
        else:
            raise AttributeError(f"{msp_class_name} is not a valid magnetic susceptibility type")
        super(MagneticSusceptibility, self).__init__('msp',
                                                     msp_type=msp_type,
                                                     msp_class=msp)
        for par in msp.get_parameters():
            addProp(self, par.name, fget=self.__a_getter(par.name), fset=self.__a_setter(par.name))
        self.interface = interface

    def switch_type(self, msp_string: str, **kwargs):
        if msp_string in _AVAILABLE_ISO_TYPES.keys():
            msp_class = _AVAILABLE_ISO_TYPES[msp_string]
            if kwargs:
                msp_class: MSPBase = msp_class.from_pars(interface=self.interface, **kwargs)
            else:
                msp_class: MSPBase = msp_class.default(interface=self.interface)
        else:
            raise AttributeError
        for par in self.msp_type.get_parameters():
            removeProp(self, par.name)
        self.msp_class = msp_class
        self.msp_type = msp_string
        for par in msp_class.get_parameters():
            addProp(self, par.name, fget=self.__a_getter(par.name), fset=self.__a_setter(par.name))

    @classmethod
    def from_pars(cls, msp_type: str, interface=None, **kwargs):
        return cls(Descriptor('msp_type',
                              value=msp_type,
                              **{k: _ANIO_DETAILS['msp_type'][k] for k in _ANIO_DETAILS['msp_type'].keys() if
                                 k != 'value'}),
                   interface=interface, **kwargs)

    @classmethod
    def default(cls, interface=None):
        return cls(Descriptor('msp_type', **_ANIO_DETAILS['msp_type']), interface=interface)

    @classmethod
    def from_string(cls, in_string: Union[str, StarLoop]) -> Tuple[List[str], List['MagneticSusceptibility']]:
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
                raise AttributeError
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
             StarEntry(self.msp_type),
             *[StarEntry(par) for par in self.msp_class.get_parameters()]
             ]
        return StarSection.from_StarEntries(s)

    @staticmethod
    def __a_getter(key: str):

        def getter(obj):
            return obj.msp_class._kwargs[key]

        return getter

    @staticmethod
    def __a_setter(key):
        def setter(obj, value):
            obj.msp_class._kwargs[key].value = value

        return setter
