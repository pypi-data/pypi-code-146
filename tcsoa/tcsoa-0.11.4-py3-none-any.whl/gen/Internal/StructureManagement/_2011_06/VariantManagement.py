from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, VariantRevision, WorkspaceObject, Variant, BOMWindow
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ModularOption(TcBaseObj):
    """
    Describes a modular option information details returned by operations ''getBOMVariantConfigOptions'' and
    ''getModuleOptionsForBom''.
    
    :var optionId: Current session Option ID given by OVE.
    :var optionName: The option name.
    :var operationTypes: Array of operation types (to, less than, greater than, ect.) in case of Int, Real Options
    :var basedOnOption: Based on option details.  This is available only if option type is not native.
    :var mvlDefinitions: MVL Definition Stored
    :var optionDescription: Option Description
    :var optionValueType: The option value data type: String/Int/Real/Logical
    :var optionType: The type of option: Native/Presents/Implements/External
    :var allowedValues: List of allowed values attached to an option
    :var defaultValue: Option default value
    :var optionScope: The scope of the option: Public / Private
    :var minValues: Array of min values, in case of Int & Real options
    :var maxValues: Array of max values, in case of Int & Real options
    """
    optionId: int = 0
    optionName: str = ''
    operationTypes: List[int] = ()
    basedOnOption: BasedOnOptionInfo = None
    mvlDefinitions: List[str] = ()
    optionDescription: str = ''
    optionValueType: int = 0
    optionType: int = 0
    allowedValues: List[str] = ()
    defaultValue: str = ''
    optionScope: int = 0
    minValues: List[float] = ()
    maxValues: List[float] = ()


@dataclass
class ModularOptions(TcBaseObj):
    """
    List of options and MVL (Modular variant Language) string for current Module or BOMLine.
    
    :var options: List of available module options for a BOMLine.
    :var mvl: MVL attached to Item or ItemRevision (module).
    """
    options: List[ModularOption] = ()
    mvl: str = ''


@dataclass
class ModularOptionsForBomResponse(TcBaseObj):
    """
    The return value of the getModularOptionsForBom SOA.
    
    :var optionsOutput: A vector of ModularOptionsOutput that contains the modular options of the requested BOM lines /
    windows
    :var serviceData: The service data for errors and returned objects.
    """
    optionsOutput: List[ModularOptionsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ModularOptionsInfo(TcBaseObj):
    """
    Wrapper structure to encapsulate an input BOMLine and all its Modular Options information, used by
    ''ModularOptionsOutput'' in response of operation ''getModularOptionsForBom''.
    
    :var bomLine: A BOM line
    :var options: Modular options and MVL attached to a given BOMLine.
    """
    bomLine: BOMLine = None
    options: ModularOptions = None


@dataclass
class ModularOptionsInput(TcBaseObj):
    """
    The input to the getModularOptionsForBom SOA Service call
    
    :var bomWindow: The current BOM window
    :var bomLines: Selected BOM lines
    """
    bomWindow: BOMWindow = None
    bomLines: List[BOMLine] = ()


@dataclass
class ModularOptionsOutput(TcBaseObj):
    """
    The output of the 'getModuleOptionsForBom' SOA call.
    
    :var bomWindow: The BOM Window
    :var optionsInfo: Modular options for BOMLine objects in the given BOMWindow.
    """
    bomWindow: BOMWindow = None
    optionsInfo: List[ModularOptionsInfo] = ()


@dataclass
class BOMVariantConfigOptionResponse(TcBaseObj):
    """
    Repose Object for getBOMVariantConfigOption
    
    :var output: Output Object
    :var serviceData: Service data for errors & returned objects
    """
    output: BOMVariantConfigOutput = None
    serviceData: ServiceData = None


@dataclass
class BOMVariantConfigOutput(TcBaseObj):
    """
    Output Structure of operation ''getBOMVariantConfigOptions'' for a given input BOMWindow.
    
    :var bomWindow: Bom Window
    :var configuredOptions: Current Configured Options
    :var dbSOSOrSVR: Saved SOS or Variant Rule currently applied on BOMWindow.
    """
    bomWindow: BOMWindow = None
    configuredOptions: List[BOMVariantConfigurationOption] = ()
    dbSOSOrSVR: WorkspaceObject = None


@dataclass
class BOMVariantConfigurationOption(TcBaseObj):
    """
    Returned object having information of Option & configuration by operation ''getBOMVariantConfigOptions''. This will
    information about a single variant Option.
    
    :var variantType: Type of variant, if Legacy or Modular
    :var howSet: Option how configured (User Set, Derived, Defaulted, variant Item or Unset )
    :var valueSet: current configured value
    :var whereSet: Used only in case of Classic Option if the option was defaulted or derived, this is returned as the
    Id of the Item that contained the expression that defined this option value. If the option was set by a saved
    variant rule, this is returned as the name of the rule.
    :var defaultSet: Default Configured way (unset, default, derived default)
    :var defaultValue: Default value set
    :var modularOption: Modular Option Object if current object type is Modular
    :var classicOption: Legacy Option if option type is Legacy
    """
    variantType: BOMVariantType = None
    howSet: int = 0
    valueSet: str = ''
    whereSet: str = ''
    defaultSet: int = 0
    defaultValue: str = ''
    modularOption: ModularOption = None
    classicOption: ClassicOption = None


@dataclass
class BasedOnOptionInfo(TcBaseObj):
    """
    "Based On" option information for variants. In case of Modular all options having type Presents, Implemented to
    External are "based on" options.
    
    :var basedOnType: Option Type: Presents / Implements / External.
    :var path: Presented Path, filled when option type is Presented.
    :var basedOptionId: Based option ID.
    :var owningModuleKey: Owning item / module id/key.
    :var owningOptionName: Owning option name.
    """
    basedOnType: int = 0
    path: str = ''
    basedOptionId: int = 0
    owningModuleKey: str = ''
    owningOptionName: str = ''


@dataclass
class ClassicOption(TcBaseObj):
    """
    Legacy Option information details returned by operation ''getBOMVariantConfigOptions''.
    
    :var optionName: Option Name
    :var optionDescription: Option Description
    :var itemId: Item Id on which Option is defined
    :var optionValues: Allowed Values in Option
    :var variant: Legacy Option Variant Object. Created 1 each for each legacy option. Using this SOA consumer can do
    further operations on RAC Side if required.
    :var variantRev: Legacy Option variant ItemRevision Object. Created 1 each for each legacy option. It stores option
    values as enum. Using this SOA consumer can do further operations on RAC Side if required.
    """
    optionName: str = ''
    optionDescription: str = ''
    itemId: str = ''
    optionValues: List[str] = ()
    variant: Variant = None
    variantRev: VariantRevision = None


class BOMVariantType(Enum):
    """
    Type of Variant (legacy Or Modular)
    """
    BOM_LEGACY = 'BOM_LEGACY'
    BOM_MODULAR = 'BOM_MODULAR'
