from typing import Optional, Union, List, Dict

from quickstats import DescriptiveEnum
from quickstats.maths.numerics import is_float

from .settings import (NORM_SYST_KEYWORD, SHAPE_SYST_KEYWORD, COMMON_SYST_DOMAIN_NAME,
                       CONSTR_GAUSSIAN, CONSTR_LOGN, CONSTR_ASYM, CONSTR_DFD, OTHER,
                       UNCERT_HI_PREFIX, UNCERT_LO_PREFIX, UNCERT_SYM_PREFIX)

class SystematicType(DescriptiveEnum):
    Norm  = (0, "Normalization sysetmatic", NORM_SYST_KEYWORD)
    Shape = (1, "Shape systematic", SHAPE_SYST_KEYWORD)
    Other = (2, "Unclassified systematic type", OTHER)
    
    def __new__(cls, value:int, description:str, keyword:str):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.keyword = keyword
        return obj    
    
class ConstraintType(DescriptiveEnum):
    LogN  = (0, "Lognormal constraint", CONSTR_LOGN, 1)
    Asym  = (1, "Assymetric constraint", CONSTR_ASYM, 4)
    Gaus  = (2, "Gaussian constraint", CONSTR_GAUSSIAN, 0)
    DFD   = (3, "Double Fermi-Dirac", CONSTR_DFD, 0)
    Other = (4, "Unclassified constraint type", OTHER, -1)
    
    def __new__(cls, value:int, description:str, keyword:str, interp_code:int):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.description = description
        obj.keyword = keyword
        obj.interp_code = interp_code
        return obj

class Systematic:
    
    def __init__(self):
        self.name = ""
        self.domain = ""
        self.raw_domain = ""
        self.process = ""
        self.whereto = ""
        self.constr_term = ""
        self.nominal = 0.
        self.beta = 0.
        self.errorlo = None
        self.errorhi = None
    
    def __eq__(self, other:"Systematic"):
        return (self.name == other.name) and (self.process == other.process) and (self.whereto == other.whereto)
    
    @staticmethod
    def default_domain():
        return COMMON_SYST_DOMAIN_NAME
    
    @staticmethod
    def common_domain():
        return COMMON_SYST_DOMAIN_NAME
    
    def is_equal(self, other:"Systematic"):
        return self.__eq__(other)
    
    def is_shape_syst(self):
        return self.get_syst_type() == SystematicType.Shape

    def get_syst_type(self):
        result = SystematicType.get_member_by_attribute("keyword", self.whereto)
        if result is None:
            return SystematicType.Other
        return result
    
    def get_constr_type(self):
        result = ConstraintType.get_member_by_attribute("keyword", self.constr_term)
        if result is None:
            return ConstraintType.Other
        return result
    
    def is_common_domain(self):
        return self.domain == COMMON_SYST_DOMAIN_NAME
    
    def set_domain(self, domain:str):
        syst_type = self.get_syst_type()
        # systematics defined in the common domain
        if domain == self.common_domain():
            # if a process name is specified, use it as domain name and 
            # remove it from common systematic
            if self.process != "":
                if syst_type == SystematicType.Shape:
                    self.domain = f"{self.whereto}_{self.name}_{self.process}"
                else:
                    self.domain = self.process
            # otherwise consider it as common systematic
            else:
                # for shape uncertainty, use NP name as domain
                if syst_type == SystematicType.Shape:
                    self.domain = f"{self.whereto}_{self.name}"
                # for yield uncertainty, consider it as common systematic
                elif syst_type == SystematicType.Norm:
                    self.domain = domain
                else:
                    raise RuntimeError(f'Unknown systematic loacation {self.whereto} '
                                       f'for NP {self.name}. Choose from "{NORM_SYST_KEYWORD}" (NormSyst) '
                                       f'or "{SHAPE_SYST_KEYWORD}" (ShapeSyst)')
        else:
            # for yield systematics under a sample, the domain name is always the sample name
            # for shape systematics under a sample, we will update it later depending on whether "Process" is specified
            self.domain = domain
            # for yield systematics under a sample, the default process name is the sample name
            # if a process name is provided in addition (e.g. uncertainties on acceptance and correction factor are separately provided in differential xs measurements), it will be <sample_name>_<process_name>
            if self.process == "":
                self.process = domain
                if syst_type == SystematicType.Shape:
                    self.domain = f"{self.whereto}_{self.name}_{self.process}"
            else:
                self.process = f"{domain}_{self.process}"
                if syst_type == SystematicType.Shape:
                    self.domain = f"{self.whereto}_{self.name}_{self.process}"
        self.raw_domain = domain
        
    def set_magnitudes(self, values:Union[float, str, List[float], List[str]]):
        # for asymmetric uncertainty, we need to be careful with the relative sign between the two components
        # if both upper and lower uncertainties are numbers, the lower number will always be forced to have opposite sign of upper
        # if either uncertainty is implemented as formula, the neither component can bear sign. Users need to make sure the sign convention is consistent
        if not isinstance(values, list):
            values = [values]
        if len(values) == 1:
            value = values[0]
            if isinstance(value, str):
                if is_float(value):
                    self.errorhi = float(value)
                    self.errorlo = float(value)
                else:
                    self.errorhi = value
                    self.errorlo = value
            elif isinstance(value, float):
                self.errorhi = value
                self.errorlo = value
            else:
                raise ValueError(f"invalid systematic magnitude: {value}")
        elif len(values) == 2:
            errhi, errlo = values
            # both are numbers, need to handle the relative sign
            if is_float(errhi) and is_float(errlo):
                if float(errhi) < 0:
                    self.errorhi = float(errhi)
                    self.errorlo = abs(float(errlo))
                else:
                    self.errorhi = float(errhi)
                    self.errorlo = -abs(float(errlo))
            else:
                self.errorhi = errhi
                self.errorlo = errlo
            if self.get_constr_type() != ConstraintType.Asym:
                self.stdout.warn(f"WARNING: The systematic {self.name} under domain {self.domain} "
                                 f"will be implemented as an asymmetric uncertainty for now. Please "
                                 f"double-check your config file and use the keyword "
                                 f"{CONSTR_ASYM} for constraint "
                                 f"term type instead of {self.constr_term} if you intend to implement "
                                 f"asymmetric uncertainties.")
    
    def get_tag_name(self):
        tag_name = f"{self.whereto}_{self.name}"
        if not self.is_common_domain():
            tag_name += f"_{self.process}"
        return tag_name
            
    def get_interp_code(self):
        constr_type = self.get_constr_type()
        return constr_type.interp_code

    def get_uncert_hi_expr(self):
        if is_float(self.errorhi):
            return f"{UNCERT_HI_PREFIX}{self.get_tag_name()}[{self.errorhi}]"
        return self.errorhi
    
    def get_uncert_lo_expr(self):
        if is_float(self.errorlo):
            return f"{UNCERT_LO_PREFIX}{self.get_tag_name()}[{self.errorlo}]"
        return self.errorlo
    
    def validate(self):
        if ((self.nominal <= 0.) and 
            (self.get_constr_type() in [ConstraintType.LogN, ConstraintType.Asym])):
            raise RuntimeError(f"failed to parse systematic {self.name}: "
                               f"constraint term {self.constr_term} received "
                               f"negative central value ({self.nominal})")