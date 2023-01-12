from __future__ import annotations

from tcsoa.gen.BusinessObjects import Cfg0ConfiguratorPerspective
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ConfigurationRosterCoverage(TcBaseObj):
    """
    Response structure for getConfigurationRosterCoverage service.
    
    :var jsonResponse: String Representing JSON output.
    :var serviceData: Information about errors if any.
    """
    jsonResponse: str = ''
    serviceData: ServiceData = None


@dataclass
class ConfigurationRosterInput(TcBaseObj):
    """
    Input Data structure for getConfigurationRosterCoverage service.
    
    :var perspective: Configurator perspective details.
    Property cfg0ProductItems of perspective must contain reference to a single Configurator context item and property
    cfg0RevisonRule must be set to a RevisionRule
    :var jsonRequest: String Representing JSON input, Please read JSON schema to understand it in detail.
    """
    perspective: Cfg0ConfiguratorPerspective = None
    jsonRequest: str = ''
